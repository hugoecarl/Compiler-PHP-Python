; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss  ; variaveis
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  ; codigo gerado pelo compilador
PUSH DWORD 0
MOV EBX, 2;
MOV [EBP - 4], EBX;
PUSH DWORD 0
MOV EBX, 5;
MOV [EBP - 8], EBX;
PUSH DWORD 0
MOV EBX, 0;
MOV [EBP - 12], EBX;
PUSH DWORD 0
MOV EBX, 5;
MOV [EBP - 16], EBX;
PUSH DWORD 0
MOV EBX, 1;
MOV [EBP - 20], EBX;
PUSH DWORD 0
MOV EBX, 0;
MOV [EBP - 24], EBX;
LOOP_0:
MOV EBX, [EBP - 12];
PUSH EBX;
MOV EBX, [EBP - 16];
POP EAX;
CMP EAX, EBX;
CALL binop_jl;
PUSH EBX;
MOV EBX, [EBP - 12];
PUSH EBX;
MOV EBX, [EBP - 16];
POP EAX;
CMP EBX, EAX;
CALL binop_je;
POP EAX;
OR EAX, EBX;
MOV EBX, EAX;
CMP EBX, False;
JE SAIDALOOP_0;
MOV EBX, [EBP - 4];
PUSH EBX;
MOV EBX, [EBP - 8];
POP EAX;
CMP EAX, EBX;
CALL binop_jg;
CMP EBX, False;
JE ELSE_0;
MOV EBX, [EBP - 8];
PUSH EBX;
MOV EBX, 1;
POP EAX;
ADD EAX, EBX;
MOV EBX, EAX;
MOV [EBP - 8], EBX;
JMP SAIDACOND_0;
ELSE_0:
MOV EBX, [EBP - 4];
PUSH EBX;
MOV EBX, [EBP - 8];
POP EAX;
CMP EAX, EBX;
CALL binop_jl;
CMP EBX, False;
JE ELSE_1;
MOV EBX, [EBP - 4];
PUSH EBX;
MOV EBX, 1;
POP EAX;
ADD EAX, EBX;
MOV EBX, EAX;
MOV [EBP - 4], EBX;
LOOP_1:
MOV EBX, [EBP - 24];
PUSH EBX;
MOV EBX, 6;
POP EAX;
CMP EAX, EBX;
CALL binop_jl;
CMP EBX, False;
JE SAIDALOOP_1;
PUSH DWORD 0
MOV EBX, 0;
MOV [EBP - 28], EBX;
LOOP_2:
MOV EBX, [EBP - 28];
PUSH EBX;
MOV EBX, 6;
POP EAX;
CMP EAX, EBX;
CALL binop_jl;
CMP EBX, False;
JE SAIDALOOP_2;
MOV EBX, 9;
PUSH EBX;
CALL print;
POP EBX;
MOV EBX, [EBP - 28];
PUSH EBX;
MOV EBX, 1;
POP EAX;
ADD EAX, EBX;
MOV EBX, EAX;
MOV [EBP - 28], EBX;
JMP LOOP_2;
SAIDALOOP_2:
MOV EBX, [EBP - 24];
PUSH EBX;
MOV EBX, 1;
POP EAX;
ADD EAX, EBX;
MOV EBX, EAX;
MOV [EBP - 24], EBX;
JMP LOOP_1;
SAIDALOOP_1:
JMP SAIDACOND_1;
ELSE_1:
MOV EBX, [EBP - 4];
PUSH EBX;
MOV EBX, [EBP - 8];
POP EAX;
CMP EBX, EAX;
CALL binop_je;
PUSH EBX;
MOV EBX, True;
POP EAX;
AND EAX, EBX;
MOV EBX, EAX;
CMP EBX, False;
JE ELSE_2;
MOV EBX, 7;
PUSH EBX;
CALL print;
POP EBX;
JMP SAIDACOND_2;
ELSE_2:
MOV EBX, [EBP - 20];
PUSH EBX;
MOV EBX, 2;
POP EAX;
IMUL EBX;
MOV EBX, EAX;
MOV [EBP - 20], EBX;
MOV EBX, [EBP - 20];
PUSH EBX;
CALL print;
POP EBX;
SAIDACOND_2:
SAIDACOND_1:
SAIDACOND_0:
MOV EBX, [EBP - 12];
PUSH EBX;
CALL print;
POP EBX;
MOV EBX, [EBP - 12];
PUSH EBX;
MOV EBX, 1;
POP EAX;
ADD EAX, EBX;
MOV EBX, EAX;
MOV [EBP - 12], EBX;
JMP LOOP_0;
SAIDALOOP_0:
MOV EBX, 25;
PUSH EBX;
MOV EBX, True;
POP EAX;
AND EAX, EBX;
MOV EBX, EAX;
PUSH EBX;
CALL print;
POP EBX;
MOV EBX, False;
PUSH EBX;
MOV EBX, False;
POP EAX;
CMP EBX, EAX;
CALL binop_je;
CMP EBX, False;
JE SAIDACOND_3;
MOV EBX, 2;
PUSH EBX;
CALL print;
POP EBX;
SAIDACOND_3:
MOV EBX, [EBP - 4];
PUSH EBX;
CALL print;
POP EBX;


  ; interrupcao de saida
  POP EBP
  MOV EAX, 1
  INT 0x80