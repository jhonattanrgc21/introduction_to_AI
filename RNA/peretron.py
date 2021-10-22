import numpy as np


class Peretron:

    def __init__(self, r , landa, training_type, iter):

        self.iter = iter
        self.training_type = training_type
        self.landa = landa
        self.r = r

    def function_transfer(self, x, str):
        if("heaviside" == str):
            return x > 0
        if("sigmoide" == str):
            return 1/(1 + np.exp(-x))

    def show(self, iter, x , y, up, out):
        out.write('\nITERACION ACTUAL: {}\n'.format(iter))
        out.write('Patron | x1 x2 | __________ Salida __________\n')
        out.write('No     |       |  Deseada Calculada Error Abs\n')
        for i in range(0,self.p):
            out.write('  {}    | {} |     {}      {}       {}\n'.format(i, x[i], y[i], up[i], abs(y[i]-up[i])))

    def solve(self, x, y, out):
        self.p = x.shape[0]
        self.inputs = x.shape[1]
        self.W = np.random.uniform(low=-0.3, high=0.3,size=(1,self.inputs))
        # self.W = np.zeros((1,self.inputs))
        it = 0
        while(it < self.iter):
            # for i in range(0,self.r):
            if self.training_type == "Lotes":
                deltaw =  np.zeros((self.inputs, 1))
            up = self.evaluation(x)
            error = y - up
            self.show(it,x,y,up, out)
            if sum(error) == 0:
                break
            for j in range(0,self.p):
                wri = self.landa*error[j]*np.transpose(x[j])
                if self.training_type == "PP":
                    self.W = self.W + wri
                else:
                    deltaw = deltaw + wri
            if self.training_type == "Lotes":
                self.W = self.W + deltaw

            it = it + 1

    def evaluation(self,x):
        up = sum(np.transpose(self.W[0]*x) - 1)
        up = self.function_transfer(up,"heaviside")
        return up


def main():
    # Patrones de entrada
    x = np.array([
        [0,0],
        [0,1],
        [1,0],
        [1,1]
    ])

    # Patrones de salida
    # y = np.array([0 , 0, 0, 1])
    # y = np.array([0 , 1, 1, 1])
    y = np.array([0 , 1, 1, 0])

    # Cantidad de casos de prueba
    n_test = int(input())
    for case in range(n_test):
        line = input().split(' ')

        # Cantidad de UP
        n_up = int(line[0])

        # Factor de aprendizaje
        landa = float(line[1])

        # Cantidad de iteraciones
        training_type = str(line[2])

        # Tipo de entrenamiento
        iter = int(line[3])

        file = 'out' + str(case + 1) + '.txt'
        out = open(file, "a")
        if training_type == 'PP':
            out.write('Tipo de entrenamiento: Patron a patron\n')
        else:
            out.write('Tipo de entrenamiento: Lotes\n')
        out.write('Constante de aprendizaje: {}\nNr de iteraciones utilizadas: {}'.format(landa, iter))

        p = Peretron(n_up, landa, iter)
        p.solve(x, y, out)

        out.close()

if __name__ == '__main__':
    main()



