def vmConstructor(filename):
	f=open(filename,'w')
	return

def writeFunction(name,nArgs):
    f.write('function %s %i\n'%(name,nArgs))
    return

def writeReturn():
	f.write('return\n')
	return
	
def writeIf(label):
	f.write('if-got %s\n'%label)
	return

def writeGoto(label):
	f.write('goto %s\n'%label)
	return
	
def writeLabel(label):
	f.write('label %s\n'%label)
	return
	
def writeArithmetic(command):
	f.write('%s\n'%command)
	return

def writePop(segment,index):
	f.write('pop %s %i\n' %(segment,index))
	return
def writePush(segment,index):
	f.write('push %s %i\n'%(segment,index))
	return

def writeCall(name,nArgs):
	f.write('call %s %i\n'%(name,nArgs))
	return

def vmclose():
	f.close()
	return
