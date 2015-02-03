
from scanner import Scanner

class ll1():
	
	stmt = "" # statement
	current_token = None

	def __init__(self):
		self.FIRST = []
		self.FOLLOW = []
		self.terminals = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y',
						  '0','1','2','3','4','5','6','7','8','9',
						   "+", "-", "*", "/", "(", ")", "<", ">", "{", "}", ";"]
		self.startSimbol = 'E'

		self.non_terminals = ['E','E2','T','T2','F']

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

	def next_token(self,token):
		return token.next()
	
	def goal(self):
		#while current_token:
		print "now = ",self.current_token.getTokenValue()
		if self.E(self.current_token):
			print "You got it!"
		#print self.current_token.getTokenValue()
		#current_token = current_token.Next

	def E(self,token):
		#print token.getTokenValue()
		if self.T(self.current_token):
			self.E2(self.current_token)
			return True
		else:
			return False

	def E2(self,token):
		print "E2: ",token.getTokenValue()
		if token.getTokenValue() in self.first('E2'):
			self.current_token = token.Next
			print "current_token: ",self.current_token.getTokenValue()
			self.T(self.current_token)
			self.E2(self.current_token)
		elif token == "$":
			return True

	def T(self,token):
		print "T: ",token.getTokenValue()
		self.F(self.current_token)
		self.T2(self.current_token)
		return True
		

	def T2(self,token):
		if token:
			print "T2: ",token.getTokenValue()
		if token.getTokenValue() in self.first('T2'):
			print token.getTokenValue()
			self.current_token = token.Next
			self.F(self.current_token)
			self.T2(self.current_token)
		elif token == "$":
			return True

	def F(self,token):
		print "F: ",token.getTokenValue()
		if token == "(":
			self.E()
		elif token.getTokenValue() in scanner.numbers:
			self.current_token = token.Next
			print "current_token: ", self.current_token.getTokenValue()
			return True
		elif token.getTokenValue() in scanner.letters: 
			self.current_token = token.Next
			return True
		else:
			print "Error: ID not found"
			return False

	def program():
		program_header()
		program_body()

	def program_header():
		"program" + ID + "is"

"""
	def program_body():
		( <declaration> ; )*
begin
( <statement> ; )*
end program
<declaration> ::=
[ global ] <procedure_declaration>
| [ global ] <variable_declaration> <procedure_declaration> ::=
<procedure_header> <procedure_body>

<procedure_header> :: = procedure <identifier>
( [<parameter_list>] )
<parameter_list> ::=
<parameter> , <parameter_list>
| <parameter>
<parameter> ::= <variable_declaration> (in | out)
<procedure_body> ::=
( <declaration> ; )*
begin
( <statement> ; )*
end procedure
<variable_declaration> ::= <type_mark> <identifier>
[ [ <array_size> ] ]
<type_mark> ::=
integer
| float
| bool
| string
<array_size> ::= 
		<number> 

<statement> ::=

	<assignment_statement> | <if_statement> | <loop_statement> | <return_statement> | <procedure_call>
"""

# --- Main ---

filename = "/Users/roses/Downloads/Repository/test_grammar.py"
scanner = Scanner()
scanner.getToken(filename)
scanner.simbolTable.addNode(scanner.simbolTable,"EOF","$")

scanner.simbolTable.printList(scanner.simbolTable)

grammar = ll1()
grammar.current_token = scanner.simbolTable.getFirst().Next

#print grammar.current_token.getTokenValue()
grammar.goal()
