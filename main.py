import ply.lex as lex
import ply.yacc as yacc

# Definir el alfabeto de L
# Tokens (palabras clave)
tokens = (
    'VARIABLE',
    'NEGATION',
    'AND',
    'OR',
    'IMPLIES',
    'EQUIVALENT',
    'LPAREN',
    'RPAREN',
    'CONSTANT',
)

# Expresiones regulares para los tokens
t_VARIABLE = r'[p-z]'
t_NEGATION = r'\~'
t_AND = r'\^'
t_OR = r'o'
t_IMPLIES = r'=>'
t_EQUIVALENT = r'<=>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_CONSTANT = r'[01]'

# Ignorar espacios en blanco
t_ignore = ' \t'

# Función para manejar errores léxicos
def t_error(t):
    print("Caracter ilegal: '%s'" % t.value[0])
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

# Definir las reglas gramaticales de L
def p_formula_variable(p):
    'formula : VARIABLE'
    p[0] = p[1]

def p_formula_negation(p):
    'formula : NEGATION formula'
    p[0] = '~' + p[2]

def p_formula_and(p):
    'formula : formula AND formula'
    p[0] = p[1] + '^' + p[3]

def p_formula_or(p):
    'formula : formula OR formula'
    p[0] = p[1] + 'o' + p[3]

def p_formula_implies(p):
    'formula : formula IMPLIES formula'
    p[0] = p[1] + '=>' + p[3]

def p_formula_equivalent(p):
    'formula : formula EQUIVALENT formula'
    p[0] = p[1] + '<=>' + p[3]

def p_formula_parentheses(p):
    'formula : LPAREN formula RPAREN'
    p[0] = '(' + p[2] + ')'

def p_formula_constant(p):
    'formula : CONSTANT'
    p[0] = p[1]

# Manejo de errores sintácticos
def p_error(p):
    if p is None:
        print("Error: La expresión está incompleta. Se esperaba más contenido.")
    else:
        print(f"Error de sintaxis en la posición {p.lexpos}: Caracter '{p.value[0]}' no esperado.")

# Crear el parser
parser = yacc.yacc()

# Función para imprimir el mensaje en verde
def print_green(text):
    print("\033[92m" + text + "\033[0m")

# Función para imprimir el mensaje en rojo
def print_red(text):
    print("\033[91m" + text + "\033[0m")

if __name__ == '__main__':
    while True:
        try:
            # Leer la entrada desde el usuario
            input_expr = input('Ingrese una expresión del cálculo proposicional (L): ')

            # Analizar léxicamente y sintácticamente la entrada
            result = parser.parse(input_expr, lexer=lexer)

            # Verificar si la expresión es bien formada
            is_well_formed = True
            # Si el resultado está vacío, significa que ocurrió un error sintáctico
            if result is None:
                is_well_formed = False

            # Imprimir el resultado en verde si es bien formada, en rojo si es mal formada
            if is_well_formed:
                print_green("Expresión bien formada: " + result)
            else:
                print_red("Expresión mal formada.")

        except EOFError:
            break
