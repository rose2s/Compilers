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
# 					  2015-01-27  Fix Automata, getToken() function
#					  2015-01-27  Fix Automata, getToken() function
#							28   Divided Separator_Token, Fix	
#						
#-------------------------------------------------------------------------------

import os,sys
from automata import DFA
from List import List

class Scanner:

	tokenType = {'s1': "IDENTIFIER",'s2': "INTLITERAL", 's3': "FLOATLITERAL",'s6': "COMP_OP",'s7': "COMP_OP_EQ",
				 's8': "ARIT_OP",'s9': "EQ",'s10': "LEFT_PAR",'s11': "RIG_PAR",'s12': "LEFT_BRA", 's13': "RIG_BRA",
				 's14': "COMMA",'s15': "SC"}

	keywords  = ["string", "case", "int", "bool", "float", "for", "and", "or", "global", "not", "in", "program", "out", "procedure",
                          "if", "begin", "then", "return", "else", "end", "EOF"]

	letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y']
	numbers = ['0','1','2','3','4','5','6','7','8','9']

	def __init__(self):
		self.lineCount = 0
		self.errorFlag = False
		self.identifier = []
		self.simbolTable = {}
		self.type_table = []
		self.value_table = []

	def isLetter(self,var):
		if var in self.letters:
			return True
		else:
			return False
	def addType_table(self,type):
		self.type_table.append(type)

	def addValue_table(self,value):
		self.value_table.append(value)

	def isNumber(self, var):
		if var in self.numbers:
			return True
		else:
			return False

	def getToken(self,filename,dfa):
		
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
		            print inp_program + " is KEYWORD"

		            token = "KEYWORD"

		            if self.simbolTable.has_key("KEYWORD"):
		            	self.simbolTable["KEYWORD"] += inp_program 
		            else:
		            	self.simbolTable["KEYWORD"] = inp_program 

		        else:
		            print inp_program + " is "+ token
		            if self.simbolTable.has_key(token): 
		            	self.simbolTable[token] += inp_program
		            else:
		            	self.simbolTable[token] = inp_program
		        
		        firstNode.addNode(firstNode,token,inp_program)

		    else:
		        print inp_program + " is "+ token

	        	if self.simbolTable.has_key(token): 
		            self.simbolTable[token] += inp_program
		        else:
		            self.simbolTable[token] = inp_program
        
	        	firstNode.addNode(firstNode,token,inp_program)

		#return token
		else:
		    self.reportError(inp_program)
		    return 

		
	def reportError(self, message):
	 	print  "\nSyntaxError: "+message+ ", in line", self.lineCount,'\n'

	def reportWarning(self, message):
	 	print message

	def printTokens(self):
		for k,v in scanner.simbolTable.items():
			print k,v

# ---- Main -----

dfa = DFA()
firstNode = List("KEYWORD","program")
firstNode.setFirst(firstNode)

# filename = raw_input('Type Filename:') 
filename = "/Users/roses/Downloads/Repository/test_grammar.py"
scanner = Scanner()

scanner.getToken(filename,dfa)

# separe token in array
for k in scanner.simbolTable.keys():
	scanner.simbolTable[k] = list(scanner.simbolTable[k])

#scanner.printTokens()
#while firstNode.Next:
#	print firstNode.getTokenValue()
		
