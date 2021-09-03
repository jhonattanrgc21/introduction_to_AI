'''
    * Autores:
        - Jhonattan Garcia, C.I: 24.423.188
        - Luis Sierra, C.I: 25.582.661

    * Electiva: Introduccion a la IA
    * Profesor: Anibal Guerra
'''

# Modulos
from random import random
from math import sin, fabs, ceil, log10

# Desarrollo de funciones
def float_to_bin(population, n_bits):
	''' Agrega el valor de la conversion de x a binario
		para cada individuo de la poblacion '''
	for individual in population:
		individual['binary'] = bin(int(str(individual['x']).split('.')[1])).lstrip('0b')
		n = len(individual['binary'])
		if n < n_bits:
			individual['binary'] = ('0' * (n_bits - n)) + individual['binary']

def create_population(n):
	''' Genera una poblacion de N individuos unicos '''
	population = []
	i = 0
	while i < n:
		x = random()
		try:
			population.index(x)
			continue
		except:
			population.append({'x': round(x, 7)})
			i += 1

	return population

def evaluate(population):
	''' Agrega el valor de la adaptacion a cada
		individuo de la poblacion '''
	for individual in population:
		individual['fadap'] = round(individual['x'] + fabs(sin(32 * individual['x'])), 7)

def add_adaptations(population):
	''' Retorna la suma de todas las adaptaciones de los
		individuos que forman la poblacion de entrada '''
	add = 0
	for individual in population:
		add += individual['fadap']
	return add

def show_progress(population, cases, generation = 0):
	''' Muestra la estadistica de la generacion actual'''
	file = 'out' + str(cases) + '.txt'
	out = open(file, "a")
	if generation:
		out.write('\n')
	out.write('GENERACION ACTUAL: {}\n'.format(generation + 1))
	out.write('Mejor adaptacion: {:7f}, Adaptacion promedio: {:7f}\n\n'.format(population[0].get('fadap'), add_adaptations(population) / len(population)))
	out.write('No\tCromosoma\t\t\t\t\tValor real\tAdaptacion\n')
	i = 0
	for individual in population:
		out.write('{}\t{}\t{}\t{}\n'.format((i + 1), individual['binary'], individual['x'], individual['fadap']))
		i += 1
	out.close()

def selection_probability(population):
	''' Agrega el valor de la probabilidad de
		seleccion a cada individuo de la poblacion '''
	t = add_adaptations(population)
	for individual in population:
		individual['prob'] = individual['fadap'] / t

def search(search_space, elem):
	''' Retorna el indice donde se encuentre elem '''
	i = 0
	n = len(search_space)
	found = False
	while i < n and not found:
		if elem <= search_space[i]:
			found = True
		else:
			i += 1
	return i

def roulette_wheel(population):
	''' Retorna dos individuos aleatorios '''
	roulette = []
	for individual in population:
		if roulette == []:
			elem = individual['prob']
		else:
			elem = individual['prob'] + roulette[-1]
		roulette.append(elem)

	while True:
		p1 = search(roulette, random())
		p2 = search(roulette, random())
		if p1 != p2:
			break
	return p1, p2

def main():
	''' Cuerpo principal '''

	# Entrada
	try:
		input = open("in.txt", "r")
	except:
		raise 'Error, no se encontro el archivo in.txt'

	# Procesos
	cases = 0
	n_bits = ceil(log10(10 ** 7) / log10(2))
	for line in input:
		cases += 1
		test = line.split(' ')
		n = int(test[0])
		pc = float(test[1])
		pm = float(test[2])
		generations = int(test[3])
		gap = int(test[4])

		# Inicializar la poblacion
		population = create_population(n)
		evaluate(population)
		float_to_bin(population, n_bits)

		# Ordenando en forma decreciente
		population.sort(key = lambda individual: individual['fadap'], reverse = True)

		# Mostrar avances
		show_progress(population, cases)

		# Recorriendo las generaciones
		for t in range(generations + 1):
			# Inicializando la nueva poblacion
			cont_new_individuals = n * gap / 100
			decendents = population[:-cont_new_individuals]

			# Generando probabilidades de seleccion
			selection_probability(population)

			# Creando los nuevos individuos
			i = 0
			while i < cont_new_individuals:
				# Seleccionando los padres
				p1, p2 = roulette_wheel(population)
				pass

			evaluate(decendents)

			# Ordenando en forma decreciente
			decendents.sort(key = lambda individual: individual['fadap'], reverse = True)
			float_to_bin(decendents, n_bits)

			# Mostrar avances
			show_progress(decendents, cases, t)
			population = decendents[:]
			decendents.clear()

	# Salida
	input.close
if __name__ == '__main__':
    main()
