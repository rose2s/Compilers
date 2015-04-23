

genStore(result, myList)    --> result = [[global], type, name], myList = [type, name]
genDeclaration(myList)		--> myList = [[global], type, name]
genLoad(myList) 			--> myList = [type, name]

# Alloca command: <result> = alloca <type>[, i32 <NumElements>][, align <alignment>]     ; yields {type*}:result
# Load command:   <result> = load <ty>* <pointer>[, align <alignment>]
# Store Command:  store <ty> <value>, <ty>* <pointer>[, align <alignment>] 


	# Load command:   %temp = load <type>* <@|var> , align 4  			-->   %1 = load float* %y, align 4
	# Store Command:  store <type> <%temp>, <type>* <@|%var>, align 4   -->   store float %1, float* %x, align 4


	Limitations in Code Generation
	- single return values

	Restrition:
	- parameter list in call must be var, not expression


	FUncDic[funcName] = {type, var}  maintain all out var for this function