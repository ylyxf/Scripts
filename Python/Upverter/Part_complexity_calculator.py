import math

def calc_complexity(pinCounts, isGeneater=False, isConn=False):
	counts_changed = math.log(pinCounts ** 4) * 0.02

	if isGeneater:
		if pinCounts <= 10:
			fp_score = min(0.1, counts_changed)
		
		elif pinCounts <= 100:
			fp_score = min(0.15, counts_changed)
			
		elif pinCounts > 500:
			fp_score = min(0.35, counts_changed)
		
		else:
			fp_score = min(0.2, counts_changed)
								
	else:
		if pinCounts > 21:
			fp_score = counts_changed
		
		else:
			if pinCounts < 6:
				fp_score = 0.19
			
			elif pinCounts < 10:
				fp_score = 0.205
				
			elif pinCounts < 16:
				fp_score = 0.225
				
			else:
				fp_score = 0.245
				
		if isConn:
			fp_score += 0.2
			
		fp_score = min(0.5, fp_score)
	
				#min(if((pinCounts<300,0.5,0.6),0.005*pinCounts))
	sym_score = min(0.005 * pinCounts, min(int(pinCounts/300), 1) / 10.0 + 0.5)
			
	return max(0.2, min(1, fp_score+sym_score))
	

def reverse_complexity(pinCounts, score):
	params = []
	for g in [True, False]:
		for c in [True, False]:
			if round(score, 3) == round(calc_complexity(pinCounts, g, c), 3):
				params.append((g,c))
				
	return params
			
			
pins = [2, 10, 20, 2, 2, 2, 25, 25, 25, 50, 50, 50, 64, 
		75, 75, 100, 100, 100, 200, 200, 200,
		365, 364, 500, 1000, 1000, 1000, 1200,
		1200, 1200, 16]
		
generated = [False, False, True, False, True, False, False, True,
			False, False, True, False, False, False, False, True, False, False, 
			True, False, False, True, False, False, True,
			False, False, True, False, False, False]
			
conns = [False, False, False, False, False, True, False, False, True, False, 
		False, True, False, False, True, False, False, 
		True, False, False, True, False, False, True, False, 
		False, True, False, False, True, True]
		
test = [0.2, 0.275, 0.25, 0.2, 0.2, 0.4, 0.3825, 0.275, 
		0.5825, 0.563, 0.4, 0.75, 0.6527, 0.7204, 0.875, 
		0.65, 0.8684, 1, 0.7, 0.9239, 1, 0.8, 1, 1, 
		0.95, 1, 1, 0.95, 1, 1, 0.526]


		
for p, g, c, i in zip(pins, generated, conns, xrange(len(pins))):
	result = round(calc_complexity(p, g, c), 4)
	if result != round(test[i], 4):
		print p, g, c, result, test[i]



