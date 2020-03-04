import sys

class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = ''

    def selectNext(self):
        if self.position == len(self.origin):
            self.actual = Token('','EOF')
            return self.actual
        if self.origin[self.position] == " ":
            self.position += 1
            return self.selectNext()
        elif self.origin[self.position] == "+":
            self.actual = Token('String', '+')
            self.position += 1
            return self.actual
        elif self.origin[self.position] == "-":
            self.actual = Token('String', '-')
            self.position += 1
            return self.actual
        elif self.origin[self.position].isnumeric():
            self.actual = ''
            while self.origin[self.position].isnumeric():
                self.actual += self.origin[self.position]
                self.position += 1
                if self.position == len(self.origin):
                    break
            return Token('Num', self.actual)


class Parser:  
    
    @staticmethod
    def parseExpression(tokens):
        result = 0
        nex = tokens.selectNext()
        
        if nex.type == 'Num':
            result = int(nex.value)

        while nex.value != 'EOF':
            nex = tokens.selectNext()
            if nex.value == '+':
                nex = tokens.selectNext()            
                if nex.value.isnumeric():
                    result += int(nex.value)
                else:
                    raise Exception('Erro')
            elif nex.value == '-':
                nex = tokens.selectNext()            
                if nex.value.isnumeric():
                    result -= int(nex.value)
                else:
                    raise Exception('Erro')
            elif nex.value.isnumeric():
                raise Exception('Erro')
        return result

 
    @staticmethod
    def run(code):
        tokens = Tokenizer(code)
        return Parser.parseExpression(tokens)

if __name__ == "__main__":
    
    print(Parser.run(sys.argv[1]))



