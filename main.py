# -----------------------------------------------------------------------------
# main.py --lex <SOURCE-FILE>
#
# Made by Simon Bernard and Ivan Klapka for the Project 1 : lexical analysis
# University of Liège - Academic year 2019-2020 - INFO0085-1 Compilers course
# -----------------------------------------------------------------------------
import argparse
import sys

# For the lexer
exec(open("lexer.py").read())
global file_name

# For the parser
exec(open("parser.py").read())

if __name__ == '__main__':
    # Parsing arguments
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument('-lex', help='Path to the input VSOP source code for lexical analysis')
    parser_arg.add_argument('-parse', help='Path to the input VSOP source code for syntax analysis')
    args = parser_arg.parse_args()

    # Check for path
    if args.lex:
        # Create lexer
        mylex = MyLexer()
        mylex.build() # Build the lexer
        mylex.lexer.line_end_pos = -1

        # Set file_name
        file_name = args.lex.split('\\')[-1:][0]
        
        # Give the lexer some input
        f = open(args.lex, "r")
        data = f.read()
        mylex.lexer.input(data)

        # Tokenize
        while True:
            tok = mylex.lexer.token()
            if not tok:
                break     # No more input

            ## Print the tokens
            # Check for string
            if (tok.type == "string_literal"):
                token_str = str(mylex.lexer.string_start_line) + "," + str(mylex.lexer.string_start_column) + "," + tok.type.replace("_","-")
                token_str += ("," + str(tok.value))
                print(token_str)

            # Check for type_identifier or object_identifier or integer_literal
            elif (tok.type == "type_identifier" or tok.type == "object_identifier" or tok.type == "integer_literal"):
                token_str = str(tok.lineno) + "," + str(tok.lexpos - mylex.lexer.line_end_pos) + "," + tok.type.replace("_","-")
                token_str += ("," + str(tok.value))
                print(token_str)
            # Rest of tokens
            else:
                token_str = str(tok.lineno) + "," + str(tok.lexpos - mylex.lexer.line_end_pos) + "," + tok.type.replace("_","-")
                print(token_str)

    elif args.parse:
        # Create lexer
        mylex = MyLexer()
        mylex.build() # Build the lexer
        mylex.lexer.line_end_pos = -1

        # Set file_name
        file_name = args.parse.split('\\')[-1:][0]

        # Create parser
        mypars = MyParser(mylex)
        mypars.build(debug=False) # Build the parser

        # Give the parser some input
        f = open(args.parse, "r")
        data = f.read()
        out = mypars.parser.parse(data)
        print(out)

    else:
        sys.stderr.write("Argument missing : Path to the input VSOP source code.\n")
        sys.exit(1)
