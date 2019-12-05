import csv
import const as CONST

def ReadData(NumRead):
	try:
		with open('/home/pi/FinalProject/FactoryGuard/DATA.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			count = 0
			for row in csv_reader:
				if count == NumRead:
					print(row)
					index = 0
					for data in row:
						print(data)
						CONST.FingerData[index] = data
						index = index +1
				count = count +1
			print('Processed Read Done.')

			csv_file.close()
			return
	except:
		print("don't Read Data")

def WriteData(DataWrite):
	try:
		with open('/home/pi/FinalProject/FactoryGuard/DATA.csv', 'a') as csv_file:
			csvwriter = csv.writer(csv_file)
			csvwriter.writerow(DataWrite) 
			csv_file.close()
			print("write Data done!")
			return
	except:
		print("Don't write data")

#ReadData(1)
#DataWrite11 =['Vo thai tuyen', '11022', 'hardware']
#WriteData(DataWrite11)
