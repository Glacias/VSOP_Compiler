# -----------------------------------------------------------------------------
# main.py --lex <SOURCE-FILE>
#
# Made by Simon Bernard and Ivan Klapka for the compilers project
# University of Liege - Academic year 2019-2020 - INFO0085-1 Compilers course
# -----------------------------------------------------------------------------
import argparse
import sys
import os
from mylexer import *
from myparser import *
from mySemanticAnalysis import *
from myLLVMGenerator import *

if __name__ == '__main__':
    # Parsing arguments
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument('path', help='Path to the input VSOP source code')
    parser_arg.add_argument('-lex', help='Part 1 : lexical analysis', action="store_true")
    parser_arg.add_argument('-parse', help='Part 2 : syntax analysis', action="store_true")
    parser_arg.add_argument('-check', help='Part 3 : semantic analysis', action="store_true")
    parser_arg.add_argument('-llvm', help='Part 4 : generating the LLVM IR', action="store_true")
    args = parser_arg.parse_args()

    # Check for wich argument was selected
    if args.lex:
        # Set file_name
        file_name = args.path.split('\\')[-1:][0]
        # Create lexer
        mylex = MyLexer(file_name)
        mylex.build() # Build the lexer
        mylex.lexer.line_end_pos = -1
        mylex.lexer.line_end_pos_table = [0]

        # Give the lexer some input
        f = open(args.path, "r")
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
        # Set file_name
        file_name = args.path.split('\\')[-1:][0]

        # Create lexer
        mylex = MyLexer(file_name)
        mylex.build() # Build the lexer
        mylex.lexer.line_end_pos = -1
        mylex.lexer.line_end_pos_table = [0]

        # Create parser
        mypars = MyParser(mylex, file_name)
        mypars.build(debug=False) # Build the parser

        # Give the parser some input
        f = open(args.path, "r")
        data = f.read()
        out = mypars.parser.parse(data)
        print(out)

    elif args.check:
        # Set file_name
        file_name = args.path.split('\\')[-1:][0]

        # Create lexer
        mylex = MyLexer(file_name)
        mylex.build() # Build the lexer
        mylex.lexer.line_end_pos = -1
        mylex.lexer.line_end_pos_table = [0]

        # Create parser
        mypars = MyParser(mylex, file_name)
        mypars.build(debug=False) # Build the parser

        # Give the parser some input
        f = open(args.path, "r")
        data = f.read()
        ast = mypars.parser.parse(data)

        # Check semantic
        updatedAstInfo = checkSemantic(ast, file_name)
        print(updatedAstInfo[0])

    elif args.llvm:
        # Set file_name
        file_name = args.path.split('\\')[-1:][0]

        # Create lexer
        mylex = MyLexer(file_name)
        mylex.build() # Build the lexer
        mylex.lexer.line_end_pos = -1
        mylex.lexer.line_end_pos_table = [0]

        # Create parser
        mypars = MyParser(mylex, file_name)
        mypars.build(debug=False) # Build the parser

        # Give the parser some input
        f = open(args.path, "r")
        data = f.read()
        ast = mypars.parser.parse(data)

        # Check semantic
        updatedAstInfo = checkSemantic(ast, file_name)
        updatedAst = updatedAstInfo[0]
        gst = updatedAstInfo[1]

        # Generate LLVM IR
        lgen = generateLLVM(updatedAst, gst, file_name)

        #Remove the first two lines
        codeStr = lgen.module.__str__().split("\n",2)[2];

        # Append to object.ll
        fObject = open("object.ll", "r")
        objectCode = fObject.read()
        codeStr = objectCode + "\n\n; Generated llvm code below\n\n" + codeStr

        # Print the llvm IR code
        print(codeStr)

    else:
        # Set file_name
        file_name = args.path.split('\\')[-1:][0]

        # Create lexer
        mylex = MyLexer(file_name)
        mylex.build() # Build the lexer
        mylex.lexer.line_end_pos = -1
        mylex.lexer.line_end_pos_table = [0]

        # Create parser
        mypars = MyParser(mylex, file_name)
        mypars.build(debug=False) # Build the parser

        # Give the parser some input
        f = open(args.path, "r")
        data = f.read()
        ast = mypars.parser.parse(data)

        # Check semantic
        updatedAstInfo = checkSemantic(ast, file_name)
        updatedAst = updatedAstInfo[0]
        gst = updatedAstInfo[1]

        # Generate LLVM IR
        lgen = generateLLVM(updatedAst, gst, file_name)

        #Remove the first two lines
        codeStr = lgen.module.__str__().split("\n",2)[2];

        # Append to object.ll
        fObject = open("object.ll", "r")
        objectCode = fObject.read()
        codeStr = objectCode + "\n\n; Generated llvm code below\n\n" + codeStr

        # Create a file that will old the llvm code string
        file_title = file_name[:-5]
        codefile = open(file_title + ".ll", "w")
        codefile.write(codeStr)
        codefile.close()

        # Compile the llvm
        cmd1 = "llc-9 " + file_title + ".ll"
        os.system(cmd1)

        # Create the executable
        cmd2 = "clang " + file_title + ".s -o " + file_title + " -lm" 
        os.system(cmd2)