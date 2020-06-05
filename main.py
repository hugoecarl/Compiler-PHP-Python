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
        if self.value in ['+', '-', '*', '/', '>', '<', 'or', 'and'] and (self.children[0].evaluate(SymbolTable)[1] == str or self.children[1].evaluate(SymbolTable)[1] == str):
            raise Exception('Operation not permitted with strings')
        if self.value == '+':
            return (self.children[0].evaluate(SymbolTable)[0] + self.children[1].evaluate(SymbolTable)[0], int) 
        elif self.value == '-':
            return (self.children[0].evaluate(SymbolTable)[0] - self.children[1].evaluate(SymbolTable)[0], int)
        elif self.value == '*':
            return (self.children[0].evaluate(SymbolTable)[0] * self.children[1].evaluate(SymbolTable)[0], int)
        elif self.value == '/':
            return (self.children[0].evaluate(SymbolTable)[0] // self.children[1].evaluate(SymbolTable)[0], int)
        elif self.value == '>':            
            return (self.children[0].evaluate(SymbolTable)[0] > self.children[1].evaluate(SymbolTable)[0], bool)
        elif self.value == '<':
            return (self.children[0].evaluate(SymbolTable)[0] < self.children[1].evaluate(SymbolTable)[0], bool)
        elif self.value == 'or':
            return (self.children[0].evaluate(SymbolTable)[0] or self.children[1].evaluate(SymbolTable)[0], bool)
        elif self.value == 'and':
            return (self.children[0].evaluate(SymbolTable)[0] and self.children[1].evaluate(SymbolTable)[0], bool)
        elif self.value == '==':
            if (self.children[0].evaluate(SymbolTable)[1] == str and self.children[1].evaluate(SymbolTable)[1] != str) or (self.children[1].evaluate(SymbolTable)[1] == str and self.children[0].evaluate(SymbolTable)[1] != str):
                raise Exception('Operation == not permitted with strings and different type')
            return (self.children[0].evaluate(SymbolTable)[0] == self.children[1].evaluate(SymbolTable)[0], bool)
        elif self.value == '.':
            return (str(self.children[0].evaluate(SymbolTable)[0]) + str(self.children[1].evaluate(SymbolTable)[0]), str)    



class UnOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        if self.children[0].evaluate(SymbolTable)[1] == str:
            raise Exception('Operation not permitted with strings')
        if self.value == '+':
            return (+self.children[0].evaluate(SymbolTable)[0], int)
        elif self.value == '-':
            return (-self.children[0].evaluate(SymbolTable)[0], int)
        elif self.value == '!':
            return (not self.children[0].evaluate(SymbolTable)[0], bool)        


class NoOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        pass


class ReadLine(Node):
        
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        self.value = int(input())
        return (self.value, int)


class IntVal(Node):
        
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        return (self.value, int)


class BoolVal(Node):
        
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        return (self.value, bool)


class StringVal(Node):
        
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable):
        return (self.value, str)


class SymbolTabl():
    
    Funcs = {}
    
    def __init__(self):
        self.Symbols = {}
        self.ret = None
    
    def Set(self, symbol, value):
        self.Symbols[symbol] = value
    
    def Get(self, symbol):
        if symbol in self.Symbols:
            return self.Symbols[symbol]
        else:
            raise Exception("Variavel inexistente")
    
    def SetReturnVal(self, value):
        self.ret = value

    def GetReturnVal(self):
        return self.ret
    
    @staticmethod
    def SetFunc(symbol, value):
        if symbol in SymbolTabl.Funcs:
            raise Exception("Funcao ja declarada")
        SymbolTabl.Funcs[symbol] = value

    @staticmethod
    def GetFunc(symbol):
        if symbol in SymbolTabl.Funcs:
            return SymbolTabl.Funcs[symbol]
        else:
            raise Exception("Funcao inexistente")


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


class WhileOp(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self, SymbolTable):
        while bool(self.children[0].evaluate(SymbolTable)[0]) == True:
            self.children[1].evaluate(SymbolTable)


class ConditionalOp(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self, SymbolTable):
        if bool(self.children[0].evaluate(SymbolTable)[0]) == True:
            return self.children[1].evaluate(SymbolTable)
        elif bool(self.children[0].evaluate(SymbolTable)[0]) == False and len(self.children) == 3:
            return self.children[2].evaluate(SymbolTable)
          

class FuncDecOp(Node):

    def __init__(self, value, children):
        self.value = value 

        self.children = children

    def evaluate(self, SymbolTable):
        SymbolTable.SetFunc(self.value, self.children)


class FuncCallOp(Node):

    def __init__(self, value, children):
        self.value = value 
        self.children = children

    def evaluate(self, SymbolTable):
        Stable = SymbolTabl()
        FuncDec = SymbolTable.GetFunc(self.value)
        if len(self.children) != len(FuncDec[0]):
            raise Exception("Wrong arguments")
        for i in range(len(FuncDec[0])):
            Stable.Set(FuncDec[0][i], self.children[i].evaluate(SymbolTable))
        FuncDec[1].evaluate(Stable)
        if Stable.GetReturnVal() != None:
            return Stable.GetReturnVal() 


class ReturnOp(Node):

    def __init__(self, children):
        self.children = children

    def evaluate(self, SymbolTable):
        SymbolTable.SetReturnVal(self.children[0].evaluate(SymbolTable)) 


class Commands(Node):

    def __init__(self, children):
        self.children = children 

    def evaluate(self, SymbolTable):
        for i in self.children:
            if SymbolTable.GetReturnVal() != None:
                break
            i.evaluate(SymbolTable)


class Echo(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self, SymbolTable):
        print(self.children[0].evaluate(SymbolTable)[0])


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:

    reserved_words = ['echo', 'while', 'if', 'else', 'or', 'and', 'readline', 'true', 'false', 'function', 'return']

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = Token(None, None)
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
            while self.origin[self.position].isalpha() or self.origin[self.position] == '_' or self.origin[self.position].isnumeric(): 
                buffer += self.origin[self.position]
                self.position += 1
                if self.position == len(self.origin):
                    break
            if buffer.lower() in Tokenizer.reserved_words:
                self.actual = Token('Reserved', buffer.lower())
                return self.actual
            elif self.actual.value == 'function':
                self.actual = Token('NameFunc', buffer)
                return self.actual
            else:
                self.actual = Token('Funcall', buffer)
                return self.actual
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
            self.position += 1
            if self.origin[self.position] == "=":
                self.position += 1
                self.actual = Token('Symbol', '==')
            else:
                self.actual = Token('Eq', '=')
            return self.actual
        elif self.origin[self.position] == ">":
            self.actual = Token('Symbol', '>')
            self.position += 1
            return self.actual
        elif self.origin[self.position] == "<":
            self.position += 1
            if self.origin[self.position] == "?":
                self.position += 1
                if self.origin[self.position].lower() == "p":
                    self.position += 1
                    if self.origin[self.position].lower() == "h":
                        self.position += 1
                        if self.origin[self.position].lower() == "p":
                            self.position += 1
                            self.actual = Token('StartProgram', None)
                            return self.actual
                raise Exception("Wrong Start Program Token")
            self.actual = Token('Symbol', '<')
            return self.actual
        elif self.origin[self.position] == "?":
            self.position += 1
            if self.origin[self.position] == ">":
                self.position += 1
                self.actual = Token('EndProgram', None)
                return self.actual
            else:
                raise Exception("Wrong End Program Token")
        elif self.origin[self.position] == "!":
            self.actual = Token('Symbol', '!')
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
        elif self.origin[self.position] == ".":
            self.actual = Token('String', '.')
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
        elif self.origin[self.position] == ",":
            self.actual = Token('Virgula', ',')
            self.position += 1
            return self.actual
        elif self.origin[self.position] == '"':
            buffer = ''
            self.position += 1
            while self.origin[self.position] != '"':
                buffer += self.origin[self.position]
                self.position += 1
                if self.position == len(self.origin):
                    raise Exception('Missing "')
            self.position += 1
            self.actual = Token('Str', buffer)
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
        else:
            raise Exception("Invalid Token")


class Parser:  

    tokens = None
    nex = None
    
    
    @staticmethod
    def parseProgram():
        commands = []
        Parser.nex = Parser.tokens.actual

        if Parser.nex.type == 'StartProgram':
            Parser.nex = Parser.tokens.selectNext()
            while Parser.nex.type != 'EndProgram':
                commands.append(Parser.parseCommand())
            Parser.nex = Parser.tokens.selectNext()
        else:
            raise Exception("Expected start of program statement")
        return Commands(commands)

    
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
                command = Assignment(var_name, [Parser.parseRelExpression()])
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
                command = Echo([Parser.parseRelExpression()])
                if Parser.nex.value == ';':
                    Parser.nex = Parser.tokens.selectNext()
                    return command
                else:
                    raise Exception("Expected ;")
            elif Parser.nex.value == 'while':
                Parser.nex = Parser.tokens.selectNext()
                if Parser.nex.value == '(':
                    Parser.nex = Parser.tokens.selectNext()
                    relexp = Parser.parseRelExpression()
                    if Parser.nex.value != ')':
                        raise Exception('Expected ")"')
                    Parser.nex = Parser.tokens.selectNext()
                    command = WhileOp([relexp, Parser.parseCommand()])
                    return command
            elif Parser.nex.value == 'if':
                Parser.nex = Parser.tokens.selectNext()
                if Parser.nex.value == '(':
                    Parser.nex = Parser.tokens.selectNext()
                    relexp = Parser.parseRelExpression()
                    if Parser.nex.value != ')':
                        raise Exception('Expected ")"')
                    Parser.nex = Parser.tokens.selectNext()
                    pcommand = Parser.parseCommand()
                    command = ConditionalOp([relexp, pcommand])
                    if Parser.nex.value == 'else':
                        Parser.nex = Parser.tokens.selectNext()
                        command = ConditionalOp([relexp, pcommand, Parser.parseCommand()])
                    return command
            elif Parser.nex.value == 'function':
                Parser.nex = Parser.tokens.selectNext()
                funcname = Parser.nex.value
                Parser.nex = Parser.tokens.selectNext()
                if Parser.nex.value == '(':
                    Parser.nex = Parser.tokens.selectNext()
                    lista_var_func = []
                    while Parser.nex.type == 'Identifier':
                        lista_var_func.append(Parser.nex.value)
                        Parser.nex = Parser.tokens.selectNext()
                        if Parser.nex.value == ',':
                            Parser.nex = Parser.tokens.selectNext()
                        elif Parser.nex.value == ')':
                            break
                        else:
                            raise Exception('Wrong declaration of function')
                    if Parser.nex.value == ')':
                        Parser.nex = Parser.tokens.selectNext()
                        command = FuncDecOp(funcname, [lista_var_func, Parser.parseBlock()])
                        return command
                    else:
                        raise Exception('Wrong declaration of function')
                else:
                    raise Exception('Wrong declaration of function')
            elif Parser.nex.value == 'return':
                Parser.nex = Parser.tokens.selectNext()
                command = ReturnOp([Parser.parseRelExpression()])
                if Parser.nex.value == ';':
                    Parser.nex = Parser.tokens.selectNext()
                    return command
                else:
                    raise Exception("Expected ;")
            else:
                raise Exception('Syntax error') 
        elif Parser.nex.type == 'Funcall':
            funcname = Parser.nex.value
            Parser.nex = Parser.tokens.selectNext()
            if Parser.nex.value == '(':
                lista_entrada = []
                Parser.nex = Parser.tokens.selectNext()
                while Parser.nex.value != ')':
                    lista_entrada.append(Parser.parseRelExpression())
                    if Parser.nex.value == ',':
                        Parser.nex = Parser.tokens.selectNext()
                    elif Parser.nex.value == ')':
                        break
                    else:
                        raise Exception('Wrong function call declaration')
                if Parser.nex.value != ')':
                    raise Exception('Wrong function call declaration')
                Parser.nex = Parser.tokens.selectNext()
                command = FuncCallOp(funcname, lista_entrada)
                if Parser.nex.value == ';':
                    Parser.nex = Parser.tokens.selectNext()
                    return command
                else:
                    raise Exception("Expected ;")
            else:
                raise Exception('Wrong function call declaration')
        else:
            return Parser.parseBlock()
                                                                                                                                                                                                                                                                        
    
    @staticmethod
    def parseRelExpression():
        result = Parser.parseExpression()
        
        while Parser.nex.value in ['==','>','<']:
            if Parser.nex.value == '==':
                    Parser.nex = Parser.tokens.selectNext()            
                    result = BinOp('==', [result, Parser.parseExpression()])
            elif Parser.nex.value == '<':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('<', [result, Parser.parseExpression()])            
            elif Parser.nex.value == '>':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('>', [result, Parser.parseExpression()])
        return result               
   
    
    @staticmethod
    def parseExpression():    
        result = Parser.parseTerm()
                
        while Parser.nex.value in ['+','-','or','.']:
            if Parser.nex.value == '+':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('+', [result, Parser.parseTerm()])
            elif Parser.nex.value == '-':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('-', [result, Parser.parseTerm()])
            elif Parser.nex.value == 'or':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('or', [result, Parser.parseTerm()])
            elif Parser.nex.value == '.':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('.', [result, Parser.parseTerm()])           
        return result

    @staticmethod
    def parseTerm():      
        result = Parser.parseFactor()
                
        while Parser.nex.value in ['*','/','and']: 
            if Parser.nex.value == '*':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('*', [result, Parser.parseFactor()])
            elif Parser.nex.value == '/':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('/', [result, Parser.parseFactor()])
            elif Parser.nex.value == 'and':
                Parser.nex = Parser.tokens.selectNext()            
                result = BinOp('and', [result, Parser.parseFactor()])     
        return result

    @staticmethod
    def parseFactor():      
        Parser.nex = Parser.tokens.actual

        if Parser.nex.type == 'Num':
            result = IntVal(int(Parser.nex.value), None)
            Parser.nex = Parser.tokens.selectNext()
        elif Parser.nex.type == 'Str':
            result = StringVal(Parser.nex.value, None)
            Parser.nex = Parser.tokens.selectNext()
        elif Parser.nex.value == '+':
            Parser.nex = Parser.tokens.selectNext()
            result = UnOp('+', [Parser.parseFactor(), None])
        elif Parser.nex.value == '-':
            Parser.nex = Parser.tokens.selectNext()
            result = UnOp('-', [Parser.parseFactor(), None])
        elif Parser.nex.value == '!':
            Parser.nex = Parser.tokens.selectNext()
            result = UnOp('!', [Parser.parseFactor(), None])
        elif Parser.nex.value == '(':
            Parser.nex = Parser.tokens.selectNext()
            result = Parser.parseRelExpression()
            if Parser.nex.value != ')':
                raise Exception('Missing ")"')
            Parser.nex = Parser.tokens.selectNext()        
        elif Parser.nex.type == 'Identifier':
            result = Identifier(Parser.nex.value)
            Parser.nex = Parser.tokens.selectNext()    
        elif Parser.nex.type == 'Reserved':
            if Parser.nex.value == 'readline':
                Parser.nex = Parser.tokens.selectNext()
                if Parser.nex.value == '(':
                    Parser.nex = Parser.tokens.selectNext()
                    if Parser.nex.value == ')':
                        Parser.nex = Parser.tokens.selectNext()
                    else:
                        raise Exception('Wrong call readline() missing ")"')
                else:
                    raise Exception('Wrong call readline() missing "("')
                result = ReadLine(None, None)
            elif Parser.nex.value == 'true':
                result = BoolVal(True, None)
                Parser.nex = Parser.tokens.selectNext()
            elif Parser.nex.value == 'false':
                result = BoolVal(False, None)
                Parser.nex = Parser.tokens.selectNext()
        elif Parser.nex.type == 'Funcall':
            funcname = Parser.nex.value
            Parser.nex = Parser.tokens.selectNext()
            if Parser.nex.value == '(':
                lista_entrada = []
                Parser.nex = Parser.tokens.selectNext()
                while Parser.nex.value != ')':
                    lista_entrada.append(Parser.parseRelExpression())
                    if Parser.nex.value == ',':
                        Parser.nex = Parser.tokens.selectNext()
                    elif Parser.nex.value == ')':
                        break
                    else:
                        raise Exception('Wrong function call declaration')
                if Parser.nex.value != ')':
                    raise Exception('Wrong function call declaration')
                Parser.nex = Parser.tokens.selectNext()
                command = FuncCallOp(funcname, lista_entrada)
                return command
            else:
                raise Exception('Wrong function call declaration')    
        else:
            raise Exception('Invalid Syntax')   
        return result 

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        res = Parser.parseProgram()
        stable = SymbolTabl()

        if Parser.tokens.actual.value == 'EOF':
            return res.evaluate(stable)
        else:
            raise Exception("EOF or signal Expected")


if __name__ == "__main__":
    
    f = open(sys.argv[1], "r")

    Parser.run(PrePro.filter(f.read()))