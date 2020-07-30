# author Dominik Capkovic 
# contact: domcapkovic@gmail.com; https://www.linkedin.com/in/dominik-čapkovič-b0ab8575/
# GitHub: https://github.com/kilimetr


import numpy as np
import matplotlib.pyplot as plt


LFO_D2887_inp = {"Cutpoints": [1, 5, 10, 30, 50, 70, 90, 95],
				 "Temp": [218, 272, 302, 361, 383, 399, 419, 436]}

def D2887wtSIMDIStoTBPvol(D2887_inp, plottt):
	order = 5
	LFO = np.polyfit(LFO_D2887_inp["Cutpoints"], LFO_D2887_inp["Temp"], order)

	CP_step = round((95-1)/4)
	print(CP_step)

	LFO_D2887_CP = np.linspace(min(LFO_D2887_inp["Cutpoints"]), max(LFO_D2887_inp["Cutpoints"]), CP_step)

	LFO_D2887_Temp = LFO[5] + LFO[4]*LFO_D2887_CP + LFO[3]*pow(LFO_D2887_CP,2) + LFO[2]*pow(LFO_D2887_CP, 3) + LFO[1]*pow(LFO_D2887_CP, 4) + LFO[0]*pow(LFO_D2887_CP, 5)

	LFO_D2887_calc = {"Cutpoints": LFO_D2887_CP,
				  "Temp": LFO_D2887_Temp}

	if plottt == True:
		plt.figure(1)
		plt.plot(LFO_D2887_inp["Cutpoints"], LFO_D2887_inp["Temp"], LFO_D2887_calc["Cutpoints"], LFO_D2887_calc["Temp"])
		plt.legend(["input", "calc"])
		plt.show()
	else:
		pass

	TBP_50 = LFO_D2887_inp["Temp"][4] * 1.8 + 32 # F

	LFO_D2887_calc["Temp"] = LFO_D2887_calc["Temp"] * 1.8 + 32

	WiCViD = {"i": [7, 6, 5, 4, 3, 2, 1],
			  "Cut Point Range": ["10 - 5 %", "30 - 10 %", "50 - 30 %", "70 - 50 %", "90 - 70 %", "95 - 90 %", "100 - 95 %"],
			  "C": [0.15779, 0.011903, 0.05342, 0.19861, 0.31531, 0.97476, 0.02172],
			  "D": [1.4296,  2.0253,   1.6988,  1.3975,  1.2938,  0.8723,  1.9733],
			  "Max delta F": [40, 75, 75, 75, 75, 40, 30]}

	V2 = []
	V3 = []
	V4 = []
	V5 = []
	V6 = []
	V7 = []

	W2 = []
	W3 = []
	W4 = []
	W5 = []
	W6 = []
	W7 = []

	dT = []

	i = 1
	for LFO_dT in LFO_D2887_calc["Temp"]:
		if i != CP_step:
			dT.append(abs(LFO_dT - LFO_D2887_calc["Temp"][i]))
			i = i + 1
		else:
			pass

	for value in LFO_D2887_calc["Cutpoints"]:
		if    5 <= value < 10:
			position_dT = np.argwhere(LFO_D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			V7.append(dT[int(position_dT)])
			W7.append(WiCViD["C"][0] * pow(V7[-1], WiCViD["D"][0]))

		elif 10 <= value < 30:
			position_dT = np.argwhere(LFO_D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			V6.append(dT[int(position_dT)])
			W6.append(WiCViD["C"][1] * pow(V6[-1], WiCViD["D"][1]))

		elif 30 <= value < 50:
			position_dT = np.argwhere(LFO_D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			V5.append(dT[int(position_dT)])
			W5.append(WiCViD["C"][2] * pow(V5[-1], WiCViD["D"][2]))

		elif 50 <= value < 70:
			position_dT = np.argwhere(LFO_D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			V4.append(dT[int(position_dT)])
			W4.append(WiCViD["C"][3] * pow(V4[-1], WiCViD["D"][3]))

		elif 70 <= value < 90:
			position_dT = np.argwhere(LFO_D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			V3.append(dT[int(position_dT)])
			W3.append(WiCViD["C"][4] * pow(V3[-1], WiCViD["D"][4]))

		elif 90 <= value < 95:
			position_dT = np.argwhere(LFO_D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			V2.append(dT[int(position_dT)])
			W2.append(WiCViD["C"][5] * pow(V2[-1], WiCViD["D"][5]))

	W7 = np.average(W7)
	W6 = np.average(W6)
	W5 = np.average(W5)
	W4 = np.average(W4)
	W3 = np.average(W3)
	W2 = np.average(W2)

	print(W7)
	print(W6)
	print(W5)
	print(W4)
	print(W3)
	print(W2)

	TBP_5  = TBP_50 - W5 - W6 - W7
	TBP_10 = TBP_50 - W5 - W6
	TBP_30 = TBP_50 - W5
	TBP_70 = TBP_50 + W4
	TBP_90 = TBP_50 + W4 + W3
	TBP_95 = TBP_50 + W4 + W3 + W2

	print(TBP_5)
	print(TBP_10)
	print(TBP_30)
	print(TBP_70)
	print(TBP_90)
	print(TBP_95)

	TBP_5  = (TBP_5  - 32) / 1.8
	TBP_10 = (TBP_10 - 32) / 1.8
	TBP_30 = (TBP_30 - 32) / 1.8
	TBP_70 = (TBP_70 - 32) / 1.8
	TBP_90 = (TBP_90 - 32) / 1.8
	TBP_95 = (TBP_95 - 32) / 1.8

	print(TBP_5)
	print(TBP_10)
	print(TBP_30)
	print(TBP_70)
	print(TBP_90)
	print(TBP_95)

	print(dT)

	TBPvol = {"Cutpoints": [5, 10, 30, 50, 70, 90, 95],
			  "Temp":	   [TBP_5, TBP_10, TBP_30, TBP_50, TBP_70, TBP_90, TBP_95]}

	return(TBPvol)


