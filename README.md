# Compilator

## EBNF:  
#### Program = "<?php", Command, "?>";
#### Block = "{", {Command}, "}";  
#### Command = (lambda | Assignament | Print), ";" | Block | Condition | Iteration;  
#### Assignment = Identifier, "=", Relexpr, ";";  
#### Print = "echo", Relexpr";";  
#### Condition = "if","(",Relexpr,")", Command, ["else", Command];
#### Iteration = "while","(",Relexpr,")", Command;
#### Relexpr = Expression, {("==" | ">" | "<"), Expression}
#### Expression = Term, {("+" | "-" | "or" | "."), Term};  
#### Term = Factor, {("*" | "/" | "and"), Factor};  
#### Factor = Number | ("+" | "-" | "!"), Factor | "(", Relexpr, ")" | Identifier | Input | Bool | String;  
#### Identifier = "$", Letter, {Letter | Digit | "_"};  
#### Number = Digit , {Digit};  
#### Letter = (a | ... | z | A | ... | Z);  
#### Digit = (0 | 1 | ... | 9);
#### String = """, Letter, {Letter}, """;  
#### Input = "readline()"  
#### Bool = true | false;  
## Diagrama:  
![Alt text](https://github.com/hugoecarl/Compilator/blob/master/diagrama.JPG)
