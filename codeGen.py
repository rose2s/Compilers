import os

class CodeGen:
	
	def __init__(self, filename):
		self.filename = filename
		self.sentence = []

	def createFile(self):
		file = open(self.filename,'a')

	def getType(self, varType):
		if varType == "integer":
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
	def genDeclaration(self, myList):
		print "CODE DECLARATION FUNCTION: ", myList
		scope = "%"
		#if self.isEmpty():
			#f.write("; External declaration\n")

		if myList[0] == "global":
			scope = "@"
			myList = myList[1:]

		name = myList[1]
		varType = self.getType(myList[0])
		
		self.sentence.append(scope)
		self.sentence.append(name+" = ")
		if len(myList) > 2:  		# array
			self.sentence.append("["+myList[2]+" x "+varType+"]")
		else:
			self.sentence.append(varType)


		self.writeToken()

	# myList = [global,name,[global, type name]]
	def genFunction(self,myList):
		print "CODE PROCEDURE: ", myList
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
			print "oi",myList
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
						self.sentence.append("["+myList[2]+" x "+ self.getType(myList[0])+"] @"+myList[1])  
						myList = myList[3:]
						if len(myList) > 3:
							self.sentence.append(", ")
					else:
						self.sentence.append(self.getType(myList[0])+" @"+myList[1])   # not global not array
						myList = myList[2:]	
						self.sentence.append(", ")		
				else:  								# last parameter
					self.sentence.append(self.getType(myList[0])+" @"+myList[1])
					myList = myList[2:]

		self.sentence.append(")")
		self.skipLine()
		self.writeToken()

		print "FUNCTION:", self.sentence

	def isEmpty(self):
		if os.stat(self.filename).st_size == 0:
			return True
		else:
			return False

	def writeToken(self):
		with open(self.filename,'a') as f:
			for t in self.sentence:
				f.write(t)
			self.skipLine()
			self.sentence = []

	def skipLine(self):
		with open(self.filename,'a') as f:
			f.write("\n")

#filename = "/Users/roses/Downloads/Repository/Rose.ll"
# = CodeGen(filename)
#.createFile()
#c.genDeclaration(["integer","X"])


