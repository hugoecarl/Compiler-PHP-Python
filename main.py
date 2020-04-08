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
        

class Node:

    def __init__(self, value, children):
        self.value = None
        self.children = children

    def evaluate(self, SymbolTable):
        return 


class BinOp(Node):
    
    def __init__(self,value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        if self.value == '+':
            return self.children[0].evaluate(SymbolTable) + self.children[1].evaluate(SymbolTable) 
        elif self.value == '-':
            return self.children[0].evaluate(SymbolTable) - self.children[1].evaluate(SymbolTable)
        elif self.value == '*':
            return self.children[0].evaluate(SymbolTable) * self.children[1].evaluate(SymbolTable)
        elif self.value == '/':
            return self.children[0].evaluate(SymbolTable) // self.children[1].evaluate(SymbolTable)


class UnOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        if self.value == '+':
            return +self.children[0].evaluate(SymbolTable)
        elif self.value == '-':
            return -self.children[0].evaluate(SymbolTable)


class NoOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        pass


class IntVal(Node):
        
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        return self.value


class SymbolTable():
    
    def __init__(self):
        self.Symbols = {}
    
    def Set(self, symbol, value):
        self.Symbols[symbol] = value

    def Get(self, symbol):
        if symbol in self.Symbols:
            return self.Symbols[symbol]
        else:
            raise Exception("Variavel inexistente")


class Assignment(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        SymbolTable.Set(self.value, self.children[0].evaluate(SymbolTable))


class Identifier(Node):

    def __init__(self, value):
        self.value = value
    
    def evaluate(self, SymbolTable):
        return SymbolTable.Get(self.value) 


class Commands(Node):

    def __init__(self, children):
        self.children = children 

    def evaluate(self, SymbolTable):
        for i in self.children:
            i.evaluate(SymbolTable)


class Echo(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self, SymbolTable):
        print(self.children[0].evaluate(SymbolTable))


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:

    reserved_words = ['echo']

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
        elif self.origin[self.position] == '\n':
            self.position += 1
            return self.selectNext()
        elif self.origin[self.position].isalpha():
            buffer = ''
            while self.origin[self.position].isalpha(): 
                buffer += self.origin[self.position]
                self.position += 1
                if self.position == len(self.origin):
                    break
            if buffer.lower() in Tokenizer.reserved_words:
                self.actual = Token('Reserved', buffer.lower())
                return self.actual
            else:
                raise Exception("Not in reserved words")
        elif self.origin[self.position] == "$":
            self.position += 1
            if self.origin[self.position].isalpha():
                var = ''
                while self.origin[self.position].isalpha() or self.origin[self.position] == '_' or self.origin[self.position].isnumeric():
                    var += self.origin[self.position]
                    self.position += 1
                    if self.position == len(self.origin):
                        break
                self.actual = Token('Identifier', var)
                return self.actual
            else:
                raise Exception("Variavel Errada")
        elif self.origin[self.position] == "=":
            self.actual = Token('Eq', '=')
            self.position += 1
            return self.actual
        elif self.origin[self.position] == ";":
            self.actual = Token('Endc', ';')
            self.position += 1
            return self.actual
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
        elif self.origin[self.position] == "{":
            self.actual = Token('Chav', '{')
            self.position += 1
            return self.actual
        elif self.origin[self.position] == "}":
            self.actual = Token('Chav', '}')
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
    def parseBlock():
        commands = []
        Parser.nex = Parser.tokens.actual

        if Parser.nex.value == '{':
            Parser.nex = Parser.tokens.selectNext()
            while Parser.nex.value != '}':
                commands.append(Parser.parseCommand())
            Parser.nex = Parser.tokens.selectNext()
            return Commands(commands)    
        else:
            raise Exception("Esperado {")

    @staticmethod 
    def parseCommand():
        Parser.nex = Parser.tokens.actual

        if Parser.nex.value == ';':
            Parser.nex = Parser.tokens.selectNext()
            return NoOp(None, None)
        elif Parser.nex.type == 'Identifier':
            var_name = Parser.nex.value
            Parser.nex = Parser.tokens.selectNext()
            if Parser.nex.value == '=':
                Parser.nex = Parser.tokens.selectNext()
                command = Assignment(var_name, [Parser.parseExpression()])
                if Parser.nex.value == ';':
                    Parser.nex = Parser.tokens.selectNext()
                    return command
                else:
                    raise Exception("Expected ;")
            else:
                raise Exception("Expected =")
        elif Parser.nex.type == "Reserved":
            if Parser.nex.value == 'echo':
                Parser.nex = Parser.tokens.selectNext()
                command = Echo([Parser.parseExpression()])
                if Parser.nex.value == ';':
                    Parser.nex = Parser.tokens.selectNext()
                    return command
                else:
                    raise Exception("Expected ;")
        else:
            return Parser.parseBlock()

    @staticmethod
    def parseExpression():    
        result = Parser.parseTerm()
                
        while Parser.nex.value in ['+','-']:
            if Parser.nex.value == '+':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('+', [result, Parser.parseTerm()])
            elif Parser.nex.value == '-':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('-', [result, Parser.parseTerm()])
        return result

    @staticmethod
    def parseTerm():      
        result = Parser.parseFactor()
                
        while Parser.nex.value in ['*','/']: 
            if Parser.nex.value == '*':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('*', [result, Parser.parseFactor()])
            elif Parser.nex.value == '/':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('/', [result, Parser.parseFactor()])
        return result

    @staticmethod
    def parseFactor():      
        Parser.nex = Parser.tokens.actual

        if Parser.nex.type == 'Num':
            result = IntVal(int(Parser.nex.value), None)
            Parser.nex = Parser.tokens.selectNext()
        elif Parser.nex.value == '+':
            Parser.nex = Parser.tokens.selectNext()
            result = UnOp('+', [Parser.parseFactor(), None])
        elif Parser.nex.value == '-':
            Parser.nex = Parser.tokens.selectNext()
            result = UnOp('-', [Parser.parseFactor(), None])
        elif Parser.nex.value == '(':
            Parser.nex = Parser.tokens.selectNext()
            result = Parser.parseExpression()
            if Parser.nex.value != ')':
                raise Exception('Parenteses n fechado')
            Parser.nex = Parser.tokens.selectNext()        
        elif Parser.nex.type == 'Identifier':
            result = Identifier(Parser.nex.value)
            Parser.nex = Parser.tokens.selectNext()    
        else:
            raise Exception('Expected Number')
        return result 

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        res = Parser.parseBlock()
        stable = SymbolTable()

        if Parser.tokens.actual.value == 'EOF':
            return res.evaluate(stable)
        else:
            raise Exception("EOF or signal Expected")


if __name__ == "__main__":
    
    f = open(sys.argv[1], "r")

    Parser.run(PrePro.filter(f.read()))
