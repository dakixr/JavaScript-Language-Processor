import sys
import tabla_simbolos as ts
import copy

from ply import lex

# Modo especial para guardar los tokens
saving_tokens = False
err = True
err2 = True



# Tipos de tokens
tokens = ['ID', 'PLUS', 'MINUS', 'LPARENT',      'RPARENT',     'LBRACKET',
          'RBRACKET',     'ASSIGN',    'COMMA',     'SEMICOLON',   'LESST', 
          'GREATERT', 'REMAINDER',    'CHAIN',    'CONSTNUM',   'NEGATION']

# Palabras reservadas
reservadas = {

    'alert':'ALERT',
    'boolean':'BOOLEAN',
    'else':'ELSE',
    'function':'FUNCTION', 
    'if':'IF',
    'input':'INPUT',
    'let':'LET',
    'number':'NUMBER',
    'return':'RETURN',
    'string':'STRING',

}

# Se añaden las palabras reservadas como tokens
tokens += list(reservadas.values()) 


############################################################
###### Expresiones regulares para detección de tokens ######
############################################################

t_ignore = ' \t'  # Ignorar los delimitadores

# NO generar token para los comentarios -> // Esto es un comentario
def t_COMMENT(t):
    r'\/\/.*'
    pass

def t_COMMENT_BLOCK(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

# Cadena de caracteres
def t_CHAIN(t):
    r'\'.*\''
    t.value = "\""+ t.value[1:-1] +"\""
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*' 

    global lexer
    global saving_tokens

    if t.value in reservadas:

        if(t.value == "input"):
            ts.zona_Input = True

        if(t.value == "let"):
            ts.zona_Delaracion = True
        
        if(t.value == "function"):
            ts.zona_Delaracion = True
            ts.dentro_de_funcion = True

        if(t.value == "return" and not ts.dentro_de_funcion):
            print("Error sintáctico linea " + str(t.lineno) + ": El return no se encuentra dentro de una función.")

        t.type = reservadas[t.value]
        t.value = ''

    else:

        index = ts.get_index(t.value)

        if saving_tokens:

            if (index is None): # No declarado
                index = ts.add_lex(t.value) # Añadir a TS

            t.value = index
            return t

        if ts.zona_Input:

            ts.zona_Input = False

            if (index is None): # No declarado
                index = ts.add_lex(t.value, var_global = True) # Añadir a TS

            t.value = index
            return t

        if ts.zona_Delaracion:

            index = ts.get_index(t.value, var_local = True)
            
            if (index is None): # No declarado

                index = ts.add_lex(t.value) # Añadir a TS
                ts.zona_Delaracion = False

            else:

                print("Error léxico línea " + str(t.lineno) + ": Identificador '%s' ya ha sido declarado." % t.value)
                pass

        else:

            if (index is None): # No declarado

                # Duplicar el lexer
                lexer_copy = copy.deepcopy(lexer)
                # pedir token
                token = lexer_copy.token()
                # ver si es igual que (
                if (token.type == "LPARENT"):
                    return t
                    
                index = ts.add_lex(t.value, var_global = True)
                t.value = index
                ts.add_tipo_desplazamiento(index,"ent")
                return t

        t.value = index

    return t

def t_REMAINDER(t):
    r'%='
    t.value = ''
    return t

def t_ASSIGN(t):
    r'='
    t.value = ''
    return t

def t_LPARENT(t):
    r'\('
    t.value = ''
    return t

def t_RPARENT(t):
    r'\)'
    t.value = ''
    return t

def t_RBRACKET(t):
    r'\}'

    if ts.dentro_de_funcion:
        ts.brakets_cont -= 1
        if ts.brakets_cont == 0:
            ts.dentro_de_funcion = False

    t.value = ''
    return t

def t_LBRACKET(t):
    r'\{'

    if ts.dentro_de_funcion:
        ts.brakets_cont += 1

    t.value = ''
    return t

def t_COMMA(t):
    r','
    t.value = ''
    return t

def t_SEMICOLON(t):
    r';'
    t.value = ''
    return t

def t_NEGATION(t):
    r'!'
    t.value = ''  
    return t

def t_LESST(t):
    r'<'
    t.value = ''  
    return t

def t_GREATERT(t):
    r'>'
    t.value = ''  
    return t

def t_PLUS(t):
    r'\+'
    t.value = ''  
    return t

def t_MINUS(t):
    r'\-'
    t.value = ''  
    return t

def t_CONSTNUM(t):
    r'\d+'     

    number = int(t.value)

    global err2

    if(number < 65536):
        t.value = number
    else: 
        #sys.exit("ERROR léxico línea: "+ str(t.lineno)+" \nEl número "+ str(number) + " se sale del rango [0-65536].")
        if err2:
            print("Error léxico línea " + str(t.lineno) + ":El número " + str(number) + " se sale del rango [0-65536].")
            err2 = False
        else:
            err2 = True  
              
        t.value = 65535

    return t

# Controlar el número de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
# Controlar los errores
def t_error(t):

    global lexer, err

    if err:
        print("Error léxico línea " + str(t.lineno) + ": Carácter ilegal: '%s'." % t.value[0])
        err = False
    else:
        err = True

    lexer.skip(1)

    pass
    

############################################################

def init():

    global lexer, file_out_tokens

    # Construir el analizador léxico
    lexer = lex.lex()

    import input_file
    # Proporcionar la entrada para lexer
    lexer.input(input_file.source_code)
            
    # Salida de tokens
    file_out_tokens = open("tokens.txt","w")

############################################################

def get_token():

    global lexer, file_out_tokens

    token = lexer.token()

    if not token: 
        file_out_tokens.close()
        lexer = lex.lex() # Reinicializar lex para el analizador sintactico
        return None  # No hay más entradas

    file_out_tokens.write("< " + token.type + ", " + str(token.value) + " >\n")

    return token

def save_tokens():

    global saving_tokens

    saving_tokens = True

    while True:
        token = get_token() # obtener los tokens e introducirlos en un fichero 
        # (tok.type, tok.value, tok.lineno, tok.lexpos) # Atributos de tok

        if not token:
            break
    
    saving_tokens = False
    ts.restore_state()
    