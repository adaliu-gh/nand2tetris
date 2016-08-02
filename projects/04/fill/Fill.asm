// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

(INIT)
@SCREEN
D=A
@ADDR
M=D
@32767
D=A
@CONSTANT
M=D
(LOOP)

@KBD
D=M
@BLACK
D;JGT
@CLEAN
D;JEQ

(BLACK)
@CONSTANT
D=M
@ADDR
A=M
M=D
@CAL
0;JMP



(CLEAN)
@ADDR
A=M
M=0
@CAL
0;JMP

(CAL)
@ADDR
MD=M+1
@KBD
D=D-A
@INIT
D;JGE
@LOOP
0;JMP
