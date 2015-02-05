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
# symbol_table nao esta compilando mas so salva os identifiers.
#-------------------------------------------------------------------------------

import os,sys
from automata import DFA
from List import List
from stack import Stack

class Lexical_Analyzer:

	tokenType = {'s1': "IDENTIFIER",'s2': "INTLITERAL", 's3': "FLOATLITERAL",'s6': "COMP_OP",'s7': "COMP_OP_EQ",
				 's8': "ARIT_OP",'s9': "EQ",'s10': "LEFT_PAR",'s11': "RIG_PAR",'s12': "LEFT_BRA", 's13': "RIG_BRA",
				 's14': "COMMA",'s15': "SC"}

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
						if self.isNumber(l[s]) or self.isLetter(l[s]) or l[s] == '_':
							word += l[s]
							if s == len(l)-1:	
								#print word			# last one
								self.run_automata(word)
							else:
								continue
								
						else: 
							self.run_automata(word)
							word = ''
							value = ''
							if s+1 < len(l):									# Each character of the line
				  				if l[s]+l[s+1] == '//':
				  					break 
				  			if l[s] in (" ","\n","\t"):
			  					continue
							else:
								self.run_automata(l[s])

			  		elif value == 'num': 		# number buffer 
			  			if self.isNumber(l[s]) or l[s] == "." or self.isLetter(l[s]):
							word += l[s]
							if s == len(l)-1:				# last one
								self.run_automata(word)
							else:
								continue
						else: 
							self.run_automata(word)
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
			  							self.run_automata(l[s])	
			  				elif l[s] in (" ","\n","\t"):
			  					continue	
			  				else:
			  					self.run_automata(l[s])


					elif value == 'op': 		# number buffer 
			  			word += l[s]
			  			self.run_automata(word)
						word = ''
						value = ''

			  		else:													# Each character of the line
				  		if s+1 < len(l):									# Each character of the line
				  			if l[s]+l[s+1] == '//':
				  				break 										# Comment -> Skip line
			  			if l[s] in (" ","\n","\t"): 
			  				continue										# White space or tab - > Skip character
			  			elif self.isLetter(l[s]):
			  				value = 'cha'  # letter
			  				word += l[s]
			  				
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
		     
		
	def reportError(self, expected, received, line):
	 	print  "\nSyntaxError: "+expected+"Expected"+", "+received+" Received, on line ", line,'\n'

	def reportWarning(self, message):
	 	print  "\nScanner Error: "+message+ ", on line", self.lineCount,'\n'

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
		self.goal(analyzer.current_token)
		
	
	def goal(self,current_token):
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

		elif token.getTokenValue() in analyzer.letters:
			token = self.scanToken()
			return True
		elif token.getTokenValue() in analyzer.numbers:
			token = self.scanToken()
			return True
		else:
			print "Error: ID not found"
			self.errorFlag = True
			return False


# ---- Main -----
# filename = raw_input('Type Filename:') 
dfa = DFA()

filename = "/Users/roses/Downloads/Repository/test_grammar.py"
analyzer = Lexical_Analyzer()
analyzer.getTokenFromFile(filename)
analyzer.tokenList.addNode(analyzer.tokenList,"EOF","$",analyzer.lineCount)
# print List
analyzer.tokenList.printList(analyzer.tokenList.Next)

analyzer.parser()

#print "\nSymbol_table: ",analyzer.simbolTable