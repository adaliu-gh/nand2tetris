from JackTokenizer import *
variables = []
classes = []
types = []
subroutines = []


def compileClass(tokens, tokennumber, f, length):

    def printtoken(token):
        writetoken(token, f)
        tokennumber[0] += 1
        return

    def compileClassName():
        if tokens[tokennumber[0]] not in classes:
            classes.append(tokens[tokennumber[0]])
        printtoken(tokens[tokennumber[0]])
        return

    def compileType():
        if tokens[tokennumber[0]] not in types:
            types.append(tokens[tokennumber[0]])
        if tokens[tokennumber[0]] in ['int', 'char', 'boolean']:
            printtoken(tokens[tokennumber[0]])
        else:
            compileClassName()
        return

    def compileVarName():
        if tokens[tokennumber[0]] not in variables:
            variables.append(tokens[tokennumber[0]])
        printtoken(tokens[tokennumber[0]])
        return

    def compileSubroutineName():
        if tokens[tokennumber[0]] not in subroutines:
            subroutines.append(tokens[tokennumber[0]])
        printtoken(tokens[tokennumber[0]])
        return

    def compileClassVarDec():
        f.write('<classVarDec>\n')
        printtoken(tokens[tokennumber[0]])
        compileType()
        while True:
            if tokens[tokennumber[0]] == ',':
                printtoken(',')
            elif tokens[tokennumber[0]] == ';':
                printtoken(';')
                break
            else:
                compileVarName()

        f.write('</classVarDec>\n')
        return

    def compileStatements():
        f.write('<statements>\n')

        def compileExpression():

            def compileExpressionList():
                f.write('<expressionList>\n')
                while True:
                    if tokennumber[0] == length:
                        return
                    if tokens[tokennumber[0]] == ')':
                        f.write('</expressionList>\n')

                        return
                    elif tokens[tokennumber[0]] == ',':
                        printtoken(',')
                    else:
                        compileExpression()

            def compileSubroutineCall():

                if tokens[tokennumber[0] + 1] == '.':
                    if tokens[tokennumber[0]] in classes:
                        compileClassName()
                    else:
                        compileVarName()
                    printtoken('.')
                    compileSubroutineName()
                    printtoken('(')
                    compileExpressionList()
                    printtoken(')')
                else:

                    compileSubroutineName()
                    printtoken('(')
                    compileExpressionList()
                    printtoken(')')

                return
            global compileSubroutineCall

            def compileTerm():
                f.write('<term>\n')
                if tokens[tokennumber[0]] in ['-', '~']:
                    printtoken(tokens[tokennumber[0]])
                    compileTerm()
                elif tokens[tokennumber[0]] == '(':
                    printtoken('(')
                    compileExpression()
                    printtoken(')')
                elif tokens[tokennumber[0] + 1] in ['(', '.']:
                    compileSubroutineCall()

                elif tokens[tokennumber[0]] in variables:
                    compileVarName()
                    if tokens[tokennumber[0]] == '[':
                        printtoken('[')
                        compileExpression()
                        printtoken(']')
                elif tokens[tokennumber[0]] == '}':

                    return
                else:

                    printtoken(tokens[tokennumber[0]])

                f.write('</term>\n')

                return

            f.write('<expression>\n')
            ops = ['+', '-', '/', '*', '&', '<', '|', '>', '=']
            while True:
                compileTerm()
                if tokennumber[0] == length:
                    return
                if tokens[tokennumber[0]] in ops:
                    printtoken(tokens[tokennumber[0]])
                else:
                    break
            f.write('</expression>\n')

            return

        def compileLet():
            f.write('<letStatement>\n')
            printtoken('let')
            compileVarName()
            if tokens[tokennumber[0]] == '[':
                printtoken('[')
                compileExpression()
                printtoken(']')
            printtoken('=')
            compileExpression()
            printtoken(';')
            f.write('</letStatement>\n')

            return

        def compileIf():
            f.write('<ifStatement>\n')
            printtoken('if')
            printtoken('(')
            compileExpression()
            printtoken(')')
            printtoken('{')
            compileStatements()
            printtoken('}')
            if tokens[tokennumber[0]] == 'else':
                printtoken('else')
                printtoken('{')
                compileStatements()
                printtoken('}')
            f.write('</ifStatement>\n')

            return

        def compileWhile():
            f.write('<whileStatement>\n')
            printtoken('while')
            printtoken('(')
            compileExpression()
            printtoken(')')
            printtoken('{')
            compileStatements()
            printtoken('}')
            f.write('</whileStatement>\n')

            return

        def compileDo():
            f.write('<doStatement>\n')
            printtoken('do')
            compileSubroutineCall()
            printtoken(';')
            f.write('</doStatement>\n')

            return

        def compileReturn():
            f.write('<returnStatement>\n')
            printtoken('return')
            if tokens[tokennumber[0]] != ';':
                compileExpression()
            printtoken(';')
            f.write('</returnStatement>\n')

            return
        while True:

            if tokens[tokennumber[0]] == 'let':
                compileLet()
            elif tokens[tokennumber[0]] == 'if':
                compileIf()
            elif tokens[tokennumber[0]] == 'while':
                compileWhile()
            elif tokens[tokennumber[0]] == 'do':
                compileDo()
            elif tokens[tokennumber[0]] == 'return':
                compileReturn()
            else:
                break
        f.write('</statements>\n')
        return

    def compileVarDec():
        f.write('<varDec>\n')
        printtoken('var')
        compileType()
        while True:
            if tokens[tokennumber[0]] == ',':
                printtoken(',')
            elif tokens[tokennumber[0]] == ';':
                printtoken(';')
                break
            else:
                compileVarName()

        f.write('</varDec>\n')
        return

    def compileSubroutineBody():
        f.write('<subroutineBody>\n')
        printtoken('{')
        while True:
            if tokens[tokennumber[0]] == 'var':
                compileVarDec()
            else:
                break
        compileStatements()
        printtoken('}')
        f.write('</subroutineBody>\n')
        return

    def compileParameterList():
        f.write('<parameterList>\n')
        while True:
            if tokens[tokennumber[0]] == ')':
                f.write('</parameterList>\n')

                return
            elif tokens[tokennumber[0]] == ',':
                printtoken(',')
            else:
                compileType()
                compileVarName()

    def compileSubroutineDec():
        f.write('<subroutineDec>\n')
        if tokens[tokennumber[0]] in ['constructor', 'function', 'method']:
            printtoken(tokens[tokennumber[0]])
            compileType()
        else:
            printtoken('void')
        compileSubroutineName()
        printtoken('(')
        compileParameterList()
        printtoken(')')
        compileSubroutineBody()
        f.write('</subroutineDec>\n')
        return

    f.write('<class>\n')
    printtoken('class')
    compileClassName()
    printtoken('{')
    while True:
        if tokens[tokennumber[0]] in ['static', 'field']:
            compileClassVarDec()
        elif tokens[tokennumber[0]] in ['constructor', 'function', 'method', 'void']:
            compileSubroutineDec()
        elif tokens[tokennumber[0]] == '}':
            printtoken('}')
            break
    f.write('</class>\n')
    return
