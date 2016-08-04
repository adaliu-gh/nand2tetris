import parser
import os,sys

commandctypes={'label':'C_LABEL','goto':'C_GOTO','if-goto':'C_IFGOTO','function':'C_FUNCTION','push':'C_PUSH','pop':'C_POP'}
arithmetics={'add':'''@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1''',

'sub':'''@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1''',

'neg':'''@SP
A=M-1
M=-M''',

'eq':'''@SP
A=M-1
D=M
A=A-1
D=M-D
@EQ%i
D;JEQ
@NOTEQ%i
D;JNE
(EQ%i)
@SP
A=M-1
A=A-1
M=-1
@END%i
0;JMP
(NOTEQ%i)
@SP
A=M-1
A=A-1
M=0
@END%i
0;JMP
(END%i)
@SP
M=M-1''',

'gt':'''@SP
A=M-1
D=M
A=A-1
D=M-D
@GT%i
D;JGT
@NOTGT%i
D;JLE
(GT%i)
@SP
A=M-1
A=A-1
M=-1
@END%i
0;JMP
(NOTGT%i)
@SP
A=M-1
A=A-1
M=0
@END%i
0;JMP
(END%i)
@SP
M=M-1''',


'lt':'''@SP
A=M-1
D=M
A=A-1
D=M-D
@LT%i
D;JLT
@NOTLT%i
D;JGE
(LT%i)
@SP
A=M-1
A=A-1
M=-1
@END%i
0;JMP
(NOTLT%i)
@SP
A=M-1
A=A-1
M=0
@END%i
0;JMP
(END%i)
@SP
M=M-1''',

'and':'''@SP
A=M-1
D=M
A=A-1
M=D&M
@SP
M=M-1''',

'or':
'''@SP
A=M-1
D=M
A=A-1
M=D|M
@SP
M=M-1''',

'not':
'''@SP
A=M-1
M=!M'''

       }

pushregex='''@%i
D=A
@%s
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1'''

popregex='''@%i
D=A
@%s
A=M
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
'''

constantregex='''@%i
D=A
@SP
A=M
M=D
@SP
M=M+1'''

pointerpop='''@SP
A=M-1
D=M
@%s
M=D
@SP
M=M-1
'''

pointerpush='''@%s
D=M
@SP
A=M
M=D
@SP
M=M+1'''

pushtemp='''@R%i
D=M
@SP
A=M
M=D
@SP
M=M+1'''

poptemp='''@SP
A=M-1
D=M
@R%i
M=D
@SP
M=M-1
'''

staticpush='''@%s.%i
D=M
@SP
A=M
M=D
@SP
M=M+1'''

staticpop='''@SP
A=M-1
D=M
@%s.%i
M=D
@SP
M=M-1'''

arg1s={'local':'LCL','argument':"ARG",'this':"THIS",'that':"THAT",'pointer':['THIS',"THAT"]}
temps={'push':pushtemp,'pop':poptemp}
statics={'push':staticpush,'pop':staticpop}
pushpop={'push':pushregex,'pop':popregex}
pointers={'push':pointerpush,'pop':pointerpop}
def writeArithmetic(command):
    return arithmetics[command]
def writepushpop(filename,command,a1,a2):
    if a1=='constant':
        code=constantregex%a2
    elif a1=='pointer':
        code=pointers[command]%arg1s[a1][a2]
    elif a1=='temp':
        code=temps[command]%(a2+5)
    elif a1=='static':
        code=statics[command]%(filename,a2)
    else:
        code=pushpop[command]%(a2,arg1s[a1])
    return code

def decode(singlefile):
    print(singlefile)
    with open(singlefile,'r') as f:
        name=os.path.basename(singlefile).split('.')[0]
        asmname=os.path.join(os.path.dirname(singlefile),"%s.asm"%name)
        asm=open(asmname,'w')
        print(asmname)
        print()
        n=0
        while True:
            line=f.readline()
            if line=='':
                break
            line=parser.removeun(line)
            if line=='':
                continue
            n+=1
            line=parser.removeun(line)
            command=line.split()[0]
            ctype=parser.commandType(command)
            a1=parser.arg1(line,ctype)
            if ctype=='C_ARITHMETIC':
                code=writeArithmetic(command)
                if command in ['eq','gt','lt']:
                    code=code%(n,n,n,n,n,n,n)
            elif ctype=='C_PUSH' or ctype=="C_POP":
                a2=parser.arg2(line)
                code=writepushpop(name,command,a1,a2)
            asm.write("%s\n"%code)
        asm.close()
if len(sys.argv)<2:
    print('Usage:file/path')
    sys.exit()

fileorpath=os.path.abspath(sys.argv[1])

#if os.path.isfile(fileorpath):
#    decode(fileorpath)
#else:
#    for foldername,subfolders,filenames in os.walk(fileorpath):
#        for filename in filenames:
#            if filename.endswith('.vm'):
#                decode(os.path.abspath(filename))

def walkthrough(fop):
    if os.path.isfile(fop):
        if fop.endswith('.vm'):
            decode(fop)
    else:
        for path in os.listdir(fop):
            walkthrough(os.path.join(fop,path))


walkthrough(fileorpath)
