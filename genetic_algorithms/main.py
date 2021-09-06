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
def float_to_bin(x, n_bits):
	''' Retorna el equivalente en binario de x '''
	binary = bin(int(str(x).split('.')[1])).lstrip('0b')
	n = len(binary)
	if n < n_bits:
		binary = ('0' * (n_bits - n)) + binary
	return binary

def create_population(n, n_bits):
	''' Genera una poblacion de N individuos unicos '''
	population = []
	i = 0
	while i < n:
		x = random()
		try:
			population.index(x)
			continue
		except:
			x = round(x, 7)
			population.append({'x': x, 'binary': float_to_bin(x, n_bits)})
			i += 1

	return population

def evaluate(population):
	''' Agrega el valor de la adaptacion a cada
		individuo de la poblacion '''
	for individual in population:
		individual['fadap'] = scientific_notation(round(float(individual['x']) + fabs(sin(32 * float(individual['x']))), 7))

def add_adaptations(population):
	''' Retorna la suma de todas las adaptaciones de los
		individuos que forman la poblacion de entrada '''
	add = 0
	for individual in population:
		add += float(individual['fadap'])
	return add

def show_progress(population, cases, generation = 0):
	''' Muestra la estadistica de la generacion actual'''
	file = 'out' + str(cases) + '.txt'
	out = open(file, "a")
	if generation:
		out.write('\n')

	out.write('GENERACION ACTUAL: {}\n'.format(generation))

	out.write('Mejor adaptacion: {}, Adaptacion promedio: {}\n\n'.format(population[0].get('fadap'), round(add_adaptations(population) / len(population), 7)))
	out.write('No\tCromosoma\t\t\t\t\tValor real\t\tAdaptacion\n')
	i = 0
	for individual in population:
		if i < 11 or i >= 91:
			out.write('{}\t{}\t{}\t\t{}\n'.format((i + 1), individual['binary'], individual['x'], individual['fadap']))

		if i == 11:
			out.write('...\t\t\t\t\t\t\t\t\t\t\t...\n'.format((i + 1), individual['binary'], individual['x'], individual['fadap']))
		i += 1
	out.close()

def selection_probability(population):
	''' Agrega el valor de la probabilidad de
		seleccion a cada individuo de la poblacion '''
	t = add_adaptations(population)
	for individual in population:
		individual['prob'] = float(individual['fadap']) / t

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

def encode(num, n_bits):
	''' Dado un numero real, obtiene su
		correspondiente numero entero  '''
	return ceil(num * (2 ** n_bits - 1))

def decoding(num, n_bits):
	''' Dado un numero entero, obtiene su
		correspondiente numero real  '''
	return round(1 / (num / (2 ** n_bits - 1)), 7)

def scientific_notation(num):
	if (str(num).find('e') != -1):
		num = format(float(num), '.7f')
	return num

def modification_point(prob, n_bits):
	''' Retorna el punto de modificacion
		para el cruce y la mutacion '''
	while True:
		i = 1
		found = False
		while i <= n_bits and not found:
			if round(random(), 7) <= prob:
				found = True
			else:
				i += 1
		if i <= n_bits:
			break

	return i

def crossing(parent1, parent2, pc, n_bits):
	''' Retorna 2 hijos de dos individuos '''
	parent1 = encode(parent1, n_bits)
	parent2 = encode(parent2, n_bits)
	while True:
		point = modification_point(pc, n_bits)
		h1 = (parent1 >> point) | (parent2 << point)
		h2 = (parent1 << point) | (parent2 >> point)
		h1 = decoding(h1, n_bits)
		h2 = decoding(h2, n_bits)
		if 0 <= h1 <= 1 and 0 <= h2 <= 1 and h1 != h2:
			break

	h1, h2 = scientific_notation(h1), scientific_notation(h2)
	return h1, h2

def mutation(p1, p2, pm, n_bits):
	''' Retorna la mutacion de p1 y p2 '''
	binary_h1 = float_to_bin(p1, n_bits)
	binary_h2 = float_to_bin(p2, n_bits)
	while True:
		point = modification_point(pm, n_bits)
		if binary_h1[point - 1] == '0':
			h1 = encode(p1, n_bits) | 1 << point
		else:
			h1 = encode(p1, n_bits) ^ 1 << point

		if binary_h2[point - 1] == '0':
			h2 = encode(p2, n_bits) | 1 << point
		else:
			h2 = encode(p2, n_bits) ^ 1 << point

		h1, h2 = decoding(h1, n_bits), decoding(h2, n_bits)
		if 0 <= h1 <= 1 and 0 <= h2 <= 1 and h1 != h2:
			break

	h1, h2 = scientific_notation(h1), scientific_notation(h2)
	return h1, h2

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
		cont_new_individuals = ceil(n * gap / 100)
		population = create_population(n, n_bits)
		evaluate(population)

		# Ordenando en forma decreciente
		#population.sort(key = lambda individual: individual['fadap'], reverse = True)
		population.sort(key = lambda individual: float(individual['fadap']), reverse = True)

		# Mostrar avances
		show_progress(population, cases)

		# Recorriendo las generaciones
		for t in range(generations):
			# Inicializando la nueva poblacion
			descendants = [{'x': population[i]['x']} for i in range(0, n - cont_new_individuals)]

			# Generando probabilidades de seleccion
			selection_probability(population)

			# Creando los nuevos individuos
			i = 0
			while i < cont_new_individuals:
				# Seleccionando los padres
				p1, p2 = roulette_wheel(population)
				elements = False

				# Cruce
				if round(random(), 7) < pc:
					elements = True
					h1, h2 = crossing(population[p1]['x'], population[p2]['x'], pc, n_bits)
				else:
					# Mutacion
					if round(random(),7) < pm:
						elements = True
						h1, h2 = mutation(population[p1]['x'], population[p2]['x'], pm, n_bits)

				# Aagregando a los nuevos individuos
				if elements:
					try:
						descendants.index(h1)
					except:
						descendants.append({'x': h1})
						i += 1

					try:
						descendants.index(h2)
					except:
						if i < cont_new_individuals:
							# Agrego los dos hijos
							descendants.append({'x': h2})
						i += 1
				else:
					continue

			# Evaluando la poblacion descendiente y creando su correspondiente binario
			for individual in descendants:
				individual['binary'] = float_to_bin(individual['x'], n_bits)

			evaluate(descendants)

			# Ordenando la poblacion descendientes en forma decreciente
			descendants.sort(key = lambda individual: float(individual['fadap']), reverse = True)

			# Mostrar avances
			show_progress(descendants, cases, t + 1)
			population = descendants[:]
			descendants.clear()
		population.clear()
	# Salida
	input.close

if __name__ == '__main__':
    main()