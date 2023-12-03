from z3 import * #import the z3 solver

slots = 3

x11 = Bool("x11")
x12 = Bool("x12")
x13 = Bool("x13")

x21 = Bool("x21")
x22 = Bool("x22")
x23 = Bool("x23")

x31 = Bool("x31")
x32 = Bool("x32")
x33 = Bool("x33")

x41 = Bool("x41")
x42 = Bool("x42")
x43 = Bool("x43")

grid_courses = [[x11, x21, x31, x41],
              [x12, x22, x32, x42],
              [x13, x23, x33, x43]]
# As linhas são os horarios e as colunas são os cursos.


#Fazendo um map para facilitar buscar os valores depois
atomic_map = {
    (1, 1): x11, (2, 1): x21, (3, 1): x31, (4, 1): x41,
    (1, 2): x12, (2, 2): x22, (3, 2): x32, (4, 2): x42,
    (1, 3): x13, (2, 3): x23, (3, 3): x33, (4, 3): x43,
}

p = [[1,2],
     [2,3],
     [2,4],
     [3,4]]
# P são os pares de horários que tem uma pessoa matriculada.

def get_atomic_pair(course1, course2, slot):
  c1 = atomic_map.get((course1, slot+1), None)
  c2 = atomic_map.get((course2, slot+1), None)
  return c1, c2


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


#O codigo abaixo gera uma lista de resultados separados por OU lógico, como na primeira parte da nossa restrição.
aux_list = []
or_restriction = []

for i in range(len(grid_courses[0])):
  for j in range(slots):
    aux_list.append(get_atomic((i+1, j+1), None))
  
  or_restriction.append(Or(aux_list)) #Adiciona as formulas na lista com um "V" (ou) entre elas.
  aux_list.clear()
    

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