
import mysql.connector
from prettytable import PrettyTable
import datetime
from datetime import date
from datetime import time
from datetime import datetime

mydb = mysql.connector.connect(

	host = "localhost",
	user = "root",
	passwd = "1234"

)



cursor = mydb.cursor()
cursor.execute("USE Airlines")
def checkdatevalidity(dt):
	try:
		if dt!=datetime.strptime(dt,"%Y-%m-%d").strftime('%Y-%m-%d'):
			raise ValueError
		return True
	except ValueError:
		return False


def task1():
	while True:
		print("-----------------------------------------------------------------------------------")
		print("Creating a new Passenger Record. Enter the correct details or Press 0 to quit")
		# GETTING INPUT:
		#NAME
		print("Enter Name of Passenger: ")
		n = input()
		if n == "0": 
			break
		if len(n) > 255:
			print("Incorrect Entry")
			continue
		#PASSNO.
		print("Enter Passportno. of Passenger: ")
		pp = input()
		if pp == "0": 
			break
		if len(pp)!=8:
			print("Incorrect Entry")
			continue
		#PHONE
		print("Enter Phone Number of Passenger: ")
		p = input()
		if p == "0": 
			break
		if len(p)!=10 or p.isdigit()==False:
			print("Incorrect Entry")
			continue
		#NATIONALITY
		print("Enter Nationality")
		nat = input()
		if nat=="0":
			break;
		if len(nat) > 255 or nat.isalpha() == False:
			print("Incorrect Entry")
			continue
		my_tuple = (n,pp,p,nat)
		my_query = "INSERT INTO Passenger (Name, Passno, Phone, Nationality) Values (%s, %s, %s, %s)"
		result = cursor.execute(my_query,my_tuple)
		mydb.commit()
		print("New Passenger Record has been successfully Added!")	
		break
	return -1

def findPassenger():
	#FINDING
	while True:
		print("Choose how you would like to find the Passenger \n 1) Find by Name, \n 2) Find by Passport no., \n 3) Find by Phone \n 4) Find by Nationality \n 5) Find by ID \n 6) View All Passengers. \n or Press 0 to Go back")
		second = input()
		if second == "1":
			print("Enter the name")
			marker = input()
			my_findquery = "SELECT * from Passenger where Name = %s"
		elif second == "2":
			print("Enter the Passport no.")
			marker = input()					
			my_findquery = "SELECT * from Passenger where Passno = %s"
		elif second == "3":
			print("Enter the Phone")
			marker = input()					
			my_findquery = "SELECT * from Passenger where Phone = %s"
		elif second == "4":
			print("Enter the Nationality")
			marker = input()					
			my_findquery = "SELECT * from Passenger where Nationality = %s"
		elif second == "5":
			print("Enter the PassengerID")
			marker = input()	
			marker = int(marker)				
			my_findquery = "SELECT * from Passenger where PassengerID = %s"
		elif second == "6":	
			marker = 1000
			my_findquery = "SELECT * from Passenger where PassengerID < %s"
		elif second == "0":
			break
		else:
			print("Incorrect entry. Try Again...")
			continue
		#RUN THE FIND QUERY	
		row_count = cursor.execute(my_findquery, (marker,))
		record = cursor.fetchall()
		if record == []:
			print("Incorrect Entry or No match, try again...")
			continue
		print("Your Entry shows the following possible Passengers: ")
		x = PrettyTable()
		x.field_names = ["ID", "Name","Passno", "Phone", "Nationality"]
		for f in record:
			x.add_row(f)
		
		print(x)		
		#RUN THE SELECT QUERY
		print("Enter the ID of the one you want to Update")
		ID = input()
		ID = int(ID)	
		return ID
	return 0		

def task2():
	while True: 
		print("-----------------------------------------------------------------------------------")			
		print("Updating Record of an Existing Passenger")
		PID = findPassenger()
		if PID == 0:
			return -1
		
		# CHECKING THE QUERY: 
		cursor.execute("SELECT COUNT(*) from Passenger")
		res = cursor.fetchall()
		row_count = res[0][0]
		#print(row_count)
		if PID > row_count or PID <0:
			print("Incorrect entry. Try Again...")
			continue
		break
		
	while True:
		print("What do you want to update? \n 1) Name, 2) Passport no., 3) Phone \n 4) Nationality \n or Press 0 if you are done Updating")
		u = input()
		if u == "1":
			my_updatequery = "Update Passenger set Name = %s where PassengerID = %s"
			print("Enter Name of Passenger: ")
			value = input()
			if value == "0": 
				break
			if len(value) > 255:
				print("Incorrect Entry")
				continue
					
		elif u == "2":
			my_updatequery = "Update Passenger set Passno = %s where PassengerID = %s"
			print("Enter Passport no. of Passenger: ")
			value = input()
			if value == "0": 
				break
			if len(value)!=8:
				print("Incorrect Entry")
				continue
					
		elif u == "3":
			my_updatequery = "Update Passenger set Phone= %s where PassengerID = %s"
			print("Enter Phone Number of Passenger: ")
			value = input()
			if value == "0": 
				break
			if len(value)!=10 or value.isdigit()==False:
				print("Incorrect Entry")
				continue
		elif u == "4":
			my_updatequery = "Update Passenger set Nationality= %s where PassengerID = %s"
			print("Enter Nationality")
			value = input()
			if value =="0":
				break;
			if len(value) > 255:
				print("Incorrect Entry")
				continue
		elif u == "0":
			break
			
		else:
			print("Incorrect Entry. Try Again...")
			continue		
		my_input = (value, PID) 
		cursor.execute(my_updatequery, my_input)
		mydb.commit()
		print("Record Updated")

	return -1

def task3():
	while True:
		print("Enter Departure airport IATA code")
		dep =input()
		if dep == "0":
			break
		elif len(dep) != 3 or dep.isalpha() == False:
			print("Incorrect Entry, Try Again...")
			continue
				
		print("Enter Arrival airport IATA code")
		arr = input()
		if arr == "0":
			break
		if len(arr) != 3 or arr.isalpha() == False or dep==arr:
			print("Incorrect Entry, Try Again...")
			continue	
	
		print("Enter Start Date in the following format: YYYY-MM-DD")
		c = input()
		if c == "0": 
			break
		if len(c)!=10:
			print("Incorrect Entry")
			continue
		valid = checkdatevalidity(c)
		if valid == False:
			print("Incorrect Entry")
			continue
	
		print("Enter Final Date in the following format: YYYY-MM-DD")
		r = input()
		if r == "0": 
			break
		if len(r)!=10:
			print("Incorrect Entry")
			continue
		valid2 = checkdatevalidity(r)
		if valid2 == False:
			print("Incorrect Entry")
			continue
	
		tpquery = "SELECT * FROM flights where Departure_from = %s and Arrival_at = %s and Departure_Date > %s and Arrival_Date < %s"
		tptuple = (dep,arr,c,r)
		cursor.execute(tpquery,tptuple)
		mans = cursor.fetchall()
		y = PrettyTable()
		y.field_names = ["ID", "Departure_from", "Departure_Date", "Departure_time", "Arrival_at", "Arrival_Date", "Arrival_time", "fare"]
		for i in mans:
			y.add_row(i)
		print(y)
		break;
	return -1


def task4():
	print("-----------------------------------------------------------------------------------")
	print("Creating a new ticket record")
	while True:
		PID = findPassenger()
		if PID == 0:
			continue;
		# CHECKING THE QUERY: 
		cursor.execute("SELECT COUNT(*) from Passenger")
		res = cursor.fetchall()
		row_count = res[0][0]
		#print(row_count)
		if PID > row_count or PID <0:
			print("Incorrect entry. Try Again...")
			continue
		# FINDING THE FLIGHT: 
		print("Choose the flight by entering its flight ID: ")
		flight_query = "SELECT * from flights"
		cursor.execute(flight_query)
		flights = cursor.fetchall()
		if flights == []:
			print("No FLights!")
			return -1
		y = PrettyTable()
		y.field_names = ["ID", "Departure_from", "Departure_Date", "Departure_time", "Arrival_at", "Arrival_Date", "Arrival_time", "fare"]
		for i in flights:
			y.add_row(i)
		print(y)
		FID = input()
		FID = int(FID)
		if FID == 0:
			break
				
		# Checking the ID
		cursor.execute("SELECT COUNT(*) from flights")
		res2 = cursor.fetchall()
		row_count2 = res2[0][0]
		if FID > row_count2 or FID < 0:
			print("Incorrect entry. Try Again...")
			continue 
					
		# CREATING TICKET RECORD 
		ticketquery = "INSERT INTO TicketRecord (PassengerID, flightID) Values (%s, %s)"
		tickettuple = (PID, FID)
		cursor.execute(ticketquery,tickettuple)
		mydb.commit()
		print("Ticket Record Has Been Created")
		break
	return -1

def task5():
	#Using departure airport IATA code and arrival airport IATA code, view the cheapest flight. 
	while True:
		print("-----------------------------------------------------------------------------------")
		print("Viewing cheapest flight")			
		print("Enter Departure airport IATA code")
		dep =input()
		if dep == "0":
			break
		elif len(dep) != 3 or dep.isalpha() == False:
			print("Incorrect Entry, Try Again...")
			continue
				
		print("Enter Arrival airport IATA code")
		arr = input()
		if arr == "0":
			break
		if len(arr) != 3 or arr.isalpha() == False:
			print("Incorrect Entry, Try Again...")
			continue
				
		#filterquery = "SELECT * FROM flights where Departure_from = %s and Arrival_at = %s"	
		ffquery = "SELECT * FROM flights where Departure_from = %s and Arrival_at = %s ORDER BY fare"
		fftuple = (dep,arr)
		cursor.execute(ffquery,fftuple)
		ans = cursor.fetchone()
		y = PrettyTable()
		y.field_names = ["ID", "Departure_from", "Departure_Date", "Departure_time", "Arrival_at", "Arrival_Date", "Arrival_time", "fare"]
		y.add_row(ans)
		print(y)
		break;
	return -1

def task6():
	while True:
		print("-----------------------------------------------------------------------------------")
		print("Viewing Flight History")
		PID = findPassenger()
		if PID == 0:
			break
		# CHECKING THE QUERY: 
		cursor.execute("SELECT COUNT(*) from Passenger")
		res = cursor.fetchall()
		row_count = res[0][0]
		#print(row_count)
		if PID > row_count or PID <0:
			print("Incorrect entry. Try Again...")
			continue
		
		#GETTING PASSENGER HISTORY
		history_query = "SELECT * FROM TicketRecord JOIN flights using (flightID) WHERE PassengerID = %s"
		cursor.execute(history_query,(PID,))
		history = cursor.fetchall()
		print("The Passenger has booked the following flights")
		if history == []:
			print("This Passenger has no flights booked")
			break
		n = PrettyTable()
		n.field_names = ["FlightID", "TicketNum", "PassengerID","Departure_from", "Departure_Date",
                                 "Departure_time", "Arrival_at", "Arrival_Date", "Arrival_time", "fare"]
		for h in history:
			n.add_row(h)
		print(n)
		break;
	return -1

def task7():
	while True:
		print("-----------------------------------------------------------------------------------")
		print("Cancelling a Ticket Record")
		print("1) Search Ticket Record by Passenger \n 2) Search by Ticket Record") 
		opt = input()
		if opt=="0":
			break;
		if opt=="1":
			k = task6()
		if opt=="2":
			print("\n Ticket Records: \n ")
			query2 = "Select * from TicketRecord"
			cursor.execute(query2)
			r = cursor.fetchall()
			k = PrettyTable()
			k.field_names = ["Record_No", "PassengerID", "flightID"]
			for i in r:
				k.add_row(i)
			print(k)
		print("Enter the Ticket no. of the record you want to cancel")
		TRID = input()
		del_query = "DELETE FROM TicketRecord WHERE Record_No = %s"
		cursor.execute(del_query,(TRID,))
		mydb.commit()
		print("Ticket Record Deleted")
		break
	return -1

def receptionist():

	print("To Log in as a Receptionist, Please add correct credentials: \n or Press 0 to Go Back")
	print("Enter username: ")
	username = input()
	if username == "0":
		return -1
	if username != "recep":
		print("Incorrect Username. Acess Denied...")
		return -1;
	print("Enter Password: ")
	password = input()
	if password == "0":
		return -1;
	if password != "1234":
		print("Incorrect Password. Acess Denied...")
		return -1;
	print("-----------------------------------------------------------------------------------")
	print("You have Logged in as a Receptionist. Welcome!")
	# LOGGED IN AS RECEPTIONIST
	logged_in = 1 
	while logged_in != 0:
	
		print("-----------------------------------------------------------------------------------")
		print("Enter the number of the task you want to execute: ")
		print(" 1) Create a new Passenger record \n 2) Update a Passenger record \n 3) View all available flights in a particular time period. \n 4) Generate ticket record for a particular passenger for a particular flight\n ​5) view the cheapest flight for a route \n 6) View flight history of a particular passenger. \n 7) Cancel a particular ticket record. \n  Press 0 to Logout")
		task = 0
		task = input()
		if task == "1":
			logged_in = task1()
		elif task == "2":
			logged_in = task2()
		elif task == "3":
		
			logged_in = task3()
		
		elif task == "4":
			logged_in = task4()
		elif task == "5":
			logged_in = task5()
		elif task == "6":
			logged_in = task6()
		elif task == "7":
		
			logged_in = task7()
		
		elif task == "0":
		
			return -1
		
		else:
		
			print("Incorrect Entry...")
			continue
		
	
	return 1

def getflightID():
	while True:
		print("Choose the flight by entering its flight ID: ")
		flight_query = "SELECT * from flights"
		cursor.execute(flight_query)
		flights = cursor.fetchall()
		if flights == []:
			print("No Flights!")
			return -1
		y = PrettyTable()
		y.field_names = ["ID", "Departure_from", "Departure_Date", "Departure_time", "Arrival_at", "Arrival_Date", "Arrival_time", "fare"]
		for i in flights:
			y.add_row(i)
		print(y)
		FID = input()
		FID = int(FID)
		if FID == 0:
			break
				
		#Checking the ID
		cursor.execute("SELECT MAX(FlightID) from flights")
		res2 = cursor.fetchall()
		row_count2 = res2[0][0]
		if FID > row_count2 or FID < 0:
			print("Incorrect entry. Try Again...")
			continue 
		#print("EXITED_____________________________")
		return FID
	return 0 


def admintask1():
	while True:
		print("Creating a New Flight record. Press 0 to quit")
		# GETTING INPUT:
		#Departure from
		print("Enter IATA code of Departure: ")
		d = input()
		if d == "0": 
			break
		if len(d) != 3 or d.isalpha() == False:
			print("Incorrect Entry")
			continue
		#Departure Date
		print("Enter Date of Departure in the following format: YYYY-MM-DD")
		c = input()
		if c == "0": 
			break
		if len(c)!=10:
			print("Incorrect Entry")
			continue
		valid = checkdatevalidity(c)
		if valid == False:
			print("Incorrect Entry")
			continue
		#Departure Time
		print("Enter Time of Departure: (HH:MM)")
		p = input()
		if p == "0": 
			break
		if len(p)>10 or len(p)==0:
			print("Incorrect Entry")
			continue
		#Arrival At
		print("Enter IATA code of Arrival: ")
		a = input()
		if a == "0": 
			break
		if len(a) != 3 or a.isalpha() == False or a==d:
			print("Incorrect Entry")
			continue		
		
		#Arrival Date
		print("Enter Date of Arrival in the following format: YYYY-MM-DD")
		ad = input()
		if ad == "0": 
			break
		if len(ad)!=10:
			print("Incorrect Entry1")
			continue
		valid = checkdatevalidity(ad)
		if valid == False:
			print("Incorrect Entry2")
			continue
		#Arrival Time
		print("Enter Time of Arrival: (HH:MM)")
		at = input()
		if at == "0": 
			break
		if len(at)>10 or len(at)==0:
			print("Incorrect Entry")
			continue
		#Fare
		print("Enter Fare of Flight")
		ff = input()
		if ff.isdigit()==False:
			print("Incorrect Entry")
			continue
		ff = int(ff)
		if ff <= 0:
			print("Incorrect Entry")
			continue
			
		my_tuple = (d,c,p,a,ad,at,ff)
		my_iquery = "INSERT INTO flights (Departure_from, Departure_Date, Departure_time, Arrival_at, Arrival_Date, Arrival_time, fare) Values (%s, %s, %s, %s, %s, %s, %s)"
		result = cursor.execute(my_iquery,my_tuple)
		mydb.commit()
		print("New Flight Record has been successfully Added!")	
		break
	return -1

def admintask2():
	while True:
		print("-----------------------------------------------------------------------------------")			
		print("Updating Record of an Existing Flight")
		FID = getflightID()
		if FID == 0:
			return -1;
		break
	
	while True:
		print("What do you want to update? \n 1) Departure_from, \n 2) Departure_Date, \n 3) Departure_time, \n 4) Arrival_at, \n 5) Arrival_Date, \n 6) Arrival_time, \n 7) fare \n Press 0 if you are done Updating")
		u = input()
		if u == "1":
			my_updatequery = "Update flights set Departure_from = %s where flightID = %s"
			print("Enter IATA code of Departure: ")
			d = input()
			if d == "0": 
				break
			if len(d) != 3 or d.isalpha() == False:
				print("Incorrect Entry")
				continue
			my_input = d
					
		elif u == "2":
			my_updatequery = "Update flights set Departure_Date = %s where flightID = %s"
			print("Enter Date of Departure in the following format: YYYY-MM-DD")
			c = input()
			if c == "0": 
				break
			if len(c)!=8:
				print("Incorrect Entry")
				continue
			valid = checkdatevalidity(ad)
			if valid == False:
				print("Incorrect Entry")
				continue
			my_input = c
					
		elif u == "3":
			my_updatequery = "Update flights set Departure_time = %s where flightID = %s"
			print("Enter Time of Departure: (HH:MM)")
			p = input()
			if p == "0": 
				break
			if len(p)>10 or len(p)==0:
				print("Incorrect Entry")
				continue
			my_input = p
		
		elif u == "4":
			my_updatequery = "Update flights set Arrival_at = %s where flightID = %s"
			print("Enter IATA code of Departure: ")
			a = input()
			if a == "0": 
				break
			if len(a) != 3 or a.isalpha() == False or a==d:
				print("Incorrect Entry")
				continue
			my_input = a
		elif u == "5":
			my_updatequery = "Update flights set Arrival_Date = %s where flightID = %s"
			#Arrival Date
			print("Enter Date of Arrival in the following format: YYYY-MM-DD")
			ad = input()
			if ad == "0": 
				break
			if len(ad)!=8:
				print("Incorrect Entry")
				continue
			valid = checkdatevalidity(ad)
			if valid == False:
				print("Incorrect Entry")
				continue
			my_input = ad
			
		elif u == "6":
			my_updatequery = "Update flights set Arrival_Time = %s where flightID = %s"
			#Arrival Time
			print("Enter Time of Arrival: (HH:MM)")
			at = input()
			if at == "0": 
				break
			if len(at)>10 or len(at)==0:
				print("Incorrect Entry")
				continue
			my_input = at

		#Fare
		elif u == "7":
			my_updatequery = "Update flights set fare = %s where flightID = %s"
			print("Enter Fare of Flight")
			ff = input()
			if ff.isdigit()==False:
				print("Incorrect Entry")
				continue
			ff = int(ff)
			if ff <= 0:
				print("Incorrect Entry")
				continue
			my_input = ff

		elif u == "0":
			break
		
		else:
			print("Incorrect Entry. Try Again...")
			continue
				
		value = (my_input, FID) 
		cursor.execute(my_updatequery, value)
		mydb.commit()
		print("Record Updated")
	return -1
				
def admintask3():
	while True:
		print("Cancelling a flight Record")
		FID = getflightID()
		if FID == 0:
			break
		del_query1= "DELETE FROM TicketRecord WHERE flightID = %s"
		cursor.execute(del_query1,(FID,))
		mydb.commit()
		
		del_query = "DELETE FROM flights WHERE flightID = %s"
		cursor.execute(del_query,(FID,))
		mydb.commit()
		print("Flight Record Deleted")
		break

	return -1
					
def admintask4():
	while True:
		print("------------------------------------------------------------------------------")
		print("View all flights landing and taking off for a particular airport on that day.")
		print("Enter IATA code of Airport: ")
		#AIRPORT
		a = input()
		if a == "0": 
			break
		if len(a) != 3 or a.isalpha() == False:
			print("Incorrect Entry")
			continue
		#DATE
		print("Enter Date in the following format: YYYY-MM-DD")
		ad = input()
		if ad == "0": 
			break
		if len(ad)!=10:
			print("Incorrect Entry")
			continue
		
		query1 = "Select * from flights where Departure_from = %s and Departure_Date = %s"
		dtuple = (a,ad)
		cursor.execute(query1,dtuple)
		deps = cursor.fetchall()
		if deps == []:
			print("No flights found...")
			continue
		print("The following flights are DEPARTING: ")
		y = PrettyTable()
		y.field_names = ["ID", "Departure_from", "Departure_Date", "Departure_time", "Arrival_at", "Arrival_Date", "Arrival_time", "fare"]
		for i in deps:
			y.add_row(i)
		print(y)
		
		query2 = "Select * from flights where Arrival_at = %s and Arrival_Date = %s"
		atuple = (a,ad)
		cursor.execute(query2,atuple)
		arrs = cursor.fetchall()
		if arrs == []:
			print("No flights found...")
			continue
		print("The following flights are ARRIVING: ")
		y = PrettyTable()
		y.field_names = ["ID", "Departure_from", "Departure_Date", "Departure_time", "Arrival_at", "Arrival_Date", "Arrival_time", "fare"]
		for i in arrs:
			y.add_row(i)
		print(y)
		break
	return -1	

def admintask5():
	print("------------------------------------------------------------------------------")
	print("Viewing every table of the DataBase")
	print("\n Passengers: \n")
	query2 = "Select * from Passenger"
	cursor.execute(query2)
	p = cursor.fetchall()
	y = PrettyTable()
	y.field_names = ["PassengerID", "Name", "Passno", "Phone", "Nationality"]
	for i in p:
		y.add_row(i)
	print(y)

	
	print("------------------------------------------------------------------------------")
	print("\n Flights: \n")
	query2 = "Select * from flights"
	cursor.execute(query2)
	f = cursor.fetchall()
	z = PrettyTable()
	z.field_names = ["ID", "Departure_from", "Departure_Date", "Departure_time", "Arrival_at", "Arrival_Date", "Arrival_time", "fare"]
	for i in f:
		z.add_row(i)
	print(z)

	print("------------------------------------------------------------------------------")
	print("\n Ticket Records: \n ")
	query2 = "Select * from TicketRecord"
	cursor.execute(query2)
	r = cursor.fetchall()
	k = PrettyTable()
	k.field_names = ["Record_No", "PassengerID", "flightID"]
	for i in r:
		k.add_row(i)
	print(k)
	return -1
	

def administrator():

	print("To Log in as an Administrator , Please add correct credentials: \n or Press 0 to Go Back")
	print("Enter username: ")
	username = input()
	if username == "0":
		return -1;
	if username != "Hamid":
		print("Incorrect Username. Acess Denied...")
		return -1;
	print("Enter Password: ")
	password = input()
	if password == "0":
		return 0;
	if password != "1234":
		print("Incorrect Password. Acess Denied...")
		return -1;
	print("You have Logged in as an Administrator")
	# LOGGED IN AS Administrator
	logged_in = 1 
	while logged_in != 0:
	
		print("-----------------------------------------------------------------------------------")		
		print("Enter the number of the task you want to execute: ") 
		print(" 1) Add a new Flight Record \n 2) Update a Flight record \n 3) Cancel a Flight record  \n 4) View all flights landing and taking off for a particular airport on a day\n 5) View every table of the database in tabular form. \n Press 0 to Logout")
		task = 0
		task = input()
		if task == "1":
			logged_in = admintask1()
		elif task == "2":
			logged_in = admintask2()
		elif task == "3":
			logged_in = admintask3()
		elif task == "4":
			logged_in = admintask4()
		elif task == "5":
			logged_in = admintask5()
		elif task == "0":
			return -1;
		else:
			print("Incorrect Entry, Try Again...")	 
	return 1

def main():
	i=1
	while i!=0:
		#Start of Program
		option = 0
		print(" \n------------------------------------------------------------------------------------------ \n")	
		print("Welcome to Airline Management System! \n Enter the number to choose how to sign in \n 1) Receptionist \n 2) Administrator")
		print ( "or Press 0 to exit")
		option = input()
		if option == "1":
			option = receptionist()
		elif option == "2":
			option = administrator()
		elif option == "0":
			break
		else:
			print("Incorrect Input. Try Again...")
			continue
	print("Goodbye!")

main()
