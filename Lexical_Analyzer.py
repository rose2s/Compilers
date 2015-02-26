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
#-------------------------------------------------------------------------------

import os,sys
from automata import DFA
from List import List
from stack import Stack

class Lexical_Analyzer:

	tokenType = {'s1': "IDENTIFIER",'s2': "INTLITERAL", 's3': "FLOATLITERAL",'s6': "COMP_OP",'s7': "COMP_OP_EQ",
				 's8': "ARIT_OP",'s10': "LEFT_PAR",'s11': "RIG_PAR",'s12': "LEFT_CH", 's13': "RIG_CH",
				 's14': "COMMA",'s15': "SC",'s16': "LEFT_BRA", 's17': "RIG_BRA",'s18': "STRING"}

	keywords  = ["string", "case", "int", "bool", "float", "for", "and", "or", "global", "not", "in", "program", "out", "procedure",
                          "if", "begin", "then", "return", "else", "end", "EOF"]

	letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y']
	numbers = ['0','1','2','3','4','5','6','7','8','9']
	simbolTable = {}

	# LL(1) grammar
	terminals = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y',
					  '0','1','2','3','4','5','6','7','8','9',
					   "+", "-", "*", "/", "(", ")", "<", ">", "{", "}", ";"]
	startSimbol = 'E'
	non_terminals = ['E','E2','T','T2','F']
	current_token = None

	def __init__(self):
		self.lineCount = 0
		self.IDtokenNum = 0
		self.errorFlag = False
		self.IFlag = False
		self.tokenList = List("KEYWORD","program",0)
		self.tokenList.setFirst(self.tokenList)
		self.EXPstack = Stack()
		self.stack = Stack()

	def isLetter(self,var):
		if var in self.letters:
			return True
		else:
			return False

	def isNumber(self, var):
		if var in self.numbers:
			return True
		else:
			return False

	def getTokenFromFile(self,filename):
		
		word = ""
		value = 0  # 0 = other, 1 = letter, 2 = number

		with open(filename) as f:
			lines = f.readlines() 							# Reads until EOF and returns a list of lines. 	
			for l in lines:
				self.lineCount += 1
				for s in range(len(l)):	

					if value == 'cha': 			# letter buffer
						if self.isNumber(l[s]) or self.isLetter(l[s].lower()) or l[s] == '_':
							word += l[s].lower()
							if s == len(l)-1:	
								#print word			# last one
								self.run_automata(word.lower())
							else:
								continue
								
						else: 
							self.run_automata(word.lower())
							word = ''
							value = ''
							if s+1 < len(l):									# Each character of the line
				  				if l[s]+l[s+1] == '//':
				  					break 
				  			if l[s] in (" ","\n","\t"):
			  					continue
							else:
								self.run_automata(l[s].lower())

			  		elif value == 'num': 		# number buffer 
			  			if self.isNumber(l[s]) or l[s] == "." or self.isLetter(l[s]):
							word += l[s]
							if s == len(l)-1:				# last one
								self.run_automata(word.lower())
							else:
								continue
						else: 
							self.run_automata(word.lower())
							word = ''
							value = ''
							if s+1 < len(l):									# Each character of the line
				  				if l[s]+l[s+1] == '//':
				  					break 	
				  			if l[s] in ("<",">",":","!","="):
			  					if s+1 < len(l):									# Each character of the line
				  					if l[s+1] == '=':
			  							value = 'op'
			  							word += l[s]
			  						else:
			  							self.run_automata(l[s].lower())	
			  				elif l[s] in (" ","\n","\t"):
			  					continue	
			  				else:
			  					self.run_automata(l[s].lower())

			  		elif value == 'str': 			# string buffer
						if l[s] != '\"':
							word += l[s]
							if s == len(l)-1:	
								#print word			# last one
								self.run_automata(word.lower())
							else:
								continue
								
						else: 
							word += l[s]
							self.run_automata(word.lower())
							word = ''
							value = ''
							if l[s] != '\"':
								if s+1 < len(l):									# Each character of the line
					  				if l[s]+l[s+1] == '//':
					  					break 
					  			if l[s] in (" ","\n","\t"):
				  					continue
								else:
									self.run_automata(l[s].lower())
							else:
								continue

					elif value == 'op': 		# number buffer 
			  			word += l[s]
			  			self.run_automata(word.lower())
						word = ''
						value = ''

			  		else:													# Each character of the line
				  		if s+1 < len(l):									# Each character of the line
				  			if l[s]+l[s+1] == '//':
				  				break 										# Comment -> Skip line
			  			if l[s] in (" ","\n","\t"): 
			  				continue										# White space or tab - > Skip character
			  			elif self.isLetter(l[s].lower()):
			  				value = 'cha'  # letter
			  				word += l[s].lower()
			  				
			  			elif self.isNumber(l[s]):
			  				value = 'num'
			  				word += l[s]
			  				
			  			elif l[s] in ("<",">",":","!","="):
			  					if s+1 < len(l):									# Each character of the line
				  					if l[s+1] == '=':
			  							value = 'op'
			  							word += l[s]
				  					else:
				  						self.run_automata(l[s])

				  		elif l[s] == "\"":
			  				value = 'str'  # string
			  				word += l[s].lower()


			  			else:
			  				self.run_automata(l[s])
			  				continue
			  			
			  			if s == len(l)-1:
							self.run_automata(l[s]) # last number


	def run_automata(self,inp_program):
		# run with word
		dfa.run_with_input_list(inp_program)

		if dfa.current_state in self.tokenType.keys():   # Accept States
			
			    token = self.tokenType[dfa.current_state]

			    if token == "IDENTIFIER":
			        if inp_program in self.keywords:
			        	token = "KEYWORD"
			        """
				    if not self.simbolTable.has_key(inp_program):
			    		print inp_program + " is " + token
			    		self.simbolTable[inp_program] = self.IDtokenNum
			    		self.IDtokenNum+= 1 
				    else: # already exists
				    	print inp_program + " is " + token + " repeated"
				    """
				
			    print inp_program + " is " + token
			    self.tokenList.addNode(self.tokenList,token,inp_program,self.lineCount)

		#return token
		else:
		    self.reportWarning(inp_program)
		     

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

	def scanToken(self):
		analyzer.current_token = analyzer.current_token.Next
		return analyzer.current_token
		
	def expression(self,current_token, sign = ";"):
		print self.EXPstack.items
		if self.E(current_token, sign):

			if self.EXPstack.isEmpty():
				print "You got it!"
				return True
			else: 
				self.reportWarning("Missing )")
				self.errorFlag = True
				return False 

	def E(self, token, sign):
		print "E: ",token.getTokenValue()
		self.T(token,sign)
		if self.E2(analyzer.current_token, sign):
			return True


	def E2(self,token, sign):
		if not self.errorFlag:
			print "E2: ",token.getTokenValue()

			if (token.getTokenValue() in self.first('E2')) or (self.relation_op(token.getTokenValue())):
				token = self.scanToken()
				self.T(token,sign)

				if self.E2(analyzer.current_token,sign):
					return True

			elif token.getTokenValue() in sign:
				print "sign", sign
				return True
			else: 
				self.reportError("aritm_op", token.getTokenValue(),token.line)
				return False
		else:
			return False

	def T(self,token,sign):
		print "T: ",token.getTokenValue()

		if self.F(token,sign):
			self.T2(analyzer.current_token,sign)
		else:
			return False


	def T2(self,token, sign):
		if token:
			print "T': ",token.getTokenValue()

		if token.getTokenValue() in sign and self.EXPstack.isEmpty():
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
			print token.getTokenValue()
			token = self.scanToken()

			if self.F(token,sign):
				self.T2(analyzer.current_token,sign)
			else:
				return False

	def F(self,token,sign):
		print "F: ",token.getTokenValue()

		if token.getTokenValue() == "(":
			self.EXPstack.push(token.getTokenValue())
			print "stack: ",self.EXPstack.peek()
			token = self.scanToken()
			self.E(token,sign)

		elif token.getTokenType() == ("IDENTIFIER"):
			token = self.scanToken()
			if token.getTokenValue() == "[":
				if self.destination(token):
					return True
				else:
					self.reportErrorMsg("Error in destination", analyzer.current_token.line)
					self.errorFlag = True
					return False
			else:
				return True

		elif token.getTokenType() in ("INTLITERAL,FLOATLITERAL"):
			token = self.scanToken()
			return True

		elif token.getTokenType() in ("STRING"):
			token = self.scanToken()
			return True

		elif token.getTokenType() in ("true","false"):
			token = self.scanToken()
			return True

		else:
			print "Error: ID not found"
			self.errorFlag = True
			return False

	def relation_op(self, relation):
	 	l = [">=","==","<=","<",">","!="]
	 	if not relation:
	 		return l
	 	elif relation in l:
	 		print "relational op: ",relation
	 		return True
	 	else:
	 		return False

	def reset(self):
		self.errorFlag = False
		while not self.stack.isEmpty():
			self.stack.pop()

	def program(self,token):
		if self.program_header(token):
			self.reset()
			self.program_body(analyzer.current_token)

	def program_header(self,token):
		print "\nProgram_header function"
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
			self.declaration(token)
			print "\nStart Program!"

			if self.statement(analyzer.current_token):

				if analyzer.current_token.getTokenValue() == "end":
					token = self.scanToken()

					if token.getTokenValue() == "program":
						print "\nEND PROGRAM"
						return True
			else:
				return False
		else:
			return False

	def type_mark(self,t):
		if t in ("integer", "float", "bool", "string"):
			return True
		else:
			return False

	def declaration(self,token):
		if not self.errorFlag:
			print "Declaration Function:", token.getTokenValue() 
			if token.getTokenValue() == "global":
				token = self.scanToken()

			if self.type_mark(token.getTokenValue()):
				self.variable_declaration(token)
				self.declaration(analyzer.current_token)

			elif token.getTokenValue() == "procedure":
				self.procedure_declaration(token)
				self.declaration(analyzer.current_token)
			
			elif token.getTokenValue() == "begin":
				return True

			else: 
				self.reportErrorMsg("Unexpected type in Declaration",token.line)
				return False
		else:
			return False

	
	def variable_declaration(self, token, parameter= False): # if parameter -> is parameter
		
		print "variable_declaration:",token.getTokenValue()

		if self.type_mark(token.getTokenValue()):  # if token in type_mark
			token = self.scanToken()

			if token.getTokenType() == "IDENTIFIER":
				token = self.scanToken()

				if token.getTokenValue() == ";" and not parameter:
					token = self.scanToken()
					return True

				elif parameter:
					if token.getTokenValue() in ("in","out"):
						print token.getTokenValue()
						token = self.scanToken()
						return True
					else:
						self.reportError("in/out", token.getTokenValue(),token.line)
						return False

				# arrays
				elif token.getTokenValue() == "[":
					token = self.scanToken()

					if token.getTokenType() in ("INTLITERAL,FLOATLITERAL"):
						token = self.scanToken()

						if token.getTokenValue() == "]":
							token = self.scanToken()

							if token.getTokenValue() == ";":
								token = self.scanToken()
								return True
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
		# falta fazer array

	def procedure_declaration(self,token):
		print "\nProcedure declaration: ",token.getTokenValue()
		self.procedure_header(token)
		self.procedure_body(analyzer.current_token)

	def procedure_header(self,token):
		print "Procedure_header function: ",token.getTokenValue()
		if token.getTokenValue() == "procedure":
			token = self.scanToken()

			if token.getTokenType() == "IDENTIFIER":
				token = self.scanToken()	

				if token.getTokenValue() == "(":
					token = self.scanToken()

					if self.type_mark(token.getTokenValue()):
						self.variable_declaration(token,True)
					
						while analyzer.current_token.getTokenValue() == ",":
							token = self.scanToken()	
							self.variable_declaration(analyzer.current_token, True)

						if analyzer.current_token.getTokenValue() == ")":
							token = self.scanToken()
							print "parametros ok"
							return True

						else: 
							self.reportErrorMsg("Missing ) in the porcedure", token.line)
							self.errorFlag = True
							return False
						
					elif analyzer.current_token.getTokenValue() == ")":
						token = self.scanToken()
						print "Function w/o parameters"
						return True

					else: 
						self.reportErrorMsg("Missing ) in the porcedure", token.line)
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

	def procedure_body(self,token):
		print "PROCEDURE_BODY FUNCTION:",token.getTokenValue()
		if not self.errorFlag:
			self.declaration(token)
		else:
			return False

		if self.statement(analyzer.current_token):

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

	def statement(self,token, if_stat = False): 
		print "Statement Function:", token.getTokenValue()
		token = self.scanToken()
		print "token:",token.getTokenValue()
		
		print "\nIF_STAT FLAG",if_stat
		print "\nIF_FLAG",self.IFlag
		print "\nPILHA",self.stack.items
		print "\nPILHA size",self.stack.size()

		if not if_stat:  # if_stat: then should execute at least one statement
			if token.getTokenValue() == "end":
				return True

			if self.IFlag:
				if token.getTokenValue() == "else" and self.stack.size() > 0:
					return True

		if token.Next.getTokenValue() in (":=","["):
			if self.assignment_statement(token):
				print "after assignment_statement", analyzer.current_token.getTokenValue()

				if self.statement(analyzer.current_token):
					return True
			else: 
				return False

		elif token.getTokenType() == "IDENTIFIER" and token.Next.getTokenValue() == "(":
			if self.procedure_call(token):
				print "after procedure_call", analyzer.current_token.getTokenValue()

				if self.statement(analyzer.current_token):
					return True
			else:
				return False

		elif token.getTokenValue() == "return":
			if self.return_statement(token):

				if self.statement(analyzer.current_token):
					return True
			else:
				return False

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() == "for":

			if self.loop_statement(token):
				print "after FOR loop", analyzer.current_token.getTokenValue()

				if self.statement(analyzer.current_token):
					return True
			else:
				return False

		elif token.getTokenType() == "KEYWORD" and token.getTokenValue() == "if":

			if self.if_statement(token):
				print "after IF Statement", analyzer.current_token.getTokenValue()

				if self.statement(analyzer.current_token):
					return True
			else:
				return False

		else:
			self.reportErrorMsg("Missing a statement",token.line)
			return False


	def assignment_statement(self,token):
		print "\nAssignment statement"
		if token.getTokenType() == "IDENTIFIER":
			token = self.scanToken()

			if token.getTokenValue() == "[":
				if self.destination(token):
					print "ok destination",analyzer.current_token.getTokenValue()

			if analyzer.current_token.getTokenValue() == ":=":
				token = self.scanToken()

				if self.expression(token,";"):

					if analyzer.current_token.getTokenValue() == ";":
						return True
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

	def destination(self,token):  # return :=
		print "\nDestination Function"
		if token.getTokenValue() == "[":
			token = self.scanToken()

			if self.expression(token,"]"):
				if analyzer.current_token.getTokenValue() == "]":
					token = self.scanToken()
					return True
			else:
				self.reportErrorMsg("Invalid Expression", token.line)
				self.errorFlag = True
				return False

	def procedure_call(self,token):
		print "\nProcedure Call Function"
		if token.getTokenType() == "IDENTIFIER":
			token = self.scanToken()
			
			if token.getTokenValue() == "(":
				token = self.scanToken()

				if token.getTokenValue() != ")":
					self.expression(token,[",",")"])

					while analyzer.current_token.getTokenValue() == ",":
						token = self.scanToken()	
						self.expression(token,[",",")"])

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
			self.reportError("Identifier", token.getTokenType(), token.line)
			self.errorFlag = True
			return False

	def loop_statement(self,token):
		print "\nLoop Statement Function"
		if token.getTokenValue() == "for":
			token = self.scanToken()

			if token.getTokenValue() == "(":
				token = self.scanToken()
				self.assignment_statement(token)

				if analyzer.current_token.getTokenValue() == ";":
					token = self.scanToken()

					if self.expression(token, ")"):

						if self.statement(token):

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


	def if_statement(self,token):
		print "\nIF Statement Function"
		if token.getTokenValue() == "if":
			self.stack.push(token.getTokenValue())
			self.IFlag = True   					# accept else after expressions
			token = self.scanToken()

			if token.getTokenValue() == "(":
				token = self.scanToken()

				if self.expression(token, ")"):
					token = self.scanToken()

					if token.getTokenValue() == "then":

						if self.statement(token, True):
							if analyzer.current_token.getTokenValue() == "else": # IF with ELSE

								if self.stack.peek() == "if":

									if self.statement(token, True):  # execute at least once
										pass

									else:
										#self.reportErrorMsg("Wrong Statement", token.line)
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
		
		# [ else ( <statement> ; )+ ]

	def return_statement(self,token):
		if token.getTokenValue() == "return":
			return True

	def reportError(self, expected, received, line):
	 	print  "\nSyntaxError: "+expected+" Expected"+", "+received+" Received, on line ", line,'\n'

	def reportWarning(self, message):
	 	print  "\nScanner Error: "+message+ ", on line", self.lineCount,'\n'

	def reportErrorMsg(self, message, line):
	 	print message,", on line ", line,'\n'

# ---- Main -----
# filename = raw_input('Type Filename:') 
dfa = DFA()

filename = "/Users/roses/Downloads/Repository/correct_program/simple_program.src"
analyzer = Lexical_Analyzer()
analyzer.getTokenFromFile(filename)
#analyzer.tokenList.addNode(analyzer.tokenList,"EOF","$",analyzer.lineCount)
# print List
#analyzer.tokenList.printList(analyzer.tokenList.Next)

analyzer.current_token = analyzer.tokenList.Next  

analyzer.program(analyzer.tokenList.Next)

#print "\nSymbol_table: ",analyzer.simbolTable