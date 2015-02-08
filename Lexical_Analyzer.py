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
# 1.0.0    Rose		  2015-02-0
#-------------------------------------------------------------------------------

import os,sys
from automata import DFA
from List import List
from stack import Stack

class Lexical_Analyzer:

	tokenType = {'s1': "IDENTIFIER",'s2': "INTLITERAL", 's3': "FLOATLITERAL",'s6': "COMP_OP",'s7': "COMP_OP_EQ",
				 's8': "ARIT_OP",'s9': "EQ",'s10': "LEFT_PAR",'s11': "RIG_PAR",'s12': "LEFT_CH", 's13': "RIG_CH",
				 's14': "COMMA",'s15': "SC",'s16': "LEFT_BRA", 's17': "RIG_BRA"}

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
		self.tokenList = List("KEYWORD","program",0)
		self.tokenList.setFirst(self.tokenList)
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
				  			if l[s] in ("<",">",":","!"):
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
			  				
			  			elif l[s] in ("<",">",":","!"):
			  					if s+1 < len(l):									# Each character of the line
				  					if l[s+1] == '=':
			  							value = 'op'
			  							word += l[s]
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
				
			    #print inp_program + " is " + token
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
			return {'+','-',')',"$"}
		elif X == 'F':
			return {'+','-','*','/',')',"$"}

	def scanToken(self):
		analyzer.current_token = analyzer.current_token.Next
		return analyzer.current_token

	def parser(self):
		analyzer.current_token = self.tokenList.Next
		self.expression(analyzer.current_token)
		
	
	def expression(self,current_token):
		if self.E(current_token):
			if self.stack.isEmpty():
				print "You got it!"
			else: 
				self.reportWarning("Missing )")
				self.errorFlag = True
				return False 

	def E(self, token):
		print "E: ",token.getTokenValue()
		self.T(token)
		if self.E2(analyzer.current_token):
			return True


	def E2(self,token):
		if not self.errorFlag:
			print "E2: ",token.getTokenValue()
			if token.getTokenValue() in self.first('E2'):
				token = self.scanToken()
				self.T(token)
				if self.E2(analyzer.current_token):
					return True
			elif token.getTokenValue() == "$":
				return True
			else: 
				self.reportError("aritm_op", token.getTokenValue(),token.line)
				return False
		else:
			return False

	def T(self,token):
		print "T: ",token.getTokenValue()
		if self.F(token):
			self.T2(analyzer.current_token)
		else:
			return False


	def T2(self,token):
		if token:
			print "T': ",token.getTokenValue()

		if token.getTokenValue() in self.first('T2'):
			print token.getTokenValue()
			token = self.scanToken()
			if self.F(token):
				self.T2(analyzer.current_token)
			else:
				return False

		elif token.getTokenValue() == "$":
			return True

		elif token.getTokenValue() == ")":
			if not self.stack.isEmpty():
				self.stack.pop()
				token = self.scanToken()
				return True
			else:
				self.reportError(") ","(", token.line)
				self.errorFlag = True
				return False

	def F(self,token):
		print "F: ",token.getTokenValue()
		print "current token: ",analyzer.current_token.getTokenValue()
		if token.getTokenValue() == "(":
			self.stack.push(token.getTokenValue())
			print "stack: ",self.stack.peek()
			token = self.scanToken()
			self.E(token)

		elif token.getTokenType() == ("IDENTIFIER"):
			token = self.scanToken()
			return True
		elif token.getTokenType() in ("INTLITERAL,FLOATLITERAL"):
			token = self.scanToken()
			return True
		else:
			print "Error: ID not found"
			self.errorFlag = True
			return False

	def reset(self):
		self.errorFlag = False
		while self.stack.isEmpty():
			self.stack.pop()

	def program(self,token):
		if self.program_header(token):
			self.reset()
			self.program_body(analyzer.current_token)

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
		if not self.errorFlag:
			self.declaration(token)
			self.statement(analyzer.current_token)

			if analyzer.current_token.getTokenValue() == "end":
				token = self.scanToken()
				if token.getTokenValue() == "program":
					print "\nChegamos ao final do program"
					return True
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
				#print "Let the game begins!"
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

		self.statement(analyzer.current_token)
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

	def statement(self,token): # terminar
		token = self.scanToken()
		return True

	def assignment_statement(self,token):
		pass
	def if_statement(self,token):
		pass

	def loop_statement(self,token):
		pass

	def return_statement(self,token):
		pass
	def procedure_call(self,token):
		pass

	def reportError(self, expected, received, line):
	 	print  "\nSyntaxError: "+expected+" Expected"+", "+received+" Received, on line ", line,'\n'

	def reportWarning(self, message):
	 	print  "\nScanner Error: "+message+ ", on line", self.lineCount,'\n'

	def reportErrorMsg(self, message, line):
	 	print message,", on line ", line,'\n'


""" 
	def statement():

	  if accept("if"):
	    x = expression()
	    y = statement()
	    return IfStatement(x, y)

	  elif accept("return"):
	    x = expression()
	    return ReturnStatement(x)

	  elif accept("{")
	    xs = []
	    while True:
	      xs.append(statement())
	      if not accept(";"):
	        break
	    expect("}")
	    return Block(xs)

	  else:
	    error("Invalid statement!")
"""

# ---- Main -----
# filename = raw_input('Type Filename:') 
dfa = DFA()

filename = "/Users/roses/Downloads/Repository/correct_program/simple_program.src"
analyzer = Lexical_Analyzer()
analyzer.getTokenFromFile(filename)
#analyzer.tokenList.addNode(analyzer.tokenList,"EOF","$",analyzer.lineCount)
# print List
analyzer.tokenList.printList(analyzer.tokenList.Next)

analyzer.current_token = analyzer.tokenList.Next  

analyzer.program(analyzer.tokenList.Next)

#print "\nSymbol_table: ",analyzer.simbolTable