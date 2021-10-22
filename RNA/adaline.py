# Modulos
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
np.set_printoptions(suppress=True)

# Declaracion de clases
class Adeline:

    def __init__(self, r, landa, training_type, iter):

        self.iter = iter
        self.training_type = training_type
        self.landa = landa
        self.r = r

    def function_transfer(self,x):
        return 1/ (1 + np.exp(-x))

    def show(self, iter, x, y, up):
        print('ITERACION ACTUAL: {}\n'.format(iter))
        print('Patron | __________ Salida __________\n')
        print('No     |  Deseada Calculada Error Abs\n')
        for i in range(0,self.p):
            if i < 12 or i >= self.p - 8:
                print('{}    |     {:.2f}      {:.2f}       {:.2f}'.format(i, y[i],up[i],abs(y[i]-up[i])))
            elif i == 12:
                print('...')
        print('\n')

    def solve(self, x, y):
        self.p = x.shape[0]
        self.inputs = x.shape[1]
        self.W = np.random.uniform(low=-0.3, high=0.3,size=(1,self.inputs))
        vectorjfw = []
        jfwprev = 0
        # self.W = np.zeros((1,self.inputs))
        it = 0
        while(it < self.iter):
            # for i in range(0,self.r):
            if self.training_type == "Lotes":
                deltaw =  np.zeros((self.inputs, 1))
            up = self.evaluation(x)
            vectorjfw.append(mean_squared_error(y,up))
            print('Error promedio: {:.6f}'.format(sum(vectorjfw) / len(vectorjfw)))
            jw = (y - up) * (up) * (1 - up)

            self.show(it, x, y, up)

            for j in range(0,self.p):
                wri = self.landa*(jw[j])*np.transpose(x[j])
                self.W = self.W + wri

            it = it + 1

    def evaluation(self,x):
        up = sum(np.transpose(self.W*x) - 0.5)
        up = self.function_transfer(up)
        return up

# Declaracion de operaciones
def main():
    ''' Cuerpo principal '''

    x0 = np.random.uniform(0, 1)
    xn = []
    xn.append(x0)
    for i in range(1,600):
        xn.append(4*xn[i-1]*(1-xn[i-1]))

    vcr = []
    vcry = []
    xn = xn[-100:]
    for i in range(0,len(xn[-100:])-2):
        vcr.append([xn[i],xn[i+1],xn[i]*xn[i],xn[i]*xn[i+1],xn[i+1]*xn[i+1]])
        vcry.append(xn[i+2])

    x = np.array(vcr)
    y = np.array(vcry)
    X_train, X_test, y_train, y_test = train_test_split( x, y, test_size=0.33, random_state=42)

    p = Adeline(1, 0.8,"PP",1000)
    print('Tipo de aprendizaje: Patron a patron\nFactor de aprendizaje: {}\nCantidad de iteraciones utilizadas: {}'.format(p.landa, p.iter))
    p.solve(X_train,y_train)


if __name__ == '__main__':
    main()