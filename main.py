import sys

class PrePro:

    @staticmethod
    def filter(string):
        string = list(string)
        i = 1 
        
        while i < len(string): 
            if string[i - 1] == '/' and string[i] == '*':
                j = i + 1
                fechou = False
                while j < len(string):
                    if string[j] == '*' and string[j + 1] == '/':
                        fechou = True
                        break
                    j += 1
                if fechou:
                    del string[i-1:j+2]
                else:
                    raise Exception('Comentário errado')
            i += 1   
        return ''.join(string)
        

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
        elif self.origin[self.position] == "*":
            self.actual = Token('String', '*')
            self.position += 1
            return self.actual
        elif self.origin[self.position] == "/":
            self.actual = Token('String', '/')
            self.position += 1
            return self.actual
        elif self.origin[self.position] == "(":
            self.actual = Token('Paren', '(')
            self.position += 1
            return self.actual
        elif self.origin[self.position] == ")":
            self.actual = Token('Paren', ')')
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
    nex = None
    
    @staticmethod
    def parseExpression():    
        result = Parser.parseTerm()
                
        while Parser.nex.value in ['+','-']:
            if Parser.nex.value == '+':
                Parser.nex = Parser.tokens.selectNext()            
                result += Parser.parseTerm()
            elif Parser.nex.value == '-':
                Parser.nex = Parser.tokens.selectNext()            
                result -= Parser.parseTerm()
        return result


    @staticmethod
    def parseTerm():
        
        result = Parser.parseFactor()
                
        while Parser.nex.value in ['*','/']: 
            if Parser.nex.value == '*':
                Parser.nex = Parser.tokens.selectNext()            
                result *= Parser.parseFactor()
            elif Parser.nex.value == '/':
                Parser.nex = Parser.tokens.selectNext()            
                result /= Parser.parseFactor()
        return result

    @staticmethod
    def parseFactor():
        
        Parser.nex = Parser.tokens.actual


        if Parser.nex.type == 'Num':
            result = int(Parser.nex.value)
            Parser.nex = Parser.tokens.selectNext()
        elif Parser.nex.value == '+':
            Parser.nex = Parser.tokens.selectNext()
            result = +Parser.parseFactor()
        elif Parser.nex.value == '-':
            Parser.nex = Parser.tokens.selectNext()
            result = -Parser.parseFactor() 
        elif Parser.nex.value == '(':
            Parser.nex = Parser.tokens.selectNext()
            result = Parser.parseExpression()
            if Parser.nex.value != ')':
                raise Exception('Parenteses n fechado')
            Parser.nex = Parser.tokens.selectNext()        
        
        else:
            raise Exception('Expected Number')
        return result 





 
    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        res = Parser.parseExpression()

        if Parser.tokens.actual.value == 'EOF':
            return res
        else:
            raise Exception("EOF or signal Expected")

if __name__ == "__main__":
    
    print(Parser.run(PrePro.filter(sys.argv[1])))
