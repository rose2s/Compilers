######Roselane Santana Silva
######EECS 6083: Compiler Theory/Compiler Laboratory
######April 24, 2015
#Compiler - Page Report

##Description

A single-pass, recursive descent LL(1) compiler written by hand for a made-up language and generates intermediate LLVM representation. This compiler project was done individually for the Spring Term of 2015.
Dependencies
This compiler was written entirely in Python 2.7.8 and Mac OSX yosemite version 10.10.3.

##Version Control
In order to maintain previous versions of the project, and ensure security of the code, I have used Git version control since the beginning of project. Git is a public version control, so the project can be accessed by using this link: https://github.com/rose2s/Compilers
Also, a log file was created, and reported description/dates for every single change in the source code.

##Usage
There are some ways to execute the project from command line.
Usage1: compiler.py < -h | --help >
This command displays all possible commands to execute the project.
Usage2: compiler.py < -i | --input > input.src 
This is the default command to execute the program.
Usage3: compiler.py < -i | --input > input.src < -s | -- st >
This command executes the program, and shows the symbol table built
Usage4: compiler.py < -i | --input > input.src < -t | -- token >
This command executes the program, and show the list of tokens

If there is no error, a generated code <input.ll> is then outputted with the intermediate LLVM representation. 

##Implementation Details
###Programming Language
Python was chosen as the implementation language because it is easy to manipulate, has its hash table (use of dictionaries), this way was easy to build the symbol table. In addition, python powerful syntaxe making fast the construction of structures like list, stack used in the compiler.

###Structure
The compiler project is structured in main 3 files (compiler.py, automata.py, and codeGeneration.py)  and two auxiliary files (list.py, stack.py).

'compiler.py' is the central file responsible for getting the command-line arguments, calling the automata class ('automata.py') and running the automata for each token in order to valid the input file, parsing, throwing scanner and parser errors if necessary, and passing tokens information to code generation. 
'codeGen.py' receives token information and generates LLVM representation. 
'stack.py' and 'list.py' are source files containing the data structure list and stack which are used in the various components of the compiler.

##6. Phases
###Scanning
The implementation of the scanner takes the input file and generates a list of tokens by splitting the source code into a list of distinct lines. At the start of each non-whitespace character, the automata is used to recognize the language by giving a type for each token or throwing a warning if it is not accepted. 

The scanner warnings are never fatal, though syntactically the tokens returned
may cause a parser error. For example, if the token is s@4, my approach was removing the non-allowed character, in this case '@', and recognize 's' and '4' separately. 


###Parsing
Type-checking is performed in expressions by returning the types from the
expression tree functions and evaluating types for compatibility if an
operation is performed. There are many other locations were type-checking is
performed in the compiler other than expressions. Many type checking were verified for parsing, Examples include, checking of array variables, undeclared variables, variables not initialized, type matching, etc.
Parser resync points are used throughout the compiler to continue parsing if
an error is encountered. 
Once a parser error is encountered in a statement or declaration, an error is displayed, an error count is incremented, and the token is moved to the next statement or declaration.
If the number of error count is greater than zero, the code will no longer
be generated.
However, there is an exception: procedures declaration have no resync point.

###Code Generation

The code was generated manually based on LLVM language reference found in this link http://llvm.org/releases/2.6/docs/LangRef.html#i_zext.

Clang also was used as example of LLVM representation. Since it transforms C code to llvm representation, it could be used for comparison.

There is a unique case in which the code generation doesn't work very well. I couldn't generate instruction for multiple return values on time. So, in order to make the generation works, the function should only have 1 "out" value. If it has more than one, only the first one will be returned.


##7. References
http://www.ece.uc.edu/~paw/classes/eecs6083/

A. Aho, M. Lam, R. Sethi, and J. Ullman Compilers: Principles, Techniques, and Tools, Addison Wesley, 2007.

Instructor: Philip A. Wilsey 

http://www.llvm.org/docs/LangRef.html

http://web.stanford.edu/class/cs143/

