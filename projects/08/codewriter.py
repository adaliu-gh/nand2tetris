import parsers
import os
import sys

commandctypes = {'label': 'C_LABEL', 'goto': 'C_GOTO', 'if-goto': 'C_IFGOTO',
                 'function': 'C_FUNCTION', 'push': 'C_PUSH', 'pop': 'C_POP', 'call': 'C_CALL', 'return': 'C_RETURN'}
functiontypes = ['C_FUNCTION', 'C_RETURN', 'C_CALL']
initials = ['@256', 'D=A', '@SP', 'M=D', '@Sys.init', '0;JMP']

arithmetics = {'add': '''@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1''',

               'sub': '''@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1''',

               'neg': '''@SP
A=M-1
M=-M''',

               'eq': '''@SP
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

               'gt': '''@SP
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


               'lt': '''@SP
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

               'and': '''@SP
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

pushregex = '''@%i
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

popregex = '''@%i
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

constantregex = '''@%i
D=A
@SP
A=M
M=D
@SP
M=M+1'''

pointerpop = '''@SP
A=M-1
D=M
@%s
M=D
@SP
M=M-1
'''

pointerpush = '''@%s
D=M
@SP
A=M
M=D
@SP
M=M+1'''

pushtemp = '''@R%i
D=M
@SP
A=M
M=D
@SP
M=M+1'''

poptemp = '''@SP
A=M-1
D=M
@R%i
M=D
@SP
M=M-1
'''

staticpush = '''@%s.%i
D=M
@SP
A=M
M=D
@SP
M=M+1'''

staticpop = '''@SP
A=M-1
D=M
@%s.%i
M=D
@SP
M=M-1'''

returncode = '''  @LCL
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
0;JMP'''

callhead = '''
@%s
D=A
@SP
A=M
M=D
@SP
M=M+1\n'''
calltail = '''@%i
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
@%s
0;JMP
(%s)\n'''

arg1s = {'local': 'LCL', 'argument': "ARG", 'this': "THIS",
         'that': "THAT", 'pointer': ['THIS', "THAT"]}
temps = {'push': pushtemp, 'pop': poptemp}
statics = {'push': staticpush, 'pop': staticpop}
pushpop = {'push': pushregex, 'pop': popregex}
pointers = {'push': pointerpush, 'pop': pointerpop}


def writeArithmetic(command):
    return arithmetics[command]


def writepushpop(filename, command, a1, a2):
    if a1 == 'constant':
        code = constantregex % a2
    elif a1 == 'pointer':
        code = pointers[command] % arg1s[a1][a2]
    elif a1 == 'temp':
        code = temps[command] % (a2 + 5)
    elif a1 == 'static':
        code = statics[command] % (filename, a2)
    else:
        code = pushpop[command] % (a2, arg1s[a1])
    return code


def writecall(line):
    a2 = parsers.arg2(line)
    code = callhead
    for i in ['LCL', 'ARG', 'THIS', 'THAT']:
        code += '''@%s
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1\n''' % i
    code += calltail

    return code


def decodebasics(basename, line, ctype, current_function):
    command = line.split()[0]
    a1 = parsers.arg1(line, ctype)
    if ctype == 'C_ARITHMETIC':
        code = writeArithmetic(command)
        if command in ['eq', 'gt', 'lt']:
            code = code % (n, n, n, n, n, n, n)
    elif ctype == 'C_PUSH' or ctype == "C_POP":
        a2 = parsers.arg2(line)
        code = writepushpop(basename, command, a1, a2)

    elif ctype == 'C_GOTO':
        label = '%s$%s' % (current_function, a1)
        code = '''@%s
                0;JMP''' % label
    elif ctype == 'C_IFGOTO':
        label = '%s$%s' % (current_function, a1)
        code = '''@SP
                A=M-1
                D=M
                @SP
                M=M-1
                @%s
                D;JNE''' % label
    elif ctype == 'C_LABEL':
        label = '%s$%s' % (current_function, a1)
        code = '''(%s)''' % label
    return code


def decode(fromfile, tofile):
    print(fromfile)
    f = open(fromfile, 'r')
    basename = os.path.basename(fromfile).split('.')[0]
    asm = tofile
    n = 0
    calls = 0
    current_function = 'null'
    while True:
        line = f.readline()
        if line == '':
            break
        line = parsers.removeun(line)
        if line == '':
            continue
        n += 1
        asm.write('//%s\n' % line)
        if line in initials:
            asm.write('%s\n' % line)
            continue
        command = line.split()[0]
        ctype = parsers.commandType(command)
        a1 = parsers.arg1(line, ctype)
        if ctype == 'C_ARITHMETIC':
            code = writeArithmetic(command)
            if command in ['eq', 'gt', 'lt']:
                code = code % (n, n, n, n, n, n, n)
        elif ctype == 'C_PUSH' or ctype == "C_POP":
            a2 = parsers.arg2(line)
            code = writepushpop(basename, command, a1, a2)

        elif ctype == 'C_GOTO':
            label = '%s$%s' % (current_function, a1)
            code = '''@%s
                    0;JMP''' % label
        elif ctype == 'C_IFGOTO':
            label = '%s$%s' % (current_function, a1)
            code = '''@SP
                    A=M-1
                    D=M
                    @SP
                    M=M-1
                    @%s
                    D;JNE''' % label
        elif ctype == 'C_LABEL':
            label = '%s$%s' % (current_function, a1)
            code = '''(%s)''' % label

        elif ctype == 'C_FUNCTION':
            code = '(%s)\n' % a1
            a2 = parsers.arg2(line)
            current_function = a1
            for i in range(a2):
                code = code + \
                    decodebasics(basename, 'push constant 0',
                                 'C_PUSH', a1) + '\n'
        elif ctype == 'C_RETURN':
            code = returncode
        elif ctype == 'C_CALL':
            calls += 1
            elements = line.split()
            if len(elements) < 3:
                a2 = 0
            else:
                a2 = int(elements[2])
            callregex = writecall(line)
            symbol = '%s.return%i' % (basename, calls)
            code = callregex % (symbol, a2, a1, symbol)
        else:
            print('nothing')

        asm.write('''@255
            M=0
            M=1\n''')
        asm.write("%s\n" % code)


if len(sys.argv) < 2:
    print('Usage:file/path')
    sys.exit()

fileorpath = os.path.abspath(sys.argv[1])
print(fileorpath)

if os.path.isfile(fileorpath):
    decode(fileorpath)
else:
    for foldername, subfolders, filenames in os.walk(fileorpath):
        foldername = os.path.abspath(foldername)
        basename = os.path.basename(foldername).split('.')[0]

        if 'Sys.vm' in filenames:
            newfile = os.path.join(foldername, '%s.asm' % basename)
            with open(newfile, 'w') as asm:
                asm.write('''@Sys.init
                         0;JMP\n''')
                for i in filenames:
                    i = os.path.join(foldername, i)
                    if i.endswith('.vm') :
                        decode(i, asm)

        else:
            for i in filenames:
                if i.endswith('.vm'):
                    tofile = open(os.path.join(
                        foldername, "%s.asm" % i.split('.')[0]), 'w')
                    i = os.path.join(foldername, i)
                    decode(i, tofile)
                    tofile.close()

  