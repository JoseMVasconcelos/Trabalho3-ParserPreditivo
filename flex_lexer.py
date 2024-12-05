# José Victor Machado de Vasconcelos (22100906)
import ply.lex as lex

class LexerFlex:
    def __init__(self):
        #Determinação dos Tokens
        tokens = (
            'ID',
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
            'ENDIF'
        )

        #Funções que representam cada token
        t_LESSER_THAN = r'<'
        t_GREATER_THAN = r'>'
        t_LESSER_EQUAL = r'<='
        t_GREATER_EQUAL = r'>='
        t_DIFFERENT = r'<>'
        t_EQUAL = r'=='
        t_PLUS = r'\+'
        t_MINUS = r'-'
        t_TIMES = r'\*'
        t_DIVIDE = r'/'
        t_ASSIGN = r':='
        t_LPAREN = r'\('
        t_RPAREN = r'\)'
        t_LBRACE = r'\{'
        t_RBRACE = r'\}'
        t_COMMA = r','
        t_SEMICOLON = r';'

        #Funções mais complexas

        def t_ID_LPAREN(t):
            r'[a-zA-Z_][a-zA-Z0-9_]*\('
            return t
        
        def t_INT(t):
            r'int'
            return t

        def t_IF(t):
            r'if'
            return t

        def t_ELSE(t):
            r'else'
            return t

        def t_DEF(t):
            r'def'
            return t

        def t_PRINT(t):
            r'print'
            return t

        def t_RETURN(t):
            r'return'
            return t

        def t_ENDIF(t):
            r'endif'
            return t
        
        def t_ID(t):
            r'[a-zA-Z_][a-zA-Z0-9_]*'
            return t

        def t_NUMBER(t):
            r'\d+'
            t.value = int(t.value)
            return t
        


        #Declaração de caracteres ignorados
        t_ignore = ' \t\n'

        #Função para detecção de caracter inválido
        def t_error(t):
            print("Invalid character:", t.value)
            t.lexer.skip(1)

        self.__lexer = lex.lex()

    #Função para execução do Lexer
    def run_lexer(self, file_path):
        tokens = {"token_values": [], "token_types": []}
        try:
            with open(file_path, 'r') as file:
                data = file.read()
                self.__lexer.input(data)
                for token in self.__lexer:
                    tokens["token_values"].append(token.value)
                    tokens["token_types"].append(token.type)
                tokens["token_values"].append("$")
                tokens["token_types"].append("$")
                return tokens
        except FileNotFoundError:
            print(f"File {file_path} not found.")