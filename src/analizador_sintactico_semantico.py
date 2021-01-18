import sys
import tabla_simbolos as ts

from ply import yacc
from analizador_lexico import tokens


precedence = (

	('right','ALERT','INPUT','IF','ELSE','RETURN'),
	('right','FUNCTION'),
	('right','BOOLEAN','STRING','NUMBER'),
	('right','LET'),
	('right','ASSIGN','REMAINDER'),
	('left','NEGATION'),
	('left','GREATERT','LESST'),
	('left','PLUS','MINUS'),
	('right','ID','CONSTNUM','CHAIN'),
    ('left','LBRACKET','RBRACKET'),
	('left','LPARENT','RPARENT')

)

# Dictionary of names
# names = { }

class Attr():
    """Clase que implemeta el el objeto atributo"""
    def __init__(self, tipo = None, id = None):
        self.tipo = tipo
        self.id = id

def p_Axioma_prima(p):
    '''Axioma_ : Axioma'''
    parse.append(1)
    p[0] = Attr(tipo = str(p[1].tipo))

    for err in errores:
        print("Error semántico " + err)

def p_Axioma_sentencia(p):
    '''Axioma : Sentencia Axioma'''
    parse.append(2)
    if (p[2].tipo == "void"):
        p[0] = Attr(tipo = str(p[1].tipo))
    else:
        p[0] = Attr(tipo = (str(p[1].tipo) + "," + str(p[2].tipo)))

def p_Axioma_funcion(p):
    '''Axioma : Funcion Axioma'''
    parse.append(3)
    if (p[2].tipo == "void"):
        p[0] = Attr(tipo = str(p[1].tipo))
    else:
        p[0] = Attr(tipo = (str(p[1].tipo) + "," + str(p[2].tipo)))

def p_Axioma_empty(p):
    '''Axioma : empty'''
    parse.append(4)
    p[0] = Attr(tipo = "void")

def p_Sentencia_S(p):
    '''Sentencia : S'''
    parse.append(5)
    p[0] = Attr(tipo = str(p[1].tipo))

def p_Sentencia_IF(p):
    '''Sentencia : IF_'''
    parse.append(6)
    p[0] = Attr(tipo = str(p[1].tipo))

def p_Sentencia_tipo_id(p):
    '''Sentencia : LET Tipo ID SEMICOLON'''
    parse.append(7)
    ts.add_tipo_desplazamiento(p[3],p[2].tipo)
    p[0] = Attr(tipo = "tipo_ok")
    
def p_IF_IF1_IF2(p):
    '''IF_ : IF1 IF2'''
    parse.append(8)
    p[0] = Attr(tipo = "tipo_ok") if p[1].tipo == "tipo_ok" and p[2].tipo != "tipo_error" else Attr(tipo = "tipo_error")

def p_IF1(p):
    '''IF1 : IF LPARENT E RPARENT Senten'''
    parse.append(9)
    p[0] = Attr(tipo = "tipo_ok") if p[3].tipo == "logico" and p[5].tipo == "tipo_ok" else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(1)) + ": La comprobación en el if debe ser un boolean o una expresión lógica.")

def p_IF2(p):
    '''IF2 : ELSE Senten'''
    parse.append(10)
    p[0] = Attr(tipo = str(p[2].tipo))

def p_IF2_empty(p):
    '''IF2 : empty'''
    parse.append(11)
    p[0] = Attr(tipo = "void")

def p_Senten(p):
    '''Senten : Sentencia'''
    parse.append(12)
    p[0] = Attr(tipo = str(p[1].tipo))

def p_Senten_Lista(p):
    '''Senten : LBRACKET Lista_Sentencias RBRACKET'''
    parse.append(13)
    p[0] = Attr(tipo = str(p[2].tipo))

def p_S_Asignacion(p):
    '''S : ID ASSIGN E SEMICOLON'''
    parse.append(14)

    if (ts.get_tipo(p[1]) == ""):
        ts.add_tipo_desplazamiento(p[1],"ent")

    p[0] = Attr(tipo = "tipo_ok") if ts.get_tipo(p[1]) == p[3].tipo else Attr(tipo = "tipo_error")
   
    if p[0].tipo == "tipo_error":     
        errores.append("linea " + str(p.lineno(1)) + ": El tipo de la asignación no coincide con el tipo de la variable: " + str(ts.get_tipo(p[1])) + " != " + str(p[3].tipo))


def p_S_Asignacion_Remainder(p):
    '''S : ID REMAINDER E SEMICOLON'''
    parse.append(15)
    p[0] = Attr(tipo = "tipo_ok") if ts.get_tipo(p[1]) == "ent" and p[3].tipo == "ent" else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(1)) + ": La operación módulo solo se puede hacer con enteros.")

def p_S_Funcion(p):
    '''S : ID LPARENT Parametros RPARENT SEMICOLON'''
    parse.append(16)

    param_list_caller = p[3].tipo.split(",") # Como tratas de llamar
    param_list_table, n_param = ts.get_list_num_params(p[1])

    if (param_list_caller[0] == "void"):
        param_list_caller.pop()
    
    ret = "tipo_error"

    if (n_param == len(param_list_caller) and ts.get_tipo(p[1]) == "funcion"):
        ret = "tipo_ok"
        for i in range(len(param_list_caller)):
            if param_list_caller[i] != param_list_table[i]:
                ret = "tipo_error"
                break

    p[0] = Attr(tipo = ret)

    if p[0].tipo == "tipo_error":
        if ts.get_tipo(p[1]) == "funcion":
            errores.append("linea " + str(p.lineno(1)) + ": Se ha llamado a la función '" + str(ts.get_lex(p[1])) + "' con argumentos incorrectos. Se esperaba: " + str(param_list_table) + ". Pero se ha recibido: "+ str(param_list_caller)+".")
        else:
            errores.append("linea " + str(p.lineno(1)) + ": La variable '" + str(ts.get_lex(p[1])) +"' no ha sido declarada como función.")

def p_S_Alert(p):
    '''S : ALERT LPARENT E RPARENT SEMICOLON'''
    parse.append(17)
    p[0] = Attr(tipo = "tipo_ok") if p[3].tipo == "ent" or p[3].tipo == "cadena" else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(1)) + ": La función 'alert' necesita un entero o cadena como argumento.")

def p_S_Input(p):
    '''S : INPUT LPARENT ID RPARENT SEMICOLON'''
    parse.append(18)

    if (ts.get_tipo(p[3]) == ""):
        ts.add_tipo_desplazamiento(p[3],"ent")

    p[0] = Attr(tipo = "tipo_ok") if ts.get_tipo(p[3]) == "ent" or ts.get_tipo(p[3]) == "cadena" else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(1)) + ": La función 'input' necesita un entero o cadena como argumento.")

def p_S_Return(p):
    '''S : RETURN X SEMICOLON'''
    parse.append(19)
    p[0] = Attr(tipo = "tipo_ok") if p[2].tipo == ts.get_return_type(ts.get_curr_function()) else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(1)) + ": El tipo de retorno '" + str(p[2].tipo) + "' no coincide con el esperado '" + str(ts.get_return_type(ts.get_curr_function())) + "'.")

def p_Parametros_E_K2(p):
    '''Parametros : E K2'''
    parse.append(20)
    if (p[2].tipo == "void"):
        p[0] = Attr(tipo = str(p[1].tipo))
    else:
        p[0] = Attr(tipo = (str(p[1].tipo) + "," + str(p[2].tipo)))

def p_Parametros_lambda(p):
    '''Parametros : empty'''
    parse.append(21)
    p[0] = Attr(tipo = "void")

def p_K2_comma(p):
    '''K2 : COMMA E K2'''
    parse.append(22)
    if (p[3].tipo == "void"):
        p[0] = Attr(tipo = str(p[2].tipo))
    else:
        p[0] = Attr(tipo = (str(p[2].tipo) + "," + str(p[3].tipo)))

def p_K2_lambda(p):
    '''K2 : empty'''
    parse.append(23)
    p[0] = Attr(tipo = "void")

def p_X(p):
    '''X : E'''
    parse.append(24)
    p[0] = Attr(tipo = str(p[1].tipo))

def p_X_lambda(p):
    '''X : empty'''
    parse.append(25)
    p[0] = Attr(tipo = "void")

def p_Funcion(p):
    '''Funcion : F1 F2 F3'''
    parse.append(26)
    p[0] = Attr(tipo = str(p[3].tipo))
    ts.add_tipo_num_parametros(p[1].id,p[2].tipo)
    ts.borrar_current_tabla()
    #ts.zona_Delaracion = False

def p_F1(p):
    '''F1 : FUNCTION Tipo_B ID'''
    parse.append(27)
    p[0] = Attr(tipo = str(p[2].tipo), id = p[3])
    ts.add_return_type_and_type(p[3], p[2].tipo)
    ts.crear_tabla(ts.get_lex(p[3]))

def p_F2(p):
    '''F2 : LPARENT Cabecera RPARENT'''
    parse.append(28)
    p[0] = Attr(tipo = p[2].tipo)

def p_F3(p):
    '''F3 : LBRACKET Lista_Sentencias RBRACKET'''
    parse.append(29)
    p[0] = Attr(tipo = p[2].tipo)

def p_Tipo_boolean(p):
    '''Tipo : BOOLEAN'''
    parse.append(30)
    p[0] = Attr(tipo = "logico")
    ts.zona_Delaracion = True

def p_Tipo_number(p):
    '''Tipo : NUMBER'''
    parse.append(31) 
    p[0] = Attr(tipo = "ent")
    ts.zona_Delaracion = True

def p_Tipo_string(p):
    '''Tipo : STRING'''
    parse.append(32)
    p[0] = Attr(tipo = "cadena")
    ts.zona_Delaracion = True

def p_Tipo_B_Tipo(p):
    '''Tipo_B : Tipo'''
    parse.append(33)
    p[0] = Attr(tipo = p[1].tipo)

def p_Tipo_B_lambda(p):
    '''Tipo_B : empty'''
    parse.append(34)
    p[0] = Attr(tipo = "void")

def p_Cabecera_Tipo(p):
    '''Cabecera : Tipo ID K'''
    parse.append(35)
    if (p[3].tipo == "void"):
        p[0] = Attr(tipo = p[1].tipo, id = p[2])
        ts.add_tipo_desplazamiento(p[2], p[1].tipo)
    else:
        p[0] = Attr(tipo = (str(p[1].tipo) + "," + str(p[3].tipo)), id = (str(p[2]) + "," + str(p[3].id)))

        list_tipos = p[0].tipo.split(",")
            
        list_id = p[0].id.split(",")

        for i in range(len(list_id)):
            ts.add_tipo_desplazamiento(int(list_id[i]), list_tipos[i])

def p_Cabecera(p):
    '''Cabecera : empty'''
    parse.append(36)
    p[0] = Attr(tipo = "void")

def p_K(p):
    '''K : COMMA Tipo ID K'''
    parse.append(37)
    if (p[4].tipo == "void"):
        p[0] = Attr(tipo = str(p[2].tipo), id = p[3])
    else:
        p[0] = Attr(tipo = (p[2].tipo + "," + p[4].tipo), id = (str(p[3]) + "," + str(p[4].id)))

def p_K1(p):
    '''K : empty'''
    parse.append(38)
    p[0] = Attr(tipo = "void")

def p_Lista_Sentencias(p):
    '''Lista_Sentencias : Sentencia Lista_Sentencias'''
    parse.append(39)
    p[0] = Attr(tipo = "tipo_ok") if p[1].tipo == "tipo_ok" and p[2].tipo != "tipo_error" else Attr(tipo = "tipo_error")

def p_Lista_Sentencias1(p):
    '''Lista_Sentencias : empty'''
    parse.append(40)
    p[0] = Attr(tipo = "void")

def p_E(p):
    '''E : NEGATION V'''
    parse.append(41)
    p[0] = Attr(tipo = "logico") if p[2].tipo == "logico" else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(1)) + ": Solo se pueden negar booleanos o expresiones booleanas.")

def p_E1(p):
    '''E : R'''
    parse.append(42)
    p[0] = Attr(tipo = str(p[1].tipo))

def p_R(p):
    '''R : R GREATERT U'''
    parse.append(43)
    p[0] = Attr(tipo = "logico") if p[1].tipo == "ent" and p[3].tipo == "ent" else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(2)) + ": Solo se pueden comparar dos enteros.")


def p_R1(p):
    '''R : R LESST U'''
    parse.append(44)
    p[0] = Attr(tipo = "logico") if p[1].tipo == "ent" and p[3].tipo == "ent" else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(2)) + ": Solo se pueden comparar dos enteros.")

def p_R2(p):
    '''R : U'''
    parse.append(45)
    p[0] = Attr(tipo = str(p[1].tipo))

def p_U(p):
    '''U : U PLUS V'''
    parse.append(46)
    p[0] = Attr(tipo = "ent") if p[1].tipo == p[3].tipo else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(2)) + ": Solo se pueden sumar enteros.")

def p_U1(p):
    '''U : U MINUS V'''
    parse.append(47)
    p[0] = Attr(tipo = "ent") if p[1].tipo == p[3].tipo else Attr(tipo = "tipo_error")

    if p[0].tipo == "tipo_error":
        errores.append("linea " + str(p.lineno(2)) + ": Solo se pueden restar enteros.")

def p_U_V(p):
    '''U : V'''
    parse.append(48)
    p[0] = Attr(tipo = p[1].tipo)

def p_V(p):
    '''V : ID'''
    parse.append(49)
    p[0] = Attr(tipo = str(ts.get_tipo(p[1])))

def p_V1(p):
    '''V : LPARENT E RPARENT'''
    parse.append(50)
    p[0] = Attr(tipo = str(p[2].tipo))

def p_V2(p):
    '''V : ID LPARENT Parametros RPARENT'''
    parse.append(51)
    p[0] = Attr(tipo = str(ts.get_return_type(p[1])))

    if ts.get_tipo(p[1]) != "funcion":
        
        try:
            func_name = int(p[1])
            func_name = ts.get_lex(p[1])
            pass
        except:
            func_name = p[1]
            pass
        
        errores.append("linea " + str(p.lineno(1)) + ": La variable '" + str(func_name) +"' no ha sido declarada como función.")
    

def p_V3(p):
    '''V : CONSTNUM'''
    parse.append(52)
    p[0] = Attr(tipo = "ent")

def p_V4(p):
    '''V : CHAIN'''
    parse.append(53)
    p[0] = Attr(tipo = "cadena")

# lambda
def p_empty(p):
    '''empty :'''
    pass

# Error rule for syntax errors
def p_error(p):
    try:
        print("Error de sintaxis linea " + str(p.lineno) +": < " + p.type + ", " + str(p.value) + " >")
        pass
    
    except:
        print("Error de sintaxis... Revisa los ;")
        pass

############################################################
def init():
    global parse, errores, parser
    # Secuencia del parse
    parse = []

    # Errores semánticos
    errores = []

    # Crear parser
    yacc.yaccdebug = False # No crear archivo de depuración
    parser = yacc.yacc()

    import input_file
    parser.parse(input_file.source_code)

############################################################

def save_parse():
    '''Guardar pasos del parse en el archivo "parse.txt"'''
    file_out_parse = open("parse.txt","w")
    file_out_parse.write("A")

    for paso in parse:
        file_out_parse.write(" " + str(paso))
    
    file_out_parse.close()



