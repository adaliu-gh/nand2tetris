@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@EQ3
D;JEQ
@NOTEQ3
D;JNE
(EQ3)
@SP
A=M-1
A=A-1
M=-1
@END3
0;JMP
(NOTEQ3)
@SP
A=M-1
A=A-1
M=0
@END3
0;JMP
(END3)
@SP
M=M-1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@EQ6
D;JEQ
@NOTEQ6
D;JNE
(EQ6)
@SP
A=M-1
A=A-1
M=-1
@END6
0;JMP
(NOTEQ6)
@SP
A=M-1
A=A-1
M=0
@END6
0;JMP
(END6)
@SP
M=M-1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@EQ9
D;JEQ
@NOTEQ9
D;JNE
(EQ9)
@SP
A=M-1
A=A-1
M=-1
@END9
0;JMP
(NOTEQ9)
@SP
A=M-1
A=A-1
M=0
@END9
0;JMP
(END9)
@SP
M=M-1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@LT12
D;JLT
@NOTLT12
D;JGE
(LT12)
@SP
A=M-1
A=A-1
M=-1
@END12
0;JMP
(NOTLT12)
@SP
A=M-1
A=A-1
M=0
@END12
0;JMP
(END12)
@SP
M=M-1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@LT15
D;JLT
@NOTLT15
D;JGE
(LT15)
@SP
A=M-1
A=A-1
M=-1
@END15
0;JMP
(NOTLT15)
@SP
A=M-1
A=A-1
M=0
@END15
0;JMP
(END15)
@SP
M=M-1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@LT18
D;JLT
@NOTLT18
D;JGE
(LT18)
@SP
A=M-1
A=A-1
M=-1
@END18
0;JMP
(NOTLT18)
@SP
A=M-1
A=A-1
M=0
@END18
0;JMP
(END18)
@SP
M=M-1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@GT21
D;JGT
@NOTGT21
D;JLE
(GT21)
@SP
A=M-1
A=A-1
M=-1
@END21
0;JMP
(NOTGT21)
@SP
A=M-1
A=A-1
M=0
@END21
0;JMP
(END21)
@SP
M=M-1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@GT24
D;JGT
@NOTGT24
D;JLE
(GT24)
@SP
A=M-1
A=A-1
M=-1
@END24
0;JMP
(NOTGT24)
@SP
A=M-1
A=A-1
M=0
@END24
0;JMP
(END24)
@SP
M=M-1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
D=M-D
@GT27
D;JGT
@NOTGT27
D;JLE
(GT27)
@SP
A=M-1
A=A-1
M=-1
@END27
0;JMP
(NOTGT27)
@SP
A=M-1
A=A-1
M=0
@END27
0;JMP
(END27)
@SP
M=M-1
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
@SP
A=M-1
M=-M
@SP
A=M-1
D=M
A=A-1
M=D&M
@SP
M=M-1
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=D|M
@SP
M=M-1
@SP
A=M-1
M=!M
