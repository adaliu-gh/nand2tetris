//function Class1.set 0
@255
            M=0
            M=1
(Class1.set)

//pop static 0
@255
            M=0
            M=1
@SP
A=M-1
D=M
@StaticsTest.0
M=D
@SP
M=M-1
//pop static 1
@255
            M=0
            M=1
@SP
A=M-1
D=M
@StaticsTest.1
M=D
@SP
M=M-1
//return
@255
            M=0
            M=1
  @LCL
D=M
@T1
M=D
@5
A=D-A
D=M
@T2
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@T1
D=M
@1
A=D-A
D=M
@THAT
M=D
@T1
D=M
@2
A=D-A
D=M
@THIS
M=D
@T1
D=M
@3
A=D-A
D=M
@ARG
M=D
@T1
D=M
@4
A=D-A
D=M
@LCL
M=D
@T2
A=M
0;JMP
//function Class1.get 0
@255
            M=0
            M=1
(Class1.get)

//push static 1
@255
            M=0
            M=1
@StaticsTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1
//return
@255
            M=0
            M=1
  @LCL
D=M
@T1
M=D
@5
A=D-A
D=M
@T2
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@T1
D=M
@1
A=D-A
D=M
@THAT
M=D
@T1
D=M
@2
A=D-A
D=M
@THIS
M=D
@T1
D=M
@3
A=D-A
D=M
@ARG
M=D
@T1
D=M
@4
A=D-A
D=M
@LCL
M=D
@T2
A=M
0;JMP
