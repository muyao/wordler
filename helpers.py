def safeInput(datType, prompt):
	try:
		return datType(input(prompt))
	except:
		return safeInput(datType, prompt)