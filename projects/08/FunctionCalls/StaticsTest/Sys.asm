//function Sys.init 0
@255
            M=0
            M=1
(Sys.init)

//push constant 8
@255
            M=0
            M=1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop temp 0
@255
            M=0
            M=1
@SP
A=M-1
D=M
@R5
M=D
@SP
M=M-1

//push constant 15
@255
            M=0
            M=1
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop temp 0
@255
            M=0
            M=1
@SP
A=M-1
D=M
@R5
M=D
@SP
M=M-1

//call Class2.get 0
@255
            M=0
            M=1

@StaticsTest.return1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
@ARG
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
@THIS
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
@THAT
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(StaticsTest.return1)

//goto WHILE
@255
            M=0
            M=1
@Sys.init$WHILE
                    0;JMP
