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
        
class Assembly():

    def __init__(self):
        self.lista_inst = []
        self.num_loop = 0
        self.saidaloop = 0
        self.num_else = 0
        self.saidacond = 0

    def addinst(self, inst):
        self.lista_inst.append(inst)

    def writeFile(self, file):
       # for i in self.lista_inst:
        #    print(i)
        f = open('modelo.asm', 'r')
        p = open('saida.asm', 'w')
        p.write('')
        p.close()
        f1 = open('saida.asm', 'a')

        
        for i in f:
            f1.write(i)
            if 'codigo gerado pelo compilador' in i:
                for j in self.lista_inst:
                    f1.write(j+'\n')
        
        f.close()
        f1.close()

    def numLoop(self):
        label = self.num_loop
        self.num_loop += 1
        return label

    def saidaLoop(self):
        label = self.saidaloop
        self.saidaloop += 1
        return label

    def numElse(self):
        label = self.num_else
        self.num_else += 1
        return label

    def saidaCond(self):
        label = self.saidacond
        self.saidacond += 1
        return label




class Node:

    def __init__(self, value, children):
        self.value = None
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        return 


class BinOp(Node):
    
    def __init__(self,value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        # if self.value in ['+', '-', '*', '/', '>', '<', 'or', 'and'] and (self.children[0].evaluate(SymbolTable)[1] == str or self.children[1].evaluate(SymbolTable)[1] == str):
        #     raise Exception('Operation not permitted with strings')
        if self.value == '+':
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('PUSH EBX;')
            self.children[1].evaluate(SymbolTable, Assembly)
            Assembly.addinst('POP EAX;')
            Assembly.addinst('ADD EAX, EBX;')
            Assembly.addinst('MOV EBX, EAX;')     
        elif self.value == '-':
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('PUSH EBX;')
            self.children[1].evaluate(SymbolTable, Assembly)
            Assembly.addinst('POP EAX;')
            Assembly.addinst('SUB EAX, EBX;')
            Assembly.addinst('MOV EBX, EAX;') 
        elif self.value == '*':
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('PUSH EBX;')
            self.children[1].evaluate(SymbolTable, Assembly)
            Assembly.addinst('POP EAX;')
            Assembly.addinst('IMUL EBX;')
            Assembly.addinst('MOV EBX, EAX;') 
        elif self.value == '/':
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('PUSH EBX;')
            self.children[1].evaluate(SymbolTable, Assembly)
            Assembly.addinst('POP EAX;')
            Assembly.addinst('IDIV EBX;')
            Assembly.addinst('MOV EBX, EAX;') 
        elif self.value == '>':            
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('PUSH EBX;')
            self.children[1].evaluate(SymbolTable, Assembly)
            Assembly.addinst('POP EAX;')
            Assembly.addinst('CMP EAX, EBX;')
            Assembly.addinst('CALL binop_jg;') 
        elif self.value == '<':
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('PUSH EBX;')
            self.children[1].evaluate(SymbolTable, Assembly)
            Assembly.addinst('POP EAX;')
            Assembly.addinst('CMP EAX, EBX;')
            Assembly.addinst('CALL binop_jl;') 
        elif self.value == 'or':
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('PUSH EBX;')
            self.children[1].evaluate(SymbolTable, Assembly)
            Assembly.addinst('POP EAX;')
            Assembly.addinst('OR EAX, EBX;')
            Assembly.addinst('MOV EBX, EAX;')     
        elif self.value == 'and':
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('PUSH EBX;')
            self.children[1].evaluate(SymbolTable, Assembly)
            Assembly.addinst('POP EAX;')
            Assembly.addinst('AND EAX, EBX;')
            Assembly.addinst('MOV EBX, EAX;')     
        elif self.value == '==':
        #     # if (self.children[0].evaluate(SymbolTable)[1] == str and self.children[1].evaluate(SymbolTable)[1] != str) or (self.children[1].evaluate(SymbolTable)[1] == str and self.children[0].evaluate(SymbolTable)[1] != str):
        #     #     raise Exception('Operation == not permitted with strings and different type')
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('PUSH EBX;')
            self.children[1].evaluate(SymbolTable, Assembly)
            Assembly.addinst('POP EAX;')
            Assembly.addinst('CMP EBX, EAX;')
            Assembly.addinst('CALL binop_je;') 
         #elif self.value == '.':
          #   return (str(self.children[0].evaluate(SymbolTable)[0]) + str(self.children[1].evaluate(SymbolTable)[0]), str)    



class UnOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        # if self.children[0].evaluate(SymbolTable)[1] == str:
        #     raise Exception('Operation not permitted with strings')
        if self.value == '+':
            self.children[0].evaluate(SymbolTable, Assembly)
        elif self.value == '-':
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('NEG EBX;')
        elif self.value == '!':
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('NOT EBX;')       


class NoOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        pass


# class ReadLine(Node):
        
#     def __init__(self, value, children):
#         self.value = value
#         self.children = children

#     def evaluate(self, SymbolTable):
#         self.value = int(input())
#         return (self.value, int)


class IntVal(Node):
        
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        Assembly.addinst('MOV EBX, ' + str(self.value) + ';')


class BoolVal(Node):
        
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        Assembly.addinst('MOV EBX, ' + str(self.value) + ';')


# class StringVal(Node):
        
#     def __init__(self, value, children):
#         self.value = value
#         self.children = children

#     def evaluate(self, SymbolTable):
#         return (self.value, str)


class SymbolTable():
    
    def __init__(self):
        self.Symbols = {}
        self.var_num = 1
    
    def Set(self, symbol, value, Assembly):
        self.Symbols[symbol] = value

    def Get(self, symbol, Assembly):
        if symbol in self.Symbols:
            Assembly.addinst('MOV EBX, [EBP - '+str(self.Symbols[symbol])+'];')  
        else:
            raise Exception("Variavel inexistente")


class Assignment(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        if self.value not in SymbolTable.Symbols:
            Assembly.addinst('PUSH DWORD 0')
            self.children[0].evaluate(SymbolTable, Assembly)
            SymbolTable.Set(self.value, SymbolTable.var_num * 4, Assembly)
            SymbolTable.var_num += 1
            Assembly.addinst('MOV [EBP - '+str(SymbolTable.Symbols[self.value])+'], EBX;')
        else:
            self.children[0].evaluate(SymbolTable, Assembly)
            Assembly.addinst('MOV [EBP - '+str(SymbolTable.Symbols[self.value])+'], EBX;')


class Identifier(Node):

    def __init__(self, value):
        self.value = value
    
    def evaluate(self, SymbolTable, Assembly):
        SymbolTable.Get(self.value, Assembly)


class WhileOp(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        nloop = Assembly.numLoop()
        sloop = Assembly.saidaLoop()
        Assembly.addinst('LOOP_'+str(nloop)+':')
        self.children[0].evaluate(SymbolTable, Assembly)
        Assembly.addinst('CMP EBX, False;')
        Assembly.addinst('JE SAIDALOOP_'+str(sloop)+';')
        self.children[1].evaluate(SymbolTable, Assembly)
        Assembly.addinst('JMP LOOP_'+str(nloop)+';')
        Assembly.addinst('SAIDALOOP_'+str(sloop)+':')


class ConditionalOp(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        nelse = Assembly.numElse()
        scond = Assembly.saidaCond()   
        self.children[0].evaluate(SymbolTable, Assembly)
        Assembly.addinst('CMP EBX, False;')
        if len(self.children) == 3:
            Assembly.addinst('JE ELSE_'+str(nelse)+';')
        else:
            Assembly.addinst('JE SAIDACOND_'+str(scond)+';')
        self.children[1].evaluate(SymbolTable, Assembly)
        if len(self.children) == 3:
            Assembly.addinst('JMP SAIDACOND_'+str(scond)+';')
            Assembly.addinst('ELSE_'+str(nelse)+':')
            self.children[2].evaluate(SymbolTable, Assembly)
        Assembly.addinst('SAIDACOND_'+str(scond)+':')

        

class Commands(Node):

    def __init__(self, children):
        self.children = children 

    def evaluate(self, SymbolTable, Assembly):
        for i in self.children:
            i.evaluate(SymbolTable, Assembly)


class Echo(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self, SymbolTable, Assembly):
        self.children[0].evaluate(SymbolTable, Assembly)
        Assembly.addinst('PUSH EBX;')
        Assembly.addinst('CALL print;')
        Assembly.addinst('POP EBX;')


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:

    reserved_words = ['echo', 'while', 'if', 'else', 'or', 'and', 'true', 'false'] #excluido readline

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
        # elif self.origin[self.position] == ".":
        #     self.actual = Token('String', '.')
        #     self.position += 1
        #     return self.actual
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
        # elif self.origin[self.position] == '"':
        #     buffer = ''
        #     self.position += 1
        #     while self.origin[self.position] != '"':
        #         buffer += self.origin[self.position]
        #         self.position += 1
        #         if self.position == len(self.origin):
        #             raise Exception('Missing "')
        #     self.position += 1
        #     self.actual = Token('Str', buffer)
        #     return self.actual
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
            if Parser.nex.value == 'while':
                Parser.nex = Parser.tokens.selectNext()
                if Parser.nex.value == '(':
                    Parser.nex = Parser.tokens.selectNext()
                    relexp = Parser.parseRelExpression()
                    if Parser.nex.value != ')':
                        raise Exception('Expected ")"')
                    Parser.nex = Parser.tokens.selectNext()
                    command = WhileOp([relexp, Parser.parseCommand()])
                    return command
            if Parser.nex.value == 'if':
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
            else:
                raise Exception('Syntax error') 
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
            # elif Parser.nex.value == '.':
            #     Parser.nex = Parser.tokens.selectNext()            
            #     result = BinOp('.', [result, Parser.parseTerm()])           
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
        # elif Parser.nex.type == 'Str':
        #     result = StringVal(Parser.nex.value, None)
        #     Parser.nex = Parser.tokens.selectNext()
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
            # if Parser.nex.value == 'readline':
            #     Parser.nex = Parser.tokens.selectNext()
            #     if Parser.nex.value == '(':
            #         Parser.nex = Parser.tokens.selectNext()
            #         if Parser.nex.value == ')':
            #             Parser.nex = Parser.tokens.selectNext()
            #         else:
            #             raise Exception('Wrong call readline() missing ")"')
            #     else:
            #         raise Exception('Wrong call readline() missing "("')
            #     result = ReadLine(None, None)
            if Parser.nex.value == 'true':
                result = BoolVal(True, None)
                Parser.nex = Parser.tokens.selectNext()
            elif Parser.nex.value == 'false':
                result = BoolVal(False, None)
                Parser.nex = Parser.tokens.selectNext()
        else:
            raise Exception('Invalid Syntax')   
        return result 

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        res = Parser.parseProgram()
        stable = SymbolTable()
        assembly = Assembly()

        if Parser.tokens.actual.value == 'EOF':
            res.evaluate(stable, assembly)
            assembly.writeFile('teste')
        else:
            raise Exception("EOF or signal Expected")


if __name__ == "__main__":
    
    f = open(sys.argv[1], "r")

    Parser.run(PrePro.filter(f.read()))
