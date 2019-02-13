import sys

#print ( 'Number of arguments:', len(sys.argv), 'arguments.')
if len(sys.argv) == 1 or len(sys.argv) > 2 :
    print (" Usage: decoder.py   abcd.dat ")
    print (" where abcd.dat is a compressed file name  ")
    print (" for example: python3 decoder.py compressed.dat   ")
    sys.exit()

inputfile =  sys.argv[1]
outputfile =  sys.argv[1] + ".txt"
#print (inputfile)
#print (outputfile)

f = open(sys.argv[1], "rb")
data = f.read()
datalens = []
myArray = []

for i in range(256):
    myArray.append(0)
#print(myArray)    

res = ""
idx = 0
for i in data[0:256]:
      datalens.append([i, idx, chr(idx)])
      idx = idx+1
datalens.sort(key=lambda x: (x[0], x[1]), reverse=True)
datalens.reverse()
print("datalens\n")
print(datalens)

for i in datalens[0:256]:
#    print(i[0])
    myArray[i[0]] =  myArray[i[0]] +1 
print("myArray\n")
print(myArray)


for i in data[256:260]:
      var = str(bin(i))
      var = var[2:]
      while len(var) < 8:
          var = "0" +  var 
      res = res + var
      #if len(res) > 1000:
      
      #res = ""
      
fin = int(res, 2)
print(fin)

code = 0
first = 0
index = 0
MAXBITS = 256
ln = 1
buffer = ""
message = ""

def getsymbol():
    global code 
    global first 
    global index 
    global MAXBITS 
    global ln
    global buffer
    global message
    global numchars
    
    while ln <= MAXBITS:
        
        code = code + int(buffer[0])         #/* get next bit */
        #print(code)
        #if len(buffer) > 2:
        if len(buffer) > 1:
           buffer = buffer[1:]
        else:
           getmorebits()
           buffer = buffer[1:]
      
        count = myArray[ln];
        if (code - count < first):       #/* if length len, return symbol */
            #print(datalens[index + (code - first)][2])    #return h->symbol[index + (code - first)];
            #print(len(buffer))
            message = message + datalens[index + (code - first)][2]
            numchars = numchars + 1
            code = 0
            first = 0
            index = 0
            ln = 1
            return
        ln = ln +1   
        index  = index + count                 #/* else update for next length */
        first = first + count
        first = first*2;
        code = code*2;
    


dat = data[260:]
numchars = 0


def getmorebits():
      global buffer
      global dat
      if len(dat) > 0:
         i = dat[0]
       #  if len(dat) > 1:
         if len(dat) > 0:
           dat = dat[1:]
         else:
           dat = []
      else:
         return
      
      var = str(bin(i))
      var = var[2:]
      #print(var)
      while len(var) < 8:
            var = "0" +  var 
      buffer = buffer + var
           
getmorebits()
while len(dat) > 0 and numchars < fin:   
  #  print( "datalen  len(dat) =" ,  len(dat) , " numchars =" , numchars , " fin = ", fin , "\n")  
    getsymbol()
print("numchars processed\n")   
print(numchars)   
#print(message)
l = open(outputfile, "w")
l.write(message)
l.close()

            
