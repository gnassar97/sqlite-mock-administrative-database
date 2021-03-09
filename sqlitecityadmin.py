import sqlite3
import sys
import random
from random import randrange
from datetime import datetime, timedelta, date, time
'''Resources for SQLite in python and implementing user logins
https://eclass.srv.ualberta.ca/pluginfile.php/5149362/mod_label/intro/SQLite-in-Python-1.pdf -- BEST
https://eclass.srv.ualberta.ca/mod/page/view.php?id=3659763 -- Assignment Spec
https://github.com/imilas/291PyLab -- BEST
https://eclass.srv.ualberta.ca/pluginfile.php/5149359/mod_label/intro/QL-eSQL.pdf?time=1567207038507 -- SQL inside applications slides
https://stackoverflow.com/questions/973541/how-to-set-sqlite3-to-be-case-insensitive-when-string-comparing -- Case sensitive for SQL'''

db = sys.argv[1]
conn = sqlite3.connect(db)
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON;')   
conn.commit()

def main():
	print("***WELCOME****")
	user = login()
	

	if user[0][0] == 'a':
		agent_prompt(str(user[0][1]))

	elif user[0][0] == 'o':
		officer_prompt()
	else:
		print(user[0][0])
		print("error")


def login():
	isUser = False
	while isUser == False:
		user = getUser()
		if len(user) != 0:
			isUser = True
		else:
			print("Invalid user id or password, please try again")
	return user 

def logout():
	print("LOGGING OUT...")
	main()

def getUser():
	username = input("User ID: ")
	pwd = input("Password: ")
	cursor.execute("SELECT utype, city FROM users WHERE uid LIKE ? AND pwd = ?", (username, pwd))
	user = cursor.fetchall()
	return user

def generateUniqueID():
	existing_IDs = []
	numbers = list(range(10000))
	random_number = random.choice(numbers)
	while random_number in existing_IDs:
		generateUniqueID()
	existing_IDs.append(random_number)
	return random_number

def officer_prompt():
	display_officer_options()

	while True:
		input_option = str(input("Select option: "))
		option = input_option

		if option == '0':
			issue_ticket()
			display_officer_options()
		elif option == '1':
			find_car_owner()
			display_officer_options()
		elif option == '2':
			logout()
		else:
			print("****ERROR***** invalid option please try again")
			display_officer_options()


def agent_prompt(user):

	display_agent_options()

	while True:
		input_option = str(input("Selection option: "))
		option = input_option

		if option == '0':
			register_birth(user)
			display_agent_options()
		elif option == '1':
			register_marriage(user)
			display_agent_options()
		elif option == '2':
			renew_vehicle_Reg()
			display_agent_options()
		elif option == '3':
			process_bill_of_sale()
			display_agent_options()
		elif option == '4':
			process_payment()
			display_agent_options()
		elif option == '5':
			get_driver_abstract()
			display_agent_options()
		elif option == '6':
			logout()
		else:
			print("****ERROR***** invalid option please try again")
			display_agent_options()

			
def display_agent_options():
	print("****Options****")
	print("Register birth (press 0)")
	print("Register Marriage (press 1)")
	print("Renew Vehicle Registration (press 2)")
	print("Process Bill of Sale (press 3)")
	print("Process Payment (press 4)")
	print("Get Driver Abstract (press 5)")
	print("Logout (press 6)")


def display_officer_options():
	print("****Options****")
	print("Issue a Ticket (press 0)")
	print("Find Car Owner (press 1)")
	print("Logout (press 2)")


def register_birth(user): #needs nbregplace and new unique id generator
	'''The agent should be able to register a birth by providing the first name, the last name, the gender, the birth date, the birth place of the newborn, 
	as well as the first and last names of the parents. The registration date is set to the day of registration (today's date) and the registration place is set to the city of the user. 
	The system should automatically assign a unique registration number to the birth record. The address and the phone of the newborn are set to those of the mother. If any of the parents is not in the database, 
	the system should get information about the parent including first name, last name, birth date, birth place, address and phone. For each parent, any column other than the first name and last name can be null if it is not provided.'''
	birthregno = randrange(1000000000)
	while True:
		cursor.execute("SELECT EXISTS(SELECT 1 FROM births WHERE regno=?)", (birthregno,))
		temp = cursor.fetchall()
		if int(temp[0][0]) == 1:
			birthregno = randrange(1000000000)
		else:
			conn.commit()
		break
	nbfname = input("Newborn's First Name: ")
	nblname = input("Newborn's Last Name: ")
	cursor.execute("SELECT fname, lname FROM persons WHERE ? LIKE fname AND ? LIKE lname", (nbfname, nblname))
	nbperson = cursor.fetchall()
	if nbperson != []:
		print("This newborn is already registered as a person in the database. Returning to agent options.")
		return
	nbregdate = date.today()
	nbregplace = str(user)
	nbgender = input("Newborn's Gender (M/F): ") 
	nbf_fname = input("Newborn's Father's First Name: ")
	nbf_lname = input("Newborn's Father's Last Name: ")
	nbm_fname = input("Newborn's Mother's First Name: ")
	nbm_lname = input("Newborn's Mother's Last Name: ")

	cursor.execute("SELECT fname, lname FROM persons WHERE ? LIKE fname AND ? LIKE lname", (nbm_fname, nbm_lname))
	nbmother = cursor.fetchall()
	cursor.execute("SELECT fname, lname FROM persons WHERE ? LIKE fname AND ? LIKE lname", (nbf_fname, nbf_lname))
	nbfather = cursor.fetchall()

	while nbmother == []:
		nbm_fname = input("Confirm Mother's first name: ") # Need to make sure this isn't null
		nbm_lname = input("Confirm Mother's last name: ") # Need to make sure this isn't null
		motherbdate = input("What is the Mother's birth date? (YYYY-MM-DD): ")
		motherbplace = input("What is the Mother's birth place? (format): ")
		motheraddress = input("What is the Mother's address? (format): ")
		motherphone = input("What is the Mother's phone number?: (###-###-####)")
		mother_data = (nbm_fname,nbm_lname,motherbdate,motherbplace,motheraddress,motherphone)
		cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", mother_data)
		conn.commit()
		break

	while nbfather == []:
		nbf_fname = input("Confirm Father's first name: ") # Need to make sure this isn't null
		nbf_lname = input("Confirm Father's last name: ") # Need to make sure this isn't null
		fatherbdate = input("What is the Father's birth date? (YYYY-MM-DD): ")
		fatherbplace = input("What is the Father's birth place?: ")
		fatheraddress = input("What is the Father's address?: ")
		fatherphone = input("What is the Father's phone number? (###-###-####): ")
		father_data = (nbf_fname,nbf_lname,fatherbdate,fatherbplace,fatheraddress,fatherphone)
		cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", father_data)
		conn.commit()
		break

	cursor.execute("SELECT address FROM persons WHERE ? LIKE fname AND ? LIKE lname", (nbm_fname, nbm_lname)) #Finds mother's address
	nbaddress = cursor.fetchall()
	cursor.execute("SELECT phone FROM persons WHERE ? LIKE fname AND ? LIKE lname", (nbm_fname, nbm_lname)) #Finds mother's phone number
	nbphone = cursor.fetchall()

	baby_data = (birthregno,nbfname,nblname,nbregdate,nbregplace,nbgender,nbf_fname,nbf_lname,nbm_fname,nbm_lname)
	person_data = (nbfname, nblname, nbregdate, nbregplace, str(nbaddress), str(nbphone))
	cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", person_data) #First we register the baby as a person
	conn.commit()
	cursor.execute("INSERT INTO births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname) VALUES (?,?,?,?,?,?,?,?,?,?)", baby_data) #We then register it as a birth
	conn.commit()
	print("Registration Complete! Returning to Agent Options")
	
	
	

def register_marriage(user):
	'''The user should be able to provide the names of the partners and the system should assign the registration date and place and a unique registration number as discussed in registering a birth. 
	If any of the partners is not found in the database, the system should get information about the partner including first name, last name, birth date, birth place, address and phone. 
	For each partner, any column other than the first name and last name can be null if it is not provided.'''
	marriageno = randrange(1000000000)
	while True:
		cursor.execute("SELECT EXISTS(SELECT 1 FROM marriages WHERE regno=?)", (marriageno,))
		temp = cursor.fetchall()
		if int(temp[0][0]) == 1:
				marriageno = randrange(1000000000)
		else:
				conn.commit()
		break
	marriagedate = date.today()
	marriageplace = str(user)
	p1fname = input("What is partner 1's first name?: ")
	p1lname = input("What is partner 1's last name?: ")
	p2fname = input("What is partner 2's first name?: ")
	p2lname = input("What is partner 2's last name?: ")

	cursor.execute("SELECT fname, lname FROM persons WHERE ? LIKE fname AND ? LIKE lname", (p1fname, p1lname))
	partner1 = cursor.fetchall()
	cursor.execute("SELECT fname, lname FROM persons WHERE ? LIKE fname AND ? LIKE lname", (p2fname, p2lname))
	partner2 = cursor.fetchall()

	while partner1 == []:
		p1fname = input("Confirm Partner 1's first name: ") # Need to make sure this isn't null
		p1lname = input("Confirm Partner 1's last name: ") # Need to make sure this isn't null
		partner1bdate = input("What is Partner 1's birth date? (YYYY-MM-DD): ")
		partner1bplace = input("What is the Partner 1's birth place? (format): ")
		partner1address = input("What is the Partner 1's address? (format): ")
		partner1phone = input("What is the Partner 1's phone number?: (###-###-####)")
		partner1_data = (p1fname,p1lname,partner1bdate,partner1bplace,partner1address,partner1phone)
		cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", partner1_data)
		conn.commit()
		break

	while partner2 == []:
		p2fname = input("Confirm Partner 2's first name: ") # Need to make sure this isn't null
		p2lname = input("Confirm Partner 2's last name: ") # Need to make sure this isn't null
		partner2bdate = input("What is the Partner 2's birth date? (YYYY-MM-DD): ")
		partner2bplace = input("What is the Partner 2's birth place?: ")
		partner2address = input("What is the Partner 2's address?: ")
		partner2phone = input("What is the Partner 2's phone number? (###-###-####): ")
		partner2_data = (p2fname,p2lname,partner2bdate,partner2bplace,partner2address,partner2phone)
		cursor.execute("INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)", partner2_data)
		conn.commit()
		break

	marriage_data = (marriageno,marriagedate,marriageplace,p1fname,p1lname,p2fname,p2lname)
	cursor.execute("INSERT INTO marriages(regno,regdate,regplace,p1_fname,p1_lname,p2_fname,p2_lname) VALUES (?,?,?,?,?,?,?)", marriage_data)
	conn.commit()
	print("Registration Complete! Returning to Agent Options")


def renew_vehicle_Reg():
	'''The user should be able to provide an existing registration number and renew the registration. 
	The system should set the new expiry date to one year from today's date if the current registration either has expired or expires today. 
	Otherwise, the system should set the new expiry to one year after the current expiry date.'''
	vehicleregno = input("Enter the vehicle's registration number: ")
	cursor.execute("SELECT expiry FROM registrations WHERE ? = regno", (vehicleregno,))
	rawexpiry = cursor.fetchall()
	if rawexpiry == []:
		print("That registration number is invalid! Returning to agent options.")
		return
	rawexpirystring = str(rawexpiry)
	#rawexpirystring = rawexpirystring.translate(None, '[(,)]') #This DOESNT work in python 3, but DOES in python 2
	rawexpirystring = rawexpirystring.translate({ord(i):None for i in '[(,)]'}) #This DOESNT work in python 2, but DOES in python 3
	currentexpiry = datetime.strptime(rawexpirystring, "'%Y-%m-%d'").date()
	todays_date = date.today()

	if currentexpiry <= todays_date:
		newexpiry = todays_date.replace(todays_date.year + 1)

	else:
		newexpiry = currentexpiry.replace(currentexpiry.year + 1)

	cursor.execute("UPDATE registrations SET expiry = ? WHERE regno = ?", (newexpiry, vehicleregno))
	conn.commit()
	print("Vehicle registration renewed! Returning.")


def process_bill_of_sale():
	'''The user should be able to record a bill of sale by providing the vin of a car, the name of the current owner, the name of the new owner, and a plate number for the new registration. 
	If the name of the current owner (that is provided) does not match the name of the most recent owner of the car in the system, the transfer cannot be made. 
	When the transfer can be made, the expiry date of the current registration is set to today's date and a 
	new registration under the new owner's name is recorded with the registration date and the expiry date set by the system to today's date and a year after today's date respectively. 
	Also a unique registration number should be assigned by the system to the new registration. The vin will be copied from the current registration to the new one.'''
	entered_vin = input("What is the VIN of the vehicle that is to be sold?: ")
	current_owner_fname = input("What is the first name of the vehicle's current owner?: ")
	current_owner_lname = input("What is the last name of the vehicle's current owner?: ")
	

	cursor.execute("SELECT r.fname FROM registrations r WHERE ? = r.vin AND ? LIKE r.fname AND ? LIKE r.lname AND regdate = (SELECT max(r2.regdate) FROM registrations r2 WHERE r.fname = r2.fname AND r.lname = r2.lname AND r.vin = r2.vin)", (entered_vin, current_owner_fname, current_owner_lname))
	latest_owner_fname = cursor.fetchall() #Need to heavily test this query, mostly for case sensitivity
	conn.commit()
	cursor.execute("SELECT r.lname FROM registrations r WHERE ? = r.vin AND ? LIKE r.fname AND ? LIKE r.lname AND regdate = (SELECT max(r2.regdate) FROM registrations r2 WHERE r.fname = r2.fname AND r.lname = r2.lname AND r.vin = r2.vin)", (entered_vin, current_owner_fname, current_owner_lname))
	latest_owner_lname = cursor.fetchall() #Need to heavily test this query, mostly for case sensitivity
	conn.commit()

	
	str_latest_owner_fname = str(latest_owner_fname)
	#str_latest_owner_fname = str_latest_owner_fname.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
	str_latest_owner_fname = str_latest_owner_fname.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3

	
	str_latest_owner_lname = str(latest_owner_lname)
	#str_latest_owner_fname = str_latest_owner_fname.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
	str_latest_owner_lname = str_latest_owner_lname.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3


	str_latest_owner_fname = str_latest_owner_fname.strip("''")
	str_latest_owner_lname = str_latest_owner_lname.strip("''")

	str_latest_owner_fname_lower = str_latest_owner_fname.lower()
	str_latest_owner_lname_lower = str_latest_owner_lname.lower()




	if (latest_owner_fname == []) or (latest_owner_lname ==[]):
		print("This person and/or vehicle does not exist in the database. Exiting.")
		return

	elif (str_latest_owner_fname_lower != current_owner_fname.lower()) or (str_latest_owner_lname_lower != current_owner_lname.lower()):
		print("The name you have entered is not the latest owner of this vehicle. Exiting.")
		return

	else: 
		new_owner_fname = input("What is the first name of the new owner?: ")
		new_owner_lname = input("What is the last name of the new owner?: ")
		cursor.execute("SELECT fname, lname FROM persons WHERE ? LIKE fname AND ? LIKE lname", (new_owner_fname, new_owner_lname))
		new_owner = cursor.fetchall()
		if new_owner == []:
			print("The new owner of this vehicle does not exist in the database. Transaction incomplete. Returning.")
			return
		entered_plate = input("What is the requested new license plate number?: ")
		current_expiry = date.today()
		cursor.execute("UPDATE registrations SET expiry = ? WHERE vin = ?", (current_expiry, entered_vin))
		conn.commit()
		new_registration_date = date.today()
		new_expiry_date = current_expiry.replace(current_expiry.year + 1)
		unique_registration_number = randrange(1000000000)
		while True:
			cursor.execute("SELECT EXISTS(SELECT 1 FROM registrations WHERE regno=?)", (unique_registration_number,))
			temp = cursor.fetchall()			
			if int(temp[0][0]) == 1:
				unique_registration_number = randrange(1000000000)
			else:
				conn.commit()
			break
		new_owner_data = (unique_registration_number, new_registration_date, new_expiry_date, entered_plate, entered_vin, new_owner_fname, new_owner_lname)
		cursor.execute("INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) VALUES (?,?,?,?,?,?,?)", new_owner_data)
		conn.commit()





def process_payment():
	'''The user should be able to record a payment by entering a valid ticket number and an amount. 
	The payment date is automatically set to the day of the payment (today's date). 
	A ticket can be paid in multiple payments but the sum of those payments cannot exceed the fine amount of the ticket.'''
	ticketnumber = input("Enter the ticket number: ")
	paymentamount = input("Enter the payment amount: ")
	paymentdate = date.today()

	cursor.execute("SELECT fine FROM tickets WHERE ? = tno", (ticketnumber,))
	fine_amount = cursor.fetchall()
	if fine_amount == []:
		   print("This ticket doesn't exist. Returning to agent operations.")
		   return
	fine_amount = str(fine_amount)
	#fine_amount = fine_amount.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
	fine_amount = fine_amount.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3


	fine_amount = float(fine_amount)


	paymentamount = float(paymentamount)

	cursor.execute("SELECT pdate FROM payments WHERE ? = tno", (ticketnumber,))
	fine_date = cursor.fetchall()
	if fine_date != []:
		fine_date_string = str(fine_date)
		#fine_date_string = fine_date_string.translate(None, '[(,)]') #This DOESNT work in python 3, but DOES in python 2
		fine_date_string = fine_date_string.translate({ord(i):None for i in '[(,)]'}) #This DOESNT work in python 2, but DOES in python 3
		fine_date_object = datetime.strptime(fine_date_string, "'%Y-%m-%d'").date()
		if fine_date_object == date.today():
			print("This ticket has already been paid today. Try again tomorrow!")
			return

	
	if paymentamount > fine_amount:
		paymentamount = fine_amount
		print("You have overpaid this ticket. The true amount paid was $" + str(paymentamount))
		fine_amount = fine_amount - paymentamount
		cursor.execute("UPDATE tickets SET fine = ? WHERE tno = ?", (fine_amount, ticketnumber))
		conn.commit()
	else:
		fine_amount = fine_amount - paymentamount
		print("Ticket paid for $" + str(paymentamount))
		cursor.execute("UPDATE tickets SET fine = ? WHERE tno = ?", (fine_amount, ticketnumber))
		conn.commit()
	payment_data = (ticketnumber, paymentdate, paymentamount)
	cursor.execute("INSERT INTO payments(tno, pdate, amount) VALUES (?,?,?)", payment_data)
	conn.commit()
	



def get_driver_abstract():
	#The user should be able to enter a first name and a last name and get a driver abstract, which includes number of tickets, the number of demerit notices, the total number of demerit points received both within the past two years and within the lifetime. 
	#The user should be given the option to see the tickets ordered from the latest to the oldest. For each ticket, you will report the ticket number, 
	#the violation date, the violation description, the fine, the registration number and the make and model of the car for which the ticket is issued. 
	#If there are more than 5 tickets, at most 5 tickets will be shown at a time, and the user can select to see more.
	abstract_fname = input("What is the driver's first name?: ")
	abstract_lname = input("What is the driver's last name?: ")
	cursor.execute("SELECT regno FROM registrations WHERE ? LIKE fname AND ? LIKE lname", (abstract_fname, abstract_lname))
	abstract_regno = cursor.fetchall()

	if len(abstract_regno) > 1:
		abstract_regno_string = str(abstract_regno)
		#abstract_regno_string = abstract_regno_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
		abstract_regno_string = abstract_regno_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
		abstract_regno_list = abstract_regno_string.split()
		print("Driver Abstract: ")
		length_of_list = range(len(abstract_regno_list))

		number_of_tickets_counter = 0
		for i in length_of_list:
			cursor.execute("SELECT COUNT(*) FROM tickets WHERE ? = regno", (abstract_regno_list[i],))
			number_of_tickets = cursor.fetchall()
			number_of_tickets_string = str(number_of_tickets)
			#number_of_tickets_string = number_of_tickets_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
			number_of_tickets_string = number_of_tickets_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
			number_of_tickets_int = int(number_of_tickets_string)
			number_of_tickets_counter += number_of_tickets_int
		number_of_tickets_string = str(number_of_tickets_counter)
		print("Number of tickets received: " + number_of_tickets_string)

		cursor.execute("SELECT COUNT(*) FROM demeritNotices WHERE ? LIKE fname AND ? LIKE lname", (abstract_fname, abstract_lname))
		number_of_demeritNotices = cursor.fetchall()
		number_of_demeritNotices_string = str(number_of_demeritNotices)
		#number_of_demeritNotices_string = number_of_demeritNotices_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
		number_of_demeritNotices_string = number_of_demeritNotices_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
		print("Number of demerit notices received: " + number_of_demeritNotices_string)

		cursor.execute("SELECT SUM(points) FROM demeritNotices WHERE ? LIKE fname AND ? LIKE lname AND ddate >= date('now', '-2 years')", (abstract_fname, abstract_lname))
		recent_number_demerits = cursor.fetchall()
		recent_number_demerits_string = str(recent_number_demerits)
		#recent_number_demerits_string = recent_number_demerits_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
		recent_number_demerits_string = recent_number_demerits_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
		print("Number of demerits within the last two years received: " + recent_number_demerits_string)

		cursor.execute("SELECT SUM(points) FROM demeritNotices WHERE ? LIKE fname AND ? LIKE lname", (abstract_fname, abstract_lname))
		total_number_demerits = cursor.fetchall()
		total_number_demerits_string = str(total_number_demerits)
		#total_number_demerits_string = total_number_demerits_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
		total_number_demerits_string = total_number_demerits_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
		print("Number of lifetime demerits received: " + total_number_demerits_string)

		optional_order = input("Would you like to see the tickets in order of latest to oldest? (Y/N): ")
		optional_order = optional_order.lower()

		while (optional_order != "y") and (optional_order != "n"):
			optional_order = input("Incorrect response. Would you like to see the tickets in order of latest to oldest? (Y/N): ")
			break

		ticket_counter = 0
		for i in length_of_list:
			if optional_order == "y":
				cursor.execute("SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM tickets t LEFT OUTER JOIN registrations r ON r.regno = t.regno LEFT OUTER JOIN vehicles v on v.vin = r.vin WHERE ? = t.regno ORDER BY t.vdate DESC", (abstract_regno_list[i],))
				abstract_info = cursor.fetchall() #might need to move this out of the for loop
				for row in abstract_info:
					print(row)
					ticket_counter += 1
					if ticket_counter == 5 and number_of_tickets_counter > 5:
						choice_of_five = input("Five tickets have been displayed, would you like to see more? (Y/N): ")
						if choice_of_five.lower() == "y":
							continue
						else:
							return


			elif optional_order == "n":
				cursor.execute("SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM tickets t LEFT OUTER JOIN registrations r ON r.regno = t.regno LEFT OUTER JOIN vehicles v on v.vin = r.vin WHERE ? = t.regno", (abstract_regno_list[i],))
				abstract_info = cursor.fetchall() #might need to move this out of the for loop
				for row in abstract_info:
					print(row)
					ticket_counter += 1
					if ticket_counter == 5 and number_of_tickets_counter > 5:
						choice_of_five = input("Five tickets have been displayed, would you like to see more? (Y/N): ")
						if choice_of_five.lower() == "y":
							continue
						else:
							return

	if len(abstract_regno) == 1:
		abstract_regno_string = str(abstract_regno)
		#abstract_regno_string = abstract_regno_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
		abstract_regno_string = abstract_regno_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
		print(abstract_regno_string)
		print("Driver Abstract: ")

	
		cursor.execute("SELECT COUNT(*) FROM tickets WHERE ? = regno", (abstract_regno_string,))
		number_of_tickets = cursor.fetchall()
		number_of_tickets_string = str(number_of_tickets)
		#number_of_tickets_string = number_of_tickets_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
		number_of_tickets_string = number_of_tickets_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
		print("Number of tickets received: " + number_of_tickets_string)

		cursor.execute("SELECT COUNT(*) FROM demeritNotices WHERE ? LIKE fname AND ? LIKE lname", (abstract_fname, abstract_lname))
		number_of_demeritNotices = cursor.fetchall()
		number_of_demeritNotices_string = str(number_of_demeritNotices)
		#number_of_demeritNotices_string = number_of_demeritNotices_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
		number_of_demeritNotices_string = number_of_demeritNotices_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
		print("Number of demerit notices received: " + number_of_demeritNotices_string)

		cursor.execute("SELECT SUM(points) FROM demeritNotices WHERE ? LIKE fname AND ? LIKE lname AND ddate >= date('now', '-2 years')", (abstract_fname, abstract_lname))
		recent_number_demerits = cursor.fetchall()
		recent_number_demerits_string = str(recent_number_demerits)
		#recent_number_demerits_string = recent_number_demerits_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
		recent_number_demerits_string = recent_number_demerits_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
		print("Number of demerits within the last two years received: " + recent_number_demerits_string)

		cursor.execute("SELECT SUM(points) FROM demeritNotices WHERE ? LIKE fname AND ? LIKE lname", (abstract_fname, abstract_lname))
		total_number_demerits = cursor.fetchall()
		total_number_demerits_string = str(total_number_demerits)
		#total_number_demerits_string = total_number_demerits_string.translate(None, '[("",)]') #This DOESNT work in python 3, but DOES in python 2
		total_number_demerits_string = total_number_demerits_string.translate({ord(i):None for i in '[("",)]'}) #This DOESNT work in python 2, but DOES in python 3
		print("Number of lifetime demerits received: " + total_number_demerits_string)

		optional_order = input("Would you like to see the tickets in order of latest to oldest? (Y/N): ")
		optional_order = optional_order.lower()

		while (optional_order != "y") and (optional_order != "n"):
			optional_order = input("Incorrect response. Would you like to see the tickets in order of latest to oldest? (Y/N): ")
			break

		if optional_order == "y":
			cursor.execute("SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM tickets t LEFT OUTER JOIN registrations r ON r.regno = t.regno LEFT OUTER JOIN vehicles v on v.vin = r.vin WHERE ? = t.regno ORDER BY t.vdate DESC", (abstract_regno_string,))
			abstract_info = cursor.fetchall()
			for row in abstract_info:
				print(row)

		elif optional_order == "n":
			cursor.execute("SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM tickets t LEFT OUTER JOIN registrations r ON r.regno = t.regno LEFT OUTER JOIN vehicles v on v.vin = r.vin WHERE ? = t.regno", (abstract_regno_string,))
			abstract_info = cursor.fetchall()
			for row in abstract_info:
				print(row)
	elif len(abstract_regno) == 0:
		print("This person has no tickets on file! Returning.")
		return

def logout(): 
	print("Logging out....")
	main()



def issue_ticket():
	'''The user should be able to provide a registration number and see the person name that is listed in the registration and the make, model, year and color of the car registered. 
	Then the user should be able to proceed and ticket the registration by providing a violation date, a violation text and a fine amount. A unique ticket number should be assigned automatically and the ticket should be recorded. 
	The violation date should be set to today's date if it is not provided.'''
	
	while True:
		regno = int(input("Enter a registration number: "))
		cursor.execute("SELECT regno, vin, fname, lname FROM registrations WHERE regno = ?;", (regno,))
		regInfo = cursor.fetchall()
		conn.commit()

		if regInfo == []:
			option = input('Registration number not found would you like to try again? (y/n): ')
			if option == 'n':
				return 
		elif regInfo[0][0] == regno:
			break
	
	vin = regInfo[0][1]
	fname = regInfo[0][2]
	lname = regInfo[0][3]

	cursor.execute("SELECT make, model, year, color FROM vehicles WHERE vin = ?;",(vin,))
	vehicleInfo = cursor.fetchall()
	conn.commit()

	make = vehicleInfo[0][0]
	model = vehicleInfo[0][1]
	year = vehicleInfo[0][2]
	color = vehicleInfo[0][3]
	
	print("\n***Vehicle Info***")
	print("Make: " + str(make))
	print("Model: " + str(model))
	print("Year: " + str(year))
	print("Color: " + str(color))

	while True:
		vDate = input('Enter violation date (YYYY-MM-DD)')
		vText = input('Enter violation text: ')
		fineAmount = input(('Enter fine amount: '))

		if fineAmount.isdigit() == False:
			print('ERROR, Invalid fine value entered please try again')
		
		if vDate == '':
			vDate = datetime.datetime.now().strftime("%Y-%m-%d")

		if vText == '':
			vText = None

		else:
			break
	
	tno = randrange(1000000000)

	while True:
		cursor.execute("SELECT EXISTS(SELECT 1 FROM tickets WHERE tno=?)", (tno,))
		temp = cursor.fetchall()
		if int(temp[0][0]) == 1:
			tno = randrange(1000000000)
		else:
			conn.commit()
			break

	
	cursor.execute("insert into tickets values(?,?,?,?,?)", (tno,regno,fineAmount,vText,vDate))
	conn.commit()


def find_car_owner(): 
	'''The user should be able to look for the owner of a car by providing one or more of make, model, year, color, and plate. 
	The system should find and return all matches. If there are more than 4 matches, you will show only the make, model, year, color, 
	and the plate of the matching cars and let the user select one. When there are less than 4 matches or when a car is selected from a list shown earlier, 
	for each match, the make, model, year, color, and the plate of the matching car will be shown as well as the latest registration date, the expiry date, and the name of the person listed in the latest registration record.'''
	selectQuery = "SELECT v.make, v.model, v.year, v.color, r.plate, regdate, expiry, fname, lname FROM vehicles v LEFT JOIN registrations r ON r.vin = v.vin WHERE "
	carDetails = ['make', 'model', 'year', 'color', 'plate']
	userSelections = []
	userValues = []

	for i in range(0, len(carDetails)): #Store inputs of the different car details
		temp = input("Enter "+carDetails[i] + ": ")
		if temp != '':
			userValues.append(temp)
			userSelections.append(carDetails[i])

	if len(userValues) == 0:
		print("ERROR, you must enter at least one of the fields")
		return

	for i in range(0, len(userSelections)):
		if i == len(userSelections) - 1:
			if userSelections[i] == 'year':
				selectQuery += 'v.'+ userSelections[i] + '=' + userValues[i]
			elif userSelections[i] == 'plate':
				selectQuery += 'r.'+userSelections[i] + '=' + single_quote(userValues[i])
			else:
				selectQuery += 'v.' + userSelections[i] + ' LIKE ' + single_quote(userValues[i])
		else:
			if userSelections[i] == 'year':
				selectQuery += 'v.'+ userSelections[i] + '=' + userValues[i] + ' AND '
			elif userSelections[i] == 'plate':
				selectQuery += 'r.'+userSelections[i] + '=' + single_quote(userValues[i]) + ' AND '
			else:
				selectQuery += 'v.' + userSelections[i] + ' LIKE ' + single_quote(userValues[i]) + ' AND '
	
	selectQuery += " GROUP BY v.vin"

	cursor.execute(selectQuery)
	fetched = cursor.fetchall()


	if len(fetched) == 0:
		print('No results found')

	elif len(fetched) >= 4:
		formated_row = '{:<10} {:>6} {:>6} {:>6} {:^10}' 
		i = 1
		for row in fetched:
			if i == 1:
				print("    "+formated_row.format("Make", "Model", "Year", "Color", "Plate"))
			
			print(str(i)+ "   " + formated_row.format(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))
			i = i + 1

		selectionRow = int(input("Select row from vehicles for more information: "))

		while (selectionRow < 1) or (selectionRow > len(fetched)):
			print("ERROR, invalid selection please try again")
			selectionRow = int(input("Select row from vehicles for more information: "))
		
		selection = fetched[selectionRow-1]

		make = str(selection[0])
		model = str(selection[1])
		year = str(selection[2])
		color = str(selection[3])
		plate = str(selection[4])
		formated_row = '{:<10} {:^10} {:^10} {:^10} {:^10} {:^15} {:^15} {:^15} {:^15}'

		if plate == "None":
			print(formated_row.format("Make", "Model", "Year", "Color", "Plate","Regdate","Expiry Date","First name", "Last name"))
			print(formated_row.format(make, model, year, color, plate, "None", "None", "None", "None"))

		else:
			selectQuery = """SELECT v.make, v.model, v.year, v.color, r.plate, r.regdate, r.expiry, r.fname, r.lname FROM vehicles v 
			LEFT JOIN registrations r ON v.vin = r.vin WHERE v.make like ? AND v.model like ? AND v.year = ? AND v.color LIKE ? AND r.plate = ?
			ORDER BY r.regdate DESC LIMIT 1"""
			cursor.execute(selectQuery, (make, model, year, color, plate))
			fetched = cursor.fetchall() 
			print(formated_row.format("Make", "Model", "Year", "Color", "Plate","Regdate","Expiry Date","First name", "Last name"))
			for row in fetched:
				print(formated_row.format(*row))

	else:
		formated_row = '{:<10} {:^10} {:^10} {:^10} {:^10} {:^15} {:^15} {:^15} {:^15}'
		selectQuery += "AND r.regdate = (SELECT MAX(regdate) FROM registrations WHERE vin = v.vin)"
		print(selectQuery)
		print(formated_row.format("Make", "Model", "Year", "Color", "Plate","Regdate","Expiry Date","First name", "Last name"))
		for row in fetched:
			print(formated_row.format(*row))


	conn.commit()


def single_quote(word):
	return "'%s'" % word

main()

	
conn.close()


