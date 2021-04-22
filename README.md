# Compilator

This project is a version of a php compilator made using python, with a pre-processing stage, a lexic, syntactic and semantic analyzer to translate the inputs from a simple text into an assembly instruction that can run in any x86-64 architecture (branch roteiro8), or just for running using python the php code (main). The whole project is built in the file main.py, to run just execute the main script with the php code or file as an input. The script first remove all comments in the pre-processing section and then tokenizes all the characters for the parser to build the stacks of commands, executing everything in the right order. You can use the .php file in the repo to run the example or build your own :).

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
