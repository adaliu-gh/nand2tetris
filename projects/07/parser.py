commandtypes={'label':'C_LABEL','goto':'C_GOTO','if-goto':'C_IFGOTO','function':'C_FUNCTION','push':'C_PUSH','pop':"C_POP"}
arithmetics=['add','sub','neg','eq','gt','lt','and','not','or']
def commandType(command):
    if command in arithmetics:
        return "C_ARITHMETIC"
    else:
        return commandtypes[command]
def arg1(line,type):
    if type=="C_ARITHMETIC":
        return line.split()[0]
    else:
        return line.split()[1]
def arg2(line):
    return int(line.split()[2])
def removeun(line):
    line=line.replace('\n','')
    if '/' in line:
        line=line.split('/')[0]
    line=line.strip()
    return line

