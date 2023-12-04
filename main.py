from SatisfiabilityMethods import SatisfiabilityMethods

sat = SatisfiabilityMethods()

cursos, slots, p = sat.initialize_inputs()
#print(f"Pares: {p}")

grid_courses = sat.create_grid(cursos, slots)
#print(f"grid: {grid_courses}")

atomic_map = sat.create_atomic_map(grid_courses)
#print(f"atomic map: {atomic_map}")

first_restriction = sat.first_restriction(atomic_map, p, slots)
#print(f"first restriction: {first_restriction}")

or_restriction = sat.second_restriction(grid_courses, slots, atomic_map)
#print(or_restriction)

not_and_restriction = sat.third_restriction(grid_courses)
#print(not_and_restriction)
second_restriction = sat.merging_restrictions(or_restriction, not_and_restriction)
#print(second_restriction)

sat.check_sat(first_restriction, second_restriction)