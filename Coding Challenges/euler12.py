from sets import Set
def recursTri(x):
	a={}
	a[1]=1
	if x>1:
		for i in range(2,x+1):
			a[i]=a[i-1]+i
	return a
print recursTri(10)
def listDiv(x):
	div=[]
	for i in range(1,x):
		if x%i==0:
			div.extend(listDiv(x/i))
	return div
x=100
a=listDiv(recursTri(x)[x])
print x
print a

