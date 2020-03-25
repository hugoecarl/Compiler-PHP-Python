# Compilator

### EBNF:  
Expression = Term, {("+" | "-"), Term};  
Term = Factor, {("*" | "/"), Factor};  
Factor = Number | ("+" | "-"), Factor | "(", Expression, ")";  
Number = (0 | 1 | ... | 9) , {(0 | 1 | ... | 9)};  

### Diagrama:  
![Alt text](https://github.com/hugoecarl/Compilator/blob/roteiro3/diagrama.jpeg)
