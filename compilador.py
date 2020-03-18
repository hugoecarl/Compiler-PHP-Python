import sys

class Compilador:
    def __init__(self):
        self.lista_num = []
        self.lista_op = []

    def parse(self):
        for i in range(1, len(sys.argv[1])):
            if sys.argv[1][i - 1].isnumeric() and sys.argv[1][i] == ' ' and sys.argv[1][i + 1].isnumeric():
                raise NameError('Espaço e número não permitido')
        
        lis = list(sys.argv[1].replace(' ', ''))  
        i = 0
        j = 0
        
        while i < len(lis):
            try:
                int(lis[j])
                j += 1 
            except:
                self.lista_num.append(int(''.join(lis[i:j])))
                if j < len(lis):
                    self.lista_op.append(lis[j])
                i = j + 1
                j = i
                pass
    
    def operacao(self):
        self.parse()
        for i in range(len(self.lista_op)):
            self.lista_num[i] = int(self.lista_num[i])
            self.lista_num[i+1] = int(self.lista_num[i+1])
            if self.lista_op[i] == '-':
                self.lista_num[i] = self.lista_num[i] - self.lista_num[i+1]
                self.lista_num[i+1] = 0
        return sum(self.lista_num) 

        

if __name__ == "__main__":
    comp = Compilador()

    if len(sys.argv[1]) == 0:
        raise NameError('Argumento Vazio')
    if sys.argv[1][-1] == '-' or sys.argv[1][-1] == '+':
        raise NameError('Sinal mal posicionado')
    
    
    print(comp.operacao())

    
        
    

