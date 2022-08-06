
import sys
#import matplotlib.pyplot as plt

input=sys.stdin.read()
input=input.rstrip()
instructions=input.split("\n")
x=[]
y=[]

#stores line no. and register value whenever variables are used
mem_store={}

type={"10000":"A","10001":"A","10110":"A","11010":"A","11011":"A","11100":"A","10010":"B","11000":"B","11001":"B","10011":"C","10111":"C","11101":"C","11110":"C","10100":"D","10101":"D","11111":"E","01100":"E","01101":"E","01111":"E","01010":"F","00000":'A',"00001":"A","00010":"B"}
reg = {"000":"R0" , "001": "R1", "010": "R2", "011": "R3", "100": "R4", "101": "R5", "110": "R6", "111":"FLAGS"}
reg_value={"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0 }
flag_value={"V":0 , "L":0, "G":0, "E":0}

#converts decimal to 16-bit binary number
def convert_to_bin(number):
    if '.' in str(number):
        s=str(number).split(".")
        int1=s[0]
        dec1=float('0'+'.'+s[1])
        int1=bin(int(int1))[2:]
        int2=''
        int2+=int1
        int2+='.'
        for i in range(5):
            dec1=dec1*2
            s=str(dec1).split(".")
            int1=s[0]
            int2+=int1
            dec1=float('0'+'.'+s[1])
        exp=len(int2.split('.')[0])-1
        if exp>7:
            exp=0
            return 99
        else:
            float1=bin(exp)[2:]
        s=int2.split('.')[0]+int2.split('.')[1]
        for i in s[6:]:
            if i=='1':
                return 88
        s=s[1:6]
        float1=float1+s
        l=''
        for i in range(16-len(float1)):
            l+='0'
        l=l+float1
        return l
    else:
        b=list(bin(number))[2:]
        unused=[]
        if len(b)<16:
            for i in range(0,16-len(b)):
                unused.append("0")
        binary="".join(((unused)+(b))[-16:])
        return binary

#converts binary to float
def convertback(n):
    dec=0
    for i in range(3):
        dec+=int(n[i])*(2**(2-i))
    s2='1'+n[3:]
    s3=s2[:dec+1]+'.'+s2[dec+1:]
    s3=s3.split('.')
    final=finaldec=0
    for i in range(len(s3[0])):
        final+=int(s3[0][i])*(2**(len(s3[0])-1-i))
    for i in range(len(s3[1])):
        finaldec+=int(s3[1][i])*(2**(-1*(i+1)))
    final=str(final+finaldec)
    return float(final)

def mem_dump():
    global instructions
    global mem_store
    i=0
    for line in instructions:
        print(line)
        i+=1

    mem=sorted(mem_store.keys())
    for item in mem:
        if(len(mem)==0):
            break
        while(item!=i):
            print("0000000000000000")
            i+=1
        print(convert_to_bin(mem_store[item]))
        i+=1

    while(i<256):
        print("0000000000000000")
        i+=1

def PC_dump():
    global PC
    PC_register=(list(convert_to_bin(PC)))[8:] #changes PC value form deicmal to 16 bit to 8 bit binary
    string="".join(PC_register)
    print(string,end=" ")

def reg_dump():
    for register in reg_value:
        print(convert_to_bin(reg_value[register]),end=" ")
    print("000000000000",end="")
    for flag in flag_value:
        print(flag_value[flag],end="")
    print("")

def pc_update(PC):
    return PC
def flag_reset():
    global flag_value
    for item in flag_value:
        flag_value[item]=0

def ee_execute(Instruction):
    global cycle,PC,check,halt
    
    cycle+=1
    y.append(PC)
    x.append(cycle)
    check=0
    opcode=(Instruction)[0:5]
    if(type[opcode]=="A"):
        reg1 = reg[(Instruction)[7:10]]
        reg2 = reg[(Instruction)[10:13]]
        reg3 = reg[(Instruction)[13:16]]
        
        
        if(opcode=="10000"):
            reg_value[reg3]=reg_value[reg2]+reg_value[reg1]
        elif(opcode=="10001"):
            if(reg_value[reg2]>reg_value[reg1]):
                reg_value[reg3]=0
                flag_value["V"]=1
                check=1
            else:reg_value[reg3]=reg_value[reg1]-reg_value[reg2]
        elif(opcode=="10110"):
            reg_value[reg3]=reg_value[reg2]*reg_value[reg1]
        elif(opcode=="11010"):
            reg_value[reg3]=reg_value[reg1]^reg_value[reg2]
        elif(opcode=="11011"):
            reg_value[reg3]=reg_value[reg1]|reg_value[reg2]
        elif(opcode=="11100"):
            reg_value[reg3]=reg_value[reg1]&reg_value[reg2]
        elif(opcode=="00000"):
            reg_value[reg3]=reg_value[reg1]+reg_value[reg2]
            if convert_to_bin(reg_value[reg3])==99:
                reg_value[reg3]=255
                flag_value["V"]=1
                check=1
            elif convert_to_bin(reg_value[reg3])==88:
                reg_value[reg3]=0
                flag_value["V"]=1
                check=1
        elif(opcode=="00001"):
            if(reg_value[reg2]>reg_value[reg1]):
                reg_value[reg3]=0
                flag_value["V"]=1
                check=1
            elif convert_to_bin(reg_value[reg3])==88:
                reg_value[reg3]=0
                flag_value["V"]=1
                check=1
            else:reg_value[reg3]=reg_value[reg1]-reg_value[reg2]
        if(reg_value[reg3]>65535 or reg_value[reg3]<0):
                flag_value["V"]=1
                reg_value[reg3]=int(convert_to_bin(reg_value[reg3]),2)
                check=1
        PC+=1
    
    elif(type[opcode]=="B"):
        reg1 = reg[(Instruction)[5:8]]
        imm = (Instruction)[8:16]
        if (opcode=="00010"):
            value=convertback(imm)
            reg_value[reg1]=value
        else:
            value = int(imm,2)
            if(opcode=="10010"):
                reg_value[reg1]=value
            elif(opcode=="11000"):
                reg_value[reg1] = reg_value[reg1] >> (value)
            elif(opcode=="11001"):
                reg_value[reg1] = reg_value[reg1]<<(value)
        PC+=1

    elif(type[opcode]=="C"):
        reg1 = reg[(Instruction)[10:13]]
        reg2 = reg[(Instruction)[13:16]]
        
        if(opcode=="10011"):
            if(reg2=="FLAGS"):
                imm="0"
                for flag in flag_value:
                    imm+=str(flag_value[flag])
                reg_value[reg1]=int(imm,2)
            elif(reg1=="FLAGS"):
                imm="0"
                for flag in flag_value:
                    imm+=str(flag_value[flag])
                reg_value[reg2]=int(imm,2)
            else:
                reg_value[reg2]=reg_value[reg1]
        elif(opcode=="10111"):
            reg_value["R0"]=reg_value[reg1]//reg_value[reg2]
            reg_value["R1"]=reg_value[reg1]%reg_value[reg2]
        elif(opcode=="11101"):
            k=list(convert_to_bin(reg_value[reg1]))
            for i in range(0,16):
                if(k[i]=="0"):
                    k[i]="1"
                elif(k[i]=="1"):
                    k[i]="0"
            reg_value[reg2]=int("".join(k),2)
        elif(opcode=="11110"):
            flag_value["V"]=0
            if(reg_value[reg1]<reg_value[reg2]):
                flag_value["L"]=1
                check=1
            elif(reg_value[reg1]>reg_value[reg2]):
                flag_value["G"]=1
                check=1
            elif(reg_value[reg1]==reg_value[reg2]):
                flag_value["E"]=1
                check=1                
        PC+=1
    
    elif(type[opcode]=="D"):
        reg1=reg[(Instruction)[5:8]]
        mem_adr=int((Instruction)[8:16],2)
        y.append(mem_adr)
        x.append(cycle)
        #load
        if(opcode=="10100"):
            if(mem_adr in mem_store):
                reg_value[reg1]=mem_store[mem_adr]
            else:
                reg_value[reg1]=0
        #store
        elif(opcode=="10101"):
            mem_store[mem_adr]=reg_value[reg1]
        
        PC+=1
    
    elif(type[opcode]=="E"):
        mem_adr=int((Instruction)[8:16],2)
        PC+=1

        if(opcode)=="11111":
            PC=mem_adr
        elif((opcode)=="01100"):
            if(flag_value["L"]==1):
                PC=mem_adr
        elif((opcode)=="01101"):
            if(flag_value["G"]==1):
                PC=mem_adr
        elif((opcode)=="01111"):
            if(flag_value["E"]==1):
                PC=mem_adr
        
    elif(type[opcode]=="F"):
        check=0
        halt=1
    if(check==0):
        flag_reset()
    


PC=0
halt=0
cycle=0    
while(halt==0):
    Instruction=instructions[PC]
    
    PC_dump()

    ee_execute(Instruction)
    
    pc_update(PC)
    
    reg_dump()
    
mem_dump()

#plt.scatter(x,y,color="pink")
#plt.show()    


