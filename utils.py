def centroLinha(linha, menor, maior):
	res = 0
	soma = 0
	pos = 10
	npreto = 0
	for pixel in linha:
		if(pixel == 0):
			soma = soma + pos
			npreto = npreto + 1
		elif(npreto != 0):
			soma = soma / npreto
			if(soma > res and npreto >= menor and npreto <= maior):
				res = soma
			soma = 0
			npreto = 0
		pos = pos + 1
	if(npreto != 0):
		soma = soma / npreto
		if(soma > res and npreto >= menor and npreto <= maior):
			res = soma
	return res
