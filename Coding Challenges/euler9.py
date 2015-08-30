def pythTriplet(top=1000):
	for i in range(1,top):
		for j in range(i+1,1000-i):
			k= 1000-i-j
			if i!=k and i*i + k*k == j*j:
				return i*j*k
print pythTriplet()


