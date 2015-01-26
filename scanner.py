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

	def __init__(self):
		self.lineCount = 0
		self.errorFlag = False
		self.identifier = []
		self.simbolTable = {}

	def getToken(self,filename,dfa):

		#with open(filename) as f:
		#lines = f.readlines() 										# Reads until EOF and returns a list of lines. 		
	  	#	for l in lines:
	  	#		for s in range(len(l)):
	  	#			print l[s],l[s+1]
	  	#			if l[s]+l[s+1] != '//':  					    # Not comment line
						#if s != " " and s != "\n" and s != "\t": 	# Not a white spapce, not Tab
		#				print l
		inp_program = "case"
		self.run_automata(inp_program)

	def run_automata(self,inp_program):
		# run with word
		print dfa.run_with_input_list(inp_program)

		if dfa.current_state in self.tokenType.keys():
		    token = self.tokenType[dfa.current_state]
		    if token == "IDENTIFIER":
		        if inp_program in self.keywords:
		            print inp_program + " is KEYWORD"
		            self.simbolTable["KEYWORD"] = inp_program
		        else:
		            print inp_program + " is "+ token
		            self.simbolTable[token] = inp_program
		    else:
		        print inp_program + " is "+ token
		        self.simbolTable[token] = inp_program
		else:
		    self.reportError("invalid "+inp_program)

	def reportError(self, message):
	 	print "Error: " + message


	def reportWarning(self, message):
	 	print message


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
tf[('s0',("!", ":"))] = 's5'
tf[('s0',("<", ">"))] = 's6'
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
filename = "/Users/roses/Downloads/program.py"
scanner = Scanner()

scanner.getToken(filename,dfa)
print scanner.simbolTable

