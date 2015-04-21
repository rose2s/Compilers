# Name:        scanner_Roselane.py
# Purpose:     Scanner 
# Author:      roses
# Created:     24/01/2015
# Copyright:   (c) roses 2014
#
# Version History:
#
# Ver      Author     Date        Notes
# -----    ---------  ----------  ---------------------------------
# 1.0.0    Rose       2015-01-24  Create function
# 1.0.0    Rose       2015-01-25  Create DFA
# 1.0.0    Rose		  2015-01-27  Fix Automata, getToken() function
# 1.0.0    Rose	  	  2015-01-27  Fix Automata, getToken() function
# 1.0.0    Rose		  2015-01-28  Divided Separator_Token, Fix	
# 1.0.0    Rose       2015-02-01  Create Grammar LL(1)
# 1.0.0    Rose		  2015-02-02  Create List
# 1.0.0    Rose		  2015-02-03  Lista salva com todos os tokens que devem ser pegos no parser()
# 1.0.0    Rose		  			  symbol_table nao esta compilando mas so salva os identifiers.
# 1.0.0    Rose		  2015-02-05 program_header function
# 1.0.0    Rose		  2015-02-05 var_declaration function
# 1.0.0    Rose		  2015-02-06 var_declaration function
# 1.0.0    Rose		  2015-02-07 procedure function function
# 1.0.0    Rose		  2015-02-08  proceure_call function
# 1.0.0    Rose		  2015-02-09 loop statement
# 1.0.0    Rose		  2015-02-09 if statement
# 1.0.0    Rose		  2015-02-24 else 
# 1.0.0    Rose		  2015-02-26 Fix bug on Parser
# 1.0.0    Rose		  2015-03-09 Simple table Management
# 1.0.0    Rose		  2015-03-11 Simple table Management with scopes
# 1.0.0    Rose		  2015-03-16 Type checking with operations
# 1.0.0    Rose		  2015-03-19 Type checking with IF, LOOP statement
# 1.0.0    Rose		  2015-03-20 Type checking with ProcedureCall statement
# 1.0.0    Rose		  2015-03-23 Minus sign
# 1.0.0    Rose		  2015-03-24 Type checking with Array variables
# 1.0.0    Rose		  2015-03-31 Start Code Gneration
# 1.0.0    Rose		  2015-04-04 Fix bug in Type checking Expressions
# 1.0.0    Rose		  2015-04-06 Fix bugs in parser
# 1.0.0    Rose		  2015-04-07 File managemente
# 1.0.0    Rose		  2015-04-08 Code Generation
# 1.0.0    Rose		  2015-04-09 Code Generation (exp)
#-------------------------------------------------------------------------------

import os,sys, getopt 
from automata import DFA
from List import List
from stack import Stack
from codeGen import CodeGen

class Lexical_Analyzer:

	# Token types used for automata
	tokenType = {'s1': "IDENTIFIER",'s2': "INTEGER", 's3': "FLOAT",'s6': "COMP_OP",'s7': "COMP_OP_EQ",
				 's8': "ARIT_OP",'s10': "LEFT_PAR",'s11': "RIG_PAR",'s12': "LEFT_CH", 's13': "RIG_CH",
				 's14': "COMMA",'s15': "SC",'s16': "LEFT_BRA", 's17': "RIG_BRA",'s18': "STRING"}

	keywords  = ["string", "case", "integer", "bool", "float", "for", "global", "not", "in", "program", "out", "procedure",
                          "if", "begin", "then", "return", "else", "end", "EOF", "true","false"]

	symbolTable = {}

	# LL(1) grammar
	terminals = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y',
					  '0','1','2','3','4','5','6','7','8','9',
					   "+", "-", "*", "/", "(", ")", "<", ">", "{", "}", ";"]
	startSimbol = 'E'
	non_terminals = ['E','E2','T','T2','F']
	current_token = None

	def __init__(self, generatedFile):
		self.lineCount = 0    								# Show the error
		self.IDtokenNum = 0   								# ID for Symbol table
		self.errorFlag = False                        		# Flag for errors     
		self.IFlag = False      							# Flag for IF statement
		self.tokenList = List("KEYWORD","program",0)		# Token List
		self.tokenList.setFirst(self.tokenList)
		self.EXPstack = Stack()								# Stack used for expressions
		self.stack = Stack()								# Stack used for parser
		self.checkExp = []									# List for Typing check expressions
		self.listGen = []
		self.tupleList = []  								# List of tuples used for generate variable declarations
		self.file = CodeGen(generatedFile)

	# Verifies if a variable is Letter
	def isLetter(self,var):
		if var in ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y'):
			return True
		else:
			return False

	# Verifies if a variable is Number
	def isNumber(self, var):
		if var in ('0','1','2','3','4','5','6','7','8','9'):
			return True
		else:
			return False

	def getFileName(self, filename):
		i = 0
		for i in range(len(filename)-1, 0, -1):
			pos = i
			if filename[i] in ("\'","/"):
				break

		return filename[i+1:]


	# Gets token and Runs automata
	def getTokenFromFile(self,filename):
		
		self.file.writeToken("; ModuleID = '"+self.getFileName(filename)+"'\n") 

		#print "Tokens:"
		word = ""
		value = 0  											   # 0 = other, 1 = letter, 2 = number

		with open(filename) as f:
			lines = f.readlines() 							   # Reads until EOF and returns a list of lines. 	
			for l in lines:									   # Loop each line
				self.lineCount += 1
				for s in range(len(l)):						   # Loop each character
					# Letter Buffer
					if value == 'cha': 						
						if self.isNumber(l[s]) or self.isLetter(l[s].lower()) or l[s] == '_': 
							word += l[s].lower()
							if s == len(l)-1:				    # If it is last character of the line		
								self.run_automata(word.lower()) # Runs automata
							else:
								continue  					    # Increments Letter Buffer
								
						else: 
							self.run_automata(word.lower())     # Runs automata
							word = ''							# Resets buffer
							value = ''
							if s+1 < len(l):					# If it is NOT last character of the line		
				  				if l[s]+l[s+1] == '//':			# If Comments then skip line
				  					break 						
				  			if l[s] in (" ","\n","\t"):			# Skips whitespace, tab, newline
			  					continue
							else:
								self.run_automata(l[s].lower()) # Runs automata with the character

			  		# Number Buffer 
			  		elif value == 'num': 		
			  			if self.isNumber(l[s]) or l[s] == "." or self.isLetter(l[s]):
							word += l[s]
							if s == len(l)-1:				    # If it is last character of the line		
								self.run_automata(word.lower()) # Runs automata
							else:
								continue						# Increments Number Buffer
						else: 
							self.run_automata(word.lower())     # Runs automata
							word = ''							# Resets buffer
							value = ''
							if s+1 < len(l):					# If it is NOT last character of the line
				  				if l[s]+l[s+1] == '//':			# If Comments then skip line
				  					break 	
				  			if l[s] in ("<",">",":","!","="):   # If Double operator then get the next character
			  					if s+1 < len(l):								
				  					if l[s+1] == '=':
			  							value = 'op'
			  							word += l[s]
			  						else:
			  							self.run_automata(l[s].lower())	

			  				elif l[s] in (" ","\n","\t"):           # Skips whitespace, tab, newline
			  					continue	
			  				else:
			  					self.run_automata(l[s].lower())     # Runs automata with the character

			  		# String Buffer
			  		elif value == 'str': 			
						if l[s] != '\"': 						    # If NOT quotes
							word += l[s]						 
							if s == len(l)-1:					    # If it is last character of the line	
								self.run_automata(word.lower())     # Runs automata
							else:
								continue						    # Increments String Buffer	
								
						else: 
							word += l[s] 			
							self.run_automata(word.lower())		    # Runs automata to validate String
							word = ''							    # Resets Buffer
							value = ''
							if l[s] != '\"':
								if s+1 < len(l):				    # If it is NOT last character of the line
					  				if l[s]+l[s+1] == '//':    	    # If Comments then skip line
					  					break 
					  			if l[s] in (" ","\n","\t"):     	# Skips whitespace, tab, newline
				  					continue
								else:
									self.run_automata(l[s].lower()) # Runs automata with the character
							else:
								continue

					# Operator Buffer
					elif value == 'op': 		
			  			word += l[s]								
			  			self.run_automata(word.lower())             # Runs automata to validate operator
						word = '' 									# Resets buffer
						value = ''

					# AND Buffer
					elif value == 'and': 		
			  			word += l[s]								
			  			self.run_automata(word.lower())             # Runs automata to validate operator
						word = '' 									# Resets buffer
						value = ''

			  		else:											
				  		if s+1 < len(l):							# If it is NOT last character of the line
				  			if l[s]+l[s+1] == '//':					# If Comments then skip line
				  				break 								
			  			if l[s] in (" ","\n","\t"):    				# Skips whitespace, tab, newline 
			  				continue	

			  			elif self.isLetter(l[s].lower()):           # If letter then flag to letter buffer
			  				value = 'cha'  							
			  				word += l[s].lower()
			  				
			  			elif self.isNumber(l[s]):					# If digit then flag to number buffer
			  				value = 'num'
			  				word += l[s]
			  				
			  			elif l[s] in ("<",">",":","!","="):			# If operator then flag to operator buffer
			  					if s+1 < len(l):									
				  					if l[s+1] == '=':				# Double operator
			  							value = 'op'
			  							word += l[s]
				  					else:
				  						self.run_automata(l[s])     # Single operator

				  		elif l[s] == "&":							# AND operator then flag to AND buffer
			  					if s+1 < len(l):									
				  					if l[s+1] == '&':			
			  							value = 'and'
			  							word += l[s]
				  					else:
				  						self.run_automata(l[s])     # Single operator

				  		elif l[s] == "\"":  						# If quotes then flag to string buffer
			  				value = 'str'  
			  				word += l[s].lower()

			  			else:
			  				self.run_automata(l[s])
			  				continue
			  			
			  			if s == len(l)-1:    						# If it is last character of the line
							self.run_automata(l[s]) 				# Runs character

	# Runs automata and sets tokens
	def run_automata(self,inp_program): 							# inp_program = word
		print inp_program
		dfa.run_with_input_list(inp_program)   						# Runs automata
		print "?", dfa.current_state
		if dfa.current_state in self.tokenType.keys():   			# If current_state in Accept States
			
			    token = self.tokenType[dfa.current_state]           # Sets token type

			    if token == "IDENTIFIER":
			        if inp_program in self.keywords:
			        	token = "KEYWORD"
				
			    #print "<"+inp_program + "> is <" + token+">"
			    self.tokenList.addNode(self.tokenList,token,inp_program,self.lineCount) # add token into Token List

		else:									
		    self.reportWarning(inp_program)   		# If current_state NOT in Accept States
		     

	def first(self,X):
		if X == 'E':
			return {self.getID(),'('}

		elif X == 'E2':
			return {'+','-'," "}

		elif X == 'T2':
			return {'*','/'," "}

	def follow(self, X):

		if X in ('E','E2'):
			return {')'," "}

		elif X in ('T','T2'):
			return {'+','-',')'}

		elif X == 'F':
			return {'+','-','*','/',')'}

	# Scans next token
	def scanToken(self):
		analyzer.current_token = analyzer.current_token.Next
		return analyzer.current_token
		
	# Validates Expression
	# Return ExpType if expression is correct
	def expression(self, current_token, sign, scope):     			# Returns True if token == sign	
		
		STlist = self.E(current_token, sign, scope)
		if STlist:								
			if self.EXPstack.isEmpty():								# Parenthesis op are pushed into Expression Stack
				print "\nCorrect Expression"
				try:
					self.file.genExpression(self.listGen)
				except:
					print "\nIt couldn't generate expression instruction"

				return STlist
			else: 
				self.reportErrorMsg("Missing )")
				self.errorFlag = True
				return False 

	def E(self, token, sign, scope):
		print "E: ",token.getTokenValue()
		STlist = self.T(token,sign, scope)

		if self.E2(analyzer.current_token, sign, scope):
			print "ST", self.checkExp
			
			if analyzer.current_token.getTokenValue() in ("&&","|"):
				self.listGen.append(analyzer.current_token.getTokenValue())  
				self.checkExp.append(analyzer.current_token.getTokenValue())
				token = self.scanToken()
				if self.E(token, sign, scope):
					return True
				else: 
					return False
			
			else:
				return True

	def E2(self,token, sign, scope):
		if not self.errorFlag:

			if (token.getTokenValue() in self.first('E2')) or (self.relation_op(token.getTokenValue())):
				self.listGen.append(token.getTokenValue())  # * or /
				self.checkExp.append(token.getTokenValue())
				token = self.scanToken()
				self.T(token,sign, scope)

				if self.E2(analyzer.current_token, sign, scope):
					return True

			elif token.getTokenValue() in ("&&","|"):
				return True

			elif token.getTokenValue() in sign:  				     # Stop Condition of the Recursion
				return True
			else: 
				self.reportError("aritm_op", token.getTokenValue(),token.line)
				return False
		else:
			return False

	def T(self,token,sign, scope):
		print "T: ",token.getTokenValue()

		STlist = self.F(token,sign, scope)
		
		if STlist:
			if self.T2(analyzer.current_token, sign, scope):
				return STlist
		else:
			return False


	def T2(self,token, sign, scope):
		if token:
			print "T': ",token.getTokenValue()

		if token.getTokenValue() in sign and self.EXPstack.isEmpty():   # Stop Condition of the Recursion
			print "sign:",sign
			return True

		elif token.getTokenValue() in ("&&","|"):
			return True

		while token.getTokenValue() == ")" and not self.EXPstack.isEmpty():
			if not self.EXPstack.isEmpty():
				self.EXPstack.pop()
				print "stack", self.EXPstack.items
				token = self.scanToken()
			else:
				self.reportError("(",")", token.line)
				self.errorFlag = True
				return False

		if token.getTokenValue() in self.first('T2'):

			# Check division by zero
			if token.getTokenValue() == "/" and token.Next.getTokenValue() == '0':
				self.reportErrorMsg("Error: Division by Zero", token.line)
				self.errorFlag = True
				return False
			# ---------------------

			print token.getTokenValue()
			self.listGen.append(token.getTokenValue())  # * or /
			self.checkExp.append(token.getTokenValue())
			token = self.scanToken()

			if self.F(token, sign, scope):
				self.T2(analyzer.current_token, sign, scope)
			else:
				return False

	def F(self, token, sign, scope):

		ST = []
		minus = False        # Flag to minus sign
 		is_array = False     # Flag that checks whether var is array or not
		print "F: ",token.getTokenValue()
		print token.getTokenType()

		while token.getTokenValue() == "(":
			self.EXPstack.push(token.getTokenValue())   		   # push Parenthesis
			print "stack: ",self.EXPstack.items
			token = self.scanToken()
			#self.E(token,sign, scope)

		if token.getTokenValue() == "-": 							# minus
			token = self.scanToken()
			minus = True
										   							
		if token.getTokenType() == ("IDENTIFIER"):

			ST = self.lookatST(token, scope)  				# STList = [name, type, size, value]

			if ST:
				if ST[3] == True or (self.isGlobal(token) and scope): #  GLOBAL  							# IF var has been initialized
					
					if self.isGlobal(token):
						var = token.getTokenValue()
					else:
						var = token.getTokenValue()
					vtype = ST[1]
					token = self.scanToken()
					
					loadList = [vtype, var]
					# Minus Type checking
					if minus:
						if ST[1].lower() not in ("integer", "int", "float"):
							self.reportErrorMsg("Minus [-] is not allowed with '"+ST[1]+"' type", analyzer.current_token.line)
							self.errorFlag = True
							return False

						elif token.getTokenValue() == "[":
							self.reportErrorMsg("Minus [-] is not allowed with array", analyzer.current_token.line)
							self.errorFlag = True
							return False
					# ---- 
					if ST[2] > 0: 									    	# If var was declared as array
						is_array = True

					if token.getTokenValue() == "[":   							# If identifier is a ARRAY

						# --- Array checking -----
						if is_array:
							if not self.destination(token, scope):
								self.errorFlag = True
								return False
							else:
								self.listGen = self.listGen[2:]     # remove destination from listGen (type, var)
	
								self.checkExp.append(ST[1].lower())  		 # var type
								self.listGen.append(ST[1].lower()) 			 # type 
								self.listGen.append(var) 		   			 # var

								loadList.append(ST[2])           		     # size
								loadList.append(token.Next.getTokenValue())  # pos
								print "loadList", loadList
								try:
									if scope != "main": 
										self.file.genLoad(loadList, scope)  # function scope
									else:
										self.file.genLoad(loadList, False)  # main scope
								except:
									print "\nIt couldn't generate Load instruction"

								return True 	

						else:
							self.reportErrorMsg("Error: Variable '"+ ST[0] +"' is not array type", analyzer.current_token.line)
							self.errorFlag = True
							return False

					else:
						if is_array: 
							self.reportErrorMsg("Error: Variable '"+ ST[0] +"' is array type", analyzer.current_token.line)
							self.errorFlag = True
							return False
						else:	
							self.checkExp.append(ST[1].lower())  				# var type
							self.listGen.append(ST[1].lower()) # type 
							self.listGen.append(var) 		 # var
							print "loadList", loadList
							try:
								self.file.genLoad(loadList) 
							except:
								print "\nIt couldn't generate Load instruction"

							return True

				else: # then it is a global variable
					self.reportErrorMsg("Error: Var '"+token.getTokenValue()+"' hasn't been initialized", analyzer.current_token.line)
					self.errorFlag = True
					return False
			else:
				#self.reportErrorMsg("Error: Var '"+token.getTokenValue()+"' hasn't been initialized", analyzer.current_token.line)
				self.errorFlag = True
				return False

		elif token.getTokenType() in ("INTEGER, FLOAT"):  
			expType = token.getTokenType() 
			print expType, " in F"

			if token.getTokenValue() in ("0","1"):   # boolean checking
				self.checkExp.append("int")
				self.listGen.append("int") # type 
				self.listGen.append(token.getTokenValue())  
			else:
				self.checkExp.append(expType.lower())
				self.listGen.append(expType.lower()) # type 
				self.listGen.append(token.getTokenValue())  
			token = self.scanToken()
			return True

		elif token.getTokenType() in ("STRING") and not minus:
			expType = token.getTokenType() 
			print expType, " in F"
			self.checkExp.append(expType.lower())
			self.listGen.append(expType.lower()) # type
			self.listGen.append(token.getTokenValue())  
			token = self.scanToken()
			return True

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() in ("true","false") and not minus:
			expType = "bool"
			print expType, " in F"
			self.checkExp.append(expType.lower())
			self.listGen.append(expType.lower()) #type
			self.listGen.append(token.getTokenValue())  
			token = self.scanToken()
			return True

		else:
			self.reportErrorMsg("Error: ID '"+token.getTokenValue()+ "' not found", analyzer.current_token.line)	
			self.errorFlag = True
			return False

	# If NOT relation then return list of relational operator
	# If relation then verify if variavel is a relational operator
	def relation_op(self, relation = False):
	 	l = [">=","==","<=","<",">","!="]

	 	if not relation:
	 		return l
	 	elif relation in l:
	 		print "relational op: ",relation
	 		return True
	 	else:
	 		return False

	# Resets errorFlag, stack
	def reset(self):
		self.errorFlag = False
		while not self.stack.isEmpty():
			self.stack.pop()

	def getRunTimeFunction(self, name):
		if name in ("getbool", "getintger", "getstring", "getfloat", "putbool", "putintger", "putstring", "putfloat"):
			return True
		else:
			return False

	# Starts to scan the program
	def program(self,token):
		if self.program_header(token):
			self.reset()
			if self.program_body(analyzer.current_token):
				if analyzer.current_token.getTokenValue() == "end":
					token = self.scanToken()

					if token.getTokenValue() == "program":
						print "\nSuccess!"
						try:
							self.file.genEnd()
						except:
							print "\nIt couldn't generate End instruction"
						
						return True

					else:
						self.reportError("program", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False
				else:
					self.reportError("end", token.getTokenValue(), token.line)
					self.errorFlag = True
					return False

	def program_header(self,token):
		if not self.errorFlag:

				if self.stack.isEmpty():

					if token.getTokenValue() == "program":
						self.stack.push(token.getTokenValue())
						self.program_header(self.scanToken())
					else:
						self.reportError("program", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False

				if self.stack.peek() == "program":

					if token.getTokenType() == "IDENTIFIER":	
						self.stack.push(token.getTokenType())
						self.program_header(self.scanToken())
					else:
						self.reportError("IDENTIFIER", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False

				if self.stack.peek() ==  "IDENTIFIER":

					if token.getTokenValue() == "is":
						self.stack.push(token.getTokenValue())
						self.program_header(self.scanToken())
					else:
						self.reportError("is", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False

				if self.stack.peek() == "is":
					return True
		else:
			return False

	def program_body(self,token):
		print "\nPrgram_Body Function: ", token.getTokenValue()

		self.addSymbolTable("global", "getbool", "proc", "bool", [])
		self.addSymbolTable("global", "getintger", "proc", "integer", [])
		self.addSymbolTable("global", "getstring", "proc", "string", [])
		self.addSymbolTable("global", "getfloat", "proc", "float", [])
		self.addSymbolTable("global", "putbool", "proc", "bool", ["bool"])
		self.addSymbolTable("global", "putintger", "proc", "integer", ["integer"])
		self.addSymbolTable("global", "putstring", "proc", "string", ["string"])
		self.addSymbolTable("global", "putfloat", "proc", "float", ["float"])

		if not self.errorFlag:
			if self.declaration(token):
				self.file.skipLine()
				print "\nStart Main Program!", self.tupleList
				try:
					self.file.genFunction(["global","main"])  # generate main function
					for l in self.tupleList:				  # generate variable declarations
						self.file.genDeclaration(l)

					self.file.skipLine()
				except:
					print "\nIt couldn't generate Variable Declaration instruction"

				self.tupleList = []

				if self.statement(analyzer.current_token):
					return True
	
				else:
					self.errorFlag = True
					return False
			else: 
				#self.reportErrorMsg("Wrong Declaration",analyzer.current_token.line)
				self.errorFlag = True
				return False

		else:
			return False

	# Checks type mark
	def type_mark(self,t):
		if t in ("integer", "float", "bool", "string"):
			return True
		else:
			return False

	def declaration(self, token, scope = "main"):
		global_scope = False

		if not self.errorFlag:
			print "Declaration Function:", token.getTokenValue() 
			if token.getTokenValue() == "global":
				global_scope = "global"
				token = self.scanToken()

			if self.type_mark(token.getTokenValue()):
				if global_scope:
					var = self.variable_declaration(token, global_scope)
				else:
					var = self.variable_declaration(token, scope)

				if var:
					if self.declaration(analyzer.current_token, scope):
						return True
					else:
						return False
				else:
					return False

			elif token.getTokenValue() == "procedure":

				if global_scope:
					proc = self.procedure_declaration(token, global_scope)
				else:
					proc = self.procedure_declaration(token, scope)

				if proc:
					if self.declaration(analyzer.current_token, scope):
						return True
					else:
						return False
				else:
					return False
			
			elif token.getTokenValue() == "begin":  # Stop condition
				return True

			elif token.getTokenValue() == "int":
				self.reportError("integer", token.getTokenValue(), token.line)
				self.errorFlag = True

			else: 
				self.reportErrorMsg("SyntaxError: Invalid Syntax in Declaration",token.line)
				self.errorFlag = True
				return False
		else:
			return False

	# If Parameter then it is parameter declaration
	def variable_declaration(self, token, scope = "main", parameterList = False): 

		size = 0
		tup = []

		print "Variable_declaration Funtion:",token.getTokenValue()

		if scope == "global":	
			self.listGen.append("global")
			if scope == "main":
				tup.append(scope)
	
		if self.type_mark(token.getTokenValue()):  						# if token in type_mark
			Type = token.getTokenValue()								# temp var to symbol table
			
			token = self.scanToken()

			if token.getTokenType() == "IDENTIFIER":
				name = token.getTokenValue()							 # temp var to symbol table
				self.listGen.append(Type)
				self.listGen.append(name)

				if scope == "main":
					tup.append(Type)
					tup.append(name)
				
				#check redeclaration of variables
				STlist = self.lookatST(token, scope, True)
				if STlist:
					self.reportErrorMsg("Error: redeclaration of '" + name + "'" , token.line)
					return False
				# ---

				token = self.scanToken()
				
				if token.getTokenValue() == ";" and not parameterList:				# var is NOT array and NOT var parameter
					token = self.scanToken()
					self.addSymbolTable(scope, name, Type, size)
					if scope != "main":
						try:
							self.file.genDeclaration(self.listGen)
						except:
							print "\nIt couldn't generate Variable Declaration instruction"
					elif len(tup):
						self.tupleList.append(tup)
					self.listGen = []
					return True
				
				elif parameterList and token.getTokenValue() != "[": 			    # var is not array, but is var parameter
					if token.getTokenValue() in ("in","out"):
						self.listGen.append(token.getTokenValue())
						token = self.scanToken()
						self.addSymbolTable(scope, name, Type, size, True)
						
						return True
					else:
						self.reportError("in/out", token.getTokenValue(),token.line)
						return False

				# Array Variables
				elif token.getTokenValue() == "[":
					token = self.scanToken()

					if token.getTokenType().lower() in ("int", "integer", "float"):
						size = token.getTokenValue()
						token = self.scanToken()
						self.listGen.append(size)
						if scope == "main":
							tup.append(size)

						if token.getTokenValue() == "]":
							token = self.scanToken()
 
							if token.getTokenValue() == ";" and not parameterList:   # var is array and NOT var parameter
								token = self.scanToken()
								self.addSymbolTable(scope, name, Type, size)
								
								if scope != "main":
									try:
										self.file.genDeclaration(self.listGen)
									except:
										print "\nIt couldn't generate Variable Declaration instruction"
					
								elif len(tup) > 0:
									self.tupleList.append(tup)

								self.listGen = []
								return True

							elif parameterList: 									 # var is array and is var parameter
								if token.getTokenValue() in ("in","out"):
									self.listGen.append(token.getTokenValue())
									token = self.scanToken()

									self.addSymbolTable(scope, name, Type, size, True)
									
									return True
								else:
									self.reportError("in/out", token.getTokenValue(),token.line)
									return False
							else: 
								self.reportError(";", token.getTokenValue(),token.line)
								return False
						else: 
							self.reportError("]", token.getTokenValue(),token.line)
							return False
					else: 
						self.reportError("array Size", token.getTokenValue(),token.line)
						return False
				else: 
					self.reportError(";",token.getTokenValue() , token.line-1)
					return False

			else: 
				self.reportError("Identifier Type", token.getTokenType(),token.line)
				return False

		else: 
			self.reportError("Type Mark", token.getTokenType(),token.line)
			return False


	# myList = [global,name,[global, type, name in|out]]
	def procedure_declaration(self, token, scope = "main"):
		print "\nProcedure Declaration Function: ",token.getTokenValue()
		
		if scope in ("global", "main"):
			self.listGen.append("global")

		new_scope = token.Next.getTokenValue()  # Procedure Name
		self.listGen.append(new_scope)

		parList = self.procedure_header(token)
		if parList:

			#check redeclaration of procedures
			STlist = self.lookatST(token.Next, scope, True)
			if STlist:
				self.reportErrorMsg("Error: redeclaration of Procedure '" + token.Next.getTokenValue() + "'" , token.line)
				self.errorFlag = True
				return False
			# ---

			if parList == True:      			# If procedure has no parameter then value = 0
				parList = 0


			self.addSymbolTable(scope, token.Next.getTokenValue(), "proc", 0, parList)  # add procedure and his scope into to ST

			self.addSymbolTable(token.Next.getTokenValue(), token.Next.getTokenValue(), "proc", 0, parList)  # add procedure in itself to allow recursion

			if self.procedure_body(analyzer.current_token, new_scope):
				try:
					self.file.genReturn(new_scope)
				except:
					print "\nIt could not generate Return instruction"
				return True
			else:
				return False
		else:
			return False

	def procedure_header(self,token):
		print "Procedure_header Function: ",token.getTokenValue()
		parList = [] 

		if token.getTokenValue() == "procedure":
			token = self.scanToken()

			if token.getTokenType() == "IDENTIFIER":
				scope = token.getTokenValue()  			# 
				token = self.scanToken()	

				if token.getTokenValue() == "(":
					token = self.scanToken()

					if self.type_mark(token.getTokenValue()):

						parList.append(token.getTokenValue())
						self.variable_declaration(token, scope, True)
					
						while analyzer.current_token.getTokenValue() == ",":
							token = self.scanToken()
							parList.append(token.getTokenValue())
							self.variable_declaration(analyzer.current_token, scope, True)


						if analyzer.current_token.getTokenValue() == ")":
							token = self.scanToken()

							try:
								self.file.genFunction(self.listGen)
							except:
								print "\nIt couldn't generate Function instruction"
							
							self.listGen = []
							return parList

						else: 
							self.reportErrorMsg("Missing ) in the procedure", token.line)
							self.errorFlag = True
							return False
						
					elif analyzer.current_token.getTokenValue() == ")":
						token = self.scanToken()
						# print "Function w/o parameters"

						try:
							self.file.genFunction(self.listGen)
						except:
							print "\nIt couldn't generate Function instruction"
						self.listGen = []
						return True

					else: 
						self.reportError("Identifier Type", token.getTokenValue(),token.line)
						self.errorFlag = True
						return False

				else:
					self.reportError("(", token.getTokenValue(), token.line)
					self.errorFlag = True
					return False
			else:
				self.reportError("Function Name", token.getTokenValue(), token.line)
				self.errorFlag = True
				return False

	def procedure_body(self,token, scope):
		print "Procedure_Body Function:",token.getTokenValue()
		#print "scope",scope
		if not self.errorFlag:
			if self.declaration(token, scope):
				pass
			else:
				self.errorFlag = True
				return False
		else:
			return False

		if self.statement(analyzer.current_token, False, scope):

			if analyzer.current_token.getTokenValue() == "end":
				token = self.scanToken()

				if token.getTokenValue() == "procedure":
					token = self.scanToken()

					if token.getTokenValue() == ";":
						print "end procedure"
						token = self.scanToken()
						return True
					else:
						print token.line
						self.reportError(";", token.getTokenValue(), token.Prior.line)
						self.errorFlag = True
						return False
				else:
					self.reportError("procedure", token.getTokenValue(), token.line)
					self.errorFlag = True
					return False
			else:
				self.reportError("end", token.getTokenValue(), token.line)
				self.errorFlag = True
				return False
		else:
			return False

	# If if_stat then "else is a sign for expressions"
	# If proc_scope then it is a statement within procedure
	def statement(self,token, if_stat = False, proc_scope = False): 
		prior = token
		token = self.scanToken()

		print "Statement Function:", token.getTokenValue()

		if not token:
			self.reportErrorMsg("SyntaxError: Missing 'end program'",prior.line+1)
			return False

		if not if_stat:  # if_stat: then should execute at least one statement
			if token.getTokenValue() == "end":
				return True

			if self.IFlag:
				if token.getTokenValue() == "else" and self.stack.size() > 0:
					return True

		if token.Next:
			if token.Next.getTokenValue() in (":=","["):
				if self.assignment_statement(token, proc_scope):
					if self.statement(analyzer.current_token, False, proc_scope):
						return True
					else:
						return False
				else: 
					return False

			elif token.getTokenType() == "IDENTIFIER" and token.Next.getTokenValue() == "(":
				if self.procedure_call(token, proc_scope):

					if self.statement(analyzer.current_token, False, proc_scope):
						return True
					else:
						return False
				else:
					return False

		if token.getTokenValue() == "return":
			if self.return_statement(token, proc_scope):

				if self.statement(analyzer.current_token, False, proc_scope):
					return True
				else:
					return False
			else:
				return False

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() == "for":

			if self.loop_statement(token, proc_scope):
				
				if self.statement(analyzer.current_token, False, proc_scope):
					return True
				else:
					return False
			else:
				return False

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() == "if":

			if self.if_statement(token, proc_scope):
			
				if self.statement(analyzer.current_token, False, proc_scope):
					return True
				else:
					return False
			else:
				return False

		elif if_stat:
			self.reportErrorMsg("Error: IF must have at least one statement",token.line)
			return False

		else:
			self.reportErrorMsg("SyntaxError: Invalid syntax in Statement ",token.line)
			return False

	# If proc_scope then it is assigment within procedure
	# listgGen = [[global], type, name, value]
	def assignment_statement(self, token, proc_scope = False):
		print "\nAssignment Statement Function"
		#print "scope",proc_scope

		if token.getTokenType() == "IDENTIFIER":

			var_token = token  # Temp procedure name
			array_var = False  # Flag that checks whether var is array or not

			# --- Declaration Check ---#
			STlist = self.lookatST(token, proc_scope)  					# Verify if var within ST
		
			if not STlist:												# Error: Undeclared var
				return False
			# ---------  ##  --------- #
			if self.isGlobal(var_token):
				self.listGen.append("global")
			
			storeList = [STlist[1], var_token.getTokenValue()]         # type, var

			# --- Array checking -----
			if STlist[2] > 0 : 											# If var was declared as array
				storeList.append(STlist[2]) 							# size of array
				array_var = True

			token = self.scanToken()

			if token.getTokenValue() == "[":  							# If array
				if array_var:
					storeList.append(token.Next.getTokenValue())  		# position of array

					if not self.destination(token, proc_scope):		  	# True if integer
						self.errorFlag = True
						return False
					
					self.listGen = []    								# clean sentence after verify expression of array
					array_var = False 
			 
				else:
					self.reportErrorMsg("Error: Variable '"+ var_token.getTokenValue() +"' is not array type", var_token.line)
					self.errorFlag = True
					return False

			if analyzer.current_token.getTokenValue() == ":=":
				if array_var: 
					self.reportErrorMsg("Error: Variable '"+ var_token.getTokenValue() +"' is array type", var_token.line)
					self.errorFlag = True
					return False
			# ---------

				token = self.scanToken()

				if self.expression(token,";", proc_scope):

					expType = self.arrayType("assigment")
					print expType, " in assignment_statement"

					if analyzer.current_token.getTokenValue() == ";":
						if self.assignTypeChecking(STlist[1], expType): # check type checking
		
							print "\nType checking okay"

							self.set_value_ST(var_token, proc_scope, True)
							try:
								if proc_scope:
									self.file.genStore(storeList, self.listGen, proc_scope, False) # true
								else:
									self.file.genStore(storeList, self.listGen, False, False)
							except:
								print "\nIt couldn't generate store instruction"
							self.listGen = []
							return True
						else:
							self.reportErrorMsg("Error: Unmatched Types!", token.line)
							self.errorFlag = True
							return False
					else:
						self.reportError(";", analyzer.current_token.getTokenValue(), analyzer.current_token.line)
						self.errorFlag = True
						return False
				else:
					#self.reportErrorMsg("Wrong Expression in assignment_statement", token.line)
					self.errorFlag = True
					return False
			else:
				self.reportError(":=", analyzer.current_token.getTokenValue(), token.line)
				self.errorFlag = True
				return False

		else:
			self.reportError("Identifier", token.getTokenType(), token.line)
			self.errorFlag = True
			return False

	# Verify array variables
	# Return True if size is int; Else return False
	def destination(self,token, scope): 
		print "\nDestination Function"
		if token.getTokenValue() == "[":
			token = self.scanToken()

			if self.expression(token,"]", scope):
				
				# --- Array Checking
				arrayType = self.arrayType("destination")

				if arrayType in ("integer", "int"):

					if analyzer.current_token.getTokenValue() == "]":
						token = self.scanToken()
						return True
				else:
					self.reportErrorMsg("Error: Invalid Array Size", token.line)
					self.errorFlag = True
					return False
				# -------

			else:
				self.reportErrorMsg("Invalid Expression", token.line)
				self.errorFlag = True
				return False

	# If proc_scope then procedure_call is within procedure
	# myList = [[global], name, [type var]
	def procedure_call(self, token, proc_scope = False):
		print "\nProcedure Call Function"
		exp_type = []
		callList  = []  # store function name, and it is passed to genCall()

		if not proc_scope or self.getRunTimeFunction(token.getTokenValue()):
			callList.append("global")

		if token.getTokenType() == "IDENTIFIER":
			callList.append(token.getTokenValue())

			STlist = self.lookatST(token, proc_scope)
			if STlist:
				if STlist[1] == "proc":   # var type

					token = self.scanToken()
					
					if token.getTokenValue() == "(":
						token = self.scanToken()

						if token.getTokenValue() != ")":
							if not self.expression(token,[",",")"], proc_scope):
								return False

							exp_type.append(self.arrayType("procedure_call"))

							callList = callList + self.listGen
							self.listGen = [] 

							while analyzer.current_token.getTokenValue() == ",":
								token = self.scanToken()	
								if not self.expression(token,[",",")"], proc_scope):
									return False

								exp_type.append(self.arrayType("procedure_call"))
								callList = callList + self.listGen
								self.listGen = [] 

						if analyzer.current_token.getTokenValue() == ")":
							token = self.scanToken()

							if token.getTokenValue() == ";":

							# --- Type checking Block		
								l1 = []
								l2 = []
	
								for p in exp_type:
									if p == "int":
										l1.append("integer")
									else:
										l1.append(p)

								for p in STlist[3]:
									if p == "int":
										l2.append("integer")
									else:
										l2.append(p)				

								if l1 == l2:  # parameter list
									print "parameter ok in procedure_call"

								else:
									self.reportErrorMsg("Error: Invalid Procedure Call", token.line)
									self.errorFlag = True
									return False

							# ---- end type checking

								try:
									self.file.genCall(callList)
								except:
									print "\nIt couldn't generate Call Function instruction"

								return True
							else:
								self.reportError(";", token.getTokenValue(), token.Prior.line)
								self.errorFlag = True
								return False
						else:
							self.reportErrorMsg("Missing ) of procedure_call", token.line)
							self.errorFlag = True
							return False
					else:
						self.reportErrorMsg("Missing ( of procedure_call", token.line)
						self.errorFlag = True
						return False
				else:
					self.reportErrorMsg("Invalid procedure name", token.line)
					self.errorFlag = True
					return False
			else:
				self.errorFlag = True
				return False
		else:
			self.reportError("Identifier", token.getTokenType(), token.line)
			self.errorFlag = True
			return False

	# If proc_scope then loop is within procedure
	def loop_statement(self,token, proc_scope = False):
		print "\nLoop Statement Function"
		#print "scope",proc_scope
		if token.getTokenValue() == "for":
			token = self.scanToken()

			if token.getTokenValue() == "(":
				token = self.scanToken()
				
				loop3 = ["integer","%"+str(token.getTokenValue())]

				self.assignment_statement(token, proc_scope)

				try:
					self.file.genLoop1()
				except:
					print "\nIt couldn't generate Loop instruction"
							
				if analyzer.current_token.getTokenValue() == ";":
					token = self.scanToken()

					if self.expression(token, ")", proc_scope):
						self.listGen = []  # 
						try:
							self.file.genLoop2()
						except:
							print "\nIt couldn't generate Loop instruction"

						# ---- Type checking

						expType = self.arrayType("loop")
						print expType, " in loop_statement"

						if expType != "bool":
							self.reportErrorMsg("Wrong Expression in loop statement", token.line)
							self.errorFlag = True
							return False
												
						# ---- end type checking

						if self.statement(token, False, proc_scope):
							try:
								self.file.genLoop3(loop3)
							except:
								print "\nIt couldn't generate Loop instruction"

							if analyzer.current_token.getTokenValue() == "end":
								token = self.scanToken()

								if token.getTokenValue() == "for":
									token = self.scanToken()

									if token.getTokenValue() == ";":
										return True
									else:
										print token.line
										self.reportError(";", token.getTokenValue(), token.Prior.line)
										self.errorFlag = True
										return False
								else:
									self.reportErrorMsg("Missing 'for' of 'End For", token.line-1)
									self.errorFlag = True
									return False
							else:
								self.reportError("end", token.getTokenValue(), token.line)
								self.errorFlag = True
								return False
						else:
							#self.reportErrorMsg("Wrong Statement ", token.line)
							self.errorFlag = True
							return False
					else:
						self.reportErrorMsg("Missing ) of LOOP", token.line)
						self.errorFlag = True
						return False
				else:
					self.reportError(";", analyzer.current_token.getTokenValue(), analyzer.current_token.line)
					self.errorFlag = True
					return False
			else:
				self.reportErrorMsg("Missing ( of LOOP", token.line)
				self.errorFlag = True
				return False
		else:
			self.reportError("for", token.getTokenValue(), token.line)
			self.errorFlag = True
			return False


	# If proc_scope then IF is within procedure
	def if_statement(self,token, proc_scope = False):
		print "\nIF Statement Function"
		#print "scope",proc_scope
		if token.getTokenValue() == "if":
			self.stack.push(token.getTokenValue())
			self.IFlag = True   					# accept else after expressions
			token = self.scanToken()

			if token.getTokenValue() == "(":
				token = self.scanToken()

				if self.expression(token, ")", proc_scope):
					token = self.scanToken()
					self.listGen = []  # after expression

					try:
						self.file.genIf()
					except:
						print "\nIt couldn't generate IF instruction"

					# ---- Type checking

					expType = self.arrayType("if")
					print expType, " in if_statement"

					if expType != "bool":

						self.reportErrorMsg("Wrong Expression in IF statement", token.line)
						self.errorFlag = True
						return False		
					# ---- end type checking

					if token.getTokenValue() == "then":

						if self.statement(token, True, proc_scope):
							if analyzer.current_token.getTokenValue() == "else": # IF with ELSE
								try:
									self.file.genElse()
								except:
									print "\nIt couldn't generate if-else instruction"

								if self.stack.peek() == "if":

									if not self.statement(token, True, proc_scope):  # execute at least once
										self.errorFlag = True
										return False

								else:
									self.reportErrorMsg("Error: IF statement must have at least one statement", token.line)
									self.errorFlag = True
									return False

							if not analyzer.current_token:
								self.reportErrorMsg("SyntaxError: Missing 'end if'", token.line+1)
								self.errorFlag = True
								return False

							if analyzer.current_token.getTokenValue() == "end": # IF without ELSE
								token = self.scanToken()

								if token.getTokenValue() == "if":
									self.stack.pop()
									token = self.scanToken()

									if token.getTokenValue() == ";":
										if token.Next.getTokenValue() == "end":  # If last Else
											self.IFlag = False
										try:
											self.file.genThen()
										except:
											print "\nIt couldn't generate if-then instruction"

										return True
									else:
										self.reportError(";", token.getTokenValue(), token.Prior.line)
										self.errorFlag = True
										return False
								else:
									self.reportError("if", token.getTokenValue(), token.line)
									self.errorFlag = True
									return False
							else:
								self.reportError("end", token.getTokenValue(), token.line)
								self.errorFlag = True
								return False
						else:
							#self.reportErrorMsg("Wrong Statement", token.line)
							self.errorFlag = True
							return False
					else:
						self.reportError("then", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False
				else:
					self.reportErrorMsg("Missing ) of IF statement", token.line)
					self.errorFlag = True
					return False
			else:
				self.reportErrorMsg("Missing ( of IF statement", token.line)
				self.errorFlag = True
				return False
		else:
			self.reportError("if", token.getTokenValue(), token.line)
			self.errorFlag = True
			return False

	# If proc_scope then Return is within procedure
	def return_statement(self, token, proc_scope = False):
		if token.getTokenValue() == "return":
			token = self.scanToken()

			if token.getTokenValue() == ";":
				return True
			else:
				self.reportError(";", token.getTokenValue(), token.Prior.line)
				self.errorFlag = True
				return False


	def reportError(self, expected, received, line):
	 	print  "\nSyntaxError: '"+expected+"' Expected"+", '"+received+"' Received, in line ", line,'\n'
	 	self.file.deleteFile()

	def reportWarning(self, message):
	 	print  "\nScanner Error: "+message+ ", in line", self.lineCount,'\n'

	def reportErrorMsg(self, message, line):
	 	print message,", in line ", line,'\n'
	 	self.file.deleteFile()

	def addSymbolTable(self, scope, name, Type, size, Value = None):
		
		if not self.symbolTable.has_key(scope):
			self.symbolTable[scope] = [[name,Type, size, Value]]
		else: # already exists
			self.symbolTable[scope].append([name,Type, size, Value])

	def printST(self):
		print "Simbol Table"
		for k in self.symbolTable.keys():
			print "\nScope:",k
			for i in range(len(self.symbolTable[k])):
				print i, self.symbolTable[k][i]


	# Call typeCheckingExp
	# Return type of expression
	# Return False if find unmacthed type
	def arrayType(self, statement_type):
		condList = []
		print "arrayType Function: statement type", statement_type, self.checkExp

		if len(self.checkExp) == 1:
			if statement_type == "if":
				if self.checkExp[0] == "bool":
					self.checkExp = []
					return "bool"
				else:
					self.checkExp = []
					return False

			elif statement_type == "loop":
				print "loop can't not be single exp"
				self.checkExp = []
				return False
		
		if len(self.checkExp) > 0:
			varType = self.checkExp[0]
		else:
			varType = False

		for i in range(0, len(self.checkExp)-1, 2):
			signal = self.checkExp[i+1]

			if self.relation_op(signal) or signal in ("&&","|"): 		 # if signal is relacional signal
				condList.append(varType)
				condList.append(signal)
				varType = self.checkExp[i+2]
			else:
				varType = self.typeChecking(varType, signal, self.checkExp[i+2]) # [type1, signal ,type2]

		if len(condList) > 0:
			condList.append(varType)
			print "cond List", condList
			varType = condList[0]
			for i in range(0, len(condList)-1, 2):
				varType = self.typeChecking(varType, condList[i+1], condList[i+2]) # [type1, signal ,type2]

		self.checkExp = []
		return varType

	def assignTypeChecking(self, type1, type2):

		print "Assignment Type Checking of", type1,type2

		if type1 in ("integer", "int") and type2 in ("integer", "int"):  
			return "integer"

		elif type1 == "float":
			if type2 in ("float","integer", "int"):
				return "float"

		elif type2 == "float":
			if type1 == "float":
				return "float"

		elif type1 == "bool":
			if type2 in ("bool", "int"):
				return "bool"

		elif type2 == type1 and type1 == "bool":
			return "bool"
		
		elif type1.lower() in ("string", "identifier"):
			if type2 in ("string", "identifier"):
				return "string"
		else:
			#print "Unmacthed types"
			return False

	def typeChecking(self, type1, signal, type2):
		
		print "\nType_checking of",type1,", and ",type2
		print "signal", signal

		if self.relation_op(signal):  					# If it is a relational signal

			if type1 in ("integer", "int") and type2 in ("integer", "int"):  
				return "bool"

			elif type1 == "float":
				if type2 in ("float","integer", "int"):
					return "bool"

			elif type2 == "float":
				if type1 in ("float","integer", "int"):
					return "bool"
			else:
				#print "Unmacthed types"
				return False

		elif signal in ("+","-","*","/"): 					# If it is a relational signal

			if type1 in ("integer", "int") and type2 in ("integer", "int"): 
				return "integer"

			elif type1 == "float":
				if type2 in ("float","integer", "int"):
					return "float"

			elif type2 == "float":
				if type1 in ("float","integer", "int"):
					return "float"
			else:
				#print "Unmacthed types"
				return False

		elif signal in ("&&", "|", "not"): 		

			if type1 in ("integer", "int") and type2 in ("integer", "int"):  
				return "integer"

			elif type1 in ("bool", "int") and type2 in ("bool", "int"):
				return "bool"

			else:
				#print "Unmacthed types"
				return False

		elif type1.lower() in ("string", "identifier"):
			if type2 in ("string", "identifier"):
				return "string"
		else:
			#print "Unmacthed types"
			return False

	# return True is var is Global
	def isGlobal(self, token): 

		if self.symbolTable.has_key("global"): 			# If ST has this Global scope
			for v in self.symbolTable["global"]:
				if v[0] == token.getTokenValue(): 	
					return True	
			return False
		else:
			return False

	# return list of var items if var in ST [name, type, size, value]
	# return False if undeclared var
	def lookatST(self, token, scope, declaration = False): 
		#print "lookatST FUNCTION"
		STlist = []
		if not scope:
			scope = "main"

		#print "scope", scope

		if self.symbolTable.has_key(scope):    			# If ST has this scope
			for v in self.symbolTable[scope]:
				if v[0] == token.getTokenValue():   	# var name
					STlist.append(v[0])  				# name
					STlist.append(v[1])  				# type
					STlist.append(v[2])	 				# size (if array)
					STlist.append(v[3])  				# value (if procedure)
					return STlist	

		# Search in global scope
		if self.symbolTable.has_key("global"): 			# If ST has this Global scope
			for v in self.symbolTable["global"]:
				if v[0] == token.getTokenValue(): 	# var name
					STlist.append(v[0])  			# name
					STlist.append(v[1])  			# type
					STlist.append(v[2])			    # size (if array)
					STlist.append(v[3])  			# value (if procedure)
					STlist.append("global scope")   # if global var
					return STlist		 # return 
		
		if not declaration:
			# Return False if not found var name
			self.reportErrorMsg("NameError: name '" + token.getTokenValue() + "' hasn't been defined", token.line)
			self.errorFlag = True
		return False

	# Assign True to the var if var in ST
	# Return false if not declared
	def set_value_ST(self, token, scope, value, declaration = False): 
		#print "set_value_ST FUNCTION"
		if not scope:
			scope = "main"

		#print "scope", scope

		if self.symbolTable.has_key(scope):    			# If ST has this scope
			for v in self.symbolTable[scope]:
				if v[0] == token.getTokenValue():   	# var name
					v[3] = value
					return True
		
		# Search in global scope
		if self.symbolTable.has_key("global"): 			# If ST has this Global scope
			for v in self.symbolTable["global"]:
				if v[0] == token.getTokenValue(): 		# var name
					v[3] = value
					return True				    		# return 
		
		if not declaration:
			# Return False if not found var name
			self.reportErrorMsg("NameError: name '" + token.getTokenValue() + "' is not defined", token.line)
			self.errorFlag = True
			
		return False

	def usage(self):
	    print "\nDescription:"
	    print "\nUsage1: input.src -a <Float> -t <Float>"
	    print "Usage2: filename.src -h"
	    print "Usage3: filename.src -f <fileName>"
	    print "-h = print this page"
	    print "\nOutput: filename.ll"

# ---- Main -----
#filename = raw_input('Type Filename:') 
dfa = DFA()
filename = "/Users/roses/Downloads/Repository/testCases/correct/test_heap.src"
generatedFile = filename[0:-3]+"ll"
  	
# If file already exists, then delete it
if os.path.exists(generatedFile):
	os.remove(generatedFile)

analyzer = Lexical_Analyzer(generatedFile)
analyzer.getTokenFromFile(filename)
analyzer.current_token = analyzer.tokenList.Next  

analyzer.program(analyzer.tokenList.Next)

print "\n",analyzer.printST()


