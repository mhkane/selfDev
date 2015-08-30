import math
def isprime(x):
	if x==1 or x==0 :
		return False
	for i in range(2,int(math.sqrt(x)+1)):
		if x%i==0:
			return False
	return True

def e10(x=2000000):
	somme=0
	for i in range(x):
		if isprime(i):
			somme+=i
	return somme
print e10()