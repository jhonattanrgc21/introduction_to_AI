import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.metrics  import mean_squared_error
# import matplotlib.pyplot as plt
# np.set_printoptions(suppress=True)

class Peretron:

    def __init__(self,r,landa,training_type,iter):

        self.iter = iter
        self.training_type = training_type
        self.landa = landa
        self.r = r

    def function_transfer(self,x,str):
        if("heaviside" == str):
            return x > 0
        if("sigmoide" == str):
            return 1/(1 + np.exp(-x))
    def show(self,iter,x,y,up):
        print('ITERACION ACTUAL: {}\n'.format(iter))
        print('Patron    | x1 x2 | __________ Salida __________\n')
        print('No        |       |  Deseada Calculada Error Abs\n')
        for i in range(0,self.p):
            print('  {}       |  {}  |     {}      {}       {}\n\n'.format(i,x[i], y[i],up[i],abs(y[i]-up[i])))

    def solve(self,x,y):
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
            self.show(it,x,y,up)
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

x = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([0, 0, 0, 1]) 
p = Peretron(1,0.3,"Lotes",1000)
p.solve(x,y)

# x0 = np.random.uniform(0, 1)
# xn = []
# xn.append(x0)
# for i in range(1,600):
#     xn.append(4*xn[i-1]*(1-xn[i-1]))

# vcr = []
# vcry = []
# xn = xn[-100:]
# for i in range(0,len(xn[-100:])-2):
#     vcr.append([xn[i],xn[i+1],xn[i]*xn[i],xn[i]*xn[i+1],xn[i+1]*xn[i+1]])
#     vcry.append(xn[i+2])



# class Adeline:

#     def __init__(self,r,landa,training_type,iter):

#         self.iter = iter
#         self.training_type = training_type
#         self.landa = landa
#         self.r = r

#     def function_transfer(self,x):
#         return 1/(1 + np.exp(-x))

#     def show(self,iter,x,y,up):
#         print('ITERACION ACTUAL: {}\n'.format(iter))
#         print('Patron | x1 x2 | __________ Salida __________\n')
#         print('No     |       |  Deseada Calculada Error Abs\n')
#         for i in range(0,self.p):
#             print('  {}    |  {}  |     {}      {}       {}\n\n'.format(i,x[i], y[i],up[i],abs(y[i]-up[i])))

#     def solve(self,x,y):
#         self.p = x.shape[0]
#         self.inputs = x.shape[1]
#         self.W = np.random.uniform(low=-0.3, high=0.3,size=(1,self.inputs))
#         vectorjfw = []
#         jfwprev = 0
#         # self.W = np.zeros((1,self.inputs))
#         it = 0
#         while(it < self.iter):
#             # for i in range(0,self.r):
#             if self.training_type == "Lotes":
#                 deltaw =  np.zeros((self.inputs, 3))
#             up = self.evaluation(x)
#             vectorjfw.append(mean_squared_error(y,up))
            
#             jw = (y - up) * (up) * (1 - up)
#             self.show(it,x,y,up)
#             for j in range(0,self.p):
#                 wri = self.landa*(jw[j])*np.transpose(x[j])
#                 self.W = self.W + wri      

#             it = it + 1              
    
#     def evaluation(self,x):
#         up = sum(np.transpose(self.W*x) - 0.5) 
#         up = self.function_transfer(up)
#         return up

# x = np.array(vcr)
# y = np.array(vcry)
# X_train, X_test, y_train, y_test = train_test_split( x, y, test_size=0.33, random_state=42)
 
# p = Adeline(1,0.3,"PP",1000)
# p.solve(X_train,y_train)



