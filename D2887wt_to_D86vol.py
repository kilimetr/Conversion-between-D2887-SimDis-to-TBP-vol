# author Dominik Capkovic 
# contact: domcapkovic@gmail.com; https://www.linkedin.com/in/dominik-čapkovič-b0ab8575/
# GitHub: https://github.com/kilimetr


import numpy as np
import matplotlib.pyplot as plt



def D2887wt_to_D86vol(D2887_inp, plottt):
	order = 5
	LFO = np.polyfit(D2887_inp["Cutpoints"], D2887_inp["Temp"], order)

	CP_step = round((95-1)/4)
	print(CP_step)

	D2887_CP = np.linspace(min(D2887_inp["Cutpoints"]), max(D2887_inp["Cutpoints"]), CP_step)

	D2887_Temp = LFO[5] + LFO[4]*D2887_CP + LFO[3]*pow(D2887_CP,2) + LFO[2]*pow(D2887_CP, 3) + LFO[1]*pow(D2887_CP, 4) + LFO[0]*pow(D2887_CP, 5)

	D2887_calc = {"Cutpoints": D2887_CP,
				      "Temp": D2887_Temp}

	if plottt == True:
		plt.figure(1)
		plt.plot(D2887_inp["Cutpoints"], D2887_inp["Temp"], D2887_calc["Cutpoints"], D2887_calc["Temp"])
		plt.legend(["input", "calc"])
		plt.show()
	else:
		pass

	D86_50 = 0.77601 * pow(D2887_inp["Temp"][4], 1.0395)
	D86_50 = D86_50 * 1.8 + 32 # F

	D2887_calc["Temp"] = D2887_calc["Temp"] * 1.8 + 32

	UiETiF = {"i": [6, 5, 4, 3, 2, 1],
			  "Cut Point Range": ["10 - 0 %", "30 - 10 %", "50 - 30 %", "70 - 50 %", "90 - 70 %", "100 - 90 %"],
			  "E": [0.30470, 0.06069, 0.07978, 0.14862, 0.30785, 2.60290],
			  "F": [1.12590, 1.51760, 1.53860, 1.42870, 1.23410, 0.65962],
			  "Max delta F": [150, 150, 100, 100, 100, 100]}

	T1 = []
	T2 = []
	T3 = []
	T4 = []
	T5 = []
	T6 = []

	U1 = []
	U2 = []
	U3 = []
	U4 = []
	U5 = []
	U6 = []

	dT = []

	i = 1
	for D2887_dT in D2887_calc["Temp"]:
		if i != CP_step:
			dT.append(abs(D2887_dT - D2887_calc["Temp"][i]))
			i = i + 1
		else:
			pass
		
	for value in D2887_calc["Cutpoints"]:
		if    0 <= value < 10:
			position_dT = np.argwhere(D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			T6.append(dT[int(position_dT)])
			U6.append(UiETiF["E"][0] * pow(T6[-1], UiETiF["F"][0]))

		elif 10 <= value < 30:
			position_dT = np.argwhere(D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			T5.append(dT[int(position_dT)])
			U5.append(UiETiF["E"][1] * pow(T5[-1], UiETiF["F"][1]))

		elif 30 <= value < 50:
			position_dT = np.argwhere(D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			T4.append(dT[int(position_dT)])
			U4.append(UiETiF["E"][2] * pow(T4[-1], UiETiF["F"][2]))

		elif 50 <= value < 70:
			position_dT = np.argwhere(D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			T3.append(dT[int(position_dT)])
			U3.append(UiETiF["E"][3] * pow(T3[-1], UiETiF["F"][3]))

		elif 70 <= value < 90:
			position_dT = np.argwhere(D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			T2.append(dT[int(position_dT)])
			U2.append(UiETiF["E"][4] * pow(T2[-1], UiETiF["F"][4]))

		elif 90 <= value < 95:
			position_dT = np.argwhere(D2887_calc["Cutpoints"] == value)
			position_dT = np.concatenate(position_dT)
			T1.append(dT[int(position_dT)])
			U1.append(UiETiF["E"][5] * pow(T1[-1], UiETiF["F"][5]))


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


