# -----------------------------------------------------------------------------
# test1.py
#
# A simple test
# -----------------------------------------------------------------------------
from ply.lex import TOKEN

keyword = {
    'and' : 'AND',
    'bool' : 'BOOL',
    'class' : 'CLASS',
    'do' : 'DO',
    'extends' : 'EXTENDS',
    'false' : 'FALSE',
    'in' : 'IN',
    'int32' : 'INT32',
    'isnull' : 'ISNULL',
    'let' : 'LET',
    'new' : 'NEW',
    'not' : 'NOT',
    'string' : 'STRING',
    'true': 'TRUE',
    'unit' : 'UNIT',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
}

# List of operators
operator = {
    '{' : 'lbrace',
    '}' : 'rbrace',
    '(' : 'lpar',
    ')' : 'rpar',
    ':' : 'colon',
    ';' : 'semicolon',
    ',' : 'coma',
    '+' : 'plus',
    '-' : 'minus',
    '*' : 'times',
    '/' : 'div',
    '^' : 'pow',
    '.' : 'dot',
    '=' : 'equal',
    '<' : 'lower',
    '<=' : 'lower_equal',
    '<-' : 'asign',
}

# List of token names + keyword
tokens = [
    'lowercase_letter',
    'uppercase_letter',
    'letter',
    'bin_digit',
    'digit',
    'hex_digit',
    'integer_literal_r',
    'integer_literal',
    'whitespace',
    'newline',
    'type_identifier',
    'object_identifier',
    'operator',
    'test'] + list(keyword.values()) + list(operator.values())

###  Tokens
# Whitespace
#t_whitespace = r'[ \t\n\r\f]'

# Literals
#literals = [ '+','-','*','/' ]

# Letters
#t_lowercase_letter = r'[a-z]'
#t_uppercase_letter = r'[A-Z]'
#t_letter = r'(' + t_lowercase_letter + r'|' + t_uppercase_letter + r')'

# Numbers
t_bin_digit = r'[0-1]';
t_digit = r'(' + t_bin_digit + r'|' + r'[2-9]' + r')'
t_hex_digit = r'(' + t_digit + r'|' + r'[a-f]' + r'|' + r'[A-F]' + r')'
t_integer_literal_r = r'(' + r'(' + r'0x' + r'(' + t_hex_digit + r'+' + r')' + r')' + r'|' + r'(' + t_digit + r'+' + r')' + r')'

# Single line comment
def t_singlelinecomment(t):
    r'//.*'
    pass

#  Line numbers and positional information
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.line_end_pos = t.lexpos
    return t

def t_whitespace(t):
    r'[ \t\r\f]'
    return t

@TOKEN(t_integer_literal_r)
def t_integer_literal(t):
    # Get next token without moving lexer state
    next_tok = get_next_token(t)
    # Checking for eof
    if not next_tok:
        return t

    ## probably should change to if type_identifier or object_identifier => pass
    
    # Checking for next token to be whitespace or operator
    if (next_tok.type in (["whitespace", "newline"] + list(operator.values()))) :
        return t
    else :
        # Print error
        error_str = file_name + ":" + str(t.lexer.lineno)
        error_str += ":" + str(t.lexpos - t.lexer.line_end_pos)
        error_str += ": " + str(t.value) + str(next_tok.value)
        error_str += " is not a valid integer literal"
        print(error_str)

        # Discard next token
        t.lexer.token()

def t_operator_long(t):
    r'<-|<='
    t.type = operator.get(t.value,'operator')
    return t

def t_operator(t):
    r'[\{\}\(\)<\.=\:\-;\*\+,/\^]'
    t.type = operator.get(t.value,'operator')
    return t

def t_type_identifier(t):
    r'[A-Z][a-zA-Z_0-9]*'
    t.type = keyword.get(t.value,'type_identifier')    # Check for keyword words
    return t

def t_object_identifier(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = keyword.get(t.value,'object_identifier')    # Check for keyword words
    return t

###  Error handling
def t_error(t):
    error_str = file_name + ":" + str(t.lexer.lineno)
    error_str += ":" + str(t.lexpos - t.lexer.line_end_pos)
    error_str += ": Invalid character '" + t.value[0] + "'"
    print(error_str)
    t.lexer.skip(1)


#####  Additionnal mode
# Declare the states/modes of the lexer
states = (
    ('commentmode','exclusive'),
#    ('stringmode','exclusive'),
)

####  String mode


####  Comment Mode
# Match the first (*. Enter commentmode state.
def t_nestedcomment(t):
    r'\(\*'
    t.lexer.comment_start_line = t.lexer.lineno   # Record the starting position
    t.lexer.comment_start_column = t.lexpos - t.lexer.line_end_pos
    t.lexer.level = 1                             # Initial level
    t.lexer.begin('commentmode')                  # Enter 'commentmode' state

# Rules for the commentmode state
def t_commentmode_lnestedcom(t):
    r'\(\*'
    t.lexer.level +=1

def t_commentmode_rnestedcom(t):
    r'\*\)'
    t.lexer.level -=1

    # If end of nested comment, return to initial
    if t.lexer.level == 0:
        #t.type = "commentmode"
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')
        #return t

# Skip any sequence of non-whitespace characters
def t_commentmode_nonspace(t):
    r'[^\s\{\}\'\"]+'
    pass

# Ignored characters (whitespace)
t_commentmode_ignore = " \t\n\r\f\v"

# For bad characters, we just skip over it
def t_commentmode_error(t):
    t.lexer.skip(1)

# For when comment is not closed
def t_commentmode_eof(t):
    error_str = file_name + ":" + str(t.lexer.comment_start_line)
    error_str += ":" + str(t.lexer.comment_start_column)
    error_str += ": Multi-line comment is not terminated when end-of-file is reached"
    print(error_str)


##### Build the lexer
import ply.lex as lex
lexer = lex.lex()
lexer.line_end_pos = 0

# Test it out
data = '''
a lol 502 +
327+
0x7
// hu 12
bool
someFun42
{}
()
<-
<=
<
=
.
:
;
,
-
+
*
/
^
someFun 42
0x45
0xabcdefgh
and
45'''

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Get next token without moving forward
def get_next_token(token):
    # Save all variables from lexer
    saved_lexpos = token.lexer.lexpos
    saved_lineno = token.lexer.lineno
    saved_end_pos = token.lexer.line_end_pos

    # Get next token
    next_token = token.lexer.token()

    # Restore variables
    token.lexer.lexpos = saved_lexpos
    token.lexer.lineno = saved_lineno
    token.lexer.line_end_pos = saved_end_pos

    return next_token

# Give the lexer some input
lexer.input(data)
global file_name
file_name = "FILENAME"

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break     # No more input
    # Ignore whitespace and newline
    if not (tok.type == "whitespace" or tok.type == "newline") :
        token_str = str(tok.lineno) + "," + str(find_column(data,tok)) + "," + str(tok.type)
        #if(tok.type == "hex_digit"):
        token_str += ("," + str(tok.value))
        #TODO
        print(token_str)
