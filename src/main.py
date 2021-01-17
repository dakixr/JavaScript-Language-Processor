import sys

# Tratar el error si no se pasan los argumentos correctos
if (len(sys.argv) != 2):
    sys.exit("Error. Incorrect usage: \"python3 main.py source_code.js\"")

import analizador_lexico # Inicializar lexico 
# Guardar tokens en tokens en tokens.txt
# analizador_lexico.save_tokens()

import analizador_sintactico # Inicializar analizador sintactico
analizador_sintactico.save_parse()

# Guardar tablas de simbolos en symbol_table.txt
import tabla_simbolos as ts
ts.save_symbol_table()