import sys

destcodes={'null':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111' }
jumpcodes={'null':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}
compcodes={'0':'101010','1':'111111','-1':'111010','D':'001100','A':'110000','!D':'001101','!A':'110001','-D':'001111','-A':'110011','D+1':'011111','A+1':'110111','D-1':'001110','A-1':'110010','D+A':'000010','D-A':'010011','A-D':'000111','D&A':'000000','D|A':'010101'}

entries={'SP':'0','LCL':'1','ARG':'2','THIS':'3','THAT':'4','SCREEN':'16384','KBD':'24576'}

for i in range(16):
    entry='R%i'% i
    entries[entry]=str(i)

if (len(sys.argv)!=2):
    sys.exit()

def removeun(line):
    line=line.replace(' ','')
    line=line.replace('\n','')
    if '/' in line:
        l=line.split('/')
        line=l[0]
    return line


def commandType(line):
    if line[0]=='@':
        return 'A_COMMAND'
    elif line[0]=='(':
        return 'L_COMMAND'
    else:
        return 'C_COMMAND'

def symbol(line):
    if line[0]=='@':
            return line[1:]
    else:
        return line[1:-1]

def parse(line):
    if '=' not in line:
           line='='+line
    if ';' not in line:
           line=line+';'
    part1=line.split('=')
    part2=part1[1].split(';')
    elements=[part1[0]]
    elements.extend(part2)
    return elements

def dest(elements):
    if elements[0]=='':
        return 'null'
    else:
        return elements[0]

def comp(elements):
    return elements[1]

def jump(line):
    if elements[2]=='':
        return 'null'
    else:
        return elements[2]

def dcdest(destsymbol):
    return destcodes[destsymbol]
def dcjump(jumpsymbol):
    return jumpcodes[jumpsymbol]
def dccomp(compsymbol):
    if 'M' in compsymbol:
        m=True
        compsymbol=compsymbol.replace('M','A')
    else:
        m=False
    code=compcodes[compsymbol]
    if m==True:
        code='1'+code
    else:
        code='0'+code
    return code

file=sys.argv[1]
with open(file) as tmp:
    n=-1
    while True:
        line=tmp.readline()
        if line=='':
            break
        line=removeun(line)
        if line=='':
            continue
        type=commandType(line)
        if type=='L_COMMAND':
            entry=symbol(line)
            entries[entry]=str(n+1)
        else:
            n+=1

with open(file) as asm:
    filename=file.split('.')[0]
    hack=open('%s1.hack'%filename,'w')
    addr=16
    while True:
        line=asm.readline()
        if line=='':
            break
        line=removeun(line)
        if line=='':
            continue
        type=commandType(line)
        if type=='A_COMMAND':
            s=symbol(line)
            if not s.isdigit():
                if s not in entries:
                    entries[s]=str(addr)
                    addr+=1
                s=entries[s]
            code=bin(int(s)).replace('b','0').rjust(16,'0')
            if len(code)>16:
                code=code[1:]
        elif type=='C_COMMAND':
            elements=parse(line)
            destcode=dcdest(dest(elements))
            compcode=dccomp(comp(elements))
            jumpcode=dcjump(jump(elements))
            code='111'+compcode+destcode+jumpcode
        else:
            continue

        hack.write('%s\n'%code)
        print('%s\t%s'%(line,code))
    hack.close()



for i in entries:
    print('%s\t%s\n'%(i,entries[i]))
