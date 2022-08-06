import sys
# dictionary for opcodes
opcodesA={'add':'10000','sub':'10001','mul':'10110','xor':'11010','or':'11011','and':'11100','addf':'00000','subf':'00001'}
opcodesB={'mov':'10010','rs':'11000','ls':'11001','movf':'00010'}
opcodesC={'mov':'10011','div':'10111','not':'11101','cmp':'11110'}
opcodesD={'ld':'10100','st':'10101'}
opcodesE={'jmp':'11111','jlt':'01100','jgt':'01101','je':'01111'}
opcodesF={'hlt':'0101000000000000'}
#opcodesG={'addf':'00000','subf':'00001','movf':'00010'}

# register dictionary
registers = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS':'111'}

#function to get opcode (binary)
def getopcode(x,y):
  if x in opcodesA:
    return 1
  elif x in opcodesC and y[0] =='R' or y=="FLAGS":
    return 3
  elif x in opcodesB:
    return 2
  elif x in opcodesD:
    return 4
  elif x in opcodesE:
    return 5
  else:
    return 0

#function to get register (binary)(if reg is valid)
def getreg(x):
  if x in registers:
    return 1
  else:
    return 0
#function to convert immediate to binary
def converttobin(n):
  if n>255 or n<0:
    return 1
  else:
    if n==0:
      return '00000000'
    else:
      s=bin(n)
      ss=s[2:]
      l=''
      if len(ss)<8:
        x=8-len(ss)
        for i in range(x):
          l+='0'
      l=l+ss
      return l
#float to binary
def convertfloat(n):
  s=str(n).split(".")
  int1=s[0]
  dec1=float('0'+'.'+s[1])
  int1=bin(int(int1))[2:]
  int2=''
  int2+=int1
  int2+='.'
  for i in range(50):
      dec1=dec1*2
      s=str(dec1).split(".")
      int1=s[0]
      int2+=int1
      dec1=float('0'+'.'+s[1])
  exp=len(int2.split('.')[0])-1
  if exp>7:
      #print("Error: floating point number out of range")
      return 1
  else:
      float1=bin(exp)[2:]
  s=int2.split('.')[0]+int2.split('.')[1]
  for i in s[6:]:
      if i=='1':
          #print("Error: floating point number out of range")
          return 1
  s=s[1:6]
  float1=float1+s
  l=''
  for i in range(8-len(float1)):
      l+='0'
  l=l+float1
  return l


#main function
f1=open("output.txt","w")
r=sys.stdin.readlines()
firstinstruction=0
for i in r:
    i=i.rstrip()

#removing empty lines
s=len(r[-1].split())
while s==0:
  r.remove(r[-1])
  s=len(r[-1].split())
r[-1]=r[-1].strip()

#splitting list to get variables
for l in range(len(r)):
  i=r[l].split()
  if len(i)!=0:
    if i[0]!= "var":
      firstinstruction=l
      break

l1=r[:firstinstruction] #list of variables
l2=r[firstinstruction:] #list of instructions

check=0 #checking to see if variables are defined at the start of the code
for i in l2:
  i=i.split()
  if len(i)!=0 and i[0]=='var':
    check=1
    break

Label={}
pc=0
for i in l2:
  index=l2.index(i)
  i=i.split()
  if len(i)==0:
    pass
  else:
    if i[0][-1]==":":
      Label[i[0][:-1]]=converttobin(pc)
      string=''
      for j in i[1:]:
        string+=j+' '
      l2[index]=string
    pc=pc+1

counthalt=0 #number of halt instructions
length=0 #number of instructions after removing empty lines
for l in range(len(l2)):
    i=l2[l].split()
    if len(i)!= 0 and i[0]=='hlt':
      counthalt+=1
    if len(i)!= 0:
      length+=1
 
for i in l2:
  if not i.strip():
    l2.remove(i)
  
Var={}
Val=length
#creating dictionary with mem address of variables
for i in range(len(l1)):
  l4=l1[i].split()
  if len(l4)!=0:
    Var[l4[1]]=converttobin(Val)
    Val=Val+1
counter=len(l1)
y=1

l2[-1]=l2[-1].rstrip()
l2[-1]=l2[-1].lstrip()
if l2[-1]!='hlt':
  opc="halt error: hlt instruction missing/not at end (line no."+ str(len(r))+")"
  f1.write(opc)
elif check==1:
  opc="variable error: variables not defined at beginning"
  f1.write(opc)
elif counthalt>1:
  opc="error: more than one hlt instruction"
  f1.write(opc)
else:
  for l in range(len(l2)-1): #traversing instructions
    i=l2[l].split()
    if len(i)==0:
      pass
    elif i[0]=='hlt':
      pass
    else:
      counter+=1
      opc=''
      a=getopcode(i[0],i[-1])
      if a==0:
        opc="invalid instruction (line no.:"+str(counter)+')'
        f1.close()
        f1=open("output.txt","w")
        f1.write(opc)
        y=0
        break
      elif a==1 and y==1: #for instruction type A
        y=1
        if len(i)!=4 or i[1][0]!='R' or i[2][0]!='R' or i[3][0]!='R':
          opc='syntax error: invalid syntax (line no.:'+str(counter)+')'
          f1.close()
          f1=open("output.txt","w")
          f1.write(opc)
          y=0
        else:
          opc=opcodesA[i[0]]+'00'
          for j in range (1,4):
            if getreg(i[j])==1:
              if i[j]!="FLAGS":
                opc+= registers[i[j]]
                y=1
              else:
                opc="invalid use of FLAGS (line no.:"+str(counter)+')'
                y=0
                break
            else:
              opc=opc="invalid: register does not exist (line no.:"+str(counter)+')'
              y=0
              break
        if y==1:
          f1.write(opc)
          f1.write("\n")
        else:
          f1.close()
          f1=open('output.txt', 'w')
          f1.write(opc)
      elif a==2 and y==1: #for instruction type B
        y=1
        if len(i)!=3 or i[1][0]!='R' :
          opc='syntax error: invalid syntax (line no.:'+str(counter)+')'
          f1.close()
          f1=open("output.txt","w")
          f1.write(opc)
          y=0
        else:
          opc=opcodesB[i[0]]
          if getreg(i[1])==1:
            if i[1]!="FLAGS":
                opc+= registers[i[1]]
                y=1
            else:
              opc="invalid use of FLAGS (line no.:"+str(counter)+')'
              y=0
          else:
            opc="invalid: register does not exist (line no.:"+str(counter)+')'
            y=0
          if y==1:
            if '.' in i[2][1:]:
              binary=convertfloat(float(i[2][1:]))
            else:
              binary=converttobin(int(i[2][1:]))
            try:
              if binary!=1:
                opc+=binary
              else:
                opc="Immediate value out of range (line no.:"+str(counter)+')'
                y=0
            except ValueError:
              opc="Invalid immediate (line no.:"+str(counter)+')'
              y=0
        if y==1:
          f1.write(opc)
          f1.write("\n")
        else:
          f1.close()
          f1=open('output.txt', 'w')
          f1.write(opc)
      elif a==3 and y==1: #for instruction type C
        #changed code from here
        opc=opcodesC[i[0]]
        y=1
        if len(i)!=3 :
          opc='syntax error: invalid syntax (line no.:'+str(counter)+')'
          f1.close()
          f1=open("output.txt","w")
          f1.write(opc)
          y=0
        else:
          opc=opcodesC[i[0]]+'00000'
          if getreg(i[1])==1 and i[0]!="mov":
            if i[1]!="FLAGS":
              opc+= registers[i[1]]
              y=1
            else:
              opc="invalid use of FLAGS (line no.:"+str(counter)+')'
              y=0
          elif getreg(i[1])==1 and i[0]=="mov":
            opc+= registers[i[1]]
            y=1
          else:
            opc="invalid: register does not exist (line no.:"+str(counter)+')'
            y=0
          if getreg(i[2])==1:
            if i[2]!="FLAGS":
              opc+= registers[i[2]]
              y=1
            else:
              opc="invalid use of FLAGS (line no.:"+str(counter)+')'
              y=0
          else:
            opc="invalid: register does not exist (line no.:"+str(counter)+')'
            y=0
        if y==1:
          f1.write(opc)
          f1.write("\n")
        else:
          f1.close()
          f1=open('output.txt', 'w')
          f1.write(opc)
          #changes ended here
      elif a==4 and y==1:  #for instruction type D
        opc=opcodesD[i[0]]
        y=1
        if len(i)!=3 :
          opc='syntax error: invalid syntax (line no.:'+str(counter)+')'
          f1.close()
          f1=open("output.txt","w")
          f1.write(opc)
          y=0
        else:
          if getreg(i[1])==1:
            if i[1]!="FLAGS":
                opc+= registers[i[1]]
                y=1
            else:
              opc="invalid use of FLAGS (line no.:"+str(counter)+')'
              y=0
          else:
            opc="invalid: register does not exist (line no.:"+str(counter)+')'
            y=0
          if y==1:
            if i[2] in Var:
              opc+=Var[i[2]]
            elif i[2] in Label:
              opc="invalid: label used as variable (line no.:"+str(counter)+')'
              y=0
            else:
              opc="invalid: variable not defined (line no.:"+str(counter)+')'
              y=0 
        if y==1:
          f1.write(opc)
          f1.write("\n")
        else:
          f1.close()
          f1=open('output.txt', 'w')
          f1.write(opc)
      elif a==5 and y==1: #for instruction type E
        opc=opcodesE[i[0]]+'000'
        y=1
        if len(i)!=2 :
          opc='syntax error: invalid syntax (line no.:'+str(counter)+')'
          f1.close()
          f1=open("output.txt","w")
          f1.write(opc)
          y=0
        else:
          if i[-1] in Label:
            opc+=str(Label[i[-1]])
          elif i[-1] in Var:
            opc= "invalid: variable used as label (line no.:"+str(counter)+')'
            y=0
          else:
            opc= "invalid: label not defined (line no.:"+str(counter)+')'
            y=0
        if y==1:
          f1.write(opc)
          f1.write("\n")
        else:
          f1.close()
          f1=open('output.txt', 'w')
          f1.write(opc)
  if y==1:
    opc=opcodesF['hlt']
    f1.write(opc)

f1.close()
f1=open('output.txt', 'r')
r1=f1.readlines()
for i in r1:
    print(i)

f1.close()