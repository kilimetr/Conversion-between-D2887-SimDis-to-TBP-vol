# author Dominik Capkovic 
# contact: domcapkovic@gmail.com; https://www.linkedin.com/in/dominik-čapkovič-b0ab8575/
# GitHub: https://github.com/kilimetr


import numpy as np
import matplotlib.pyplot as plt



def D86vol_to_TBPvol(D86_inp, plottt):
	order = 5
	LFO = np.polyfit(D86_inp["Cutpoints"], D86_inp["Temp"], order)

	CP_step = round((95-1)/4)
	print(CP_step)

	D86_CP = np.linspace(min(D86_inp["Cutpoints"]), max(D86_inp["Cutpoints"]), CP_step)

	D86_Temp = LFO[5] + LFO[4]*D86_CP + LFO[3]*pow(D86_CP,2) + LFO[2]*pow(D86_CP, 3) + LFO[1]*pow(D86_CP, 4) + LFO[0]*pow(D86_CP, 5)

	D86_calc = {"Cutpoints": D86_CP,
				"Temp": 	 D86_Temp}

	if plottt == True:
		plt.figure(1)
		plt.plot(D86_inp["Cutpoints"], D86_inp["Temp"], D86_calc["Cutpoints"], D86_calc["Temp"])
		plt.legend(["input", "calc"])
		plt.show()
	else:
		pass

	TBP_50 = 0.8718 * pow(D86_inp["Temp"][4], 1.0258)
	D86_50 = D86_50 * 1.8 + 32 # F

	TBP_calc["Temp"] = TBP_calc["Temp"] * 1.8 + 32

	YiAXiB = {"i": [6, 5, 4, 3, 2, 1],
			  "Cut Point Range": ["10 - 0 %", "30 - 10 %", "50 - 30 %", "70 - 50 %", "90 - 70 %", "100 - 90 %"],
			  "A": [7.4012,  4.90040, 3.03050, 2.52820, 3.04190, 0.11798],
			  "B": [0.60244, 0.71644, 0.80076, 0.82002, 0.75497, 1.66060],
			  "Max delta F": [100, 250, 250, 150, 100, 1000000]}

	X1 = []
	X2 = []
	X3 = []
	X4 = []
	X5 = []
	X6 = []

	Y1 = []
	Y2 = []
	Y3 = []
	Y4 = []
	Y5 = []
	Y6 = []

	dT = []

	i = 1
	for D86_dT in D86_calc["Temp"]:
		if i != CP_step:
			dT.append(abs(D86_dT - D86_calc["Temp"][i]))
			i = i + 1
		else:
			pass
		
	for value in D86_calc["Cutpoints"]:
		if    0 <= value < 10:
			position_dT = np.argwhere(D86_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			X6.append(dT[int(position_dT)])
			Y6.append(YiAXiB["A"][0] * pow(X6[-1], YiAXiB["B"][0]))

		elif 10 <= value < 30:
			position_dT = np.argwhere(D86_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			X5.append(dT[int(position_dT)])
			Y5.append(YiAXiB["A"][1] * pow(X5[-1], YiAXiB["B"][1]))

		elif 30 <= value < 50:
			position_dT = np.argwhere(D86_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			X4.append(dT[int(position_dT)])
			Y4.append(YiAXiB["A"][2] * pow(X4[-1], YiAXiB["B"][2]))

		elif 50 <= value < 70:
			position_dT = np.argwhere(D86_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			X3.append(dT[int(position_dT)])
			Y3.append(YiAXiB["A"][3] * pow(X3[-1], YiAXiB["B"][3]))

		elif 70 <= value < 90:
			position_dT = np.argwhere(D86_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			X2.append(dT[int(position_dT)])
			Y2.append(YiAXiB["A"][4] * pow(X2[-1], YiAXiB["B"][4]))

		elif 90 <= value < 95:
			position_dT = np.argwhere(D86_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			X1.append(dT[int(position_dT)])
			Y1.append(YiAXiB["A"][5] * pow(X1[-1], YiAXiB["B"][5]))


	U6 = np.average(U6)
	U5 = np.average(U5)
	U4 = np.average(U4)
	U3 = np.average(U3)
	U2 = np.average(U2)
	U1 = np.average(U1)

	print(U6)
	print(U5)
	print(U4)
	print(U3)
	print(U2)
	print(U1)

	D86_0   = D86_50 - U4 - U5 - U6
	D86_10  = D86_50 - U4 - U5
	D86_30  = D86_50 - U4
	D86_70  = D86_50 + U3
	D86_90  = D86_50 + U3 + U2
	D86_100 = D86_50 + U3 + U2 + U1

	print(D86_0)
	print(D86_10)
	print(D86_30)
	print(D86_70)
	print(D86_90)
	print(D86_100)

	D86_0   = (D86_0   - 32) / 1.8
	D86_10  = (D86_10  - 32) / 1.8
	D86_30  = (D86_30  - 32) / 1.8
	D86_70  = (D86_70  - 32) / 1.8
	D86_90  = (D86_90  - 32) / 1.8
	D86_100 = (D86_100 - 32) / 1.8

	print(D86_0)
	print(D86_10)
	print(D86_30)
	print(D86_70)
	print(D86_90)
	print(D86_100)

	print(dT)

	D86vol = {"Cutpoints": [0, 10, 30, 50, 70, 90, 100],
			  "Temp":	   [D86_0, D86_10, D86_30, D86_50, D86_70, D86_90, D86_100]}

	return(D86vol)


