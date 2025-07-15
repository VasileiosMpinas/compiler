#BASILEIOS MPINAS, AM:4434. Username: cse84434
#NIKOLETTA MPINTZILAIOU, AM:4435. Username: cse84435
#-----------------------------------------------------------------------
#Dokimasame ta arxeia _test_parser.ci, ex1px1.ci, examspx2.ci, px3max.ci
#ta opoia trexoun kanonika kai paragetai o endiamesos kwdikas tous sta antistoixa arxeia me katalixi .int, 
#kathws kai o kwdikas ths main tous se C sta antistoixa arxeia me katalixi .c. 
#Ston parakatw kwdika perilambanetai to kommati gia ton lektiko analuth, ton suntaktiko analuth me thn 
#paragwgh tou endiamesou kwdika kai oti proodo kaname me ton pinaka symbolwn.
#Trexei me thn entolh px.python3 met_4434_4435.py examspx2.ci
#------------------------------------------------------------------------
from __future__ import print_function
from cProfile import label
from glob import glob
import string
import sys
from winreg import HKEY_LOCAL_MACHINE

class Quad:
	def __init__(self,number,operator, operand1, operand2, operand3):
		self.number = number
		self.operator = operator
		self.operand1 = operand1
		self.operand2 = operand2
		self.operand3 = operand3
		
	def genQuad(operator, operand1, operand2, operand3):
		global listOfQuads
		global num_q
		quad= Quad(num_q,operator, operand1, operand2, operand3)
		listOfQuads.append(quad)
		num_q+=1
	
	def nextQuad():
		global num_q
		return num_q

	def newTemp():
		global num_temp
		result="T_"+str(num_temp)
		num_temp+=1
		return result

	def emptyList():
		newlist=[]
		return newlist

	def makeList(label):
		labelList=[]
		labelList.append(label)
		return labelList
		
	def mergeList(list1, list2):
		list=list1+list2
		return list

	def backpatch(list,label): #where list is a list of quads
		global listOfQuads
		for x in list:
			updQuad=listOfQuads[x-1]
			updQuad.operand3=label
		list=[]
		return list
	
	def printQuad(quad):
		print(quad.number, end=": ")
		print(quad.operator, end=" ,")
		print(quad.operand1, end=" ,")
		print(quad.operand2, end=" ,")
		print(quad.operand3, end="\n")
		
	def printList(): #for testing
		global listOfQuads
		for i in listOfQuads:
			Quad.printQuad(i)
			
	def forOutput():
		global listOfQuads
		global listOfQuadsToBePrinted
		for quad in listOfQuads:
			iter=str(quad.number)
			listOfQuadsToBePrinted.append(iter)
			listOfQuadsToBePrinted.append(': ')
			iter=quad.operator
			listOfQuadsToBePrinted.append(iter)
			listOfQuadsToBePrinted.append(', ')
			iter=str(quad.operand1)
			listOfQuadsToBePrinted.append(iter)
			listOfQuadsToBePrinted.append(', ')
			iter=str(quad.operand2)
			listOfQuadsToBePrinted.append(iter)
			listOfQuadsToBePrinted.append(', ')
			iter=str(quad.operand3)
			listOfQuadsToBePrinted.append(iter)
			listOfQuadsToBePrinted.append('\n ')

	def forOutputSymb():
		global symbol_matrix
		global formal_matrix
		global symbol_matrix_to_print
		global listVal
		value=listVal
		for i in range(0, len(symbol_matrix)):
			if len(symbol_matrix[i])!=0:
				symbol_matrix_to_print.append(str(value))
				symbol_matrix_to_print.append(':')
				for j in range(0, len(symbol_matrix[i])):
					symbol_matrix_to_print.append(str(symbol_matrix[i][j][0])+' ')
				value-=1
				
				symbol_matrix_to_print.append('\n')
		symbol_matrix_to_print.append('##########################################')
		symbol_matrix_to_print.append('\n')
			
	def forOutputAsm():
		global offset
		### final_code ####

		global finalCodeList
		global FCL_print
		global framelength_main_Pos
		FCL_print.append("L0:   j main\n")
		for i in range(0, len(finalCodeList)):
			FCL_print.append(finalCodeList[i])
			FCL_print.append('\n')
		FCL_print[2*framelength_main_Pos-1]+=str(offset)


	def forOutputC(output_name):
		global listOfQuads
		global name_token
		alpha=string.ascii_letters
		listOfVar=[]
		listOfMainQuads=[]
		f = open(output_name, "w")
		f.write("#include <stdio.h>\nint main()\n{\n")
		f.close()
		f = open(output_name, "a")
		flagNotMain=0
		for quad in listOfQuads:
			qn=quad.number
			q0=quad.operator
			q1=quad.operand1
			q2=quad.operand2
			q3=quad.operand3
			if quad.operator=='begin_block' and quad.operand1!=str(name_token):
				flagNotMain=1
			elif quad.operator=='begin_block' and quad.operand1==str(name_token):
					flagNotMain=0
			else:
				if flagNotMain!=1:
					stq1= str(q1)
					if str(q1) in alpha and str(q1) not in listOfVar:
						listOfVar.append(q1)
						listOfMainQuads.append(quad)
					elif str(q2) in alpha and str(q2) not in listOfVar:
						listOfVar.append(q2)
						listOfMainQuads.append(quad)
					elif str(q3) in alpha:
						if q3 not in listOfVar:
							listOfVar.append(q3)
						listOfMainQuads.append(quad)
					elif q0=='jump':
						listOfMainQuads.append(quad)
					elif q0 in ["=","<=" ,">=" ,">","<","<>"]:
						if 'T_'==stq1[:2]:
							listOfVar.append(q1)
						listOfMainQuads.append(quad)
					else:
						pass
		temp_int='\tint '			
		for var in listOfVar:
			temp_int+=var+' ,'
			if var==listOfVar[-1]:
				temp_int=temp_int[:-1]
		temp_int+=";\n"
		f.write(temp_int)
		the_string=''
		for a_quad in listOfMainQuads:
			qn=a_quad.number
			q0=a_quad.operator
			q1=a_quad.operand1
			q2=a_quad.operand2
			q3=a_quad.operand3
			if a_quad.operator==':=':
				the_string="\tL_"+str(qn)+": "+str(q3)+"="+str(q1)+";\n"+" "

			elif a_quad.operator in ['+','-','*','/']:
				the_string="\tL_"+str(qn)+": "+str(q3)+"="+str(q1)+a_quad.operator+str(q2)+";\n"
			elif a_quad.operator in ["=","<=" ,">=" ,">","<","<>"]:
				if a_quad.operator=='=':
					the_string="\tL_"+str(qn)+": if ("+str(q1)+"=="+str(q2)+") goto L_"+str(q3)+"; \n"
				elif a_quad.operator=="<>":
					the_string="\tL_"+str(qn)+": if ("+str(q1)+"!="+str(q2)+") goto L_"+str(q3)+"; \n"
				else:
						the_string="\tL_"+str(qn)+": if ("+str(q1)+a_quad.operator+str(q2)+") goto L_"+str(q3)+"; \n"
			elif a_quad.operator=='jump':
				the_string="\tL_"+str(qn)+": goto L_"+str(q3)+"; \n"
			elif a_quad.operator=='out':
				the_string="\tL_"+str(qn)+": printf(\"%d\","+str(q1)+"); \n"
			elif a_quad.operator=='ret':	
				the_string="\tL_"+str(qn)+": return ("+str(q1)+"); \n"
			elif a_quad.operator=='halt':
				the_string="\tL_"+str(qn)+": return 0; \n"
			else:
				pass
			f.write(the_string)
		num=str(qn+1)
		f.write("\tL_"+num+": {}\n}")
		f.close()

class Token:
	def __init__(self,recognized_string, family, line_number):
		self.recognized_string = recognized_string
		self.family = family
		self.line_number = line_number

class Lex:
	def __init__(self,file_name):
		self.file_name = file_name
		self.parser = 0
		self.line_number=1
	
	def f_error(prev_st,char,inp,line_number):
				print('Lexical error!')
				if prev_st==0 or prev_st==2 and inp==22:#NIL
						print('Foreign char found at line: ',line_number)
						print('This character does not belong in the C-imple language: ',char)
				elif prev_st==1 and inp==1: 			#incorect number
						print('Incorrect number found at line: ',line_number)
						print('Was looking for digit but found letter: ',char)
				elif prev_st==3 and inp==21: 			#rem-comments don't close
						print('Was waiting to close comments but found eof at line: ',line_number)
				elif prev_st==4 and inp!=4: 			#asg
						print('Incomplete assignment found at line: ',line_number)
						print('Was waiting for = to complete assignment but found char: ',char)
				elif prev_st==1 and inp==0:				#out of bounds number
						print('Invalid number found at line: ',line_number)
						print('Number is out of bounds!')
				else:
						print('Invalid string found at line: ',line_number)
				exit()
	
	def lex(self):
		file_name=self.file_name
		file = open(file_name, "r") 
		digits=string.digits#[0,1,2,3,4,5,6,7,8,9]
		alpha=string.ascii_letters
		delim=['.',',',';']
		brack=['(',')','{','}','[',']']
		#-----------non final states
		start=0     #first state
		dig=1		
		idk=2
		rem=3
		asg=4
		smaller=5
		larger=6
		#-------------final states
		relOp=10
		delimeter=11
		grpSymbol=12
		addOp=13 
		mulOp=14
		assignment=15
		idORkey=16	#identfier or keyword
		number=17
		error=-1	
		eof=-2		#end of file 	
		nil=-3		#Not In Language

		Trans_Diagram=[[dig,idk,rem,asg,relOp,smaller,larger,delimeter,grpSymbol,addOp,mulOp,start,eof,error],
					[dig,error,number,number,number,number,number,number,number,number,number,number,number,number],
					[idk,idk,idORkey,idORkey,idORkey,idORkey,idORkey,idORkey,idORkey,idORkey,idORkey,idORkey,idORkey,idORkey],
					[rem,rem,start,rem,rem,rem,rem,rem,rem,rem,rem,rem,error,rem],
					[error,error,error,error,assignment,error,error,error,error,error,error,error,error,error],
					[relOp,relOp,relOp,error,relOp,error,relOp,error,relOp,error,error,relOp,error,error],
					[relOp,relOp,relOp,error,relOp,error,error,error,relOp,error,error,relOp,error,error]]
		rsrv_words=['program','declare','if','else','while','switchcase','forcase','incase','case','default','not','and','or','function','procedure','call','return','in','inout','input','print']
		returned_string=''
		inp=0
		code=0
		state=start
		prev_st=start
	
		while(state>=0 or state<18):		#while in start or not final state
			file.seek(self.parser)
			char=file.read(1)
			if char=='': 					# END OF FILE
				inp=12
			elif char in string.whitespace:
				inp=11
			elif char in digits:
				inp=0
			elif char in alpha:
				inp=1	
			elif char=='#':
				inp=2
			elif char==':':
				inp=3
			elif char=='=':
				inp=4
			elif char=='<':
				inp=5
			elif char=='>':
				inp=6
			elif char in delim: 			#comments/reminders
				inp=7
			elif char in brack:
				inp=8
			elif char=='+' or char=='-':
				inp=9
			elif char=='*' or char=='/':
				inp=10
			else:
				inp=13 						#NIL
			prev_st=state		

			state=Trans_Diagram[state][inp]	#change state
			if state==-1: 					#ERROR
				Lex.f_error(prev_st,char,inp,self.line_number)
				object=Token('','error',self.line_number)
				return object
			elif state==-2:					#EOF
				object=Token('eof','eof',self.line_number)
				return object
			elif state==3:
				self.parser+=1
			elif state==asg:
				self.parser+=1
			elif state==smaller or state==larger:
				file.seek(self.parser+1)
				next_c=file.read(1)		
				if (char=='<' and next_c=='=') or (char=='<' and next_c=='>'):
					self.parser+=1
					file.seek(self.parser)
					returned_string+=char
				elif (char=='>' and next_c=='='):
					self.parser+=1
					file.seek(self.parser)
					returned_string+=char
				else:
					self.parser+=1
					returned_string+=char
					object=Token(returned_string,'REL_OP',self.line_number)
					return object
			elif state==idk or state==dig:	#peeks at next symbol,doesn't use it
				file.seek(self.parser+1)
				next_c=file.read(1)		
				if state==dig and next_c in alpha:
					returned_string+=char
					Lex.f_error(state,next_c,1,self.line_number)
					state=-1
					object=Token('','error',self.line_number)
					return object
				if next_c not in digits and next_c not in alpha:
					self.parser+=1
					returned_string+=char
					lim=pow(2, 32)-1
					if state==dig and int(returned_string) not in range(-lim, lim+1):#check if number is valid
						Lex.f_error(state,char,0,self.line_number)
						state=-1
						object=Token('','error',self.line_number)
						return object
					elif state==idk and len(returned_string)>30:	#check if id/keyword is valid
						Lex.f_error(state,char,1,self.line_number)
						state=-1
						object=Token('','error',self.line_number)
						return object
					else: 
						if state==idk:
							state=16
							if returned_string in rsrv_words:
								object=Token(returned_string,'keyword',self.line_number)
							else:	
								object=Token(returned_string,'identifier',self.line_number)
						else: 
							state=17
							object=Token(returned_string,'number',self.line_number)
					return object
				else:
					self.parser+=1
					file.seek(self.parser)
					returned_string+=char
			elif state==start:
				file.seek(self.parser+1)
				next_c=file.read(1)
				if char=='\n' and next_c=='\n':
					self.line_number+=1	#change line
					self.parser+=2
				elif char=='\n':
					self.line_number+=1	
					self.parser+=1
				else:
					self.parser+=1
			elif state==15:
				self.parser+=1
				temp=':'+char
				returned_string+=temp
				object=Token(returned_string,'assignment',self.line_number)
				return object
			else:
				self.parser+=1
				returned_string+=char
				if state==delimeter:
					object=Token(returned_string,'delimeter',self.line_number)
				elif state==grpSymbol: 
					object=Token(returned_string,'grpSymbol',self.line_number)
				elif state==relOp:
					object=Token(returned_string,'REL_OP',self.line_number)
				elif state==addOp: 
					object=Token(returned_string,'ADD_OP',self.line_number)
				else: 	
					object=Token(returned_string,'MUL_OP',self.line_number)
				return object

class syntax:
	def get_token(obj1):
		token=obj1.lex()
		listOftokens.append(token)
		return token

	def syntax_analyzer(file_name):
		global token
		global obj1
		obj1=Lex(file_name)
		token=obj1.lex()
		syntax.program()
		print('Read all lines without error.')
		print('Compilation of C-imple program successfully completed!')
		
	def program():
		global token
		global file_name
		global name_token
		global id_place
		global listOfProgId
		if token.recognized_string == 'program':
				token = syntax.get_token(obj1)
				if token.family == 'identifier':
					id_place=syntax.ID(id_place)
					name_token=id_place
					listOfProgId.append(name_token) #add main prog id
					syntax.programBlock()
					if token.recognized_string == '.':
						token = syntax.get_token(obj1)
						if token.recognized_string == 'eof':
												token = syntax.get_token(obj1)
						else:
							print('Syntax error at line: ',token.line_number)
							print('Unexpected character found after .')
							exit()
					else:   
						print('Syntax error at line: ',token.line_number)
						print('Expected . to end program but found: ',token.recognized_string)
						exit()
				else:
					print('Program name/identifier expected at line: ',token.line_number)
					print('Instead found: ',token.family)
					exit()
		else:
			print('Syntax error. The keyword program was expected at line: ',token.line_number)
			exit()
	
	def programBlock():
		global token
		global file_name
		global id_place
		global name_token
		global listOfProgId
		#### symbol_matrix ####
		global offset
		global symbol_matrix
		global formal_matrix
		global listVal
		global formVal
		global FuncName
		#### final_code ####
		global finalCodeList
		global func_label
		if token.recognized_string == "{":
			token = syntax.get_token(obj1)
			syntax.declarations()
			syntax.subprograms()
			i=len(listOfProgId)-1
			if i==0:
				#IN MAIN BODY
				Quad.genQuad("begin_block",name_token,"_","_")
				#### final_code ####
				Label=FinalCode.newLabel()
				finalCodeList.append("main:")
				finalCodeList.append(Label+":	addi sp,sp,")
				framelength_main_Pos=len(finalCodeList)
				finalCodeList.append("		mv gp,sp")
			else:
				#NOT IN MAIN BODY
				Quad.genQuad("begin_block",listOfProgId[i],"_","_")
				result=Procedure_Function.updateFrame(0)
				symbol_matrix[listVal-1].append(result)

				Label=FinalCode.newLabel()
				finalCodeList.append(Label+":	sw ra, -0(sp)")
				func_label.append([Label,listOfProgId[i]])
				finalCodeList[framelength_main_Pos]+=str(offset)
				
			syntax.blockstatements()
			i=len(listOfProgId)-1
			if i==0:
				#IN MAIN BODY
				Quad.genQuad("halt","_","_","_")
				Quad.genQuad("end_block",name_token,"_","_")
				#### final_code ####
				Label=FinalCode.newLabel()
				finalCodeList.append(Label+":	li a0,0")
				finalCodeList.append("		li a7,93")
				finalCodeList.append("		ecall")
			else:
				#NOT IN MAIN BODY
				Quad.genQuad("end_block",listOfProgId[i],"_","_")
				listOfProgId.pop()
			#### final_code ####
			Label=FinalCode.newLabel()
			finalCodeList.append(Label+':	')
			finalCodeList[len(finalCodeList)-1]+='lw ra, -0(sp)'	
			finalCodeList.append('		jr ra')
				
			if token.recognized_string == "}":
				if len(formal_matrix)>0:
					while len(formal_matrix)>0:
						symbol_matrix[formVal].append(formal_matrix[-1])
						formal_matrix.pop()
				Scope.makeMatrix(0)
				output_name=file_name[:-3]+'.symb'
				Quad.forOutputSymb()
				f = open(output_name, "w")
				for z in symbol_matrix_to_print:
					f.write(z)
				listVal-=1
				symbol_matrix.reverse()
				symbol_matrix.pop()
				token= syntax.get_token(obj1)
			else:
				print('Syntax error at line: ',token.line_number)
				print('Expected } to end programBlock but found: ',token.recognized_string)
				exit()
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected { to start programBlock but found: ',token.recognized_string)
			exit()

	def declarations():
		global token
		global symbol_matrix
		global offset
		global listVal
		while token.recognized_string== 'declare':
			token = syntax.get_token(obj1)
			result=Variable.funcV(0)
			symbol_matrix[listVal].append(result)
			syntax.varlist()
			if token.recognized_string== ';':
					token = syntax.get_token(obj1)
			else:
					print('Syntax error at line: ',token.line_number)
					print('Expected ; after varlist but found: ',token.recognized_string)
					exit()
			
	def varlist():
		global token
		global id_place
		global listVal
		if token.family == "identifier":
				id_place=syntax.ID(id_place) 
				while token.recognized_string== ',':
						token = syntax.get_token(obj1)
						result=Variable.funcV(0)#
						symbol_matrix[listVal].append(result)
						if token.family == "identifier":
								id_place=syntax.ID(id_place)
			
	
	def subprograms():
		global token
		while token.recognized_string =="function" or token.recognized_string=="procedure":
			syntax.subprogram()
	
	def subprogram():
		global token
		global id_place
		global listOfProgId
		global listVal
		global formVal
		global FuncName
		global symbol_matrix
		global formal_matrix
		if token.recognized_string == "function" or token.recognized_string=="procedure":
			token = syntax.get_token(obj1)
			FuncName=token.recognized_string
			Scope.addNewLayer(0)
			formVal=listVal
			listVal+=1
			if token.family =="identifier":
				id=syntax.ID(id_place)
				listOfProgId.append(id)
				if token.recognized_string == "(":
					token = syntax.get_token(obj1)
					syntax.formalparlist()
					if token.recognized_string == ")":					
						token = syntax.get_token(obj1)
						syntax.programBlock()
					else:
						print('Syntax error at line: ',token.line_number)
						print('Expected ) after formalparlist but found: ',token.recognized_string)
						exit()
				else:
					print('Syntax error at line: ',token.line_number)
					print('Expected ( after id but found: ',token.recognized_string)
					exit()
			else:
				print('Name/identifier expected at line: ',token.line_number)
				print('Instead found token of family: ',token.family)
				exit()
		else:
			print('Procedure or function name/identifier expected at line: ',token.line_number)
			print('Instead found : ',token.recognized_string)
			exit()

	def formalparlist():
		global token
		if token.recognized_string =="in" or token.recognized_string =="inout":
			syntax.formalparitem()
			result=Parameter.funcP(0)
			symbol_matrix[listVal].append(result)
			while token.recognized_string == ',':
				token = syntax.get_token(obj1)
				syntax.formalparitem()
				result=Parameter.funcP(0)
				symbol_matrix[listVal].append(result)
				
	
	def formalparitem():
		global token
		global id_place
		global FormMode
		global FormName
		global formal_matrix
		global symbol_matrix
		if token.recognized_string == "in" or token.recognized_string == "inout":
			if token.recognized_string == "in":
				FormMode='CV'
			elif token.recognized_string == "inout":
				FormMode='REF'
			token = syntax.get_token(obj1)
			if token.family == "identifier":
				id_place=syntax.ID(id_place)
				FormName=id_place
				FormalParameter.printFormalParameter(0)
				
			else:
				print('Name/identifier expected at line: ',token.line_number)
				print('Instead found token of family: ',token.family)
				exit()
		else:
			print('In/inout expected at line: ',token.line_number)
			print('Instead found: ',token.recognized_string)
			exit()

	def statement():
			global token
			if token.family == "identifier":
					syntax.assignStat()
			elif token.recognized_string == "if":
					syntax.ifStat()
			elif token.recognized_string == "while":
					token = syntax.get_token(obj1)
					syntax.whileStat()
			elif token.recognized_string == "switchcase":
					token = syntax.get_token(obj1)
					syntax.switchcaseStat()
			elif token.recognized_string == "forcase":
					token = syntax.get_token(obj1)
					syntax.forcaseStat()
			elif token.recognized_string == "incase":
					token = syntax.get_token(obj1)
					syntax.incaseStat()
			elif token.recognized_string == "call":
					token = syntax.get_token(obj1)
					syntax.callStat()
			elif token.recognized_string == "return":
					token = syntax.get_token(obj1)
					syntax.returnStat()
			elif token.recognized_string == "input":
					token = syntax.get_token(obj1)
					syntax.inputStat()
			elif token.recognized_string == "print":
					token = syntax.get_token(obj1)
					syntax.printStat()
			else:
				pass

	def statements():
			global token
			if token.recognized_string == "{":
					token = syntax.get_token(obj1)
					syntax.statement()
					while token.recognized_string == ';':
							token = syntax.get_token(obj1)
							syntax.statement()
					if token.recognized_string == "}":
							token = syntax.get_token(obj1)
					else:
							print('Syntax error at line: ',token.line_number)
							print('Expected } after statement-loop but found: ',token.recognized_string)
							exit()
			else:
					syntax.statement()
					if token.recognized_string == ";":
							token = syntax.get_token(obj1)
					else:
							print('Syntax error at line: ',token.line_number)
							print('Expected ; after statement but found: ',token.recognized_string)
							exit()
	
	def blockstatements():
		global token
		syntax.statement()
		while token.recognized_string == ';':
			token = syntax.get_token(obj1)
			syntax.statement()
	
	def condition(): 
		global token
		global b_list_true
		global b_list_false
		global q_list_true
		global q_list_false
		global tempQ_list_true
		global tempQ_list_false
		global tempQ_true_created
		global tempQ_false_created
		####### final_code_globals #####
		global r_final_list_true
		global r_final_list_false
		global labelNum
		global labelsList
		global listOfQuads
		global orand_count
		syntax.boolterm()#Q1 
		b_list_true=q_list_true
		b_list_false=q_list_false
		while token.recognized_string == 'or':
			b_list_false=Quad.backpatch(b_list_false,Quad.nextQuad())#P2
			token = syntax.get_token(obj1)
			tempQ_false_created=0
			tempQ_true_created=0
			syntax.boolterm() 
			#P3
			b_list_true=Quad.mergeList(b_list_true,tempR_list_true)
			b_list_false=tempQ_list_false

			#### final_code ####
			nextLabel=FinalCode.newLabel()
			labelNum-=1
			for i in range(0, len(r_final_list_true)):
				finalCodeList[r_final_list_true[0]]+=nextLabel
				r_final_list_true.pop(0)

			for i in range(0, len(r_final_list_false)):
				finalCodeList[r_final_list_false[0]]+=labelsList[0]
				r_final_list_false.pop(0)
				labelsList.pop(0)
			
			orand_count+=1
			####################


	def ifStat():
		global token
		global r_list_true
		global r_list_false
		global b_list_false
		global b_list_true
		#### final_code_globals ####
		global ifVal
		global finalCodeList
		global skipLabel
		global labelNum
		global r_final_list_true
		global r_final_list_false
		global orand_count

		token = syntax.get_token(obj1)
		if token.recognized_string == '(':
			token = syntax.get_token(obj1)
			syntax.condition()
			if token.recognized_string == ')':
				#P1
				b_list_true=Quad.backpatch(b_list_true,Quad.nextQuad())
				token = syntax.get_token(obj1)
				nextLabel=FinalCode.newLabel()
				labelNum-=1
				if orand_count==0:
					r_list_true=Quad.backpatch(r_list_true,Quad.nextQuad())
					finalCodeList[r_final_list_true[0]]+=nextLabel
					r_final_list_true.pop(0)
					
				else:
					b_list_true=Quad.backpatch(b_list_true,Quad.nextQuad())
					orand_count=0
				syntax.statements()
				#P2
				ifList=Quad.makeList(Quad.nextQuad())
				Quad.genQuad('jump','_','_','_')
				#### final_code ####
				Label=FinalCode.newLabel()
				finalCodeList.append(Label+":	j  ")

				FCL_iflist=len(finalCodeList)-1
				####################
				
			else:
				print('Syntax error at line: ',token.line_number)
				print('Expected ) after condition but found: ',token.recognized_string)
				exit()
			#
			
			syntax.elsepart()
			ifList=Quad.backpatch(ifList,Quad.nextQuad())

			skipLabel=FinalCode.newLabel()
			labelNum-=1
			if orand_count==0:
				r_list_false=Quad.backpatch(r_list_false,Quad.nextQuad())
				for i in range(0, len(r_final_list_false)):
					finalCodeList[r_final_list_false[0]]+=skipLabel
					r_final_list_false.pop(0)
			else:
				b_list_false=Quad.backpatch(b_list_false,Quad.nextQuad())
				orand_count=0	
			finalCodeList[FCL_iflist]+=skipLabel

			#### arxikopoiisi pinakwn ####
			
			r_final_list_false=[]
			

		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected ( after if but found: ',token.recognized_string)
			exit()
	
	def elsepart():
		global token
		global labelNum
		if token.recognized_string == 'else':
			token = syntax.get_token(obj1)
			syntax.statements()


	def whileStat():
		global token
		global r_list_true
		global r_list_false
		global b_list_true
		global b_list_false
		global q_list_true
		global q_list_false
		global finalCodeList
		global FuncName
		whcond_list_true=[]
		whcond_list_false=[]
		global tempQ_list_false
		#### final_code_global ####
		global labelNum
		global r_final_list_true
		global r_final_list_false
		global orand_count
		############################
		b_quad=''
		fcode_list=[]
		if token.recognized_string == "(":
			token = syntax.get_token(obj1)
			#P1
			condQuad=Quad.nextQuad()
			loopLabel=FinalCode.newLabel()
			labelNum-=1
			
			syntax.condition()
			whcond_list_true=b_list_true
			whcond_list_false=b_list_false
			if token.recognized_string == ")":
				#P2
				whcond_list_true=Quad.backpatch(whcond_list_true,Quad.nextQuad())
				token = syntax.get_token(obj1)
				nextLabel=FinalCode.newLabel()
				labelNum-=1
				if orand_count==0:
						r_list_true=Quad.backpatch(r_list_true,Quad.nextQuad())
						finalCodeList[r_final_list_true[0]]+=nextLabel
						r_final_list_true.pop(0)
				else:
					b_list_true=Quad.backpatch(b_list_true,Quad.nextQuad())
					orand_count=0
				syntax.statements()
				#P3
				Quad.genQuad('jump','_','_',condQuad)
				Label=FinalCode.newLabel()

				finalCodeList.append(Label+":	j "+loopLabel)
				whcond_list_false=Quad.backpatch(whcond_list_false,Quad.nextQuad())
			else:
				print('Syntax error at line: ',token.line_number)
				print('Expected ) after condition but found: ',token.recognized_string)
				exit()
			skipLabel=FinalCode.newLabel()
			labelNum-=1
			if orand_count==0:
				r_list_false=Quad.backpatch(r_list_true,Quad.nextQuad())
				for i in range(0, len(r_final_list_false)):
					finalCodeList[r_final_list_false[0]]+=skipLabel
					r_final_list_false.pop(0)
			else:
				b_list_false=Quad.backpatch(b_list_true,Quad.nextQuad())
				orand_count=0
			fcode_list.append('j '+str(FuncName))
			
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected ( after while but found: ',token.recognized_string)
			exit()

	def switchcaseStat():
		global token
		global r_list_true
		global r_list_false
		global b_list_true
		global b_list_false
		#### final_code ####
		global finalCodeList
		global labelNum
		global r_final_list_true
		global r_final_list_false
		global orand_count
		####################
		exitList=Quad.emptyList()#P0
		FCL_switchlist=[]
		while token.recognized_string == "case":
			token = syntax.get_token(obj1)
			if token.recognized_string == "(":
				token = syntax.get_token(obj1)
				syntax.condition()
				if token.recognized_string == ")":
					#P1
					if orand_count==0:
						r_list_true=Quad.backpatch(r_list_true,Quad.nextQuad())
					else:
						b_list_true=Quad.backpatch(b_list_true,Quad.nextQuad())
					token = syntax.get_token(obj1)
					#### final_code ####
					nextLabel=FinalCode.newLabel()
					labelNum-=1
					###################
					syntax.statements()
					#P2
					t=Quad.makeList(Quad.nextQuad())
					Quad.genQuad('jump','_','_','_')

					finalCodeList.pop(len(finalCodeList)-1)
					Label=FinalCode.newLabel()
					finalCodeList.append(Label+":	j  ")
					FCL_switchlist.append(len(finalCodeList)-1)
					exitList=Quad.mergeList(exitList,t)
					b_list_false=Quad.backpatch(b_list_false,Quad.nextQuad())
					if orand_count==0:
						r_list_false=Quad.backpatch(r_list_true,Quad.nextQuad())
					else:
						b_list_false=Quad.backpatch(b_list_true,Quad.nextQuad())

				else:
					print('Syntax error at line: ',token.line_number)
					print('Expected ) after condition but found: ',token.recognized_string)
					exit()
			else:
				print('Syntax error at line: ',token.line_number)
				print('Expected ( after case but found: ',token.recognized_string)
				exit()

			skipLabel=FinalCode.newLabel()
			labelNum-=1
			if orand_count==0:
				skipLabel=FinalCode.newLabel()
				labelNum-=1
				finalCodeList[r_final_list_true[0]]+=nextLabel
				r_final_list_true.pop(0)
				for i in range(0, len(r_final_list_false)):
					finalCodeList[r_final_list_false[0]]+=skipLabel
					r_final_list_false.pop(0)
			else:
				orand_count=0
			
		if token.recognized_string == "default":
				token = syntax.get_token(obj1)
				syntax.statements()
				#P3
				exitList=Quad.backpatch(exitList,Quad.nextQuad())
		else:
				print('Syntax error at line: ',token.line_number)
				print('Expected default but found: ',token.recognized_string)
				exit()
		skipLabel=FinalCode.newLabel()
		labelNum-=1
		for i in range(0, len(FCL_switchlist)):
			finalCodeList[FCL_switchlist[i]]+=skipLabel
		FCL_switchlist=[]

	def forcaseStat():
		global token
		global r_list_true
		global r_list_false
		global b_list_true
		global b_list_false
		#### final_code ####
		global labelNum
		global r_final_list_true
		global r_final_list_false
		global orand_count
		firstCondQuad=Quad.nextQuad()
		loopLabel=FinalCode.newLabel()
		labelNum-=1
		while token.recognized_string == "case":
			token = syntax.get_token(obj1)
			if token.recognized_string == "(":
				token = syntax.get_token(obj1)
				syntax.condition()
				if token.recognized_string == ")":
					token = syntax.get_token(obj1)
					if orand_count==0:
						r_list_true=Quad.backpatch(r_list_true,Quad.nextQuad())
					else:
						b_list_true=Quad.backpatch(b_list_true,Quad.nextQuad())
					nextLabel=FinalCode.newLabel()
					labelNum-=1
				
					syntax.statements()
					Quad.genQuad('jump','_','_',firstCondQuad)
					#### final_code ####
					Label=FinalCode.newLabel()
					finalCodeList.append(Label+":	j "+loopLabel)
					if orand_count==0:
						r_list_false=Quad.backpatch(r_list_false,Quad.nextQuad())
					else:
						b_list_false=Quad.backpatch(b_list_false,Quad.nextQuad())

				else:
					print('Syntax error at line: ',token.line_number)
					print('Expected ) after condition but found: ',token.recognized_string)
					exit()

				skipLabel=FinalCode.newLabel()
				labelNum-=1
				if orand_count==0:
					skipLabel=FinalCode.newLabel()
					labelNum-=1
					finalCodeList[r_final_list_true[0]]+=nextLabel
					r_final_list_true.pop(0)
					for i in range(0, len(r_final_list_false)):
						finalCodeList[r_final_list_false[0]]+=skipLabel
						r_final_list_false.pop(0)
				else:
					orand_count=0
			else:
				print('Syntax error at line: ',token.line_number)
				print('Expected ( after case but found: ',token.recognized_string)
				exit()
		if token.recognized_string == "default":
			token = syntax.get_token(obj1)
			syntax.statements()
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected default but found: ',token.recognized_string)
			exit()

	def incaseStat():
		global token
		global r_list_true
		global r_list_false
		global b_list_true
		global b_list_false
		#### symbol_matrix ####
		global symbol_matrix
		#### final_code ####
		global finalCodeList
		global r_final_list_true
		global r_final_list_false
		global orand_count
		global labelNum
		global Tcall
		exitList=Quad.emptyList()
		FCL_incaselist=[]
		incaseFlag=Quad.newTemp()
		firstCondQuad=Quad.nextQuad()
		loopLabel=FinalCode.newLabel()
		while token.recognized_string == "case":
			token = syntax.get_token(obj1)
			Quad.genQuad(':=',0,'_',incaseFlag)
			Tcall=incaseFlag
			print(incaseFlag)
			result=Variable.funcV(0)
			symbol_matrix[listVal].append(result)
			Tcall=""
			Label=FinalCode.newLabel()
			finalCodeList.append(Label+':    ')
			backPos=len(finalCodeList)-1
			nextPos=len(finalCodeList)
			FinalCode.loadvr(incaseFlag, "t1")
			if len(finalCodeList)>nextPos:
				finalCodeList[backPos]+=finalCodeList[nextPos]
				finalCodeList.pop(nextPos)
			FinalCode.storerv("t1", incaseFlag)
			if token.recognized_string == "(":
					token = syntax.get_token(obj1)
					syntax.condition()
					if token.recognized_string == ")":
							token = syntax.get_token(obj1)
							if orand_count==0:
								r_list_true=Quad.backpatch(r_list_true,Quad.nextQuad())
							else:
								b_list_true=Quad.backpatch(b_list_true,Quad.nextQuad())

							nextLabel=FinalCode.newLabel()
							labelNum-=1
							syntax.statements()
							t=Quad.makeList(Quad.nextQuad())
							exitList=Quad.mergeList(exitList,t)
							b_list_false=Quad.backpatch(b_list_false,Quad.nextQuad())
							if orand_count==0:
								r_list_false=Quad.backpatch(r_list_false,Quad.nextQuad())
							else:
								b_list_false=Quad.backpatch(b_list_false,Quad.nextQuad())
					else:
							print('Syntax error at line: ',token.line_number)
							print('Expected ) after condition but found: ',token.recognized_string)
							exit()
					skipLabel=FinalCode.newLabel()
					labelNum-=1
					if orand_count==0:
						skipLabel=FinalCode.newLabel()
						labelNum-=1
						finalCodeList[r_final_list_true[0]]+=nextLabel
						r_final_list_true.pop(0)
						for i in range(0, len(r_final_list_false)):
							finalCodeList[r_final_list_false[i]]+=skipLabel
							r_final_list_false.pop(0)
					else:
						orand_count=0
			
			else:
					print('Syntax error at line: ',token.line_number)
					print('Expected ( after case but found: ',token.recognized_string)
					exit()
		Quad.genQuad('=',incaseFlag,1,firstCondQuad)
		Label=FinalCode.newLabel()
		finalCodeList.append(Label+":	")
		backPos=len(finalCodeList)-1
		nextPos=len(finalCodeList)
		FinalCode.loadvr(incaseFlag, "t1")
		if len(finalCodeList)>nextPos:
				finalCodeList[backPos]+=finalCodeList[nextPos]
				finalCodeList.pop(nextPos)
		FinalCode.loadvr("1", "t2")
		finalCodeList.append('	beq t1, t2, '+loopLabel)
		if token.recognized_string == "default":
			token = syntax.get_token(obj1)
			syntax.statements()
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected default but found: ',token.recognized_string)
			exit()
	
	def callStat():
		global token
		global id_place
		global finalCodeList
		global func_label
		if token.family == "identifier":
			id=syntax.ID(id_place)
			if token.recognized_string == "(":
				token = syntax.get_token(obj1)
				syntax.actualparlist()
				if token.recognized_string == ")":
					token = syntax.get_token(obj1)
					Quad.genQuad('call',id,'_','_')
					Label=FinalCode.newLabel()
					finalCodeList.append(Label+":	sw sp,-4(fp)")
					finalCodeList.append("	addi sp,sp,")
					for i in range(0, len(func_label)):
						if id in func_label[i]:
							finalCodeList.append("	jal "+func_label[0][0])

				else:
					print('Syntax error at line: ',token.line_number)
					print('Expected ) after actual parameter list but found: ',token.recognized_string)
					exit()
			else:
				print('Syntax error at line: ',token.line_number)
				print('Expected ( after ID but found: ',token.recognized_string)
				exit()
		else:
			print('name/identifier expected at line: ',token.line_number)
			print('Instead found token of family: ',token.family)
			exit()

	def returnStat():
		global token
		global e_place
		global funcList
		global finalCodeList
		if token.recognized_string == "(":
			token = syntax.get_token(obj1)
			e_place=syntax.expression(e_place)
			if token.recognized_string == ")":
				token = syntax.get_token(obj1)
				Quad.genQuad('ret',e_place,'_','_')
				Label=FinalCode.newLabel()
				offsetOfVal, b=FinalCode.searchForOffset(e_place)
				finalCodeList.append(Label+"	addi t0,sp,-"+str(offsetOfVal))
				finalCodeList.append("	sw t0,-8(fp)")
				if len(funcList)!=0:
						funcList.pop()
			else:
				print('Syntax error at line: ',token.line_number)
				print('Expected ) after expression but found: ',token.recognized_string)
				exit()
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected ( after return but found: ',token.recognized_string)
			exit()

	def inputStat():
		global token
		global id_place
		if token.recognized_string == "(":
				token = syntax.get_token(obj1)
				if token.family == "identifier":
						id_place=syntax.ID(id_place)
						if token.recognized_string == ")":
								token = syntax.get_token(obj1)
								Quad.genQuad('in',id_place,'_','_')
						else:
								print('Syntax error at line: ',token.line_number)
								print('Expected ) after id but found: ',token.recognized_string)
								exit()
				else:
						print('statement name/identifier expected at line: ',token.line_number)
						print('Instead found token of family: ',token.family)
						exit()
		else:
				print('Syntax error at line: ',token.line_number)
				print('Expected ( after input but found: ',token.recognized_string)
				exit()
	
	def assignStat():
		global token
		global id_place
		global e_place
		global assignFlag
		#### symbol_matrix ####
		global symbol_matrix
		global offset
		global listVal
		global Tcall
		global num_temp
		global labelNum
		id=syntax.ID(id_place)
		if token.recognized_string == ":=":
			token = syntax.get_token(obj1)
			assignFlag=1
			e_place=syntax.expression(e_place)
			Quad.genQuad(':=',e_place,'_',id)
			if "_" in id:
				Tcall=id
				result=Variable.funcV(0)
				symbol_matrix[listVal].append(result)
				Tcall=""
			Label=FinalCode.newLabel()
			finalCodeList.append(Label+':    ')
			backPos=len(finalCodeList)-1
			nextPos=len(finalCodeList)
			FinalCode.loadvr(e_place, "t1")
			if len(finalCodeList)>nextPos:
				finalCodeList[backPos]+=finalCodeList[nextPos]
				finalCodeList.pop(nextPos)
			FinalCode.storerv("t1", id)
			
			
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected := after ID but found: ',token.recognized_string)
			exit()
	
	def printStat():
		global token
		global e_place
		if token.recognized_string == "(":
				token = syntax.get_token(obj1)
				e_place=syntax.expression(e_place)
				if token.recognized_string == ")":
						token = syntax.get_token(obj1)
						Quad.genQuad('out',e_place,'_','_')
				else:
						print('Syntax error at line: ',token.line_number)
						print('Expected ) after expression but found: ',token.recognized_string)
						exit()
		else:
				print('Syntax error at line: ',token.line_number)
				print('Expected ( after print but found: ',token.recognized_string)
				exit()

	def actualparitem(e_place):
		global token
		global id_place
		global cv_flag
		global ref_flag
		global assignFlag
		global assignFlagCV
		global assignFlagREF
		global saveParType
		global symbol_matrix
		global FormMode
		global listVal
		global FormName
		if token.recognized_string == "in":
				if saveParType==1:
					assignFlagCV=1
				token = syntax.get_token(obj1)
				cv_flag=1
				e_place=syntax.expression(e_place)
				
				return e_place
		elif token.recognized_string == "inout":
				if saveParType==1:
					assignFlagREF=1
				token = syntax.get_token(obj1)
				ref_flag=1
				if token.family == "identifier":
					id_place=syntax.ID(id_place)
					FormMode='REF'
					FormName=id_place
					result=Parameter.funcP(0)
					if result[0]!=',':
						symbol_matrix[0].append(result)
					return id_place
				else:
						print('name/identifier expected at line: ',token.line_number)
						print('Instead found token of family: ',token.family)
						exit()
		else:
			print('in/inout expected at line: ',token.line_number)
			print('Instead found: ',token.recognized_string)
			exit()

	def actualparlist():
		global token
		global e_place
		global cv_flag
		global ref_flag
		global been_returned
		global assignFlag
		global innerFlag
		#### final_code ####
		global finalCodeList
		if token.recognized_string == "in" or token.recognized_string == "inout":
			new_place=syntax.actualparitem(e_place)
			if assignFlag==1:
				innerFlag=1
			temp_new_place=new_place
			Label=FinalCode.newLabel()
			finalCodeList.append(Label+":	addi fp,sp,")
			if cv_flag==1 and been_returned==0: #IN AND hasn't been in par...RET position
				Quad.genQuad('par',new_place,'CV','_')
				cv_flag=0
				#### final_code ####
				FinalCode.loadvr(new_place, "t1")
				offsetOfVal, b=FinalCode.searchForOffset(new_place)
				finalCodeList.append("	sw t0,-"+str(offsetOfVal)+"(fp)")
				
			else:#not a inside par, but a Temp var.Still reading par of insider func
				innerFlag=0
			if ref_flag==1 and been_returned==0:#INOUT AND hasn't been in par...RET position
				Quad.genQuad('par',new_place,'REF','_')
				finalCodeList.append("	addi t0,sp,")
				ref_flag=0
				#### final_code ####
				FinalCode.storeForParamRef(new_place)
				####################
			while token.recognized_string == ',': #next par
				token = syntax.get_token(obj1)
				new_place=syntax.actualparitem(e_place)
				if cv_flag==1 and been_returned==1:
					Quad.genQuad('par',new_place,'CV','_')
					cv_flag=0
					#### final_code ####
					Label=FinalCode.newLabel()
					finalCodeList.append(Label+":")
					labelhold=len(finalCodeList)-1
					FinalCode.loadvr(new_place, "t1")
					finalCodeList[labelhold]+=finalCodeList[labelhold+1]
					finalCodeList.pop(labelhold+1)
					offsetOfVal, b=FinalCode.searchForOffset(new_place)
					finalCodeList.append("	sw t0,-"+str(offsetOfVal)+"(fp)")
					####################
				elif cv_flag==1 and been_returned==0:
					Quad.genQuad('par',new_place,'CV','_')
					cv_flag=0
					#### final_code ####
					Label=FinalCode.newLabel()
					finalCodeList.append(Label+":")
					labelhold=len(finalCodeList)-1
					FinalCode.loadvr(new_place, "t1")
					finalCodeList[labelhold]+=finalCodeList[labelhold+1]
					finalCodeList.pop(labelhold+1)
					offsetOfVal, b=FinalCode.searchForOffset(new_place)
					finalCodeList.append("	sw t0,-"+str(offsetOfVal)+"(fp)")
					####################
				elif ref_flag==1 and been_returned==1:
					Quad.genQuad('par',new_place,'REF','_')
					ref_flag=0
					#### final_code ####
					Label=FinalCode.newLabel()
					finalCodeList.append(Label+":")
					labelhold=len(finalCodeList)-1
					FinalCode.storeForParamRef(new_place)
					finalCodeList[labelhold]+=finalCodeList[labelhold+1]
					finalCodeList.pop(labelhold+1)
					####################
				elif ref_flag==1 and been_returned==0:
					Quad.genQuad('par',new_place,'REF','_')
					ref_flag=0
					#### final_code ####
					Label=FinalCode.newLabel()
					finalCodeList.append(Label+":")
					labelhold=len(finalCodeList)-1
					FinalCode.storeForParamRef(new_place)
					finalCodeList[labelhold]+=finalCodeList[labelhold+1]
					finalCodeList.pop(labelhold+1)
					####################
				else:#not a inside par, but a Temp var.Should be a part of outer's pars
					pass
			if innerFlag==-1:#inside actualparlist finished
				innerFlag=-2
			elif innerFlag==-2:#all inside actualparlist finished, can move on to outside
				assignFlag=1
			else:
				#innerFlag==0, still readin pars of inside func
				pass

	def boolterm():#Q 
		global token
		global q_list_true
		global q_list_false
		global r_list_true
		global r_list_false
		global tempQ_list_false
		global tempQ_list_true
		global tempR_list_false
		global tempR_list_true
		global tempQ_false_created
		global tempQ_true_created
		global tempR_false_created
		global tempR_true_created
		####### final_code_globals #####
		global r_final_list_true
		global r_final_list_false
		global finalCodeList
		global labelNum
		global labelsList
		global orand_count
		syntax.boolfactor()#R1
		q_list_true=r_list_true
		q_list_false=r_list_false
		#P1
		while token.recognized_string == 'and':
			a=Quad.nextQuad()
			q_list_true=Quad.backpatch(q_list_true,Quad.nextQuad())#P2
			token = syntax.get_token(obj1)
			tempR_false_created=0
			tempR_true_created=0
			syntax.boolfactor() 
			#P3
			q_list_false=Quad.mergeList(q_list_false,tempR_list_false)
			q_list_true=tempR_list_true

			#### final_code ####
			nextLabel=FinalCode.newLabel()
			labelNum-=1			
			for i in range(0, len(r_final_list_true)):
				finalCodeList[r_final_list_true[i]]+=labelsList[0]
				labelsList.pop(0)
			r_final_list_true=[]
				
				
			for i in range(0, len(r_final_list_false)):
				finalCodeList[r_final_list_false[i]]+=nextLabel
			r_final_list_false=[]
			
			orand_count+=1
			####################
		if tempQ_false_created==0 and tempQ_true_created==0:
			tempQ_list_true=q_list_true
			tempQ_list_false=q_list_false
			tempQ_false_created=1
			tempQ_true_created=1

	def boolfactor(): 
		global token
		global e_place
		e1_place=''
		e2_place=''
		operator_exp=''
		global q_list_true
		global q_list_false
		global r_list_true
		global r_list_false
		global tempQ_list_false
		global tempQ_list_true
		global tempR_list_false
		global tempR_list_true
		global tempR_false_created
		global tempR_true_created
		#### final_code ####
		global r_final_list_true
		global r_final_list_false
		global labelNum
		if token.recognized_string == "not":
				token = syntax.get_token(obj1)
				if token.recognized_string == "[":
						token = syntax.get_token(obj1)
						
						syntax.condition()#P1 
						if token.recognized_string == "]":
								token = syntax.get_token(obj1)
						else:
								print('Syntax error at line: ',token.line_number)
								print('Expected ] after condition but found: ',token.recognized_string)
								exit()
				else:
						print('Syntax error at line: ',token.line_number)
						print('Expected [ after not but found: ',token.recognized_string)
						exit()
		elif token.recognized_string == "[":
				token = syntax.get_token(obj1)
				syntax.condition() 
				if token.recognized_string == "]":
						token = syntax.get_token(obj1)
				else:
						print('Syntax error at line: ',token.line_number)
						print('Expected ] after condition but found: ',token.recognized_string)
						exit()
		else:
				e1_place=syntax.expression(e_place)
				if token.family=="REL_OP":
						tempR_false_created=0
						tempR_true_created=0
						operator=syntax.REL_OP(operator_exp)
						
						e2_place=syntax.expression(e_place)
						r_list_true=Quad.makeList(Quad.nextQuad())
						Quad.genQuad(operator,e1_place,e2_place,'_')

						Label=FinalCode.newLabel()
						finalCodeList.append(Label+':    ')
						backPos=len(finalCodeList)-1
						nextPos=len(finalCodeList)
						FinalCode.loadvr(e1_place, "t1")
						FinalCode.loadvr(e2_place, "t2")
						if len(finalCodeList)>nextPos:
							finalCodeList[backPos]+=finalCodeList[nextPos]
							finalCodeList.pop(nextPos)
						if operator=='=':
							finalCodeList.append('	beq t1, t2, ')
						elif operator=='>':
							finalCodeList.append('	bgt t1, t2, ')
						elif operator=='<':
							finalCodeList.append('	blt t1, t2, ')
						elif operator=='<=':
							finalCodeList.append('	ble t1, t2, ')
						elif operator=='>=':
							finalCodeList.append('	bge t1, t2, ')
						elif operator=='<>':
							finalCodeList.append('	bne t1, t2, ')
						r_list_false=Quad.makeList(Quad.nextQuad())
						Quad.genQuad('jump','_','_','_')
						#### final_code ####
						Label=FinalCode.newLabel()
						labelNum-=1
						labelsList.append(Label)
						r_final_list_true.append(len(finalCodeList)-1)
						Label=FinalCode.newLabel()
						finalCodeList.append(Label+":	b ")
						r_final_list_false.append(len(finalCodeList)-1)


				else:
					print('Syntax error at line: ',token.line_number)
					print('Expected relational operation between expressions but found: ',token.recognized_string)
					exit()
		if tempR_false_created==0 and tempR_true_created==0:
			tempR_list_false=r_list_false
			tempR_list_true=r_list_true
			tempR_false_created=1
			tempR_true_created=1

	def optionalSign():
		global token
		operator_exp=''
		if token.family == 'ADD_OP':
			operator_exp=syntax.ADD_OP(operator_exp)#

	def expression(e_place):
		global token
		global symbol_matrix
		global listVal
		global Tcall
		global num_temp
		global labelNum
		t1_place=''
		t2_place=''
		operator_exp=''
		syntax.optionalSign()
		t1_place=syntax.term(t1_place)
		while token.family == 'ADD_OP':
			operator_exp=syntax.ADD_OP(operator_exp)
			t2_place=syntax.term(t2_place)
			w = Quad.newTemp()
			Quad.genQuad(operator_exp,t1_place,t2_place,w)
			
			Label=FinalCode.newLabel()
			finalCodeList.append(Label+':	')
			backPos=len(finalCodeList)-1
			nextPos=len(finalCodeList)
			FinalCode.loadvr(t1_place, "t1")
			if len(finalCodeList)>nextPos:
				finalCodeList[backPos]+=finalCodeList[nextPos]
				finalCodeList.pop(nextPos)
			else:
				finalCodeList.pop(backPos)
				labelNum-=1
			
			FinalCode.loadvr(t2_place, "t2")
			

			if operator_exp=='+':
				finalCodeList.append("	add t1, t1, t2")
			if operator_exp=='-':
				finalCodeList.append("	sub t1, t1, t2")
			if "_" in w:
				Tcall=w
				result=Variable.funcV(0)
				symbol_matrix[listVal].append(result)
				Tcall=""
			
			FinalCode.storerv("t1",w)
			t1_place=w
		return t1_place

	def term(t_place):
		global token
		global symbol_matrix
		global listVal
		global Tcall
		global num_temp
		global labelNum
		f1_place=''
		f2_place=''
		operator_exp=''
		f1_place=syntax.factor(f1_place)
		while token.family == 'MUL_OP':
			operator_exp=syntax.MUL_OP(operator_exp)
			f2_place=syntax.factor(f2_place)
			w = Quad.newTemp()
			Quad.genQuad(operator_exp,f1_place,f2_place,w)

			Label=FinalCode.newLabel()
			finalCodeList.append(Label+':	')
			backPos=len(finalCodeList)-1
			nextPos=len(finalCodeList)
			FinalCode.loadvr(f1_place, "t1")
			FinalCode.loadvr(f2_place, "t2")
			if len(finalCodeList)>nextPos:
				finalCodeList[backPos]+=finalCodeList[nextPos]
				finalCodeList.pop(nextPos)

			if operator_exp=='*':
				finalCodeList.append("	mul t1, t1, t2")
			if operator_exp=='/':
				finalCodeList.append("	div t1, t1, t2")
			if "_" in w:
				Tcall=w
				result=Variable.funcV(0)
				symbol_matrix[listVal].append(result)
				Tcall=""
			FinalCode.storerv("t1",w)
			f1_place=w	
		t_place=f1_place
		return t_place

	def factor(f_place): 
		global token
		global id_place
		global e_place
		global cv_flag
		global been_returned
		global assignFlag
		global innerFlag
		global saveParType
		if token.recognized_string == "(":
				token = syntax.get_token(obj1)
				f_place=syntax.expression(e_place)
				if token.recognized_string == ")":
						token = syntax.get_token(obj1)
				else:
						print('Syntax error at line: ',token.line_number)
						print('Expected ) after expression but found: ',token.recognized_string)
						exit()
		elif token.family == "identifier":
				id_place=token.recognized_string
				if assignFlag==1 and innerFlag==-1:
					assignFlag=0 #to read inside actualparlist
					innerFlag=0
					saveParType=1 #to save the par types if there are 'inner' funcs called
				f_place=syntax.ID(id_place)
				new_w=syntax.idtail(f_place)
				if (not new_w):
					been_returned=0
				else:
					f_place=new_w
		elif token.family=='number':
				f_place=token.recognized_string
				syntax.INTEGER()
		else:
					print('Syntax error at line: ',token.line_number)
					print('Expected integer after expression but found: ',token.recognized_string) #**********************
					exit()
		return f_place

	def idtail(f_place):
		global token
		global been_returned
		global funcList
		global assignFlag
		global assignFlagCV
		global assignFlagREF
		global innerFlag
		#### symbol_matrix ####
		global offset
		global framelength
		global FormName
		global FormMode
		#### final_code ####
		global finalCodeList
		global func_label
		if offset<framelength:
			offset=4+framelength
		if token.recognized_string == "(":
				token = syntax.get_token(obj1)
				syntax.actualparlist()
				if innerFlag==-2:#inside actualparlist finished,can move to outer
					assignFlag=1
				if token.recognized_string == ")":
						token =syntax.get_token(obj1)
						w = Quad.newTemp()
						FormMode='CV'
						FormName=w
						result=Parameter.funcP(0)
						if result[0]!=',':
							symbol_matrix[listVal].append(result)
						if assignFlag==1: #closing outer func
							if assignFlagCV==1:
								syntax.makeFuncExtra('CV')
								
							else:
								syntax.makeFuncExtra('REF')
						Quad.genQuad('par',w,'RET','_')
						#### final_code ####
						Label=FinalCode.newLabel()
						finalCodeList.append(Label+":")
						labelhold=len(finalCodeList)-1
						FinalCode.storeForParamRef(w)
						finalCodeList[labelhold]+=finalCodeList[labelhold+1]
						finalCodeList.pop(labelhold+1)
						####################
						if innerFlag==0:	#inside inner func
							innerFlag=-1	#finishes the pars of an inside func
						if innerFlag!=1:	#need to save the temp var T
							funcList.append(w)		# to hold the T
							assignFlagCV=1
						been_returned=1 #w has been in quad par,w,ret,_
						Quad.genQuad('call',f_place,'_','_')
						#### final_code ####
						Label=FinalCode.newLabel()
						finalCodeList.append(Label+":	sw sp,-4(fp)")
						finalCodeList.append("	addi sp,sp,")
						for i in range(0, len(func_label)):
							if id in func_label[i]:
								finalCodeList.append("	jal "+func_label[0][0])
						#####################
						return w
				else:
						print('Syntax error at line: ',token.line_number)
						print('Expected ) after actual parameter list but found: ',token.recognized_string)
						exit()
		
	def REL_OP(operator_exp):
		global token
		operator_exp=''
		relopchars=["=","<=" ,">=" ,">","<","<>"]
		if token.recognized_string in relopchars:
			operator_exp=token.recognized_string
			token = syntax.get_token(obj1)
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected REL_OP character after expression but found: ',token.recognized_string)
			exit()
		return operator_exp

	def ADD_OP(operator_exp):
		global token
		operator_exp=''
		if token.recognized_string =="+" or token.recognized_string =="-":
			operator_exp=token.recognized_string
			token = syntax.get_token(obj1)
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected + or - after expression but found: ',token.recognized_string)
			exit()
		return operator_exp

	def MUL_OP(operator_exp):
		global token
		operator_exp=''
		if token.recognized_string =="*" or token.recognized_string =="/":
			operator_exp=token.recognized_string
			token = syntax.get_token(obj1)
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected * or / after expression but found: ',token.recognized_string)
			exit()
		return operator_exp
	
	def INTEGER():
		global token
		if token.recognized_string.isdigit():
			token = syntax.get_token(obj1)
		else:
			print('Syntax error at line: ',token.line_number)
			print('Expected number after expression but found: ',token.recognized_string)
			exit()
	
	def ID(id_place):
		global token
		if token.family=='identifier':
			id_place=token.recognized_string
			token = syntax.get_token(obj1)
		else:
			print('Syntax error at line: ',token.line_number)
			print('expected identifier but found token of family: ',token.family)
			exit()
		return id_place
	
	def makeFuncExtra(place):
		global funcList
		for i in range(0, len(funcList)):
			Quad.genQuad('par',funcList[i], place,'_')
		funcList=[]
		pass

class Scope:
	def __init__(self, level):
		self.level=level
	
	def addNewLayer(self):
		global symbol_matrix
		global offset
		layer=[]
		symbol_matrix.append(layer)
		offset=12
		return symbol_matrix
    
	def deleteLayer(self):
		self.level.pop()
		return self.level
	
	def makeMatrix(self):
		global symbol_matrix
		for i in range(0, len(symbol_matrix)):
			for j in range(0, len(symbol_matrix[i])):
				for k in range(1, len(symbol_matrix[i][j])):
					symbol_matrix[i][j][0]=symbol_matrix[i][j][0]+str(symbol_matrix[i][j][1])
					symbol_matrix[i][j].remove(symbol_matrix[i][j][1])
		symbol_matrix.reverse()


class Entity:   # to connect all
    def __init__(self, name):
        self.name=name
        
    def addNewEntity(self, list,type):
        global a
        if type=="declare":        # we can pick the next variables if they are after a ","
            result=Variable.funcV(self.name)            
        list[0].append(result)
        
    def searchEntity(list, value):
        for i in range(0, len(list)):
            for j in range(0, len(list[i])):
                if value in list[i][j]:
                    return True        
        return False

    def upOff():
        global offset
        offset+=4
        return offset

class Variable(Entity):
	def __init__(self, name, datatype, offset):
		self.datatype=datatype
		self.offset=offset
		Entity.__init__(self, name)
	
	def funcV(self):
		global token
		global symbol_matrix
		global offset
		global Tcall
		list=[]
		
		if "_" in Tcall:
			list.append(Tcall)
			list.append('/')
			list.append(offset)			
		else:
			list.append(token.recognized_string)
			list.append('/')
			list.append(offset)
		offset=Entity.upOff()
		return list


class FormalParameter(Entity):
	def __init__(self, name, datatype, mode):
		self.datatype=datatype
		self.mode=mode
		Entity.__init__(self, name)
	
	def addFormalParameter(self):
		global FormMode
		global FormName
		list=[]             # a list to hold the mode of the formal parameter
		list.append('[')
		list.append(FormName)
		list.append('/')
		list.append(FormMode)
		list.append(']')
		return list
	
	def printFormalParameter(self):
		global formal_matrix
		result=FormalParameter.addFormalParameter(0)
		formal_matrix.append(result)
		return formal_matrix


class Parameter(Variable, FormalParameter):
	def __init__(self, name, datatype, mode, offset):
		Variable.__init__(self, name, datatype, offset)
		FormalParameter.__init__(self, name, datatype, mode)
		
	def funcP(self):
		global offset
		global FormMode
		global FormName
		list=[]
		list.append(FormName)
		list.append('/')
		list.append(offset)
		list.append('/')
		list.append(FormMode)
		offset=Entity.upOff()
		return list

class Procedure_Function(Entity):
	def __init__(self, name, startingQuad, framelength, formalParameters):
		Entity.__init__(self, name)
		self.startingQuad=startingQuad
		self.framelength=framelength
		self.formalParameters=formalParameters
	
	def funcF(self):
		global FuncName
		global framelength
		global offset
		list=[]
		list.append(FuncName)
		if framelength!=0:
			list.append('/')
			list.append(str(framelength))
			offset=framelength
			offset=Entity.upOff()
		return list
	
	def updateFrame(self):
		global offset
		global framelength
		global layer
		framelength=offset
		return Procedure_Function.funcF(0)

    
class FinalCode:
	def newLabel():
		global labelNum
		labelNum+=1
		nextLabel="L"+str(labelNum)
		return nextLabel

	def searchForOffset(t_place):
		global symbol_matrix
		global finalCodeList
		global listVal
		b=listVal
		offsetOfVal=0

		while b>=0:
			for i in range(0, len(symbol_matrix[b])):

				if len(symbol_matrix[b][i])==1:
					y=symbol_matrix[b][i][0].split("/")
					if y[0]==t_place:
						offsetOfVal=y[1]
					
				if symbol_matrix[b][i][0]==t_place:
					offsetOfVal=symbol_matrix[b][i][2]
			b-=1

		return offsetOfVal, b

	def gnlvcode(t_place):
		global finalCodeList
		global listVal
		
		offsetOfVal, b=FinalCode.searchForOffset(t_place)
		n=listVal-b-1
		finalCodeList.append("	lw t0, -4(sp)")
		while n>0:
			finalCodeList.append("	lw t0, -4(t0)")
			n-=1
		finalCodeList.append("	addi t0, t0, "+str(offsetOfVal))
		if offsetOfVal==0:
			print("ERROR: the value is not in symbol_matrix")
			exit(1)
		if n==-1 and  offsetOfVal!=0:
			return offsetOfVal
		
		return offsetOfVal
			

	def typofParam_check(t_place):
		global symbol_matrix
		global finalCodeList
		global offset
		global listVal
		b=listVal
		while b>=0:
			for i in range(0, len(symbol_matrix[b])):
				if len(symbol_matrix[b][i])==1:   ##### one or more strings in symbol_matrix
					a=symbol_matrix[b][i][0].split("/")
					if b==0 and a[0] in t_place and len(a)==2:
						return 'Global_Param'
					elif b!=0 and a[0] in t_place and len(a)==2:
						return 'Parameter'
					elif len(a)==3:
						return a[2]		


				elif b==0 and symbol_matrix[b][i][0] in t_place and len(symbol_matrix[b][i])==3:
					return 'Global_Param'
				elif b!=0 and symbol_matrix[b][i][0] in t_place and len(symbol_matrix[b][i])==3:
					return 'Parameter'

				elif len(symbol_matrix[b][i])>3:
					if symbol_matrix[b][i][0]==t_place:
						return symbol_matrix[b][i][4]
			b-=1

				
	def loadvr(t_place, register):
		global symbol_matrix
		global finalCodeList
		global listVal
		b=listVal
		typeOfPar=''
		
		offsetOfVal, b=FinalCode.searchForOffset(t_place)
		typeOfPar=FinalCode.typofParam_check(t_place)
		if t_place.isdigit()==True:
			finalCodeList.append("	li "+register+","+ str(t_place))
		elif typeOfPar=='CV' or typeOfPar=='Parameter':
			finalCodeList.append("	lw  "+register+",-"+str(offsetOfVal)+"(sp)")	
		elif typeOfPar=='REF':
			finalCodeList.append("	lw  t0,-"+str(offsetOfVal)+"(sp)")	
			finalCodeList.append("	lw  "+register+",(t0)")				
		elif listVal!=b and (typeOfPar=='CV' or typeOfPar=='Parameter'):
			FinalCode.gnlvcode(t_place)
			finalCodeList.append("	lw  "+register+",(t0)")	
		elif listVal!=b and typeOfPar=='REF':
			FinalCode.gnlvcode(t_place)
			finalCodeList.append("	lw  t0,(t0)")
			finalCodeList.append("	lw  "+register+",(t0)")	
		elif typeOfPar=='Global_Param':
			finalCodeList.append("	lw  "+register+",-"+str(offsetOfVal)+"(gp)")	
		

	def storerv(register, t_place):
		global symbol_matrix
		global finalCodeList
		global listVal
		typeOfPar=''
		
		offsetOfVal, b=FinalCode.searchForOffset(t_place)
		typeOfPar=FinalCode.typofParam_check(t_place)
		if t_place.isdigit()==True:
			FinalCode.loadvr(t_place, "t0")
			FinalCode.storerv("t0", t_place)
		elif typeOfPar=='CV' or typeOfPar=='Parameter':
			finalCodeList.append("	sw  "+register+",-"+str(offsetOfVal)+"(sp)")	
		elif typeOfPar=='REF':
			finalCodeList.append("	lw  t0,-"+str(offsetOfVal)+"(sp)")	
			finalCodeList.append("	sw  "+register+",(t0)")				
		elif listVal!=b and typeOfPar=='CV':
			FinalCode.gnlvcode(t_place)
			finalCodeList.append("	sw  "+register+",(t0)")	
		elif listVal!=b and typeOfPar=='REF':
			FinalCode.gnlvcode(t_place)
			finalCodeList.append("	lw  t0,(t0)")
			finalCodeList.append("	sw  "+register+",(t0)")	
		elif typeOfPar=='Global_Param':
			finalCodeList.append("	sw  "+register+",-"+str(offsetOfVal)+"(gp)")	


	def storeForParamRef(t_place):
		global symbol_matrix
		global finalCodeList
		global listVal
		typeOfPar=''
		
		typeOfPar=FinalCode.typofParam_check(t_place)
		offsetOfVal, b=FinalCode.searchForOffset(t_place)
		print(t_place,offsetOfVal)
		if listVal!=b and typeOfPar=='CV':
			FinalCode.gnlvcode(t_place)
			finalCodeList.append("	sw t0,-"+str(offsetOfVal)+"(fp)")	
		elif typeOfPar=='CV' or typeOfPar=='Parameter':
			finalCodeList.append("	addi  t0,sp,"+str(offsetOfVal))	
			finalCodeList.append("	sw t0,-"+str(offsetOfVal)+"(fp)")
		elif typeOfPar=='Global_Param':
			finalCodeList.append("	addi  t0,gp,"+str(offsetOfVal))
			finalCodeList.append("	sw t0,-"+str(offsetOfVal)+"(gp)")

		elif listVal!=b and typeOfPar=='REF':
			FinalCode.gnlvcode(t_place)
			finalCodeList.append("	lw  t0,(t0)")
			finalCodeList.append("	sw t0,-"+str(offsetOfVal)+"(fp)")	
		elif typeOfPar=='REF':
			finalCodeList.append("	lw  t0,-"+str(offsetOfVal)+"(sp)")	
			finalCodeList.append("	sw t0,-"+str(offsetOfVal)+"(fp)")
		

if len(sys.argv)!=2:
	print("Warinig! You haven't entered file correctly")
	exit()
file_name=sys.argv[1]
id_place=''
e_place=''
name_token=''
listOfQuads=[]
listOfQuadsToBePrinted=[]
num_q=1
num_temp=1
listOftokens=[]
assignFlag=0
assignFlagCV=0
assignFlagREF=0
cv_flag=0
ref_flag=0
innerFlag=-1
saveParType=0
been_returned=0
b_list_true=[]
b_list_false=[]
q_list_true=[]
q_list_false=[]
r_list_true=[]
r_list_false=[]
whcond_list_true=[]
whcond_list_false=[]
funcList=[]
tempQ_false_created=0
tempQ_true_created=0
tempR_false_created=0
tempR_true_created=0
tempQ_list_false=[]
tempQ_list_true=[]
tempR_list_false=[]
tempR_list_true=[]
listOfProgId=[]
#######################
symbol_matrix=[[]]
formal_matrix=[]
offset=12
layer=0
listVal=0
FuncName=''
FormMode=''
FormName=''
framelength=0
symbol_matrix_to_print=[]
formVal=0
Tcall=""
#######################
finalCodeList=[]
FCL_pos=[]
FCL_print=[]
r_final_list_true=[]
r_final_list_false=[]
labelNum=0
labelsList=[]
orand_count=0
skipLabel=''
func_label=[]
ifVal=0
#######################
syntax.syntax_analyzer(file_name)
print('Quads: ')
Quad.printList()
output_name=file_name[:-3]+'.int' 
f = open(output_name, "w")
Quad.forOutput() 
for z in listOfQuadsToBePrinted:
    f.write(z)
##################################
output_name=output_name[:-3]+'c' 
Quad.forOutputC(output_name)
##################################
output_name=file_name[:-3]+'.asm' 
f = open(output_name, "w")
Quad.forOutputAsm()
for z in FCL_print:
    f.write(z)
