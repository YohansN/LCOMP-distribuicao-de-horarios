from z3 import * #import the z3 solver

#INPUTS

#Fazendo inputs genericos
cursos = int(input("Numero de Minicursos: "))
slots = int(input("Quantos slots serão disponibilizados? "))

p = []

while True:
    entrada = input("Digite dois valores inteiros separados por um espaço (ou 'sair' para terminar): ")
    if entrada.lower() == 'sair':
        break
    valores_entrada = entrada.split()
    if len(valores_entrada) != 2:
        print("Por favor, insira dois valores inteiros separados por um espaço.")
        continue
    try:
        valor1 = int(valores_entrada[0])
        valor2 = int(valores_entrada[1])
        p.append([valor1, valor2])
    except ValueError:
        print("Entrada inválida. Certifique-se de inserir números inteiros.")

def create_grid(slots, cursos):
    solver = Solver()

    grid = [[Bool(f'x{j}{i}') for j in range(1, cursos + 1)] for i in range(1, slots + 1)]
    
    for row in grid:
      solver.add(row)

    return grid

def create_atomic_map(grid):
    atomic_map = {}
    num_rows = len(grid)
    num_cols = len(grid[0])

    for j in range(num_rows):
        for i in range(num_cols):
            atomic_map[(i+1, j+1)] = grid[j][i]

    return atomic_map

grid_courses = create_grid(slots, cursos)
atomic_map = create_atomic_map(grid_courses)

def get_atomic_pair(course1, course2, slot):
  c1 = atomic_map.get((course1, slot+1), None)
  c2 = atomic_map.get((course2, slot+1), None)
  return c1, c2

#FUNÇÃO QUE CRIA A RESTRIÇÃO: Minicursos com inscrições em comum não podem ser ofertados no mesmo slot.
atomicas = []

for i in range(len(p)): #len(p) equivale ao tamanho da lista de Pares.
  for j in range(slots): #para percorrer todos as linhas ou slots.
    atomicas.append(get_atomic_pair(p[i][0], p[i][1], j)) #Aqui pegamos as variáveis de acordo com os pares em P.

not_and_restrictions = []
and_restrictions = []
final_restriction_1 = []

for i in range(len(atomicas)):
  not_and_restrictions.append(Not(And(atomicas[i][0], atomicas[i][1])))


#for i in range(len(not_and_restrictions)):
and_restrictions.append(And(not_and_restrictions))
final_restriction_1 = and_restrictions

def get_atomic(course, slot):
  return atomic_map.get(course, slot)

#FUNÇÃO QUE CRIA A RESTRIÇÃO: Cada minicurso deve ser ofertado em pelo menos um slot.
#O codigo abaixo gera uma lista de resultados separados por OU lógico, como na primeira parte da nossa restrição.
aux_list = []
or_restriction = []

for i in range(len(grid_courses[0])):
  for j in range(slots):
    aux_list.append(get_atomic((i+1, j+1), None))
  
  or_restriction.append(Or(aux_list)) #Adiciona as formulas na lista com um "V" (ou) entre elas.
  aux_list.clear()
    

#FUNÇÃO QUE CRIA A RESTRIÇÃO: Cada minicurso deve ser ofertado em no máximo um slot.
#O codigo abaixo gera uma lista de resultados como na segunda parte da nossa restrição.
not_and_restriction = []
aux_list = []

num_colunas = len(grid_courses[0])

for coluna in range(num_colunas):
  combinations = []
  for i in range(len(grid_courses)):
    for j in range(i + 1, len(grid_courses)):
      combinations.append((grid_courses[i][coluna], grid_courses[j][coluna]))

  # Adicionar as combinações de pares da coluna atual à lista principal
  aux_list.append(combinations)

for i in range(len(aux_list)):
  for j in range(len(aux_list[0])):
    not_and_restriction.append(Not(And(aux_list[i][j])))

# JUNTANDO AS DUAS PARTES DA SEGUNDA RESTRIÇÃO
and_restriction = []
final_restriction_2 = []

and_restriction.append(And(or_restriction))
and_restriction.append(And(not_and_restriction))

final_restriction_2.append(And(and_restriction))


s = Solver() # allocate solver to theck satisfiability
s.add(final_restriction_1) # add a formula to the solver
s.add(final_restriction_2) # add a formula to the solver
r = s.check () # check satisfiability
if r == sat:
  print ("SATISFIABLE")
  m = s.model() # read model (o modelo é uma valoração na qual a fórmula é verdadeira)
  print(m)
else:
  print ("UNSATISFIABLE")