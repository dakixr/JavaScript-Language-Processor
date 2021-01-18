import sys


print("\n____________________________________________________________________________________")
print('''
 /$$$$$$$  /$$$$$$$  /$$                            /$$$$$$       /$$$$$$  /$$$$$$$ 
| $$__  $$| $$__  $$| $$                           /$$__  $$     /$$__  $$| $$____/ 
| $$  \ $$| $$  \ $$| $$                          | $$  \__/    |__/  \ $$| $$      
| $$$$$$$/| $$  | $$| $$             /$$$$$$      | $$ /$$$$      /$$$$$$/| $$$$$$$ 
| $$____/ | $$  | $$| $$            |______/      | $$|_  $$     /$$____/ |_____  $$
| $$      | $$  | $$| $$                          | $$  \ $$    | $$       /$$  \ $$
| $$      | $$$$$$$/| $$$$$$$$                    |  $$$$$$/ /$$| $$$$$$$$|  $$$$$$/
|__/      |_______/ |________/                     \______/ |__/|________/ \______/ ''')
print("____________________________________________________________________________________\n")

while True:

    import input_file
    input_file.init()
    input_file.get_file()

    print("+ Archivo procesado: '" + str(input_file.file_in.name) + "'\n")

    import analizador_lexico # Inicializar lexico 
    analizador_lexico.init()
    # Guardar tokens en tokens en tokens.txt
    analizador_lexico.save_tokens()


    import analizador_sintactico_semantico # Inicializar analizador sintactico
    analizador_sintactico_semantico.init()
    analizador_sintactico_semantico.save_parse()


    # Guardar tablas de simbolos en symbol_table.txt
    import tabla_simbolos as ts
    ts.save_symbol_table()

    print("------------------------------------------------------------------------------------")
    print("Tokens generados correctamente.")
    print("Parse generado correctamente.")
    print("Tabla de simbolos generada correctamente.")
    print("____________________________________________________________________________________")



