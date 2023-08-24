## University Project: Alternative JavaScript Language Processor

---

### Overview
This project is focused on the design and implementation of a language processor for an alternative version of JavaScript. We delved into lexical, syntactical, and semantic analysis, further integrating a symbol table and an error manager. The entire processor is implemented in Python, leveraging its versatile syntax.

### Features:

#### 1. **Lexical Analyzer**:
   - **Tokens Design**: Manages and recognizes tokens like ID, PLUS, MINUS, ASSIGN, etc.
   - **Grammar Definition**: Outlines the characters and sequences the processor can handle.
   - **Symbol Table**: Implemented using a dynamic, linear organization in Python. For each scope, a separate symbol table is maintained.

#### 2. **Syntactic Analyzer**:
   - **Grammar Options**:
     * Statements: Conditional compound (`if`, `if-else`).
     * Special Operators: Assignment with remainder (`%=`).
     * Analysis Technique: Ascending.
     * Comments: Block comments (`/* */`).
     * Strings: Single quotes (`‘ ’`).
   - **Demonstration**: The ascending syntactic analyzer works efficiently with the LR grammar, building the tree from leaves to root based on shift-reduce operations.
   - **LR Table**: This tool ensures our grammar is conflict-free and suitable for the parser.

#### 3. **Automaton & Test Cases**:
   - The automaton's states and complete test cases (including source code, parser dumps, and syntax trees) are available in the [project's GitHub repository](https://github.com/Dakixr/25-PDL/archive/main.zip).

---

### Execution Workflow:

```python
print("\n____________________________________________________________________________________")
print("Alternative JavaScript Language Processor")
print("____________________________________________________________________________________\n")

while True:
    import input_file, analizador_lexico, analizador_sintactico_semantico, tabla_simbolos as ts
    
    # Fetch and display input file
    input_file.init()
    input_file.get_file()
    print(f"+ Processed file: '{input_file.file_in.name}'\n")
    
    # Lexical Analysis: Token Generation
    analizador_lexico.init()
    analizador_lexico.save_tokens()

    # Syntactical and Semantic Analysis
    analizador_sintactico_semantico.init()
    analizador_sintactico_semantico.save_parse()
    
    # Save symbols to symbol table
    ts.save_symbol_table()

    print("------------------------------------------------------------------------------------")
    print("Tokens, Parse, and Symbol Table generated successfully!")
    print("____________________________________________________________________________________")
```

---

**Note**: This project is both a demonstration of language processing concepts and a testament to the adaptability of Python for diverse programming tasks. Whether you're looking into advanced computer science concepts or practical applications of Python, this project offers a comprehensive insight.
