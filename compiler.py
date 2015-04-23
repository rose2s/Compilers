# Name:        scanner_Roselane.py
# Purpose:     Scanner 
# Author:      roses
# Created:     24/01/2015
# Copyright:   (c) roses 2014
#-------------------------------------------------------------------------------

import os,sys, getopt 
from automata import DFA
from List import List
from stack import Stack
from codeGen import CodeGen

class Compiler:

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
		self.lineCount = 0    								# Show the line of error
		self.errorFlag = False                        		# Flag for errors     
		self.IFlag = False      							# Flag for IF statement
		self.tokenList = List("KEYWORD","program",0)		# Token List
		self.tokenList.setFirst(self.tokenList)
		self.EXPstack = Stack()								# Stack used for expressions
		self.stack = Stack()								# Stack used for parser
		self.checkExp = []									# List for Type checking expressions
		self.listGen = []									# List passed to code genatation
		self.tupleList = []  								# List of tuples used for generate variable declarations
		self.file = CodeGen(generatedFile)					# Instance of Code Genetation Class
		self.errorFound = 0									# Holds number of erros found
		self.scannerError = 0

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

	# Gets path/filemane.src and return only filename
	def getFileName(self, filename):
		i = 0
		for i in range(len(filename)-1, 0, -1):
			pos = i
			if filename[i] in ("\'","/"):  
				break

		return filename[i+1:]


	# Gets token and Runs automata
	def getTokenFromFile(self,filename):
		
		self.file.writeToken("; ModuleID = '"+self.getFileName(filename)+"'\n")  # generates ModuleID												

		word = ""
		value = 0  											   # 0 = other, 1 = letter, 2 = number
		print "\n"

		with open(filename) as f:
			lines = f.readlines() 							   # Reads until EOF and returns a list of lines. 	
			for l in lines:									   # Loop each line
				self.lineCount += 1							   
				for s in range(len(l)):						   # Loop in each character
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
				  			if l[s] in (" ","\n","\t", "\r"):	# Skips whitespace, tab, newline
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

			  				elif l[s] in (" ","\n","\t","\r"):      # Skips whitespace, tab, newline
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
					  			if l[s] in (" ","\n","\t", "\r"):   # Skips whitespace, tab, newline
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
			  			if l[s] in (" ","\n","\t", "\r"):    		# Skips whitespace, tab, newline 
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
		
		if self.scannerError >0:									# If found error in scanner phase
			print "---------------------------------------------------\n"

	# Runs automata and sets tokens
	def run_automata(self,inp_program): 							# inp_program = word
		dfa.run_with_input_list(inp_program)   						# Runs automata
		if dfa.current_state in self.tokenType.keys():   			# If current_state in Accept States
			
			    token = self.tokenType[dfa.current_state]           # Sets token type

			    if token == "IDENTIFIER":
			        if inp_program in self.keywords:
			        	token = "KEYWORD"
				
			    self.tokenList.addNode(self.tokenList,token,inp_program,self.lineCount) # add token into Token List

		else:		
			self.scannerError = self.scannerError + 1				# Increment scanner error				
			self.reportWarning(inp_program)   						# If current_state NOT in Accept States
	

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
	# Return Expression Type (ExpType) if expression is correct
	def expression(self, current_token, sign, scope):     			# Returns True if token == sign	
		
		STlist = self.E(current_token, sign, scope)
		if STlist:								
			if self.EXPstack.isEmpty():								# Parentheses op are pushed into Expression Stack
				try:
					self.file.genExpression(self.listGen)
				except:
					print "\nIt couldn't generate expression instruction"

				return STlist
			else: 
				self.reportErrorMsg("Missing )", analyzer.current_token.line)
				self.errorFlag = True
				return False 

	def E(self, token, sign, scope):

		STlist = self.T(token,sign, scope)

		if self.E2(analyzer.current_token, sign, scope):
			
			if analyzer.current_token.getTokenValue() in ("&&","|"):
				self.listGen.append(analyzer.current_token.getTokenValue())    # add into list to generate expression
				self.checkExp.append(analyzer.current_token.getTokenValue())   # add into list to do type checking
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
				self.listGen.append(token.getTokenValue())  				# add (*|/) into list to generate expression
				self.checkExp.append(token.getTokenValue())					# add into list to do type checking
				token = self.scanToken()
				self.T(token,sign, scope)

				if self.E2(analyzer.current_token, sign, scope):
					return True

			elif token.getTokenValue() in ("&&","|"):
				return True

			elif token.getTokenValue() in sign:  				     # Stop Condition of Recursion
				return True
			else: 
				self.reportError("aritm_op", token.getTokenValue(),token.line)
				return False
		else:
			return False

	def T(self,token, sign, scope):
		STlist = self.F(token,sign, scope)
		
		if STlist:
			if self.T2(analyzer.current_token, sign, scope):
				return STlist
		else:
			return False


	def T2(self,token, sign, scope):

		if token.getTokenValue() in sign and self.EXPstack.isEmpty():   # Stop Condition of the Recursion
			return True

		elif token.getTokenValue() in ("&&","|"):
			return True

		while token.getTokenValue() == ")" and not self.EXPstack.isEmpty():
			if not self.EXPstack.isEmpty():
				self.EXPstack.pop()
				token = self.scanToken()
			else:
				self.reportError("(",")", token.line)
				self.errorFlag = True
				return False

		if token.getTokenValue() in self.first('T2'):

			# Check Division by zero
			if token.getTokenValue() == "/" and token.Next.getTokenValue() == '0':
				self.reportErrorMsg("Error: Division by Zero", token.line)
				self.errorFlag = True
				return False
			# ---------------------

			self.listGen.append(token.getTokenValue())  					# add into list to generate expression
			self.checkExp.append(token.getTokenValue())						# add into list to do type checking
			token = self.scanToken()

			if self.F(token, sign, scope):
				self.T2(analyzer.current_token, sign, scope)
			else:
				return False

	def F(self, token, sign, scope):

		ST = []
		minus = False        									   # Flag to minus sign
 		is_array = False     									   # Flag that checks whether var is array or not

		while token.getTokenValue() == "(":
			self.EXPstack.push(token.getTokenValue())   		    # push Parenthesis to stack
			token = self.scanToken()

		if token.getTokenValue() == "-": 						    # If minus
			token = self.scanToken()
			minus = True
										   							
		if token.getTokenType() == ("IDENTIFIER"):

			ST = self.lookatST(token, scope)  						  # STList = [name, type, size, value]

			if ST:
				if ST[3] == True or (self.isGlobal(token) and scope): #  If var has been initialized or is global
					
					if self.isGlobal(token):
						var = token.getTokenValue()
					else:
						var = token.getTokenValue()

					vtype = ST[1] 									  # type
					token = self.scanToken()						  # scan token
					
					loadList = [vtype, var]							  # Generate Load instruction <type, var>

					# ------ Block: Minus Type checking  --------------
					if minus:
						if ST[1].lower() not in ("integer", "int", "float"):
							self.reportErrorMsg("Minus [-] is not allowed with '"+ST[1]+"' type", analyzer.current_token.line)
							self.errorFlag = True
							return False

						elif token.getTokenValue() == "[":
							self.reportErrorMsg("Minus [-] is not allowed with array", analyzer.current_token.line)
							self.errorFlag = True
							return False
					# ----------- End Minus Block -----------------------

					# ----------- Block: Array checking -----------------

					if ST[2] > 0: 									    	# If var was declared as Array
						is_array = True

					if token.getTokenValue() == "[":   						# If identifier is a ARRAY

						
						if is_array:

							if not self.destination(token, scope):
								self.errorFlag = True
								return False
							else:
								self.listGen = self.listGen[:-2]     		# Remove (type, var) from listGen 
	
								self.checkExp.append(ST[1].lower())  	    # Add var type to checking list
								self.listGen.append(ST[1].lower()) 			# Add var type to generation list 
								self.listGen.append(var) 		   			# Add var name to generation list

								loadList.append(ST[2])           		    # Add size to load List
								loadList.append(token.Next.getTokenValue()) # Add array position to load list

								try:
									if scope != "main": 
										self.file.genLoad(loadList, scope)  # Function scope
									else:
										self.file.genLoad(loadList, False)  # Main scope
								except:
									print "\nIt couldn't generate Load instruction"

								return True 	
						
						else:
							self.reportErrorMsg("Error: Variable '"+ ST[0] +"' is not array type", analyzer.current_token.line)
							self.errorFlag = True
							return False
					# -------------- End Array block ------------------

					else:
						if is_array: 
							self.reportErrorMsg("Error: Variable '"+ ST[0] +"' is array type", analyzer.current_token.line)
							self.errorFlag = True
							return False
						else:	
							self.checkExp.append(ST[1].lower())  			# Add var type to checking list
							self.listGen.append(ST[1].lower()) 				# Add var type to generation list 
							self.listGen.append(var) 		 				# Add var name to generation list

							try:
								self.file.genLoad(loadList)                 # Generate Load instruction <type, var, size, pos>
							except:
								print "\nIt couldn't generate Load instruction"

							return True

				else: 
					self.reportErrorMsg("Error: Var '"+token.getTokenValue()+"' hasn't been initialized", analyzer.current_token.line)
					self.errorFlag = True
					return False
			else:
				self.errorFlag = True
				return False

		elif token.getTokenType() in ("INTEGER, FLOAT"):  
			expType = token.getTokenType() 

			if token.getTokenValue() in ("0","1"):   					# Boolean type checking
				self.checkExp.append("int")								# Add "int" to do type checking
				self.listGen.append("int") 								# Add "int" to generation list
				self.listGen.append(token.getTokenValue())  			# Add var to generation list
			else:
				self.checkExp.append(expType.lower())					# Add type to do type checking
				self.listGen.append(expType.lower()) 					# Add type to generation list
				self.listGen.append(token.getTokenValue())  			# Add var to generation list

			token = self.scanToken()									# Scan next token
			return True

		elif token.getTokenType() in ("STRING") and not minus:
			expType = token.getTokenType() 

			self.checkExp.append(expType.lower())						# Add type to do type checking
			self.listGen.append(expType.lower()) 						# Add type to do generation list
			self.listGen.append(token.getTokenValue())  				# Add var to generation list
			token = self.scanToken()									# Scan next token
			return True

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() in ("true","false") and not minus:
			expType = "bool"
			self.checkExp.append(expType.lower())    					# Add "bool" to do type checking
			self.listGen.append(expType.lower()) 						# Add "bool" to do generation list
			self.listGen.append(token.getTokenValue())  				# Add var to do generation list
			token = self.scanToken()									# Scan next token
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
	 		return True
	 	else:
	 		return False

	# Resets errorFlag, and Stack
	def reset(self):
		self.errorFlag = False
		while not self.stack.isEmpty():
			self.stack.pop()

	# If <name> is runTimeFUnction then return True otherwise return False
	def getRunTimeFunction(self, name):
		if name in ("getbool", "getinteger", "getstring", "getfloat", "putbool", "putinteger", "putstring", "putfloat"):
			return True
		else:
			return False

	# Increments number of errors found		
	def incrementErrorFound(self):
		self.errorFound = self.errorFound + 1;

	# Starts to scan the program
	def program(self,token):
		if self.program_header(token):
			self.reset()

			if self.program_body(analyzer.current_token):
				if analyzer.current_token.getTokenValue() == "end":
					token = self.scanToken()

					if token.getTokenValue() == "program":

						if self.errorFound == 0:
							print "\nSuccess!\n No error was found\n"
							
							try:
								self.file.genEnd()    							# Generate end of output
							except:
								print "\nIt couldn't generate End instruction"
							return True

						elif self.errorFound == 1:
							print "\n"+str(self.errorFound)+" error was found"
							self.file.deleteFile()       						# Delete output genereted
						else:
							print "\n"+str(self.errorFound)+" errors were found"
							self.file.deleteFile()                              # Delete output genereted

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
						self.stack.push(token.getTokenValue())  					 # Push <program>
						self.program_header(self.scanToken())
					else:
						self.reportError("program", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False

				if self.stack.peek() == "program":

					if token.getTokenType() == "IDENTIFIER":	
						self.stack.push(token.getTokenType())						 # Push program name
						self.program_header(self.scanToken())
					else:
						self.reportError("IDENTIFIER", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False

				if self.stack.peek() ==  "IDENTIFIER":

					if token.getTokenValue() == "is":
						self.stack.push(token.getTokenValue())                        # Push <is>
						self.program_header(self.scanToken())
					else:
						self.reportError("is", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False

				if self.stack.peek() == "is":     									   # If top is <is>
					return True
		else:
			return False

	def program_body(self,token):

		# Add all RunTimeFunctions to Symbol Table --> [scope, name, procedure, in|out, return type]
		self.addSymbolTable("global", "getbool", "proc", "out", ["bool"])  
		self.addSymbolTable("global", "getinteger", "proc", "out", ["integer"])
		self.addSymbolTable("global", "getstring", "proc", "out", ["string"])
		self.addSymbolTable("global", "getfloat", "proc", "out", ["float"])
		self.addSymbolTable("global", "putbool", "proc", "in", ["bool"])
		self.addSymbolTable("global", "putinteger", "proc", "in", ["integer"])
		self.addSymbolTable("global", "putstring", "proc", "in", ["string"])
		self.addSymbolTable("global", "putfloat", "proc", "in", ["float"])

		if not self.errorFlag:
			if self.declaration(token):
				self.file.skipLine()

				try:
					self.file.genFunction(["global","main"])  		# Generate Main function
					for l in self.tupleList:				  		
						self.file.genDeclaration(l)					# Generate all variable declarations

					self.file.skipLine()                            # Generate skipLine
				except:
					print "\nIt couldn't generate Variable Declaration Instruction"

				self.tupleList = []
				if self.statement(analyzer.current_token):
					return True
				else:
					self.errorFlag = True
					return False
			else: 
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
		self.errorFlag = False

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
					self.incrementErrorFound()									# Increment error found
					if self.resync_declaration_token(analyzer.current_token):   # Recover point to Declaration Function
						if self.declaration(analyzer.current_token): 
							return True
						else:
							return False
					else:
						return False

			else:
				self.incrementErrorFound()										# Increment error found
				if self.resync_declaration_token(analyzer.current_token):   	# Recover point to Declaration Function
					if self.declaration(analyzer.current_token): 
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
					self.incrementErrorFound()  								# Doesn't recover point for procedure erros
					return False
			else:
				self.incrementErrorFound()      								# Doesn't recover point for procedure erros
				return False

		elif token.getTokenValue() == "begin":  								# Stop condition
			return True

		elif token.getTokenValue() == "int":
			self.reportError("integer", token.getTokenValue(), token.line)
			self.incrementErrorFound()											# Increment error found
			if self.resync_declaration_token(analyzer.current_token):    		# Recover point to Declaration Function
				if self.declaration(analyzer.current_token): 
					return True
				else:
					return False
			else:
				return False

		else: 
			self.reportErrorMsg("SyntaxError: Invalid Syntax in Declaration", token.line)
			self.incrementErrorFound()											# Increment error found
			if self.resync_declaration_token(analyzer.current_token):   		# Recover point to Declaration Function
				if self.declaration(analyzer.current_token): 
					return True
				else:
					return False
			else:
				return False

	# If Parameter then it is parameter declaration
	def variable_declaration(self, token, scope = "main", parameterList = False): 

		size = 0   														# Hold array size
		tup = []   														# List of variable declaration

		if scope == "global":	
			self.listGen.append("global")                               # Add scope to generation list
			if scope == "main":
				tup.append(scope)										# If main scope then add to tup list
	
		if self.type_mark(token.getTokenValue()):  						# If token in type_mark
			Type = token.getTokenValue()								# Temp. var to symbol table
			
			token = self.scanToken()									# Scan next token

			if token.getTokenType() == "IDENTIFIER":
				name = token.getTokenValue()							# Temp. var to symbol table
				self.listGen.append(Type)								# Add type to generation list
				self.listGen.append(name)								# Add name to generation list

				if scope == "main":										# If main scope, add it to tup list
					tup.append(Type)
					tup.append(name)
				
				# ------- Block: Redeclaration checking --------
				STlist = self.lookatST(token, scope, True)
				if STlist:
					self.reportErrorMsg("Error: redeclaration of '" + name + "'" , token.line)
					return False
				# ------ End redeclaration block ---------------

				token = self.scanToken()          						# Scan next token
				
				if token.getTokenValue() == ";" and not parameterList:	# Var is NOT array and NOT var parameter
					token = self.scanToken()
					self.addSymbolTable(scope, name, Type, size)		# Add var to symbol table

					if scope != "main":
						try:
							self.file.genDeclaration(self.listGen)      # Generate Declaration instruction
						except:
							print "\nIt couldn't generate Variable Declaration instruction"

					elif len(tup) > 0:
						self.tupleList.append(tup)
					self.listGen = []
					return True
				
				elif parameterList and token.getTokenValue() != "[": 		# Var is not array, but is var parameter
					if token.getTokenValue() in ("in","out"):
						self.listGen.append(token.getTokenValue())      	# Add in|out to generation list
						token = self.scanToken()
						self.addSymbolTable(scope, name, Type, size, True)  # Add var into symbol table
						
						return True
					else:
						self.reportError("in/out", token.getTokenValue(),token.line)
						return False

				elif token.getTokenValue() == "[":                      	# Array Variables
					token = self.scanToken()

					if token.getTokenType().lower() in ("int", "integer", "float"):
						size = token.getTokenValue()
						token = self.scanToken()

						self.listGen.append(size)                     	 	# Add size into generation list
						if scope == "main":
							tup.append(size)						   		# If main scope then add size to tup 

						if token.getTokenValue() == "]":
							token = self.scanToken()
 
							if token.getTokenValue() == ";" and not parameterList: # var is array and NOT var parameter
								token = self.scanToken()
								self.addSymbolTable(scope, name, Type, size)       # Add var into symbol table
								
								if scope != "main":
									try:
										self.file.genDeclaration(self.listGen)     # Generate Declaration Instruction
									except:
										print "\nIt couldn't generate Variable Declaration instruction"
					
								elif len(tup) > 0:
									self.tupleList.append(tup)

								self.listGen = []
								return True

							elif parameterList: 										# Var is array and is var parameter
								if token.getTokenValue() in ("in","out"):
									self.listGen.append(token.getTokenValue())      	# Add in|out to generation list
									token = self.scanToken()

									self.addSymbolTable(scope, name, Type, size, True)  # Add array var into symbol table
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
					self.reportError(";",token.getTokenValue(), token.Prior.line)
					return False

			else: 
				self.reportError("Identifier Type", token.getTokenType(),token.line)
				return False

		else: 
			self.reportError("Type Mark", token.getTokenType(),token.line)
			return False


	# myList = [global,name,[global, type, name in|out]]
	def procedure_declaration(self, token, scope = "main"):
		
		if scope in ("global", "main"):
			self.listGen.append("global")

		new_scope = token.Next.getTokenValue()  					# Procedure Name
		self.listGen.append(new_scope)								# Add procedure name to gen. list

		parList = self.procedure_header(token)
		if parList:

			#----- Block: Redeclaration of procedures checking
			STlist = self.lookatST(token.Next, scope, True)
			if STlist:
				self.reportErrorMsg("Error: redeclaration of Procedure '" + token.Next.getTokenValue() + "'" , token.line)
				self.errorFlag = True
				return False
			# ---- End block ---------------------------------

			if parList == True:      								# If procedure has no parameter then value = []
				parList = []


			self.addSymbolTable(scope, token.Next.getTokenValue(), "proc", 0, parList)  # Add procedure and his scope into to ST

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
		parList = []                                   				# parameter list

		if token.getTokenValue() == "procedure":
			token = self.scanToken()

			if token.getTokenType() == "IDENTIFIER":
				scope = token.getTokenValue()  			 
				token = self.scanToken()	

				if token.getTokenValue() == "(":
					token = self.scanToken()

					if self.type_mark(token.getTokenValue()):

						parList.append(token.getTokenValue()) 		# Add type to parameter list
						self.variable_declaration(token, scope, True)
					
						while analyzer.current_token.getTokenValue() == ",":
							token = self.scanToken()
							parList.append(token.getTokenValue())  # Add type to parameter list
							self.variable_declaration(analyzer.current_token, scope, True)

						if analyzer.current_token.getTokenValue() == ")":
							token = self.scanToken()

							try:
								self.file.genFunction(self.listGen)   # Generate Function
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

						try:
							self.file.genFunction(self.listGen)      # Generate Function
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
		if not self.errorFlag:
			if not self.declaration(token, scope):
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
						token = self.scanToken()
						return True

					else:
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
	def statement(self, token, if_stat = False, proc_scope = False): 
		prior = token  											# hold previous line
		token = self.scanToken()
		self.errorFlag = False
		self.checkExp = []

		if not token:
			self.reportErrorMsg("SyntaxError: Missing 'end program'",prior.line+1)
			return False

		if not if_stat:  										# if_stat: then should execute at least one statement
			if token.getTokenValue() == "end":
				return True

			if self.IFlag:										
				if token.getTokenValue() == "else" and self.stack.size() > 0:		
					return True

		if token.Next:										  				# Go to assignment statement
			if token.Next.getTokenValue() in (":=","["):
				if self.assignment_statement(token, proc_scope):
					if self.statement(analyzer.current_token, False, proc_scope):
						return True
					else:
						return False
				else: 
					self.incrementErrorFound()
					self.resync_statement_token(analyzer.current_token, ";") # Recover point to statement
					if self.statement(analyzer.current_token, False, proc_scope):
						return True
					else:
						return False

			elif token.getTokenType() == "IDENTIFIER" and token.Next.getTokenValue() == "(":
				if self.procedure_call(token, proc_scope):      			# Go to procedure Call statement

					if self.statement(analyzer.current_token, False, proc_scope):
						return True
					else:
						return False
				else:
					self.incrementErrorFound()
					self.resync_statement_token(analyzer.current_token, ";") # Recover point to statement
					if self.statement(analyzer.current_token, False, proc_scope):
						return True
					else:
						return False

		if token.getTokenValue() == "return":
			if self.return_statement(token, proc_scope):  					# Go ro return statement

				if self.statement(analyzer.current_token, False, proc_scope):
					return True
				else:
					return False
			else:
				self.incrementErrorFound()
				self.resync_statement_token(analyzer.current_token, ";")  	# Recover point to statement
				if self.statement(analyzer.current_token, False, proc_scope):
					return True
				else:
					return False

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() == "for":

			if self.loop_statement(token, proc_scope):						# Go to Loop statement
				
				if self.statement(analyzer.current_token, False, proc_scope):
					return True
				else:
					return False
			else:
				self.incrementErrorFound()
				if self.resync_end_token(analyzer.current_token, "for"):  	# Recover point to statement
					if self.statement(analyzer.current_token, False, proc_scope):
						return True
					else:
						return False
				else:
					return False

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() == "if":

			if self.if_statement(token, proc_scope):						# Go to If statement
			
				if self.statement(analyzer.current_token, False, proc_scope):
					return True
				else:
					return False
			else:
				self.incrementErrorFound()
				if self.resync_end_token(analyzer.current_token, "if"):  # Recover point to statement
					if self.statement(analyzer.current_token, False, proc_scope):
						return True
					else:
						return False
				else:
					return False

		elif if_stat:
			self.reportErrorMsg("Error: IF must have at least one statement", token.line)
			return False

		else:
			self.reportErrorMsg("SyntaxError: Invalid syntax in Statement ",token.line)
			return False

	# If proc_scope then it is assigment within procedure
	# listgGen = [[global], type, name, value]
	def assignment_statement(self, token, proc_scope = False):
		if token.getTokenType() == "IDENTIFIER":

			var_token = token  										    # Temp procedure name
			array_var = False  											# Flag that checks whether var is array or not

			# --- Block: Declaration Check ------
			STlist = self.lookatST(token, proc_scope)  					# Verify if var within ST
		
			if not STlist:												# Error: Undeclared var
				return False
			# --------- end block  --------------

			if self.isGlobal(var_token):
				self.listGen.append("global")
			
			storeList = [STlist[1], var_token.getTokenValue()]         # type, var

			# --- Block: Array checking ---------
			if STlist[2] > 0 : 											# If var was declared as array
				storeList.append(STlist[2]) 							# Save size of array
				array_var = True

			token = self.scanToken()

			if token.getTokenValue() == "[":  							# If array
				if array_var:
					storeList.append(token.Next.getTokenValue())  		# Save position of array

					if not self.destination(token, proc_scope):		  	# True if size is integer type
						self.errorFlag = True
						return False
					
					self.listGen = []    								# Clean sentence after verify expression of array
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
			# -------- end array block -----------

				token = self.scanToken()

				if self.expression(token,";", proc_scope):

					expType = self.arrayType("assigment")                	# return type of expression

					if analyzer.current_token.getTokenValue() == ";":
						if self.assignTypeChecking(STlist[1], expType):  	# Assignment type checking
							self.set_value_ST(var_token, proc_scope, True)  # Add value into st

							try:
								if proc_scope:
									self.file.genStore(storeList, self.listGen, proc_scope, False) 
								else:
									self.file.genStore(storeList, self.listGen, False, False)
							except:
								print "\nIt couldn't generate store instruction"

							self.listGen = []
							return True
						else:
							self.reportErrorMsg("TypeError: Unmatched Types!", token.line)
							self.errorFlag = True
							return False
					else:
						self.reportError(";", analyzer.current_token.getTokenValue(), analyzer.current_token.line)
						self.errorFlag = True
						return False
				else:
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
	# Return True if size is int otherwise return False
	def destination(self,token, scope): 
		if token.getTokenValue() == "[":
			token = self.scanToken()
			temp  = self.checkExp
			self.checkExp = []    

			if self.expression(token,"]", scope):

				arrayType = self.arrayType("destination")

				if arrayType in ("integer", "int"):

					if analyzer.current_token.getTokenValue() == "]":
						token = self.scanToken()
						self.checkExp = temp
						return True
				else:
					self.reportErrorMsg("Error: Invalid Array Size", token.line)
					self.errorFlag = True
					return False
			else:
				self.reportErrorMsg("Invalid Expression", token.line)
				self.errorFlag = True
				return False

	# If proc_scope then procedure_call is within procedure
	# myList = [[global], name, [type var]
	def procedure_call(self, token, proc_scope = False):
		exp_type = []										# 
		callList  = []  									# store function name, and it is passed to genCall()

		if not proc_scope or self.getRunTimeFunction(token.getTokenValue()):
			callList.append("global")

		if token.getTokenType() == "IDENTIFIER":
			callList.append(token.getTokenValue()) 			# Add function name to call list

			STlist = self.lookatST(token, proc_scope)		# Info about var from ST
			if STlist:
				if STlist[1] == "proc":   					# var type == proc then it is a procedure call
					token = self.scanToken()
					
					if token.getTokenValue() == "(":
						token = self.scanToken()

						if token.getTokenValue() != ")":
							if not self.expression(token,[",",")"], proc_scope):
								return False

							if len(self.checkExp) == 1 and self.isNumber(self.listGen[1]):  # literal
								exp_type.append(self.arrayType("procedure_call"))
								callList.append(exp_type[-1])               				# type of literal
								callList.append(self.listGen[1]) 							# literal
							
							else:															# var
								exp_type.append(self.arrayType("procedure_call"))
								callList.append(exp_type[-1])               				# type of expression
								callList.append("%"+str(self.file.temp-1)) 					# temp that holds the expression
							
							self.listGen = [] 

							while analyzer.current_token.getTokenValue() == ",":
								token = self.scanToken()	
								if not self.expression(token,[",",")"], proc_scope):
									return False

								if len(self.checkExp) == 1 and self.isNumber(self.listGen[1]):  # doesn't need a temp
									exp_type.append(self.arrayType("procedure_call"))
									callList.append(exp_type[-1])               				# type of literal
									callList.append(self.listGen[1]) 							# literal
								else:
									exp_type.append(self.arrayType("procedure_call")) 			# needs a temp
									callList.append(exp_type[-1])               				# type of expression
									callList.append("%"+str(self.file.temp-1)) 					# temp that holds the expression
								
								self.listGen = []
 
						if analyzer.current_token.getTokenValue() == ")":
							token = self.scanToken()

							if token.getTokenValue() == ";":

							# --- Block: Type checking ---------	
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

								if l1 != l2:  												# parameter list
									self.reportErrorMsg("Error: Invalid Procedure Call", token.line)
									self.errorFlag = True
									return False

							# ---- end type checking -----------

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
		if token.getTokenValue() == "for":
			token = self.scanToken()

			if token.getTokenValue() == "(":
				token = self.scanToken()
				
				loop3 = ["integer","%"+str(token.getTokenValue())]   # Generate loop instruction

				self.assignment_statement(token, proc_scope)

				try:
					self.file.genLoop1()                        	 # Generate loop instruction part1
				except:
					print "\nIt couldn't generate Loop instruction"
							
				if analyzer.current_token.getTokenValue() == ";":
					token = self.scanToken()

					if self.expression(token, ")", proc_scope):
						self.listGen = []  
						try:
							self.file.genLoop2()   					# Generate loop instruction part2
						except:
							print "\nIt couldn't generate Loop instruction"

						# ---- Block: Type checking -----------------

						expType = self.arrayType("loop")

						if expType != "bool":
							self.reportErrorMsg("Wrong Expression in loop statement", token.line)
							self.errorFlag = True
							return False
												
						# ---- end type checking

						if self.statement(token, False, proc_scope):
							try:
								self.file.genLoop3(loop3)    		# Generate loop instruction part3
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
		if token.getTokenValue() == "if":
			self.stack.push(token.getTokenValue())
			self.IFlag = True   							# accept else after expressions
			token = self.scanToken()

			if token.getTokenValue() == "(":
				token = self.scanToken()

				if self.expression(token, ")", proc_scope):
					token = self.scanToken()
					self.listGen = []  						# Clean list after expression

					try:
						self.file.genIf()                   # Generate If instruction 
					except:
						print "\nIt couldn't generate IF instruction"

					# ---- Block: Type checking --------
					expType = self.arrayType("if")
					if expType != "bool":

						self.reportErrorMsg("Wrong Expression in IF statement", token.line)
						self.errorFlag = True
						return False		
					# ---- end type checking ---------

					if token.getTokenValue() == "then":

						if self.statement(token, True, proc_scope):
							if analyzer.current_token.getTokenValue() == "else": 	# IF with ELSE
								try:
									self.file.genElse()       						# Generate Else instruction instruction
								except:
									print "\nIt couldn't generate if-else instruction"

								if self.stack.peek() == "if":

									if not self.statement(token, True, proc_scope):  # Execute at least once
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

							if analyzer.current_token.getTokenValue() == "end": 	# IF without ELSE
								token = self.scanToken()

								if token.getTokenValue() == "if":
									self.stack.pop()
									token = self.scanToken()

									if token.getTokenValue() == ";":
										if token.Next.getTokenValue() == "end":  	# If it is last Else
											self.IFlag = False
										try:
											self.file.genThen()                     # Generate IfFalse instruction
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
							self.errorFlag = True
							return False
					else:
						self.reportError("then", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False
				else:
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
	 	print  "SyntaxError: '"+expected+"' Expected"+", '"+received+"' Received, in line ", line,'\n'
	 	self.file.deleteFile() 

	def reportWarning(self, message):
	 	print  "Scanner Error: "+message+ ", in line", self.lineCount,'\n'

	def reportErrorMsg(self, message, line):
	 	print message,", in line ", line,'\n'
	 	self.file.deleteFile()

	def addSymbolTable(self, scope, name, Type, size, Value = None):
		
		if not self.symbolTable.has_key(scope):
			self.symbolTable[scope] = [[name,Type, size, Value]]
		else: 														# var already exists
			self.symbolTable[scope].append([name,Type, size, Value])

	def printST(self):
		print "***** Simbol Table ******"
		for k in self.symbolTable.keys():
			print "\nScope:",k
			for i in range(len(self.symbolTable[k])):
				print i, self.symbolTable[k][i]

	# Call typeCheckingExp function, Return type of expression or return False if unmacthed type
	def arrayType(self, statement_type):
		condList = []

		if len(self.checkExp) == 1:
			if statement_type == "if":
				if self.checkExp[0] == "bool":
					self.checkExp = []
					return "bool"
				else:
					self.checkExp = []
					return False

			elif statement_type == "loop":
				print "TypeError: Loop can't not be single expression"
				self.checkExp = []
				return False
		
		if len(self.checkExp) > 0:
			varType = self.checkExp[0]
		else:
			varType = False

		for i in range(0, len(self.checkExp)-1, 2):
			signal = self.checkExp[i+1]

			if self.relation_op(signal) or signal in ("&&","|"): 		 		# if signal is relacional signal
				condList.append(varType)
				condList.append(signal)
				varType = self.checkExp[i+2]
			else:
				varType = self.typeChecking(varType, signal, self.checkExp[i+2]) # [type1, signal ,type2]

		if len(condList) > 0:
			condList.append(varType)
			varType = condList[0]
			for i in range(0, len(condList)-1, 2):
				varType = self.typeChecking(varType, condList[i+1], condList[i+2]) # [type1, signal ,type2]

		self.checkExp = []
		return varType

	def assignTypeChecking(self, type1, type2):

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
			return False

	def typeChecking(self, type1, signal, type2):
		if self.relation_op(signal):  						# If it is a relational signal

			if type1 in ("integer", "int") and type2 in ("integer", "int"):  
				return "bool"

			elif type1 == "float":
				if type2 in ("float","integer", "int"):
					return "bool"

			elif type2 == "float":
				if type1 in ("float","integer", "int"):
					return "bool"
			else:
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
				return False

		elif signal in ("&&", "|", "not"): 		

			if type1 in ("integer", "int") and type2 in ("integer", "int"):  
				return "integer"

			elif type1 in ("bool", "int") and type2 in ("bool", "int"):
				return "bool"

			else:
				return False

		elif type1.lower() in ("string", "identifier"):
			if type2 in ("string", "identifier"):
				return "string"
		else:
			return False

	# return True is Global var
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
		STlist = []
		if not scope:
			scope = "main"

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
				if v[0] == token.getTokenValue(): 		# var name
					STlist.append(v[0])  				# name
					STlist.append(v[1])  				# type
					STlist.append(v[2])			    	# size (if array)
					STlist.append(v[3])  				# value (if procedure)
					STlist.append("global scope")   	# if global var
					return STlist		 				# return 
		
		if not declaration:
			# Return False if not found var name
			self.reportErrorMsg("NameError: name '" + token.getTokenValue() + "' hasn't been defined", token.line)
			self.errorFlag = True
		return False

	# Assign True to the var if var in ST
	# Return false if not declared
	def set_value_ST(self, token, scope, value, declaration = False): 
		if not scope:
			scope = "main"

		if self.symbolTable.has_key(scope):    			# If ST has this scope
			for v in self.symbolTable[scope]:
				if v[0] == token.getTokenValue():   	# var name
					v[3] = value 						# new value
					return True
		
		# Search in global scope
		if self.symbolTable.has_key("global"): 			# If ST has this Global scope
			for v in self.symbolTable["global"]:
				if v[0] == token.getTokenValue(): 		# var name
					v[3] = value 						# new value
					return True				    		# return 
		
		if not declaration:
			# Return False if not found var name
			self.reportErrorMsg("NameError: name '" + token.getTokenValue() + "' is not defined", token.line)
			self.errorFlag = True
			
		return False

	# Moves the current token to next declaration
	def resync_declaration_token(self, token):
		while token.getTokenValue() not in (";", "begin") and token.Next != None:
			token = self.scanToken()

		if token.Next and token.getTokenValue() != "begin":
			token = self.scanToken()
		
		if not token.Next:   					# if last token
			return False

		return True

	# Moves the current token to next statement
	def resync_statement_token(self, token, signal):
		while token.getTokenValue() != signal:
			token = self.scanToken()

	# Moves the current token to next if/for statement
	def resync_end_token(self, token, signal):
		while token.getTokenValue() != "end":
			token = self.scanToken()

		token = self.scanToken()  
		if token.getTokenValue() == signal:
			token = self.scanToken() # ;
			return token
		else:
			return False 

# -------------------------------- Main Block ------------------------------------
if __name__ == '__main__':
	#filename = "/Users/roses/Downloads/Repository/testCases/correct/test2.src"

	try:
	    opts, args = getopt.getopt(sys.argv[1:],'i:hst', ['input=', 'help', 'st', 'token'])
	except getopt.GetoptError as err:
		print str(err)
		sys.exit()

	filename = False

	for opt, arg in opts:  								  		# Save values in variables
		if opt in ('-i', '--input'):

			dfa = DFA()									 		# new instance of automata
			filename = arg
			generatedFile = filename[0:-3]+"ll"		  	  		# output file.ll
	  	
			if os.path.exists(generatedFile):  			  		# If file already exists, then delete it
				os.remove(generatedFile)

			analyzer = Compiler(generatedFile)     		  		# new instance of compiler class

			try: 
				with open(filename) as f:
					pass
		
				analyzer.getTokenFromFile(filename) 	  		# Execute scanner phase
				analyzer.current_token = analyzer.tokenList.Next  

				analyzer.program(analyzer.tokenList.Next) 		# Execute parser phase

			except IOError as e:						  		# Didn't find the file
				print "I/O error({0}): {1}".format(e.errno, e.strerror), filename 

		elif opt in ('-h', '--help'):							# Options from command line
			print "\nDescription:"
			print "\nUsage1: compiler.py < -i | --input > input.src "
			print "Usage2: compiler.py < -h | --help >"
			print "Usage3: compiler.py < -i | --input > input.src < -s | -- st >"
			print "\nOutput: input.ll"
			sys.exit()

		if opt in ('-s', '--st'):
			if filename:
				print "\n", analyzer.printST()
			else:
				print "Usage: compiler.py -i input.src -st"

		elif opt in ('-t', '--token'):
			if filename:
				analyzer.tokenList.printList(analyzer.tokenList)
			else:
				print "Usage: compiler.py -i input.src -token"
	   
	   