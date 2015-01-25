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
#-------------------------------------------------------------------------------

import os,sys 

class Scanner:

	def __init__(self,filename):
		lineCount = 0
		errorFlag = False
		keywords  = ["string", "case", "int", "bool", "float", "for", "and", "or", "global", "not", "in", "program", "out", "procedure",
						  "if", "begin", "then", "return", "else", "end", "EOF"]

		operands = {"add": +, "sub": -, "mult": *, "div": /}
		simbolTable = {}
		tokenType = ["IDENTIFIER","OPERATOR","KEYWORD","STRINGLITERAL","INTLITERAL","FLOATLITERAL"]


		with open(filename) as f:
			lines = f.readlines() 										# Reads until EOF and returns a list of lines. 		
		  		for l in lines:
		  			for s in range(len(l)):
		  				print l[s],l[s+1]
		  				if l[s]+l[s+1] != '//':  					    # Not comment line
							#if s != " " and s != "\n" and s != "\t": 	# Not a white spapce, not Tab
							print l


	def reportError(self, message):
	 	print "Error: " + message


	def reportWarning(self, message):
	 	print message

	def getToken(self):
		print "nothing"


# ---- Main -----
# filename = raw_input('Type Filename:') 

filename = "/Users/roses/Downloads/program.py"
scanner = Scanner(filename)

