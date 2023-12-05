from z3 import * #import the z3 solver

class SatisfiabilityMethods:

    def __init__(self):
        self.cursos = int
        self.slots = int
        self.p = []
        self.atomic_map = {}
        self.grid = []
    
    def initialize_inputs(self):
        self.cursos = int(input("Numero de Minicursos: "))
        self.slots = int(input("Quantos slots serão disponibilizados? "))
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
                self.p.append([valor1, valor2])
            except ValueError:
                print("Entrada inválida. Certifique-se de inserir números inteiros.")
        return self.cursos, self.slots, self.p

    def create_grid(self, cursos, slots):
        solver = Solver()
        grid = [[Bool(f'x{j}{i}') for j in range(1, cursos + 1)] for i in range(1, slots + 1)]
        for row in grid:
            solver.add(row)
        return grid

    def create_atomic_map(self, grid):
        atomic_map = {}
        num_rows = len(grid)
        num_cols = len(grid[0])

        for j in range(num_rows):
            for i in range(num_cols):
                atomic_map[(i+1, j+1)] = grid[j][i]

        return atomic_map

    def get_atomic_pair(self, atomic_map, course1, course2, slot):
        c1 = atomic_map.get((course1, slot), None)
        c2 = atomic_map.get((course2, slot), None)
        return c1, c2
    
    def get_atomic(self, atomic_map, course, slot):
        return atomic_map.get((course, slot), None)

    #MÉTODO QUE CRIA A RESTRIÇÃO: Minicursos com inscrições em comum não podem ser ofertados no mesmo slot.
    def create_first_restriction(self, atomic_map, p, slots):
        
        atomicas = []
        for i in range(len(p)): #len(p) equivale ao tamanho da lista de Pares.
          for j in range(slots): #para percorrer todos as linhas ou slots.
            atomicas.append(self.get_atomic_pair(atomic_map, p[i][0], p[i][1], j+1)) #Aqui pegamos as variáveis de acordo com os pares em P.
        
        not_and_restrictions = []
        for i in range(len(atomicas)):
            not_and_restrictions.append(Not(And(atomicas[i][0], atomicas[i][1])))
        
        first_restriction = []
        first_restriction.append(And(not_and_restrictions))
        return first_restriction
    
    #MÉTODO QUE CRIA A RESTRIÇÃO: Cada minicurso deve ser ofertado em pelo menos um slot.
    def create_second_restriction(self, grid_courses, slots, atomic_map):
        aux_list = []
        second_restriction = []

        for i in range(len(grid_courses[0])):
            for j in range(slots):
                aux_list.append(self.get_atomic(atomic_map, i+1, j+1))
            second_restriction.append(Or(aux_list)) #Adiciona as formulas na lista com um "V" (ou) entre elas.
            aux_list.clear()

        return second_restriction

    #MÉTODO QUE CRIA A RESTRIÇÃO: Cada minicurso deve ser ofertado em no máximo um slot.
    def create_third_restriction(self, grid_courses):        
        aux_list = []
        num_colunas = len(grid_courses[0])

        for coluna in range(num_colunas):
            combinations = []
            for i in range(len(grid_courses)):
                for j in range(i + 1, len(grid_courses)):
                    combinations.append((grid_courses[i][coluna], grid_courses[j][coluna]))
            aux_list.append(combinations)

        third_restriction = []
        for i in range(len(aux_list)):
            for j in range(len(aux_list[0])):
                third_restriction.append(Not(And(aux_list[i][j])))

        return third_restriction
    
    
    def check_sat(self, first_restriction, second_restriction, third_restriction):
        s = Solver()
        s.add(first_restriction)
        s.add(second_restriction)
        s.add(third_restriction)
        r = s.check ()
        if r == sat:
            print ("SATISFIABLE")
            m = s.model()
            self.formated_output(m)
            #print(m)
        else:
            print ("UNSATISFIABLE")
    
    def formated_output(self, m):
        #FORMATANDO OUTPUT
        true_valuations = []
        for decl in m.decls():
            val = m[decl]
            if(val == True):
                true_valuations.append(decl.name())
        true_valuations.sort()

        output_formated_list = []
        true_valuations_output_list = []

        for i in range(len(true_valuations)):
            output_formated_list.append(true_valuations[i][:1] + true_valuations[i][2:])

        for i in range(len(output_formated_list)):
            true_valuations_output_list.append(output_formated_list[i].replace("x", "s"))

        for i in range(len(true_valuations_output_list)):
            print(f"{i+1} {true_valuations_output_list[i]}")

    def solution(self):
        #setup
        cursos, slots, p = self.initialize_inputs()
        grid_courses = self.create_grid(cursos, slots)
        atomic_map = self.create_atomic_map(grid_courses)

        #criando formulas de restrição
        first_restriction = self.create_first_restriction(atomic_map, p, slots)
        second_restriction = self.create_second_restriction(grid_courses, slots, atomic_map)
        third_restriction = self.create_third_restriction(grid_courses)

        #Verificando satisfatibilidade e dando output com resultado
        self.check_sat(first_restriction, second_restriction, third_restriction)