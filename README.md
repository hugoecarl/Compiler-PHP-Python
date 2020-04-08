# Compilator

## EBNF:  
#### Block = "{", {Command}, "}";  
#### Command = (lambda | Assignament | Print), ";" | Block;  
#### Assignment = Identifier, "=", Expression, ";";  
#### Print = "echo", Expression, ";";  
#### Expression = Term, {("+" | "-"), Term};  
#### Term = Factor, {("*" | "/"), Factor};  
#### Factor = Number | ("+" | "-"), Factor | "(", Expression, ")" | Identifier;  
#### Identifier = "$", Letter, {Letter | Digit | "_"};  
#### Number = Digit , {Digit};  
#### Letter = (a | ... | z | A | ... | Z);  
#### Digit = (0 | 1 | ... | 9);  

### Diagrama:  
![Alt text](https://github.com/hugoecarl/Compilator/blob/roteiro5/diagrama.jpeg)
