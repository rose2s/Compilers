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
#-------------------------------------------------------------------------------

import os,sys
from automata import DFA

class Scanner:

	tokenType = {'s1': "IDENTIFIER",'s2': "INTLITERAL", 's3': "FLOATLITERAL",'s6': "OPERATOR",'s7': "OPERATOR",'s8': "SEPARATOR"}
	keywords  = ["string", "case", "int", "bool", "float", "for", "and", "or", "global", "not", "in", "program", "out", "procedure",
                          "if", "begin", "then", "return", "else", "end", "EOF"]

	letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y']
	numbers = ['0','1','2','3','4','5','6','7','8','9']

	def __init__(self):
		self.lineCount = 0
		self.errorFlag = False
		self.identifier = []
		self.simbolTable = {}

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

	def getToken(self,filename,dfa):
		
		word = ""
		value = 0  # 0 = other, 1 = letter, 2 = number

		with open(filename) as f:
			lines = f.readlines() 							# Reads until EOF and returns a list of lines. 	
			for l in lines:
				self.lineCount += 1
				for s in range(len(l)):	

					if value == 1: 			# letter buffer
						if l[s] != " " and l[s] != "(":
							word += l[s]
							if s == len(l)-1:				# last one
								self.run_automata(word)
							else:
								continue
								
						else: 
							self.run_automata(word)
							word = ""
							value = 0
							if l[s] == "(":
								self.run_automata(l[s])

			  		elif value == 2: 		# number buffer 
			  			if self.isNumber(l[s]) or l[s] == ".":
							word += l[s]
							if s == len(l)-1:				# last one
								self.run_automata(word)
							else:
								continue
						else: 
							self.run_automata(word)
							word = ""
							value = 0
			  		else:													# Each character of the line
				  		if s+1 < len(l):									# Each character of the line
				  			if l[s]+l[s+1] == '//':
				  				break 										# Comment -> Skip line
			  			if l[s] == " " or l[s] == "\n" or l[s] == "\t": 
			  				continue										# White space or tab - > Skip character
			  			elif self.isLetter(l[s]):
			  				value = 1  # letter
			  				word += l[s]
			  				if s == len(l)-1:
								self.run_automata(l[s]) # last word
			  			elif self.isNumber(l[s]):
			  				value = 2
			  				word += l[s]
			  				if s == len(l)-1:
								self.run_automata(l[s]) # last number
			  			else:
			  				self.run_automata(l[s])


	def run_automata(self,inp_program):
		# run with word
		dfa.run_with_input_list(inp_program)

		if dfa.current_state in self.tokenType.keys():   # Accept States
			
		    token = self.tokenType[dfa.current_state]
		    if token == "IDENTIFIER":
		        if inp_program in self.keywords:
		            print inp_program + " is KEYWORD"
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
		    else:
		        print inp_program + " is "+ token
		        if self.simbolTable.has_key(token): 
		            self.simbolTable[token] += inp_program
		        else:
		            self.simbolTable[token] = inp_program
		    #return token
		else:
		    self.reportError(inp_program)
		    #return None

		
	def reportError(self, message):
	 	print "Error: " + message


	def reportWarning(self, message):
	 	print message

	def printTokens(self):
		for k,v in scanner.simbolTable.items():
			print k,v


# ---- Main -----

# --- Automata ---
states = {'s0', 's1', 's2','s3','s4','s5','s6','s7','s8'}
alphabet = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y',
            '0','1','2','3','4','5','6','7','8','9',
            ":", ";", ",", "+", "-", "*", "/", "(", ")", "<", ">", "!", "=", "{", "}"}
tf = {}
# identifier transition
tf[('s0', ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y'))] = 's1'
tf[('s1', ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y'))] = 's1'
tf[('s1', ('0','1','2','3','4','5','6','7','8','9'))] = 's1'
# int transition
tf[('s0', ('0','1','2','3','4','5','6','7','8','9'))] = 's2'
tf[('s2', ('0','1','2','3','4','5','6','7','8','9'))] = 's2'
# float transition 
tf[('s0',('.'))] = 's4'
tf[('s4', ('0','1','2','3','4','5','6','7','8','9'))] = 's3'
tf[('s2',('.'))] = 's3'
tf[('s3', ('0','1','2','3','4','5','6','7','8','9'))] = 's3'
# operator token
tf[('s0',("!"))] = 's5'
tf[('s0',("<", ">",':'))] = 's6'
tf[('s5',("="))] = 's7'
tf[('s6',("="))] = 's7'
tf[('s0',("+", "-", "*", "/", "="))] = 's7'
# separator token
tf[('s0',("(", ")", "{", "}",";",","))] = 's8'

start_state = 's0'
accept_states = {'s1','s2','s3','s6', 's7','s8'}
# id = s1, int = s2, float=s4, op=s6,s7, sep=s8

dfa = DFA(states, alphabet, tf, start_state, accept_states)

# filename = raw_input('Type Filename:') 
filename = "/Users/roses/Downloads/Repository/test_program.py"
scanner = Scanner()

scanner.getToken(filename,dfa)

# separe token in array
for k in scanner.simbolTable.keys():
	scanner.simbolTable[k] = list(scanner.simbolTable[k])

#scanner.printTokens()