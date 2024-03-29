#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# main.py --lex <SOURCE-FILE>
#
# Made by Simon Bernard and Ivan Klapka for the compilers project
# University of Liege - Academic year 2019-2020 - INFO0085-1 Compilers course
# -----------------------------------------------------------------------------
import argparse
import sys
import os
from llvmlite import ir
from myLexer import *
from myParser import *
from mySemanticAnalysis import *
from myLLVMGenerator import *
from myObject import *

if __name__ == '__main__':
    # Parsing arguments
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument('path', help='Path to the input VSOP source code', metavar='<SOURCE-FILE>')
    grp = parser_arg.add_mutually_exclusive_group()
    grp.add_argument('-lex', help='Part 1 : lexical analysis', action="store_true")
    grp.add_argument('-parse', help='Part 2 : syntax analysis', action="store_true")
    grp.add_argument('-check', help='Part 3 : semantic analysis', action="store_true")
    grp.add_argument('-llvm', help='Part 4 : generating the LLVM IR', action="store_true")
    parser_arg.add_argument('-ext', help='Special mode incuding extensions', action="store_true")
    args = parser_arg.parse_args()

    # Set file_name
    file_name = args.path.split('\\')[-1:][0]
    # Get the type of the file
    file_type = file_name.split('.')[1]

    # Check for which argument was selected
    # For extensions launch a special main
    if args.ext:
        from mainExt import *
        mainExt(args)

    # Check that the type of the file is .vsop
    elif file_type != "vsop":
        sys.stderr.write("File extension should be .vsop")
        sys.exit(1)

    # Lexical analysis
    elif args.lex:
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

    # Syntax analysis
    elif args.parse:
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
        # Exit if an error was detected
        if mypars.errFlag:
            sys.exit(1)
        print(out)

    # Semantic analysis
    elif args.check:
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
        # Exit if an error was detected
        if mypars.errFlag:
            sys.exit(1)

        # Check semantic
        updatedAstInfo = checkSemantic(ast, file_name)
        print(updatedAstInfo[0])

    # Code generation
    elif args.llvm:
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
        # Exit if an error was detected
        if mypars.errFlag:
            sys.exit(1)

        # Check semantic
        updatedAstInfo = checkSemantic(ast, file_name)
        updatedAst = updatedAstInfo[0]
        gst = updatedAstInfo[1]

        # Generate LLVM IR
        lgen = generateLLVM(updatedAst, gst, file_name)

        #Remove the first two lines
        codeStr = lgen.module.__str__().split("\n",2)[2];

        # Append to object.ll
        objectCode = getObjectLL()
        codeStr = objectCode + "\n\n; Generated llvm code below\n\n" + codeStr

        # Print the llvm IR code
        print(codeStr)

    # Create executable
    else:
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
        # Exit if an error was detected
        if mypars.errFlag:
            sys.exit(1)

        # Check semantic
        updatedAstInfo = checkSemantic(ast, file_name)
        updatedAst = updatedAstInfo[0]
        gst = updatedAstInfo[1]

        # Generate LLVM IR
        lgen = generateLLVM(updatedAst, gst, file_name)

        #Remove the first two lines
        codeStr = lgen.module.__str__().split("\n",2)[2];

        # Append to object.ll
        objectCode = getObjectLL()
        codeStr = objectCode + "\n\n; Generated llvm code below\n\n" + codeStr

        # Create a file that will old the llvm code string
        file_title = file_name[:-5]
        codefile = open(file_title + "_to_compile.ll", "w")
        codefile.write(codeStr)
        codefile.close()

        # Compile the llvm
        cmd1 = "llc-9 " + file_title + "_to_compile.ll"
        os.system(cmd1)

        # Create the executable
        cmd2 = "clang " + file_title + "_to_compile.s -o " + file_title + " -lm" 
        os.system(cmd2)