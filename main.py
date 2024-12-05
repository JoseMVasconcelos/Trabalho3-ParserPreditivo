# José Victor Vasconcelos (22100906)
# Lexer flex utilizado no trabalho parte 1, adaptado para novos tokens criados no trabalho parte 2
import sys
import os
from flex_lexer import LexerFlex

def main():

    # Tabela de transição baseada no trabalho parte 2
    transition_table = {
        "S": {"$": "MAIN $", "DEF": "MAIN $", "LBRACE": "MAIN $", "INT": "MAIN $", "ID": "MAIN $", "SEMICOLON": "MAIN $", "PRINT": "MAIN $", "RETURN": "MAIN $", "IF": "MAIN $"},
        "MAIN": {"$": "", "DEF": "FLIST", "LBRACE": "STMT", "INT": "STMT", "ID": "STMT", "SEMICOLON": "STMT", "PRINT": "STMT", "RETURN": "STMT", "IF": "STMT"},
        "FLIST": {"DEF": "FDEF FLIST2"},
        "FLIST2": {"$": "", "DEF": "FLIST"},
        "FDEF": { "DEF": "DEF ID_LPAREN PARLIST RPAREN LBRACE STMTLIST RBRACE"},
        "PARLIST": {"RPAREN": "", "INT": "INT ID PARLIST2"},
        "PARLIST2": {"RPAREN": "", "COMMA": "COMMA PARLIST"},
        "VARLIST": {"ID": "ID VARLIST2"},
        "VARLIST2": {"COMMA": "COMMA VARLIST", "SEMICOLON": ""},
        "STMT": {"LBRACE": "LBRACE STMTLIST RBRACE", "INT": "INT VARLIST SEMICOLON", "ID": "ATRIBST SEMICOLON", "SEMICOLON": "SEMICOLON", "PRINT": "PRINTST SEMICOLON", "RETURN": "RETURNST SEMICOLON", "IF": "IFSTMT"},
        "ATRIBST": {"ID": "ID ASSIGN ATRIBST2"},
        "ATRIBST2": {"ID_LPAREN": "FCALL", "ID": "EXPR", "LPAREN": "EXPR", "NUMBER": "EXPR"},
        "FCALL": {"ID_LPAREN": "ID_LPAREN PARLISTCALL RPAREN"},
        "PARLISTCALL": {"ID": "ID PARLISTCALL2", "RPAREN": ""},
        "PARLISTCALL2": {"RPAREN": "", "COMMA": "COMMA PARLISTCALL"},
        "PRINTST": {"PRINT": "PRINT EXPR"},
        "RETURNST": {"RETURN": "RETURN RETURNST2"},
        "RETURNST2": {"ID": "ID", "SEMICOLON": ""},
        "IFSTMT": {"IF": "IF LPAREN EXPR RPAREN STMT IFSTMT2"},
        "IFSTMT2": {"ELSE": "ELSE STMT ENDIF", "ENDIF": "ENDIF"},
        "STMTLIST": {"ID": "STMT STMTLIST2", "LBRACE": "STMT STMTLIST2", "INT": "STMT STMTLIST2", "SEMICOLON": "STMT STMTLIST2", "PRINT": "STMT STMTLIST2", "RETURN": "STMT STMTLIST2", "IF": "STMT STMTLIST2"},
        "STMTLIST2": {"ID": "STMTLIST", "LBRACE": "STMTLIST", "RBRACE": "", "INT": "STMTLIST", "SEMICOLON": "STMTLIST", "PRINT": "STMTLIST", "RETURN": "STMTLIST", "IF": "STMTLIST"},
        "EXPR": {"ID": "NUMEXPR EXPR2", "LPAREN": "NUMEXPR EXPR2", "NUMBER": "NUMEXPR EXPR2"},
        "EXPR2": {"RPAREN": "", "SEMICOLON": "", "LESSER_THAN": "LESSER_THAN NUMEXPR", "LESSER_EQUAL": "LESSER_EQUAL NUMEXPR", "GREATER_THAN": "GREATER_THAN NUMEXPR", "GREATER_EQUAL": "GREATER_EQUAL NUMEXPR", "EQUAL": "EQUAL NUMEXPR", "DIFFERENT": "DIFFERENT NUMEXPR"},
        "NUMEXPR": {"ID": "TERM NUMEXPR2", "LPAREN": "TERM NUMEXPR2", "NUMBER": "TERM NUMEXPR2"},
        "NUMEXPR2": {"RPAREN": "", "SEMICOLON": "", "LESSER_THAN": "", "LESSER_EQUAL": "", "GREATER_THAN": "", "GREATER_EQUAL": "", "EQUAL": "", "DIFFERENT": "", "PLUS": "PLUS TERM NUMEXPR2", "MINUS": "MINUS TERM NUMEXPR2"},
        "TERM": {"ID": "FACTOR TERM2", "LPAREN": "FACTOR TERM2", "NUMBER": "FACTOR TERM2"},
        "TERM2": {"RPAREN": "", "SEMICOLON": "", "LESSER_THAN": "", "LESSER_EQUAL": "", "GREATER_THAN": "", "GREATER_EQUAL": "", "EQUAL": "", "DIFFERENT": "", "PLUS": "", "MINUS": "", "TIMES": "TIMES FACTOR TERM2", "DIVIDE": "DIVIDE FACTOR TERM2"},
        "FACTOR": {"ID": "ID", "LPAREN": "LPAREN NUMEXPR RPAREN", "NUMBER": "NUMBER"}
    }

    # Lista de terminais para comparação no algoritmo
    terminal_list = ('ID',
            'NUMBER',
            'LESSER_THAN',
            'GREATER_THAN',
            'LESSER_EQUAL',
            'GREATER_EQUAL',
            'DIFFERENT',
            'EQUAL',
            'INT',
            'IF',
            'ELSE',
            'DEF',
            'PRINT',
            'RETURN',
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'ASSIGN',
            'LPAREN',
            'RPAREN',
            'LBRACE',
            'RBRACE',
            'COMMA',
            'SEMICOLON',
            'ID_LPAREN',
            'ENDIF')

    # Variáveis e objetos usados para o algoritmo
    def predictive_parser(file):
        lexer = LexerFlex()
        tokens = lexer.run_lexer(file)
        token_pointer = 0
        symbol_stack = ["MAIN", "$"]
        current_symbol = symbol_stack[0]
        current_token = None

        # Variáveis para demonstração no fim
        match_count = 0
        match_sequence = []
        transitions = []

        # Algoritimo visto em sala, adaptado para python
        while (current_symbol != "$"):
            try:
                current_token = tokens["token_types"][token_pointer]
                if (current_symbol == current_token):
                    symbol_stack.pop(0)
                    token_pointer += 1
                    match_count += 1
                    print(f'MATCH! Symbol: "{current_symbol}" Token: "{current_token}"')
                    match_sequence.append(current_symbol)

                elif (current_symbol in terminal_list):
                    print(f'ERROR! Symbol: "{current_symbol}" IS TERMINAL SYMBOL BUT DOES NOT MATCH THE "{current_token}" INPUT!')
                    print("--------------------------------------------------------")
                    return False
                elif (transition_table[current_symbol][current_token] or transition_table[current_symbol][current_token] == ""):
                    symbol_stack.pop(0)
                    if (not transition_table[current_symbol][current_token] == ""):
                        print(f'TRANSITION! "{current_symbol}" -> "{transition_table[current_symbol][current_token]}"')
                        transitions.append(current_symbol + " -> " + transition_table[current_symbol][current_token])
                        to_stack = transition_table[current_symbol][current_token].split(" ")
                        to_stack.reverse()
                        for x in to_stack:
                            symbol_stack.insert(0, x)
                    else:
                        print(f'TRANSITION! "{current_symbol}" -> EPSILON!')
                        pass
                current_symbol = symbol_stack[0]
            except KeyError:
                print(f'ERROR! Symbol: "{current_symbol}" TO: "{current_token}" NO TRANSITION FOUND!')
                print("--------------------------------------------------------")
                return False
            
        print()
        print()
        print()
        print(f'TOTAL MATCH OF {match_count} TOKENS!')
        print(match_sequence)
        print("--------------------------------------------------------")
        print("ORDER OF TRANSITIONS:")
        for x in transitions:
            print(x)
        print("--------------------------------------------------------")
        return True
                

    # Args de entrada, nome do arquivo a ser lido
    args = sys.argv[1:]
    if (len(args) <= 0):
        print("NEED A FILEPATH AS ARGS!")
        exit()
    
    file = args[0]
    if os.path.isfile(file):
        if file.endswith(".txt"):
            matched_file = predictive_parser(file)
        if (matched_file):
            print(f'FILE: "{file}" MATCHED STATEMENT!')
        else:
            print(f'ERROR! FILE: "{file}" DID NOT MATCH STATEMENT!')
    else:
        print(f'ERROR! FILE: "{file}" NOT FOUND!')
main()

