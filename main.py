import sys

class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.selectNext()
        

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
            num = ''
            while self.origin[self.position].isnumeric():
                num += self.origin[self.position]
                self.position += 1
                if self.position == len(self.origin):
                    break
            self.actual = Token('Num', int(num))
            return self.actual


class Parser:  

    tokens = None
    
    @staticmethod
    def parseExpression():
        result = 0
        nex = Parser.tokens.actual
        
        if nex.type == 'Num':
            result = int(nex.value)
            nex = Parser.tokens.selectNext()
                
            while nex.value in ['+','-']:
            
                if nex.value == '+':
                    nex = Parser.tokens.selectNext()            
                    if nex.type == 'Num':
                        result += nex.value
                    else:
                        raise Exception('Expected Number')
                elif nex.value == '-':
                    nex = Parser.tokens.selectNext()            
                    if nex.type == 'Num':
                        result -= nex.value
                    else:
                        raise Exception('Expected Number')
                nex = Parser.tokens.selectNext() 
            return result
        else:
            raise Exception('Expected number')

 
    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        res = Parser.parseExpression()

        if Parser.tokens.actual.value == 'EOF':
            return res
        else:
            raise Exception("EOF or signal Expected")

if __name__ == "__main__":
    
    print(Parser.run(sys.argv[1]))
