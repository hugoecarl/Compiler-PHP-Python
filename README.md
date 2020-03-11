# Compilator

###EBNF:
Expression = Term, {("+" | "-"), Term};
Term = Number, {("*" | "/"), Number};
Number = (0 | 1 | ... | 9) , {(0 | 1 | ... | 9)};

###Diagrama:
![Alt text](https://github.com/hugoecarl/Compilator/blob/roteiro2/diagrama.jpeg)
