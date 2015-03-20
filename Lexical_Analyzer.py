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
#-------------------------------------------------------------------------------

import os,sys
from automata import DFA
from List import List
from stack import Stack

class Lexical_Analyzer:

	# Token types used for automata
	tokenType = {'s1': "IDENTIFIER",'s2': "INTEGER", 's3': "FLOAT",'s6': "COMP_OP",'s7': "COMP_OP_EQ",
				 's8': "ARIT_OP",'s10': "LEFT_PAR",'s11': "RIG_PAR",'s12': "LEFT_CH", 's13': "RIG_CH",
				 's14': "COMMA",'s15': "SC",'s16': "LEFT_BRA", 's17': "RIG_BRA",'s18': "STRING"}

	keywords  = ["string", "case", "integer", "bool", "float", "for", "and", "or", "global", "not", "in", "program", "out", "procedure",
                          "if", "begin", "then", "return", "else", "end", "EOF", "true","false"]

	symbolTable = {}

	# LL(1) grammar
	terminals = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y',
					  '0','1','2','3','4','5','6','7','8','9',
					   "+", "-", "*", "/", "(", ")", "<", ">", "{", "}", ";"]
	startSimbol = 'E'
	non_terminals = ['E','E2','T','T2','F']
	current_token = None

	def __init__(self):
		self.lineCount = 0    								# Show the error
		self.IDtokenNum = 0   								# ID for Symbol table
		self.errorFlag = False                        		# Flag for errors     
		self.IFlag = False      							# Flag for IF statement
		self.tokenList = List("KEYWORD","program",0)		# Token List
		self.tokenList.setFirst(self.tokenList)
		self.EXPstack = Stack()								# Stack used for expressions
		self.stack = Stack()								# Stack used for parser
		self.checkExp = []									# List for Typing check expressions

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

	# Gets token and Runs automata
	def getTokenFromFile(self,filename):
		
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

		dfa.run_with_input_list(inp_program)   						# Runs automata

		if dfa.current_state in self.tokenType.keys():   			# If current_state in Accept States
			
			    token = self.tokenType[dfa.current_state]           # Sets token type

			    if token == "IDENTIFIER":
			        if inp_program in self.keywords:
			        	token = "KEYWORD"
				
			    print inp_program + " is " + token
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
		#print STlist[1], " in Expression"
		if STlist:								

			if self.EXPstack.isEmpty():								# Parenthesis op are pushed into Expression Stack
				return STlist
			else: 
				self.reportWarning("Missing )")
				self.errorFlag = True
				return False 

	def E(self, token, sign, scope):
		print "E: ",token.getTokenValue()
		STlist = self.T(token,sign, scope)
		#print STlist[1], " in E"

		if self.E2(analyzer.current_token, sign, scope):
			print "ST", self.checkExp
			return True

	def E2(self,token, sign, scope):
		if not self.errorFlag:
			#print "E2: ",token.getTokenValue()

			if (token.getTokenValue() in self.first('E2')) or (self.relation_op(token.getTokenValue())):
				self.checkExp.append(token.getTokenValue())
				token = self.scanToken()
				self.T(token,sign, scope)

				if self.E2(analyzer.current_token, sign, scope):
					return True

			elif token.getTokenValue() in sign:  				     # Stop Condition of the Recursion
				#print "sign", sign
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
			#print STlist[1], " in T"
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

		elif token.getTokenValue() == ")":
			if not self.EXPstack.isEmpty():
				self.EXPstack.pop()
				token = self.scanToken()
			else:
				self.reportError(") ","(", token.line)
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
			self.checkExp.append(token.getTokenValue())
			token = self.scanToken()

			if self.F(token, sign, scope):
				self.T2(analyzer.current_token, sign, scope)
			else:
				return False

	def F(self,token, sign, scope):
		print "F: ",token.getTokenValue()
		print token.getTokenType()

		if token.getTokenValue() == "(":
			self.EXPstack.push(token.getTokenValue())   		   # push Parenthesis
			print "stack: ",self.EXPstack.peek()
			token = self.scanToken()
			self.E(token,sign)

		elif token.getTokenType() == ("IDENTIFIER"):
			STlist = self.lookatST(token, scope)
			if STlist:
				token = self.scanToken()
				if token.getTokenValue() == "[":                	   # If array
					if self.destination(token, scope):
						return STlist 							 
					else:
						self.reportErrorMsg("Error in destination", analyzer.current_token.line)
						self.errorFlag = True
						return False
				else:
					self.checkExp.append(STlist[1].lower())  			# var type
					return True
			else:
				return False

		elif token.getTokenType() in ("INTEGER, FLOAT"):  
			expType = token.getTokenType() 
			print expType, " in F"
			token = self.scanToken()
			self.checkExp.append(expType.lower())
			return True

		elif token.getTokenType() in ("STRING"):
			expType = token.getTokenType() 
			print expType, " in F"
			token = self.scanToken()
			self.checkExp.append(expType.lower())
			return True

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() in ("true","false"):
			expType = "bool"
			print expType, " in F"
			token = self.scanToken()
			self.checkExp.append(expType.lower())
			return True

		else:
			print "Error: ID not found"
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

	# Starts to scan the program
	def program(self,token):
		if self.program_header(token):
			self.reset()
			self.program_body(analyzer.current_token)

	def program_header(self,token):
		print "\nProgram_header Function"
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
		if not self.errorFlag:
			if self.declaration(token):
				print "\nStart Main Program!"

				if self.statement(analyzer.current_token):

					if analyzer.current_token.getTokenValue() == "end":
						token = self.scanToken()

						if token.getTokenValue() == "program":
							print "\nCORRECT PROGRAM"
							return True
				else:
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

			else: 
				self.reportErrorMsg("Unexpected type in Declaration",token.line)
				self.errorFlag = True
				return False
		else:
			return False

	# If Parameter then it is parameter declaration
	def variable_declaration(self, token, scope = "main", parameterList = False): 

		size = 0
		print "Variable_declaration Funtion:",token.getTokenValue()

		if self.type_mark(token.getTokenValue()):  						# if token in type_mark
			Type = token.getTokenValue()								# temp var to symbol table
			token = self.scanToken()

			if token.getTokenType() == "IDENTIFIER":
				name = token.getTokenValue()							 # temp var to symbol table

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
					return True
				
				elif parameterList and token.getTokenValue() != "[": 			    # var is not array, but is var parameter
					if token.getTokenValue() in ("in","out"):
						print token.getTokenValue()
						token = self.scanToken()
						self.addSymbolTable(scope, name, Type, size)
						return True
					else:
						self.reportError("in/out", token.getTokenValue(),token.line)
						return False

				# Array Variables
				elif token.getTokenValue() == "[":
					token = self.scanToken()

					if token.getTokenType() in ("INTEGER, FLOAT"):
						size = token.getTokenValue()
						token = self.scanToken()

						if token.getTokenValue() == "]":
							token = self.scanToken()
 
							if token.getTokenValue() == ";" and not parameterList:   # var is array and NOT var parameter
								token = self.scanToken()
								self.addSymbolTable(scope, name, Type, size)
								return True

							elif parameterList: 									 # var is array and is var parameter
								if token.getTokenValue() in ("in","out"):
									print token.getTokenValue()
									token = self.scanToken()

									self.addSymbolTable(scope, name, Type, size)
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
					self.reportErrorMsg("Undentified character", token.line)
					return False

			else: 
				self.reportError("Identifier Type", token.getTokenType(),token.line)
				return False

		else: 
			self.reportError("Type Mark", token.getTokenType(),token.line)
			return False


	def procedure_declaration(self, token, scope = "main"):
		print "\nProcedure Declaration Function: ",token.getTokenValue()

		new_scope = token.Next.getTokenValue()  # Procedure Name

		parList = self.procedure_header(token)
		
		if parList:
			if parList == True:      # If procedure has no parameter
				parList = 0
			self.addSymbolTable(scope, token.Next.getTokenValue(), "proc", 0, parList)  # add procedure and his scope into to ST

			if self.procedure_body(analyzer.current_token, new_scope):
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
							return parList

						else: 
							self.reportErrorMsg("Missing ) in the procedure", token.line)
							self.errorFlag = True
							return False
						
					elif analyzer.current_token.getTokenValue() == ")":
						token = self.scanToken()
						print "Function w/o parameters"
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
		print "scope",scope
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
					print "end procedure"
					token = self.scanToken()
					return True
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
		print "Statement Function:", token.getTokenValue()
		print "scope",proc_scope
		token = self.scanToken()
		print "token:",token.getTokenValue()

		if not if_stat:  # if_stat: then should execute at least one statement
			if token.getTokenValue() == "end":
				return True

			if self.IFlag:
				if token.getTokenValue() == "else" and self.stack.size() > 0:
					return True

		if token.Next.getTokenValue() in (":=","["):
			if self.assignment_statement(token, proc_scope):
				if self.statement(analyzer.current_token, False, proc_scope):
					return True
			else: 
				return False

		elif token.getTokenType() == "IDENTIFIER" and token.Next.getTokenValue() == "(":
			if self.procedure_call(token, proc_scope):

				if self.statement(analyzer.current_token, False, proc_scope):
					return True
			else:
				return False

		elif token.getTokenValue() == "return":
			if self.return_statement(token, proc_scope):

				if self.statement(analyzer.current_token, False, proc_scope):
					return True
			else:
				return False

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() == "for":

			if self.loop_statement(token, proc_scope):
				print "after FOR loop", analyzer.current_token.getTokenValue()

				if self.statement(analyzer.current_token, False, proc_scope):
					return True
			else:
				return False

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() == "if":

			if self.if_statement(token, proc_scope):
				print "after IF Statement", analyzer.current_token.getTokenValue()

				if self.statement(analyzer.current_token, False, proc_scope):
					return True
			else:
				return False

		else:
			self.reportErrorMsg("Missing a statement",token.line)
			return False

	# If proc_scope then it is assigment within procedure
	def assignment_statement(self, token, proc_scope = False):
		print "\nAssignment Statement Function"
		print "scope",proc_scope
		print token.getTokenValue()
		print token.getTokenType()
		if token.getTokenType() == "IDENTIFIER":

			var_token = token

			# --- Declaration Check ---#
			STlist = self.lookatST(token, proc_scope)  					# Verify if var within ST
			if not STlist:												# Error: Undeclared var
				return False
			# ---------  ##  --------- #

			token = self.scanToken()

			if token.getTokenValue() == "[":  							# If array
				size = self.destination(token, proc_scope)
				if size:
					pass

			if analyzer.current_token.getTokenValue() == ":=":
				token = self.scanToken()

				if self.expression(token,";", proc_scope):
					expType = self.arrayType("assigment")
					print expType, " in assignment_statement"

					if analyzer.current_token.getTokenValue() == ";":
						if self.assigTypeChecking(STlist[1], expType): # check type checking
		
							print "Type checking okay"
							self.checkExp = []
							print self.checkExp
							self.add_value_ST(var_token, proc_scope, True)
							return True
						else:
							print "Type unmacthed!"
							self.errorFlag = True
							return False
					else:
						self.reportError(";", token.getTokenValue(), token.line)
						self.errorFlag = True
						return False
				else:
					self.reportErrorMsg("Wrong Expression in assignment_statement", token.line)
					self.errorFlag = True
					return False
			else:
				self.reportError(":=", token.getTokenValue(), token.line)
				self.errorFlag = True
				return False

		else:
			self.reportError("Identifier", token.getTokenType(), token.line)
			self.errorFlag = True
			return False

	def destination(self,token, scope): 
		print "\nDestination Function"
		if token.getTokenValue() == "[":
			token = self.scanToken()

			if self.expression(token,"]", scope):
				
				# array checking
				arrayType = self.arrayType("destination")
				if arrayType == "integer":

					if analyzer.current_token.getTokenValue() == "]":
						token = self.scanToken()
						return True
				else:
					self.reportErrorMsg("Invalid Array Size", token.line)
					self.errorFlag = True
					return False


			else:
				self.reportErrorMsg("Invalid Expression", token.line)
				self.errorFlag = True
				return False

	# If proc_scope then procedure_call is within procedure
	def procedure_call(self,token, proc_scope = False):
		print "\nProcedure Call Function"
		#callList = []

		if token.getTokenType() == "IDENTIFIER":
			STlist = self.lookatST(token, proc_scope)
			print STlist

			if STlist:
				if STlist[1] == "proc":   # var type
					#callList = self.look_procedure_at_ST(token, proc_scope)

					token = self.scanToken()
					
					if token.getTokenValue() == "(":
						token = self.scanToken()

						if token.getTokenValue() != ")":
							self.expression(token,[",",")"], proc_scope)

							while analyzer.current_token.getTokenValue() == ",":
								token = self.scanToken()	
								self.expression(token,[",",")"], proc_scope)

							# --- Type checking Block
							if self.checkExp == STlist[3]:  # parameter list
								print "parameter ok in procedure_call"
							else:
								self.reportErrorMsg("Invalid Procedure Call", token.line)
								self.errorFlag = True
								return False

							# ---- end type checking

						if analyzer.current_token.getTokenValue() == ")":
							token = self.scanToken()

							if token.getTokenValue() == ";":
									return True
							else:
								self.reportError(";", token.getTokenValue(), token.line)
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
		print "scope",proc_scope
		if token.getTokenValue() == "for":
			token = self.scanToken()

			if token.getTokenValue() == "(":
				token = self.scanToken()
				self.assignment_statement(token, proc_scope)

				if analyzer.current_token.getTokenValue() == ";":
					token = self.scanToken()

					if self.expression(token, ")", proc_scope):

						# ---- Type checking

						expType = self.arrayType("loop")
						print expType, " in loop_statement"
						self.checkExp = []
						print self.checkExp

						if expType:
							print "expression ok in loop Expression"
						else:
							self.reportErrorMsg("Wrong Expression in loop statement", token.line)
							self.errorFlag = True
							return False
												
						# ---- end type checking

						if self.statement(token, False, proc_scope):

							if analyzer.current_token.getTokenValue() == "end":
								token = self.scanToken()

								if token.getTokenValue() == "for":
									return True
								else:
									self.reportErrorMsg("Missing 'for' of 'End For", token.line)
									self.errorFlag = True
									return False
							else:
								self.reportError("end", token.getTokenValue(), token.line)
								self.errorFlag = True
								return False
						else:
							self.reportErrorMsg("Wrong Statement", token.line)
							self.errorFlag = True
							return False
					else:
						self.reportErrorMsg("Missing ) of LOOP", token.line)
						self.errorFlag = True
						return False
				else:
					self.reportError(";", token.getTokenValue(), token.line)
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
		print "scope",proc_scope
		if token.getTokenValue() == "if":
			self.stack.push(token.getTokenValue())
			self.IFlag = True   					# accept else after expressions
			token = self.scanToken()

			if token.getTokenValue() == "(":
				token = self.scanToken()

				if self.expression(token, ")", proc_scope):
					token = self.scanToken()

					# ---- Type checking

					expType = self.arrayType("if")
					print expType, " in if_statement"
					self.checkExp = []
					print self.checkExp

					if expType:
						print "expression ok in IF Expression"
					else:
						self.reportErrorMsg("Wrong Expression in IF statement", token.line)
						self.errorFlag = True
						return False
											
					# ---- end type checking

					if token.getTokenValue() == "then":

						if self.statement(token, True, proc_scope):
							if analyzer.current_token.getTokenValue() == "else": # IF with ELSE

								if self.stack.peek() == "if":

									if self.statement(token, True, proc_scope):  # execute at least once
										pass

									else:
										self.errorFlag = True
										return False

								else:
									self.reportErrorMsg("Missing IF statement", token.line)
									self.errorFlag = True
									return False

							if analyzer.current_token.getTokenValue() == "end": # IF without ELSE
								token = self.scanToken()

								if token.getTokenValue() == "if":
									self.stack.pop()
									if token.Next.getTokenValue() == "end":  # If last Else
										self.IFlag = False
									return True
								else:
									self.reportError("if", token.getTokenValue(), token.line)
									self.errorFlag = True
									return False
							else:
								self.reportError("end", token.getTokenValue(), token.line)
								self.errorFlag = True
								return False
						else:
							self.reportErrorMsg("Wrong Statement", token.line)
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
	def return_statement(self,token, proc_scope = False):
		if token.getTokenValue() == "return":
			return True

	def reportError(self, expected, received, line):
	 	print  "\nSyntaxError: "+expected+" Expected"+", "+received+" Received, in line ", line,'\n'

	def reportWarning(self, message):
	 	print  "\nScanner Error: "+message+ ", in line", self.lineCount,'\n'

	def reportErrorMsg(self, message, line):
	 	print message,", in line ", line,'\n'

	def addSymbolTable(self, scope, name, Type, size, Value = None):
		
		if not self.symbolTable.has_key(scope):
			self.symbolTable[scope] = [[name,Type, size, Value]]
		else: # already exists
			self.symbolTable[scope].append([name,Type, size, Value])

	def printST(self):
		for k in self.symbolTable.keys():
			print "\nScope:",k
			for i in range(len(self.symbolTable[k])):
				print i, self.symbolTable[k][i]

	def assigTypeChecking(self, type1, type2):
		if type1 == type2 and type2 == "integer":  
			return "integer"

		elif type1 == "float":
			if type2 in ("float","integer"):
				return "float"

		elif type1.lower() in ("string", "identifier"):
			if type2 in ("string", "identifier"):
				return "string"

		elif type1 == type2 and type2 == "bool":
			return "bool"

		else:
			print "Unmacthed types"
			return False

	# Call typeCheckingExp
	# Return type of expression
	# Return False if find unmacthed type
	def arrayType(self, statement_type):
		print "arrayType Function: statement type", statement_type

		if len(self.checkExp) == 1:
			if statement_type == "if":
				if self.checkExp[0] == "bool":
					return "bool"
				else:
					return False

			elif statement_type == "loop":
				print "loop can't not be single exp"
				return False
		
		varType = self.checkExp[0]
		for i in range(0, len(self.checkExp)-1, 2):
			varType = self.typeCheckingExp(varType, self.checkExp[i+1],self.checkExp[i+2], statement_type)
		return varType

	def typeCheckingExp(self, type1, signal, type2, statement_type):

		if statement_type in ("if", "loop"):
			if signal in (">","<","<=",">=","!=", "=="):
				pass
			else:
				return False

		#if signal in ("+","-","*","/"):
		if type1 == "integer":
			if type2 == "integer":
				return "integer"

			elif type2 == "float":
				return "float"

		elif type1 == "float":
			if type2 in ("float","integer"):
				return "float"

		elif type1 == "string":
			if type2 == "string":
				return "string"

		if type1 == "bool":
			if type2 == "bool":
				return "bool"

		else:
			print "Unmacthed types"
			return False
	


		# make relational expressions
		#elif sign in ("<", ">", "<=", ">="):

	# return list of var items if var in ST
	# return False if undeclared var
	def lookatST(self, token, scope, declaration = False): 
		print "lookatST FUNCTION"
		STlist = []
		if not scope:
			scope = "main"

		print "scope", scope

		if self.symbolTable.has_key(scope):    			# If ST has this scope
			for v in self.symbolTable[scope]:
				if v[0] == token.getTokenValue():   	# var name
					STlist.append(v[0])  # name
					STlist.append(v[1])  # type
					STlist.append(v[2])	 # size (if array)
					STlist.append(v[3])  # value (if procedure)
					return STlist	

		# Search in global scope
		if self.symbolTable.has_key("global"): 			# If ST has this Global scope
			for v in self.symbolTable["global"]:
				if v[0] == token.getTokenValue(): 		# var name
					STlist.append(v[0],v[1],v[2],v[3])  # name, type, size, value
					return STlist				    	# return 
		
		if not declaration:
			# Return False if not found var name
			self.reportErrorMsg("NameError: name '" + token.getTokenValue() + "' is not defined", token.line)
			self.errorFlag = True
		return False

	def add_value_ST(self, token, scope, value, declaration = False): 
		print "add_value_ST FUNCTION"
		if not scope:
			scope = "main"

		print "scope", scope

		if self.symbolTable.has_key(scope):    			# If ST has this scope
			for v in self.symbolTable[scope]:
				if v[0] == token.getTokenValue():   	# var name
					print "v[3]", v[3]
					v[3] = value
					return True
	
		self.symbolTable[scope][i][3] = "Rose"
		
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

# ---- Main -----
# filename = raw_input('Type Filename:') 
dfa = DFA()

filename = "/Users/roses/Downloads/Repository/test.src"
analyzer = Lexical_Analyzer()
analyzer.getTokenFromFile(filename)

analyzer.current_token = analyzer.tokenList.Next  

analyzer.program(analyzer.tokenList.Next)

print "\n",analyzer.printST()
