from JackTokenizer import *
from SymbolTable import *
variables = []
classes = []
types = []
subroutines = []


def compileClass(tokens, tokennumber, syntax, length):

    def printtoken(token):
        t = tokenType(token)
        syntax.append([t, writetokens[t](token)])
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
        syntax.append('<classVarDec>')
        kind = tokens[tokennumber[0]]
        printtoken(kind)
        compileType()
        while True:
            if tokens[tokennumber[0]] == ',':
                printtoken(',')
            elif tokens[tokennumber[0]] == ';':
                printtoken(';')
                break
            else:
                compileVarName()

        syntax.append('</classVarDec>')
        return

    def compileStatements():
        syntax.append('<statements>')

        def compileExpression():

            def compileExpressionList():
                syntax.append('<expressionList>')
                while True:
                    if tokennumber[0] == length:
                        return
                    if tokens[tokennumber[0]] == ')':
                        syntax.append('</expressionList>')

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
                syntax.append('<term>')
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

                syntax.append('</term>')

                return

            syntax.append('<expression>')
            ops = ['+', '-', '/', '*', '&', '<', '|', '>', '=']
            while True:
                compileTerm()
                if tokennumber[0] == length:
                    return
                if tokens[tokennumber[0]] in ops:
                    printtoken(tokens[tokennumber[0]])
                else:
                    break
            syntax.append('</expression>')

            return

        def compileLet():
            syntax.append('<letStatement>')
            printtoken('let')
            compileVarName()
            if tokens[tokennumber[0]] == '[':
                printtoken('[')
                compileExpression()
                printtoken(']')
            printtoken('=')
            compileExpression()
            printtoken(';')
            syntax.append('</letStatement>')

            return

        def compileIf():
            syntax.append('<ifStatement>')
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
            syntax.append('</ifStatement>')

            return

        def compileWhile():
            syntax.append('<whileStatement>')
            printtoken('while')
            printtoken('(')
            compileExpression()
            printtoken(')')
            printtoken('{')
            compileStatements()
            printtoken('}')
            syntax.append('</whileStatement>')

            return

        def compileDo():
            syntax.append('<doStatement>')
            printtoken('do')
            compileSubroutineCall()
            printtoken(';')
            syntax.append('</doStatement>')

            return

        def compileReturn():
            syntax.append('<returnStatement>')
            printtoken('return')
            if tokens[tokennumber[0]] != ';':
                compileExpression()
            printtoken(';')
            syntax.append('</returnStatement>')

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
        syntax.append('</statements>')
        return

    def compileVarDec():
        syntax.append('<varDec>')
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

        syntax.append('</varDec>')
        return

    def compileSubroutineBody():
        syntax.append('<subroutineBody>')
        printtoken('{')
        while True:
            if tokens[tokennumber[0]] == 'var':
                compileVarDec()
            else:
                break
        compileStatements()
        printtoken('}')
        syntax.append('</subroutineBody>')
        return

    def compileParameterList():
        syntax.append('<parameterList>')
        while True:
            if tokens[tokennumber[0]] == ')':
                syntax.append('</parameterList>')

                return
            elif tokens[tokennumber[0]] == ',':
                printtoken(',')
            else:
                compileType()
                compileVarName()

    def compileSubroutineDec():
        syntax.append('<subroutineDec>')
        
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
        syntax.append('</subroutineDec>')
        return

    syntax.append('<class>')
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
    syntax.append('</class>')
    return
