
from scanner import Scanner

class ll1():
	
	stmt = "" # statement

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
	
	def goal(self,token):
		token = self.next_token()
		E(token)


	def E(self,token):
		if self.T(token):
			self.E2(token)
		else:
			return False

	def E2(self,token):
		if token in self.first('E2'):
			print token
			token = scan()
			T(token)
			E2(token)
		elif token == " ":
			return

	def T(self,token):
		F(token)
		T2(token)

	def T2(self,token):
		if token in self.first('T2'):
			print token
			F(token)
			T2(token)
		else:
		#elif token == " ":
			return

	def F(self,token):
		if token == "(":
			E()
		elif token in scanner.numbers:
			token = self.next_token()
			return True
		elif token in scanner.letters: 
			token = self.next_token()
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
scanner = Scanner()

