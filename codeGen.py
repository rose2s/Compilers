import os

# Alloca command: <result> = alloca <type>[, i32 <NumElements>][, align <alignment>]     ; yields {type*}:result
# Load command:   <result> = load <ty>* <pointer>[, align <alignment>]
# Store Command:  store <ty> <value>, <ty>* <pointer>[, align <alignment>]       
class CodeGen:
	
	def __init__(self, filename):
		self.filename = filename
		self.sentence = []
		self.temp 	  = 1
		self.tempDic  = {}

	def createFile(self):
		file = open(self.filename,'a')

	def getTemp(self, var):
		#print "VAR in dict ",var
		for k,v in self.tempDic.items():
			print k
			if k == var:
				return v
		return False

	def setTemp(self):
		self.temp = self.temp + 1;

	def getType(self, varType):
		if varType == "integer":
			return "i32"
		elif varType == "int":
			return "i32"
		elif varType == "float":
			return "float"
		elif varType == "bool":
			return "i1"
		elif varType == "string":
			return "string"				# FIX STRING TYPE
		else:
			return False

	# myList=[type, name]
	# @|%var = alloca type, align 4
	def genDeclaration(self, myList):
		print "CODE DECLARATION FUNCTION: ", myList
		scope = "%"

		if myList[0] == "global":
			scope = "@"
			myList = myList[1:]

		name = myList[1]
		varType = self.getType(myList[0])
		
		self.sentence.append(scope)
		self.sentence.append(name+" = alloca ")
		if len(myList) > 2:  		# array
			self.sentence.append("["+myList[2]+" x "+varType+"]")
		else:
			self.sentence.append(varType+", align 4")

		self.writeToken()

	# Load command:   %temp = load <type>* <@|var> , align 4  			-->   %1 = load float* %y, align 4
	# Store Command:  store <type> <%temp>, <type>* <@|%var>, align 4   -->   store float %1, float* %x, align 4
	# myList = [global, vartype, var, value]
	def genStore(self, myList):
		print "\nGenCode for Store: ", myList
		scope = "%"

		if myList[0] == "global":
			scope = "@"
			myList = myList[1:]

		varType = self.getType(myList[0])
		name = myList[1]

		self.sentence.append("store ")
		self.sentence.append(varType)

		if len(myList) == 4:
			value = myList[3]    # value
			if self.getTemp(value):
				self.sentence.append(" %"+self.getTemp(value)+", ")
			else:
				self.sentence.append(" "+value+", ")
		else:
			value = myList[3]    # value
			self.sentence.append(" %"+str(self.temp-1)+", ")

		self.sentence.append(varType+"* ")
		self.sentence.append(scope+name)
		self.sentence.append(", align 4")

		self.writeToken()

	# Load command:   %temp = load <type>* <@|var> , align 4  -->   %1 = load float* %y, align 4
	# myList = [vartype, var]
	#  <result> = op type value, var
	def genLoad(self, myList):
		print "\nGenCode for Load: ", myList

		varType = self.getType(myList[0])
		name = myList[1]
		
		self.tempDic[name] = str(self.temp)
		print self.tempDic

		self.sentence.append("%")
		self.sentence.append(str(self.temp))
		self.setTemp()
		self.sentence.append(" = load ")
		self.sentence.append(varType)
		self.sentence.append("* ")
		self.sentence.append(name)
		self.sentence.append(", align 4")
		print "sentence",self.sentence

		self.writeToken()

	# myList = [type, '%a', '+', type, '%b']
	#   %4 = add nsw i32 %2, %3
	def genExpression(self,myList):
		print "\nGenCode for Expression: "
		if myList[0] == "global":
			myList = myList[3:]	 # remove type and var of code assignment
		else:
			myList = myList[2:]  # remove type and var of code assignment
		print myList

		if len(myList) > 2:  # fazer p len == 2 --> tem tem add
		#	for i in range(0,len(myList),3)
			self.sentence.append("%")
			self.sentence.append(str(self.temp))
			self.setTemp()
			self.sentence.append(" = ")
			self.sentence.append(self.getOp(myList[2],myList[0])+" ")
			self.sentence.append(self.getType(myList[0])+" ")
			# 1 operand
			if self.getTemp(myList[1]):
				self.sentence.append("%"+self.getTemp(myList[1])+", ")
			else:
				self.sentence.append(" "+myList[1]+", ")
				
			# 2 operand
			if self.getTemp(myList[4]):
				self.sentence.append("%"+self.getTemp(myList[4]))
			else:
				self.sentence.append(myList[4])

		print "sentence",self.sentence
		self.writeToken()

	def getCompOp(self, code, typeVar):
		if typeVar in ("int", "integer"):
			if code == "==":
				return "eq"
			elif code == "!=":
				return "ne"
			elif code == ">":
				return "sgt" 
			elif code == "<=":
				return "sle"

		elif typeVar == "float":
			if code == "==":
				return "oeq"
			elif code == "!=":
				return "one"
			elif code == ">":
				return "ogt" 
			elif code == "<=":
				return "ole"

# <result> = icmp eq i32 4, 5          ; yields: result=false
# <result> = icmp ne float* %X, %X     ; y
	def getOp(self, op, typeVar):
		if typeVar in ("int","integer"):
			if op == '+':
				return "add"
			elif op == '-':
				return "sub"
			elif op == '*':
				return "mul"
			elif op == '/':
				return "sdiv"
			elif op == '&&':
				return "and"
			elif op == '|':
				return "or"

		elif typeVar == "float":
			if op == '+':
				return "fadd"
			elif op == '-':
				return "fsub"
			elif op == '*':
				return "fmul"
			elif op == '/':
				return "fdiv"


	# myList = [global,name,[global, type name]]
	def genFunction(self,myList):
		print "\nGenCode for procedure: ", myList
		scope = "%"
		#; function
		self.sentence.append("declare void ")
		# define i32 @main(i32 %argc, i8** %argv) { entry:
		if myList[0] == "global":
			scope = "@"
			myList = myList[1:]

		self.sentence.append(scope)
		funcName = myList[0]
		myList = myList[1:]
		self.sentence.append(funcName+"(")
		
		while len(myList) > 0:
			print "parameter list",myList
			if myList[0] == "global":
				if len(myList) > 3:
					if self.getType(myList[3]) == False: # global and array
						self.sentence.append("["+myList[3]+" x "+ self.getType(myList[1])+"] @"+myList[2]) 
						myList = myList[4:]
						self.sentence.append(", ")
					else:
						self.sentence.append(self.getType(myList[1])+" @"+myList[2])    # global but not array
						myList = myList[3:]
						if len(myList) > 4:	
							self.sentence.append(", ")
				else:  										# last parameter
					self.sentence.append(self.getType(myList[1])+" @"+myList[2])
					myList = myList[3:]
					
			else:
				if len(myList) > 2:
					print "type", myList[2]
					if (myList[2] != "global" and self.getType(myList[2]) == False):  # not global but array
						self.sentence.append("["+myList[2]+" x "+ self.getType(myList[0])+"] %"+myList[1])  
						myList = myList[3:]
						if len(myList) > 3:
							self.sentence.append(", ")
					else:
						self.sentence.append(self.getType(myList[0])+" %"+myList[1])   # not global not array
						myList = myList[2:]	
						self.sentence.append(", ")		
				else:  								# last parameter
					self.sentence.append(self.getType(myList[0])+" %"+myList[1])
					myList = myList[2:]

		self.sentence.append(") {")
		self.skipLine()
		self.writeToken()
		self.sentence.append("entry:")
		self.writeToken()
		self.skipLine()
		#self.sentence.append("}")
		#self.writeToken()

		print "FUNCTION:", self.sentence

	def isEmpty(self):
		if os.stat(self.filename).st_size == 0:
			return True
		else:
			return False

	def writeToken(self):
		#print "mistList", self.sentence
		with open(self.filename,'a') as f:
			#f.write("\n")
			for t in self.sentence:
				#print "t: ",t
				f.write(t)
			self.skipLine()
			self.sentence = []

	def skipLine(self):
		with open(self.filename,'a') as f:
			f.write("\n")

	def deleteFile(self):
		if os.path.exists(self.filename):
			os.remove(self.filename)

#filename = "/Users/roses/Downloads/Repository/Rose.ll"
# = CodeGen(filename)
#.createFile()
#c.genDeclaration(["integer","X"])


