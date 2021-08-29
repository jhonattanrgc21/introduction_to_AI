'''
    * Autores:
        - Jhonattan Garcia, C.I: 24.423.188
        - Luis Sierra, C.I: 25.582.661

    * Materia: Introduccion a la IA
    * Profesor: Anibal Guerra
'''

# Modulos
from random import random
from math import sin, fabs
from bitstring import BitArray

# Desarrollo de funciones
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
			population.append({'x': x})
			i += 1

	return population

def evaluate(population):
	''' Agrega el valor de la adaptacion a cada
		individuo de la poblacion '''
	for individual in population:
		individual['fadap'] = individual['x'] + fabs(sin(32 * individual['x']))
	return population

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
	out.write('GENERACION ACTUAL: {}\n'.format(generation + 1))
	out.write('Mejor adaptacion: {:7f}, Adaptacion promedio: {:7f}\n\n'.format(population[0].get('fadap'), add_adaptations(population) / len(population)))
	out.write('No\tCromosoma\t\t\t\t\t\t\tValor real\tAdaptacion\n')
	i = 0
	for individual in population:
		chromosome = BitArray(float = individual['fadap'], length = 32)
		out.write('{}\t{}\t{:7f}\t{:7f}\n'.format((i + 1), chromosome.bin, individual['x'], individual['fadap']))
		i += 1
	out.close()

def main():
	''' Cuerpo principal '''

	# Entrada
	try:
		input = open("in.txt", "r")
	except:
		raise 'Error, no se encontro el archivo in.txt'

	cases = 0
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
		population = evaluate(population)

		# Ordenando en forma decreciente
		population.sort(key = lambda individual: individual['fadap'], reverse = True)

		# Mostrar avances
		show_progress(population, cases)

	# Salida
	input.close
if __name__ == '__main__':
    main()
