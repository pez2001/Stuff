import math

"""
prime gap symmetric ocillation observation
2-3 gaplen = 0
     |     
	 | 
	 | 
 ----x----
	 |
	 |
	 |    



3-5-7 gaplen = 1
o    |    o 
	 | 
	 | 
 ----x----
	 |
	 |
o	 |    o   






o    |     o
	o|o
	o|o
o----x----o
	o|o
	o|o
o	 |    o


	o|o	
     |
     |
o----x----o
     |
     |
    o|o
  
  
o    |    o
  o  |  o
    o|o
o----x----o
    o|o
  o  |  o
o    |    o

""" 
  
  
  


"""
2, 1, 2, 
#0,3,0
2, 4, 2, 
#2,-2,2
4, 2, 4,
#2,0,2
6, 2, 6,
#-2,0,-2
4, 2, 4,
#2,4,-2
6, 6, 2,
#0,-2,0
6, 4, 2,
#0,0,4
6, 4, 6, 
#2,0,-4
8, 4, 2, 
#-4,-2,2
4, 2, 4, 
#10,2,2
14, 4, 6, 
#-12,6,-4
2, 10, 2, 
#4,-4,2
6, 6, 4, 
#0,0,-2
6, 6, 2, 
#4,-4,2
10, 2, 4, 
#-8,10,8
2, 12, 12, 
#2,-10,-8
4, 2, 4, 

6, 2, 10, 

6, 6, 6, 
2, 6, 4, 
2, 10, 14, 
4, 2, 4, 
14, 6, 10, 
2, 4, 6, 
8, 6, 6, 
4, 6, 8, 
4, 8, 10, 
2, 10, 2, 
6, 4, 6, 
8, 4, 2, 
4, 12, 8, 
4, 8, 4, 


6, 12 


"""



fib = [0 for i in range(30+2)]
fib[1] = 1

for i in range(30):	
	fib[i+2] = fib[i+0]+fib[i+1]

print("fibs:")
print(fib)
print("")

ifib = [0 for i in range(100+3)]
ifib[102] = 20103
ifib[101] = 17688

for i in range(100):	
	ifib[100-i] = abs(ifib[100-i+1]-ifib[100-i+2])

print("ifibs:")
print(ifib)
print("")


pgaps = (2,1, 2, 2, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 14, 4, 6, 2, 10, 2, 6, 6, 4, 6, 6, 2, 10, 2, 4, 2, 12, 12, 4, 2, 4, 6, 2, 10, 6, 6, 6, 2, 6, 4, 2, 10, 14, 4, 2, 4, 14, 6, 10, 2, 4, 6, 8, 6, 6, 4, 6, 8, 4, 8, 10, 2, 10, 2, 6, 4, 6, 8, 4, 2, 4, 12, 8, 4, 8, 4, 6, 12 )
print("pgaps:")
print(pgaps)
print("")


p = 2
q = 0
l = 0 
m = 0
for i in pgaps:
	print(i-1 ,end = " ")
	if(q == fib[p]*2):
		print("")
		#if(l == fib[m]*2):
		#	p+=1
		#	l=0
		#	m+=1
		p+=1
		q = 0
		l+=1
	#p = 
	q+=1
print("")
print("triple diff:")
p = 1
tdiff = [0 for i in range(len(pgaps)-3)]
for i in range(len(pgaps)-3):
	tdiff[i] = pgaps[i+3]-pgaps[i]
	print(pgaps[i+3]-pgaps[i], end = " ")
	if(p==3):
		print("")
		p=0
	p+=1
	
print("")
print("tdiff:")
print(tdiff)

print("2. degree triple diff:")
p = 1
tdiff2 = [0 for i in range(len(tdiff)-3)]
for i in range(len(tdiff)-3):
	tdiff2[i] = tdiff[i+3]-tdiff[i]
	print((tdiff[i+3]-tdiff[i])/2, end = " ")
	if(p==3):
		print("")
		p=0
	p+=1

print("")
print("pgaps-tdiff2:")
	
for i in range(len(tdiff)):
	if(tdiff[i]>0):
		o = pgaps[i]-tdiff[i]
	else:
		o = pgaps[i]
	
	print(math.log(pgaps[i],pgaps[i+1]),end = " ")
	
	
	
	
	