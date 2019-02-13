import sys
import binascii
#print ( 'Number of arguments:', len(sys.argv), 'arguments.')
if len(sys.argv) == 1 or len(sys.argv) > 2 :
    print (" Usage: encoder.py   abcd ")
    print (" where abcd is a text file name  ")
    print (" for example: python3 encoder.py result.txt   ")
    sys.exit()

#print ( sys.argv[1] )
inputfile = sys.argv[1]
outputfile  = sys.argv[1] + ".dat"
#print (inputfile)
#print (outputfile)
f = open(sys.argv[1], "rb")
data = f.read().decode()
#print(data)
text = data
letterArray = []
total = 0


#********************************************************
def checkchars(character):
    global letterArray
    if len(letterArray) > 0:
       for entry in letterArray:
          if entry[1] == character:
              entry[0] = entry[0] + 1
              return
       letterArray.append([1, character, "0"])
    else:
       letterArray.append([1, character, "0"])
#********************************************************    
for character in data:
    total = total + 1
    checkchars(character)
    data = data[1:]
print("letterArray after counting letters")
print(letterArray)
letterArray.sort(key=lambda x: (x[0], x[1]), reverse=True)
print("letterArray after counting letters and sort ")
print(letterArray)
letterArray.reverse()
print("letterArray after counting letters and sort and reverse")
print(letterArray)
#********************************************************
def inplace_huffman_p1(A, n):
    i = 0
    s = 0
    done = 0
    t = 0
    

    while t < n-1:
        i = 0
        summ = 0
        while i < 2:
            tvar1 = (s > n-1)
            tvar2 = (done < t and A[done][0] < A[s][0])
            if tvar1 or tvar2 or A[-1][0] == 0 :
              #  print("done = ", done, "A[done][0]=", A[done][0],"\n")
              #  print("s = ", s, "A[s][0]=", A[s][0],"\n")
                summ = summ + A[done][0]
                A[done][0] = t
                A[done][2] = "2"
                done = done+1
            
            else:
                summ = summ + A[s][0]
                if s > t:
                    A[s][0] = 0
                    A[s][2] = "-"
                
                s = s + 1;
                if s > n-1:
                    s = s - 1 
            i = i + 1
        
        A[t][0] = summ;
        A[t][2] = "1";
        t = t+1
     #   print( "t=next vacant=",t,"s=next leaf=",s,"done=next tree node= ",done , A )
    
    print( "t=next vacant=",t,"s=next leaf=",s,"done=next tree node= ",done , A )
    #print(A)
    #disp_array("Phase 1", A, n)
#**********************************************     
def inplace_huffman_p2(A, n):

    level_top = n - 2
    depth = 1
    i = n
    k = n
    j = n
    total_nodes_at_level = 2;
    while i > 0:
        k=level_top
        while k > 0 and  A[k-1][0] >= level_top:
            k = k - 1
        
        internal_nodes_at_level = level_top - k
        leaves_at_level = total_nodes_at_level - internal_nodes_at_level

        j = 0
        while j < leaves_at_level:
            i = i - 1
            A[i][0] = depth
            j = j + 1
        
 
        total_nodes_at_level = internal_nodes_at_level * 2
        level_top = k
        depth = depth + 1
    print("after ph2") 
    print(A)
    #disp_array("Phase 2", A, n)
#***************************************************************     
def codelister(A, n): 
    #print (data) 
    code = 0 
    for idx in range(len(A)):
        #print (A[idx][0] + " " +  str(bin(code)))
        tmp = str(bin(code))
        tmp = tmp[2:]
        
        while len(tmp) < A[idx][0]:
            tmp = "0" + tmp
        #print(tmp)
        A[idx].append(tmp)
        
        #A[idx].append(str(bin(code)))
        code = code + 1
        if idx+1  < len(A):
           code = code << (A[idx+1][0] - A[idx][0])
    print("\nCodes\n") 
    print(A)
#*******************************************
    encoded = ""
    byterep = ""
#write code lenghts

    f = open(outputfile,"w")
    for idx in range(256):
        done = 0
        #print(chr(idx))
        for symbol in A:
           if chr(idx) == symbol[1]:
               #print(chr(idx))
               open(outputfile,"ab").write(symbol[0].to_bytes(1, 'little'))
               done = 1
        if done == 0:
            open(outputfile,"ab").write((255).to_bytes(1, 'little'))

    numenc = len(text).to_bytes(4, byteorder='big')
    print("number of characters")
    print( len(text) )
#write number of characters     
    print(numenc)
    open(outputfile,"ab").write(numenc)
#write encoded text 

    for letter in text:
       for symbol in A:
         if symbol[1] == letter:
            encoded = encoded + symbol[3]
            if len(encoded) >= 8:

                enc = int(encoded[:8], 2).to_bytes(1, 'little')
                #print(enc)
                byterep = byterep + str(enc)
                encoded = encoded[8:]
                open(outputfile,"ab").write(enc)
#process last byte 
    while len(encoded) != 8:
        encoded = encoded + "0"

    enc = int(encoded[:8], 2).to_bytes(1, 'little')
    byterep = byterep + str(enc)
    open(outputfile,"ab").write(enc)
 
#***************************************************************            

print("letterArray before inplace_huffman_p1")
print(letterArray)
inplace_huffman_p1(letterArray, len(letterArray))
inplace_huffman_p2(letterArray, len(letterArray))    
#sort letterArray
print("sort letterArray  after huffman_p1 and huffman_p2")
letterArray.sort(key=lambda x: (x[0], x[1]))
print(letterArray )
codelister(letterArray, len(letterArray))    
#***************************************************************
