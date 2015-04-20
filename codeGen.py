import os
from stack import Stack   

class CodeGen:
	
	def __init__(self, filename):
		self.filename = filename           
		self.sentence = []					# save sentence to be generated
		self.temp 	  = 1					# count for temporary variables
		self.tempDic  = {}					# sabe latest temporary variable for each variable already loaded.
		self.ifStack = Stack()				# Stack for If statement generation
		self.loopStack = Stack()			# Stack for Loop statement generation
		self.ifCount = 1					# count for If statement generation
		self.loopCount = 1					# count for Loop statement generation
		self.funcDic = {}					# save name of function, and its return type
		self.function = {}					# save function name, and its parameters var

	def createFile(self):
		file = open(self.filename,'a')

	# returns temporary variable for "var" variable, or false if it doesn't exist
	def getTemp(self, var):
		for k,v in self.tempDic.items():
			if k in (var, "@"+var, "%"+var):
				return v
		return False

	# increments count for temporary variables
	def setTemp(self):
		self.temp = self.temp + 1;

	# returns representation that goes with each type
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
			return "i8"			
		else:
			return False

	# generates header
	def genModule(self, filename):
		self.sentence.append("; ModuleID = "+filename+"\n")
		self.writeToken()

	# generates end of file
	def genEnd(self):
		self.sentence = []
		self.sentence.append("ret 0\n}\n")  # return for main function
		self.sentence.append("attributes #0 = { nounwind }")
		self.writeToken()

	# generates alloca instruction --> format: @|%var = alloca type, align 4 ... myList=[type, name]
	def genDeclaration(self, myList, parameter = False):
		print "GenCode for Declaration (alloca): ", myList
		
		scope = "%"
		if myList[0] == "global":
			scope  = "@"
			myList = myList[1:]

		varType = str(self.getType(myList[0]))
		name    = str(myList[1])
		
		self.sentence.append(scope)
		self.sentence.append(name+" = alloca ")

		if len(myList) > 2:  													# If array
			if parameter:
				self.sentence.append(varType+"*, align 4")  				    #  par = type *
			else: 											
				self.sentence.append("["+myList[2]+" x "+varType+"], align 4")  # no par = [size x type] 
		else:
			self.sentence.append(varType+", align 4")

		self.writeToken()

	# generates Store instruction --> result = [type, var,[size]], myList = [[global], vartype, name]
	def genStore(self, result, myList, inFunction = False, alloca = False):
		print "\nGenCode for Store: ", result, myList, inFunction, alloca, self.function
		scope = "%"
		if result[0] == "global":
			scope = "@"
			result = result[1:]

		varType = self.getType(result[0])
		name = result[1]

		if len(result) > 2:  								# array
			if not alloca:
				if self.function.has_key(inFunction):
					if name in self.function[inFunction]:	 # if is parameter var
						self.genLoad([result[0], "%"+str(self.getTemp(result[1]))], True)

				self.sentence.append("%"+str(self.temp))
				self.setTemp()
				if self.function.has_key(inFunction):
					if name in self.function[inFunction]:	 # if is parameter var
						self.sentence.append(" = getelementptr inbounds "+str(self.getType(result[0]))+"* %"+str(self.temp-2))
						self.sentence.append(", "+self.getType(result[0])+" "+str(result[3])+"\n")
				else:
					self.sentence.append(" = getelementptr inbounds ["+str(result[2])+" x "+str(self.getType(result[0]))+"]* %"+result[1])
					self.sentence.append(", "+self.getType(result[0])+" 0, "+self.getType(result[0])+" "+str(result[3])+"\n")

		self.sentence.append("store ")
		self.sentence.append(varType)
		if len(result) > 2 and alloca:  								# array
			self.sentence.append("*")

		if len(myList) == 2:   	 										# simple assignment [type, value]
			value = myList[1]  
			
			if myList[1][0] == "%":
				value = myList[1][1:] 

			print self.tempDic
			if self.getTemp(value):         							# if var is loaded
				self.sentence.append(" %"+str(self.getTemp(value))+", ")
			else:														# is literal
				self.sentence.append(" "+value+", ")					
		else: 											
			self.sentence.append(" %"+str(self.temp-1)+", ")

		self.sentence.append(varType)

		if len(result) > 2 and alloca:  								# array
			self.sentence.append("** ")
		else:
			self.sentence.append("* ")

		if inFunction:	
			if alloca:
				self.sentence.append(scope+name)												# should be temporary variable instead of variable

			elif name in self.function[inFunction] or len(result) > 2:		# parameter var	ou array					
				self.sentence.append("%"+str(self.temp-1))
			else:
				self.sentence.append(scope+name)		
			
		elif len(result) > 2:  # not function, but array
			self.sentence.append("%"+str(self.temp-1))
		else: 
			self.sentence.append(scope+name)

		self.sentence.append(", align 4")
		self.writeToken()

	# add new temporary variable for a variable
	def addTemp(self, name): 
		self.tempDic[name] = str(self.temp)
		print self.tempDic
		self.setTemp()

	#  generates Load instruction --> myList = [vartype, var]
	def genLoad(self, myList, isArrayFunction = False):
		print "\nGenCode for Load: ", myList, isArrayFunction										# add temporary var that goes with "name"

		varType = self.getType(myList[0])
		name = myList[1]

		if name[0] == "%":
			name = name[1:] 

		if len(myList) == 4:  # array in 
			if not isArrayFunction:
			#if not self.function.has_key(isArrayFunction):
			#	if myList[1] in self.function[isArrayFunction]:
				self.sentence.append("%"+str(self.temp))
				self.setTemp()

				self.sentence.append(" = getelementptr inbounds ["+str(myList[2])+" x "+varType+"]* %"+name)
				self.sentence.append(", "+varType+" 0, "+varType+" "+str(myList[3])+"\n")

		x = self.getTemp(name)  # previous temporary var for name
		self.addTemp(name) 
		self.sentence.append("%")
		self.sentence.append(str(self.getTemp(name)))
		self.sentence.append(" = load ")
		self.sentence.append(varType)

		if isArrayFunction:
			self.sentence.append("** ")
			if len(myList) == 4:  # array
				self.sentence.append("%"+str(x))
			else:
				self.sentence.append(name)
		else:
			self.sentence.append("* ")
			if len(myList) == 4:  # array
				self.sentence.append("%"+str(self.temp-2))
			else:
				self.sentence.append(name)

		self.sentence.append(", align 4")

		self.writeToken()

	# generates Call instruction --> myList = [[global], name, [type, var]
	def genCall(self, myList):  													
		print "\nGenCode for Call: ", myList
		write = [] 														# sentence to be generated

		scope = "%"

		if myList[0] == "global":
			scope = "@"
			myList = myList[1:]

		name = myList[0]
		myList = myList[1:]

		typee = self.funcDic[name]  									# Gets type of function return if it is not void
		if not typee:
			typee = "void"

		write.append("%")
		write.append(str(self.temp))
		self.setTemp()
		write.append(" = call ")
		write.append(typee+" ")
		write.append(scope)
		write.append(name+"(")

		for l in range(0,len(myList)-1,2):  							# loop over all function parameters

			write.append(self.getType(myList[l])+" ")
			if myList[l+1][0] in ("@","%"):  							# if var
				write.append("%"+str(self.getTemp(myList[l+1])))
			else:
				write.append(myList[l+1])

			if l < len(myList)-2:
				write.append(", ")

		write.append(")")
		self.sentence = write
		self.writeToken()

	# generates exprpession --> myList = [type, op1, signal, type, op2]
	def genExpression(self,myList):
		#if self.getCompOp(myList[2],myList[3]):
		#	self.genCompExp(myList)
		#elif self.getOp(myList[2],myList[3]):
		self.genAritmExpression(myList)

	#def genCompExp(self, myList):
	#	print "GenCode for Comp Exp", myList
	#	myList = myList[5:]
	#	print myList

	# generates exprpession --> myList = [type, op1, signal, type, op2]
	def genAritmExpression(self, myList):
		print "\nGenCode for Aritm Expression: ",myList

		if myList[0] == "global":
			myList = myList[1:]	

		if len(myList) > 2:  												# If expression has a operation

			while len(myList) > 0:      									# loop over all single-assignment expression
				self.sentence.append("%")
				self.sentence.append(str(self.temp))
				self.setTemp()
				self.sentence.append(" = ")
				self.sentence.append(self.getOp(myList[2],myList[3]))  		# <type, op>
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
				
				self.writeToken()
				myList = myList[3:]

				myList[1] = "%"+str(self.temp-1)		  						# result of previous operation

				if len(myList) == 2:
					myList = []

	# returns operator that goes with the code
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

	# returns operator that goes with the "op"
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

	# increments if count
	def setIfCount(self):
		self.ifCount = self.ifCount + 1;

	# increments loop count
	def setLoopCount(self):
		self.loopCount = self.loopCount + 1;

	# generates If statement
	def genIf(self):
		
		ifTrue = "ifTrue"+str(self.ifCount)  									# creates label ifTrue
		ifFalse = "ifFalse"+str(self.ifCount)									# creates label ifFalse
		self.setIfCount()
		
		self.ifStack.push(ifTrue)												# add label to ifStack
		self.ifStack.push(ifFalse)												# add label to ifStack

		self.genCoBr(str(self.temp-1), ifTrue, ifFalse)							# generates condicional branch

	# generates Else statement
	def genElse(self):
		elseVar = self.ifStack.peek() 											# gets ifFalse label from the top of ifStack

		end = "end"+str(self.ifStack.peek()[-1])  								# creates last character of the top (current ifCount)
		self.ifStack.push(end)													# add label to ifStack

		self.genUnBr(self.ifStack.peek())										# generates unconditional branch

		self.genLabel(elseVar)													# generates Else label

	# generates ifFalse statement 
	def genThen(self):		
		self.genUnBr(self.ifStack.peek())										# gene

		self.sentence.append(self.ifStack.peek()+": ")  
		self.writeToken()

		if (self.ifStack.peek()[0:3] == "end"):  #else+count
			self.ifStack.pop()
		self.ifStack.pop()  # remove ifFalse
		self.ifStack.pop()  # remove ifTrue

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
                                  
	# myList = [global,name,[global, type, name, in|out]]
	def genFunction(self, myList):
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
	
		if len(myList) == 1:
			myList = []
		else:
			myList = myList[1:]

		writeList.append(funcName+"(")

		while len(myList) > 0:
			print "\nParameter list",myList
			if myList[0] == "global":
				if len(myList) > 4: 					 # or var is array e|or has more than 1 var
					if myList[3] not in ("in","out"):             # global and array

						writeList.append(self.getType(myList[1])+"* @"+myList[2])

						allocaList.append([myList[1], self.temp, myList[2], myList[3]]) # type, new Nemp, var, size
						self.addTemp(myList[2])

						if self.function.has_key(funcName):  # add name of parameter
							self.function[funcName].append(myList[2])
						else:
							self.function[funcName] = [myList[2]]

						if myList[4] == "out":
							outList.append(myList[1]) # type
							outList.append(myList[2]) # var
						myList = myList[5:]
						writeList.append(", ")
					else:										# global but not array  
						writeList.append(self.getType(myList[1])+" @"+myList[2])

						allocaList.append([myList[1], self.temp, myList[2]]) # type, new Nemp
						self.addTemp(myList[2])

						if self.function.has_key(funcName):  # add name of parameter
							self.function[funcName].append(myList[2])
						else:
							self.function[funcName] = [myList[2]]
						
						if myList[3] == "out":
							outList.append(myList[1]) # type
							outList.append(myList[2]) # var
						myList = myList[4:]	
						self.sentence.append(", ")
				else:  										# last parameter
					self.sentence.append(self.getType(myList[1])+" @"+myList[2])

					allocaList.append([myList[1], self.temp, myList[2]]) # type, new Nemp
					self.addTemp(myList[2])

					if self.function.has_key(funcName):  # add name of parameter
							self.function[funcName].append(myList[2])
					else:
						self.function[funcName] = [myList[2]]
					
					if myList[3] == "out":
						outList.append(myList[1]) # type
						outList.append(myList[2]) # var
					myList = myList[4:]
					
			else:
				if len(myList) > 3:   
					if myList[2] not in ("in","out"):     # not global but array    
						writeList.append(self.getType(myList[0])+"* %"+myList[1])

						allocaList.append([myList[0], self.temp, myList[1], myList[2]]) # type, new Nemp, var, size
						self.addTemp(myList[1])
						
						if self.function.has_key(funcName):  # add name of parameter
							self.function[funcName].append(myList[1])
						else:
							self.function[funcName] = [myList[1]]

						if myList[3] == "out":
							outList.append(myList[0]) # type
							outList.append(myList[1]) # var
						myList = myList[4:]
						
						if len(myList) > 0:
							writeList.append(", ")
					else:									# not global, and not array
						writeList.append(self.getType(myList[0])+" %"+myList[1]) 

						allocaList.append([myList[0], self.temp, myList[1]]) # type, new Nemp
						self.addTemp(myList[1])

						if self.function.has_key(funcName):  # add name of parameter

							self.function[funcName].append(myList[1])
						else:
							self.function[funcName] = [myList[1]]
						
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

					if not self.function.has_key(funcName):  # add name of parameter
	
						self.function[funcName] = [myList[1]]
					else:
						self.function[funcName].append(myList[1])
					
					if myList[2] == "out":
						outList.append(myList[0]) # type
						outList.append(myList[1]) # var
					myList = myList[4:]

		writeList.append(") #0 {\n")
		writeList.append("entry:")

		if len(outList) > 0:
			returnType = self.getType(outList[0])
			self.funcDic[funcName] = [returnType,outList[1]]
		elif funcName == "main":
			returnType = "i32"
		else:
			returnType = "void"

		self.sentence.append("; Function Attrs: nounwind\n")
		self.sentence.append("declare "+returnType+" ")
		self.sentence = self.sentence + writeList
		self.writeToken()

		# alloca all parameter list
		for l in allocaList:								 # array
			if len(l) == 4:
				self.genDeclaration([l[0],l[1],l[3]], True) 
				self.genStore([l[0],str(l[1]),l[3]], [l[0],"%"+str(l[2])], funcName, True)
			else:
				self.genDeclaration([l[0],l[1]], True)
				self.genStore([l[0],str(l[1])], [l[0],"%"+str(l[2])], funcName, True)

		self.skipLine()
	
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

	def getFuncDic(self, var):
		if self.funcDic.has_key(var):
			return self.funcDic[var]
		else:
			return False

	def genReturn(self, var):
		print "GenCode for Return", var
		var = self.getFuncDic(var)

		self.sentence.append("\nret ")
		if var:  # void
			self.sentence.append(var[0]+" ")
			self.sentence.append("%"+self.getTemp(var[1]))  # fix this temp
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


