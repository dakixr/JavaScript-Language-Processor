lista_tabla = [{}]
lista_nombres_tabla = ["PRINCIPAL"]
ultimo_indice = 0
indice_tablas = [0]
zona_Delaracion = False
zona_Input = False
number_etiq_func = 1

lista_tabla[0]["1"] = { "desplazamiento": 0 } # Aqui se guarda el desplazamiento local

def restore_state():
    '''Devolver la tabla de simbolos a su estado incicial.'''

    global lista_tabla, lista_nombres_tabla
    global ultimo_indice, indice_tablas
    global zona_Delaracion, zona_Input
    global number_etiq_func

    lista_tabla = [{}]
    lista_nombres_tabla = ["PRINCIPAL"]
    ultimo_indice = 0
    indice_tablas = [0]
    zona_Delaracion = False
    zona_Input = False
    number_etiq_func = 1

    lista_tabla[0]["1"] = { "desplazamiento": 0 } # Aqui se guarda el desplazamiento local

def get_index(lex, var_local = False):
    '''Devolver el index del identidficador'''

    global lista_tabla
    global indice_tablas

    if var_local:
        if (lex in lista_tabla[indice_tablas[-1]]): # Si el lexema está en la TS
            return lista_tabla[indice_tablas[-1]][lex]["index"]
        else:
            return None

    for i in range(0,len(indice_tablas)):
        if (lex in lista_tabla[indice_tablas[i]]): # Si el lexema está en la TS
            return lista_tabla[indice_tablas[i]][lex]["index"]
    return None

def get_lex(index):
    '''Devolver el lexema del index'''

    global lista_tabla
    global indice_tablas

    for i in range(0,len(indice_tablas)): # Sacar el indice de lista_tabla
        for lex in lista_tabla[indice_tablas[i]]: # Recorrer lista_tabla
            if (lex !="1" and lista_tabla[indice_tablas[i]][lex]["index"] == index):
                return lex
    return None

def get_return_type(index):
    '''Devolver el tipo de retorno de la función'''

    lex = get_lex(index)

    global lista_tabla
    global indice_tablas

    for i in range(len(indice_tablas)):
        if (lex in lista_tabla[indice_tablas[i]]): # Si el lexema está en la TS
            return lista_tabla[indice_tablas[i]][lex]["TipoRetorno"]
    return None

def get_tipo(index):
    '''Devolver el tipo del identidficador'''

    lex = get_lex(index)

    global lista_tabla
    global indice_tablas

    for i in range(len(indice_tablas)):
        if (lex in lista_tabla[indice_tablas[i]]): # Si el lexema está en la TS
                return lista_tabla[indice_tablas[i]][lex]["Tipo"]
    return None

def get_curr_function():
    '''Devolver el id de la función ejecutandose.'''
    global lista_nombres_tabla
    return get_index(lista_nombres_tabla[-1])

def get_list_num_params(index):
    '''Devuelve una lista con los parametros de la función y el número de param.'''

    global lista_tabla
    global indice_tablas

    lex = get_lex(index)
    n_param = lista_tabla[0][lex]["numParam"]
    lista_param = []

    if type(n_param) is not int:
        return None, None

    for i in range(n_param):
        lista_param.append(lista_tabla[0][lex]["TipoParam" + str(i+1)])
    
    return lista_param, n_param

def add_lex(lex, var_global = False):
    '''Devolver el index del identidficador y si no existe, crear una 
       entrada en la lista_tabla de símbolos.'''

    global lista_tabla
    global ultimo_indice
    global indice_tablas

    indice_tabla = indice_tablas[-1] if not var_global else 0

    if (lex not in lista_tabla[indice_tabla]): # Si el lexema aun no está en la TS
        lista_tabla[indice_tabla][lex] = {
            "index": ultimo_indice,
            "lexema": lex,
            "Tipo": "",
            "Despl": "",
            "numParam": "",
            "TipoRetorno": "",
            "EtiqFuncion": "",
            "Param": ""
        }
        ultimo_indice += 1 # Se incrementa el índice
    return lista_tabla[indice_tabla][lex]["index"]

def crear_tabla(name_funcion):
    '''Crear una nueva tabla de simbolos'''

    global lista_nombres_tabla
    global lista_tabla
    global indice_tablas
    global number_etiq_func

    lista_tabla.append({})
    lista_tabla[0][name_funcion]["EtiqFuncion"] = name_funcion + str(number_etiq_func)
    number_etiq_func += 1
    lista_tabla[-1]["1"] = { "desplazamiento": 0 } # Aqui se guarda el desplazamiento local
    lista_nombres_tabla.append(name_funcion)
    indice_tablas.append(len(lista_tabla)-1)

def borrar_current_tabla():
    '''Eliminar del stack la tabla correspondiente'''

    global indice_tablas
    indice_tablas.pop()
    
def add_tipo_desplazamiento(index, tipo):
    '''Añadir un tipo y desplazamiento a la tabla de simbolos de un determinado ID.'''

    lex = get_lex(index)

    global lista_tabla
    global indice_tablas

    if tipo == "cadena":
        ancho = 16
    if tipo == "ent":
        ancho = 1
    if tipo == "logico":
        ancho = 1
    
    desplazamiento = lista_tabla[indice_tablas[-1]]["1"]["desplazamiento"]

    if (lex in lista_tabla[indice_tablas[-1]]): # Si el lexema está en la TS
        lista_tabla[indice_tablas[-1]][lex]["Tipo"] = tipo
        lista_tabla[indice_tablas[-1]][lex]["Despl"] = desplazamiento
    else:
        lista_tabla[0][lex]["Tipo"] = tipo
        lista_tabla[0][lex]["Despl"] = desplazamiento
    
    lista_tabla[indice_tablas[-1]]["1"]["desplazamiento"] += ancho

def add_tipo_num_parametros(index, tipo_param_str):
    '''Añade los tipos de parametros a la tabla se simbolos'''

    global lista_tabla
    global indice_tablas
        
    lex = get_lex(index)

    tipo_param_list = tipo_param_str.split(",")

    if len(tipo_param_list) == 1 and tipo_param_list[0] == "void":
        lista_tabla[indice_tablas[0]][lex]["numParam"] = 0
        return

    lista_tabla[indice_tablas[0]][lex]["numParam"] = len(tipo_param_list)
        
    for i in range(len(tipo_param_list)):
        lista_tabla[indice_tablas[0]][lex]["TipoParam"+str(i+1)] = tipo_param_list[i]


def add_return_type_and_type(index, tipo_retorno):
    '''Añadir un tipo de retorno a la tabla de simbolos del id seleccionado y tipo función.'''

    lex = get_lex(index)

    global lista_tabla
    global indice_tablas

    if (lex in lista_tabla[indice_tablas[-1]]): # Si el lexema está en la TS
        lista_tabla[indice_tablas[-1]][lex]["TipoRetorno"] = tipo_retorno
        lista_tabla[indice_tablas[-1]][lex]["Tipo"] = "funcion"


# Crear el fichero resultado de la lista_tabla de símbolos
def save_symbol_table():
    '''Guardar a un archivo externo "symbol_table.txt" la tabla de simbolos.'''

    file_out = open("tabla de simbolos.txt","w")

    for i in range(len(lista_tabla)):

        file_out.write("TABLA " + lista_nombres_tabla[i] + " # "+ str(i+1) +":\n")

        for entry in lista_tabla[i]:

            if (entry == "1"):
                continue

            file_out.write("\n")
            file_out.write("* LEXEMA : '" + lista_tabla[i][entry]["lexema"] + "'\n")
            file_out.write("ATRIBUTOS: \n")
            
            for attr in lista_tabla[i][entry]: # Para todos los atributos de ese lexema en la TS
                # Se escriben todos los atributos que no estén vacíos, menos index y lexema
                if (attr != "index" and attr != "lexema" and lista_tabla[i][entry][attr] != ""): 
                    try:
                        attr_val = int(lista_tabla[i][entry][attr])
                        pass
                    except:
                        attr_val = lista_tabla[i][entry][attr]

                    attr_val_final = str(attr_val) if type(attr_val) == int else ("'" + str(attr_val) + "'")
                    file_out.write("+ " + attr + " : " + attr_val_final + "\n")
            
            file_out.write("\n-------------------------------\n")
        file_out.write("\n")
    file_out.close()


