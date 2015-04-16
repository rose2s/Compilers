import os
from stack import Stack

# Alloca command: <result> = alloca <type>[, i32 <NumElements>][, align <alignment>]     ; yields {type*}:result
# Load command:   <result> = load <ty>* <pointer>[, align <alignment>]
# Store Command:  store <ty> <value>, <ty>* <pointer>[, align <alignment>]    


class CodeGen:
	
	def __init__(self, filename):
		self.filename = filename
		self.sentence = []
		self.temp 	  = 1
		self.tempDic  = {}
		self.ifStack = Stack()
		self.loopStack = Stack()
		self.ifCount = 1
		self.loopCount = 1
		self.funcDic = {}

	def createFile(self):
		file = open(self.filename,'a')

	def getTemp(self, var):
		for k,v in self.tempDic.items():
			if k in (var, "@"+var, "%"+var):
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

	def genModule(self, filename):
		self.sentence.append("; ModuleID = "+filename+"\n")
		self.writeToken()

	def genEnd(self):
		self.sentence = []
		self.sentence.append("\n}\n")
		self.sentence.append("attributes #0 = { nounwind }")
		self.writeToken()

	# @|%var = alloca type, align 4 ... myList=[type, name]
	def genDeclaration(self, myList):
		print "CODE DECLARATION FUNCTION: ", myList
		print "sentence", self.sentence
		scope = "%"

		if myList[0] == "global":
			scope = "@"
			myList = myList[1:]

		name = str(myList[1])
		varType = str(self.getType(myList[0]))
		
		self.sentence.append(scope)

		self.sentence.append(name+" = alloca ")

		if len(myList) > 2:  		# array
			self.sentence.append("["+myList[2]+" x "+varType+"], align 4")
		else:
			self.sentence.append(varType+", align 4")

		self.writeToken()

	# Load command:   %temp = load <type>* <@|var> , align 4  			-->   %1 = load float* %y, align 4
	# Store Command:  store <type> <%temp>, <type>* <@|%var>, align 4   -->   store float %1, float* %x, align 4
	# myList = [global, vartype, var, value]
	def genStore(self, result, myList, isFunction = False):
		print "\nGenCode for Store: ", result, myList
		scope = "%"

		if result[0] == "global":
			scope = "@"
			result = result[1:]

		varType = self.getType(result[0])
		name = result[1]

		self.sentence.append("store ")
		self.sentence.append(varType)

		if len(myList) == 2:   	 # single assignment [type, value]
			value = myList[1]    # value
			if self.getTemp(value):
				self.sentence.append(" %"+str(self.getTemp(value))+", ")
			else:
				self.sentence.append(" "+value+", ")
		else:
			value = myList[1]    # value
			self.sentence.append(" %"+str(self.temp-1)+", ")

		self.sentence.append(varType+"* ")

		if isFunction:
			print "oi", self.tempDic
			name = str(self.getTemp(name))
			self.sentence.append(scope+name)
		else:
			self.sentence.append(scope+name)
		self.sentence.append(", align 4")

		self.writeToken()

	def addTemp(self, name): 
		self.tempDic[name] = str(self.temp)
		print self.tempDic
		self.setTemp()

	# Load command:   %temp = load <type>* <@|var> , align 4  -->   %1 = load float* %y, align 4
	# myList = [vartype, var]
	#  <result> = op type value, var
	def genLoad(self, myList):
		print "\nGenCode for Load: ", myList

		varType = self.getType(myList[0])
		name = myList[1]
		
		self.addTemp(name)

		self.sentence.append("%")
		self.sentence.append(str(self.getTemp(name)))
		self.sentence.append(" = load ")
		self.sentence.append(varType)
		self.sentence.append("* ")
		self.sentence.append(name)
		self.sentence.append(", align 4")
		print "sentence",self.sentence

		self.writeToken()

	def genCall(self, myList):  # myList = [[global], name, [type var]
		#%3 = call i32 @sum(i32 %2)
		write = []
		print "\nGenCode for Call: ", myList
		scope = "%"

		if myList[0] == "global":
			scope = "@"
			myList = myList[1:]

		name = myList[0]
		myList = myList[1:]

		typee = self.funcDic[name]

		write.append("%")
		write.append(str(self.temp))
		self.setTemp()
		write.append(" = call ")
		write.append(typee+" ")
		write.append(scope)
		write.append(name+"(")

		print "myList",myList
		for l in range(0,len(myList)-1,2):
			print l

			write.append(self.getType(myList[l])+" ")
			if myList[l+1][0] in ("@","%"):  # if var
				write.append("%"+str(self.getTemp(myList[l+1])))
			else:
				write.append(myList[l+1])

			if l < len(myList)-2:
				write.append(", ")

		write.append(")")
		print "sentence now", self.sentence
		print write 
		self.sentence = write
		self.writeToken()

	# myList = [type, '%a', '+', type, '%b']
	#   %4 = add nsw i32 %2, %3

	def genExpression(self,myList):
		#if self.getCompOp(myList[2],myList[3]):
		#	self.genCompExp(myList)
		#elif self.getOp(myList[2],myList[3]):
			self.genAritmExpression(myList)

	def genCompExp(self, myList):
		print "GenCode for Comp Exp", myList
		myList = myList[5:]
		print myList

	def genAritmExpression(self,myList):
		print "\nGenCode for Aritm Expression: "
		if myList[0] == "global":
			myList = myList[1:]	 # remove type and var of code assignment
		print myList

		if len(myList) > 2:  # fazer p len == 2 --> tem tem add

			while len(myList) > 0:
				self.sentence.append("%")
				self.sentence.append(str(self.temp))
				self.setTemp()
				self.sentence.append(" = ")
				self.sentence.append(self.getOp(myList[2],myList[3]))
				self.sentence.append(" "+self.getType(myList[3]))
				
				# 1 operand
				if self.getTemp(myList[1]):
					x = str("%")+self.getTemp(myList[1])
				else:
					x = myList[1]

				self.sentence.append(" "+ x +", ")
				# 2 operand
				if self.getTemp(myList[4]):
					y = str("%")+self.getTemp(myList[4])
				else:
					y = myList[4]
				self.sentence.append(y)
				
				print "sentence",self.sentence
				self.writeToken()
				#self.skipLine()
				myList = myList[3:]
				print "after cut", myList
				myList[1] = "%"+str(self.temp-1)		  # result of previous operation
				print "under operation: ",myList
				if len(myList) == 2:
					myList = []

	def getCompOp(self, code, typeVar):
		if typeVar in ("int", "integer"):
			if code == "==":
				return "icmp eq"
			elif code == "!=":
				return "icmp ne"
			elif code == ">":
				return "icmp sgt" 
			elif code == "<":
				return "icmp slt" 
			elif code == ">=":
				return "icmp sge" 
			elif code == "<=":
				return "icmp sle"

		elif typeVar == "float":
			if code == "==":
				return "fcmp oeq"
			elif code == "!=":
				return "fcmp one"
			elif code == ">":
				return "fcmp ogt" 
			elif code == "<":
				return "fcmp olt"
			elif code == ">=":
				return "fcmp oge"
			elif code == "<=":
				return "fcmp ole"
		else:
			return False

# <result> = icmp eq i32 4, 5          ; yields: result=false
# <result> = icmp ne float* %X, %X     ; y
	def getOp(self, op, typeVar):
		print "\ngetOp FUnction <op>, <type>: ", op, typeVar
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
			elif op == "==":
				return "icmp eq"
			elif op == "!=":
				return "icmp ne"
			elif op == ">":
				return "icmp sgt" 
			elif op == "<":
				return "icmp slt" 
			elif op == ">=":
				return "icmp sge" 
			elif op == "<=":
				return "icmp sle"

		elif typeVar == "float":
			if op == '+':
				return "fadd"
			elif op == '-':
				return "fsub"
			elif op == '*':
				return "fmul"
			elif op == '/':
				return "fdiv"
			elif op == "==":
				return "fcmp oeq"
			elif op == "!=":
				return "fcmp one"
			elif op == ">":
				return "fcmp ogt" 
			elif op == "<":
				return "fcmp olt"
			elif op == ">=":
				return "fcmp oge"
			elif op == "<=":
				return "fcmp ole"
		else:
			return False

	def setIfCount(self):
		self.ifCount = self.ifCount + 1;

	def setLoopCount(self):
		self.loopCount = self.loopCount + 1;

	def genIf(self):
		
		ifTrue = "ifTrue"+str(self.ifCount)
		ifFalse = "ifFalse"+str(self.ifCount)
		self.setIfCount()
		
		self.ifStack.push(ifTrue)
		self.ifStack.push(ifFalse)

		self.genCoBr(str(self.temp-1), ifTrue, ifFalse)

	def genLoop1(self):
		self.genUnBr("loop"+str(self.loopCount))

		self.genLabel("loop"+str(self.loopCount))
		#self.setTemp()

	def genLoop2(self):
		loopTrue = "loopTrue"+str(self.loopCount)
		loopFalse = "loopFalse"+str(self.loopCount)
		self.setLoopCount()
		
		self.loopStack.push(loopTrue)
		self.loopStack.push(loopFalse)

		self.genCoBr(str(self.temp-1), loopTrue, loopFalse)

	def genLoop3(self, myList):
		
		self.genUnBr(self.temp)
		self.genLabel(self.temp)
		self.setTemp()
		self.genLoad(myList)
		myList[1] = myList[1][1]

		myList.append("+")
		myList.append("integer")
		myList.append("1")
		self.genAritmExpression(myList)
		self.genStore(myList[:2],myList)
		loopFalse = self.loopStack.pop()
		loopTrue = self.loopStack.pop()
		self.genUnBr("loop"+str(loopFalse[-1]))
		self.genLabel(loopFalse)
                                  
   
	# br label %next
	def genElse(self):
		elseVar = self.ifStack.peek() 

		end = "end"+str(self.ifStack.peek()[-1])  #
		self.ifStack.push(end)

		self.genUnBr(self.ifStack.peek())

		self.genLabel(elseVar)

	def genThen(self):		
		self.genUnBr(self.ifStack.peek())

		self.sentence.append(self.ifStack.peek()+": ")  
		self.writeToken()

		if (self.ifStack.peek()[0:3] == "end"):  #else+count
			self.ifStack.pop()
		self.ifStack.pop()  # remove ifFalse
		self.ifStack.pop()  # remove ifTrue

	# myList = [global,name,[global, type, name, in|out]]
	def genFunction(self,myList):
		writeList = []
		outList = []
		allocaList = []

		print "\nGenCode for procedure: ", myList
		scope = "%"

		if myList[0] == "global":
			scope = "@"
			myList = myList[1:]

		writeList.append(scope)
		funcName = myList[0]
		myList = myList[1:]
		writeList.append(funcName+"(")

		while len(myList) > 0:
			print "\nParameter list",myList
			if myList[0] == "global":
				if len(myList) > 4: 					 # or var is array e|or has more than 1 var
					if myList[3] not in ("in","out"):             # global and array

						writeList.append("["+myList[3]+" x "+ self.getType(myList[1])+"] @"+myList[2])

						allocaList.append([myList[1], self.temp, myList[2]]) # type, new Nemp
						self.addTemp(myList[2])
						
						if myList[4] == "out":
							outList.append(myList[1]) # type
							outList.append(myList[2]) # var
						myList = myList[5:]
						writeList.append(", ")
					else:										# global but not array  
						writeList.append(self.getType(myList[1])+" @"+myList[2])

						allocaList.append([myList[1], self.temp, myList[2]]) # type, new Nemp
						self.addTemp(myList[2])
						
						if myList[3] == "out":
							outList.append(myList[1]) # type
							outList.append(myList[2]) # var
						myList = myList[4:]	
						self.sentence.append(", ")
				else:  										# last parameter
					self.sentence.append(self.getType(myList[1])+" @"+myList[2])

					allocaList.append([myList[1], self.temp, myList[2]]) # type, new Nemp
					self.addTemp(myList[2])
					
					if myList[3] == "out":
						outList.append(myList[1]) # type
						outList.append(myList[2]) # var
					myList = myList[4:]
					
			else:
				if len(myList) > 3:   
					print "type", myList[2]
					if myList[2] not in ("in","out"):     # not global but array    
						writeList.append("["+myList[2]+" x "+ self.getType(myList[0])+"] %"+myList[1])

						allocaList.append([myList[0], self.temp, myList[1]]) # type, new Nemp
						self.addTemp(myList[1])
						
						if myList[3] == "out":
							outList.append(myList[0]) # type
							outList.append(myList[1]) # var
						myList = myList[4:]
						writeList.append(", ")
					else:									# not global, and not array
						writeList.append(self.getType(myList[0])+" %"+myList[1]) 

						allocaList.append([myList[0], self.temp, myList[1]]) # type, new Nemp
						self.addTemp(myList[1])
						
						if myList[2] == "out":
							outList.append(myList[0]) # type
							outList.append(myList[1]) # var
						myList = myList[3:]	
						print "list", myList
						print "outList", outList
						writeList.append(", ")
				else:  								# last parameter
					writeList.append(self.getType(myList[0])+" %"+myList[1])

					allocaList.append([myList[0], self.temp, myList[1]]) # type, new Nemp
					self.addTemp(myList[1])
					
					if myList[2] == "out":
						outList.append(myList[0]) # type
						outList.append(myList[1]) # var
					myList = myList[4:]

		writeList.append(") #0 {\n")
		writeList.append("entry:")
		if len(outList) > 0:
			returnType = self.getType(outList[0])
		else:
			returnType = "void"
		self.funcDic[funcName] = returnType

		self.sentence.append("; Function Attrs: nounwind\n")
		self.sentence.append("declare "+returnType+" ")
		self.sentence = self.sentence + writeList
		self.writeToken()

		# alloca all parameter list
		for l in allocaList:
			self.genDeclaration([l[0],l[1]])
			self.genStore([l[0],str(l[1])], [l[0],"%"+str(l[2])])
	
	def genUnBr(self, label):  # unconditional Branch
		self.sentence.append("br ")
		self.sentence.append("label %"+str(label))
		self.sentence.append("                                       ; Unconditional branch")	
		self.writeToken()
		self.skipLine()

	def genCoBr(self, cond, label1, label2):    # conditional Branch
		self.sentence.append("br i1 %")
		self.sentence.append(cond+", label %")
		self.sentence.append(label1+" ")
		self.sentence.append(", label %")
		self.sentence.append(label2)
		self.sentence.append("           ; Conditional branch")	
		self.writeToken()
		self.skipLine()
		self.genLabel(label1)

	def genLabel(self, label):
		self.sentence.append(str(label)+": ")	
		self.writeToken()

	def genReturn(self, var):
		typee = self.funcDic[var]

		self.sentence.append("ret ")
		if typee:  # vooid
			self.sentence.append(typee+" ")
			self.sentence.append("%"+str(self.temp-1))  # fix this temp
		else:
			self.sentence.append("void")

		self.sentence.append("\n}")
		self.writeToken()

	def isEmpty(self):
		if os.stat(self.filename).st_size == 0:
			return True
		else:
			return False

	def writeToken(self, var = False):
		
		if var:
			self.sentence.append(var)

		with open(self.filename,'a') as f:
			for t in self.sentence:
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


