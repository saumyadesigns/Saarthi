import mysql.connector
import random 
connection1 = mysql.connector.connect(host = 'localhost', username = 'root', password = 'root', database = 'saarthi' )
my_cursor = connection1.cursor()

                  #for showing price estimate 
global driver_user_id 



def find_user_id(fname,lname):
    check_exists_query = "SELECT * FROM customer where first_name =  '%s'  and last_name =  '%s'  " % (fname,lname)
    my_cursor.execute(check_exists_query)
    q = my_cursor.fetchall()
    return q[0][0]


def book_type():
    global booking_type
    booking_type = "reservation"

def register_new(fname,lname):
    
    connection2 = mysql.connector.connect(host = 'localhost', username = 'root', password = 'root', database = 'saarthi' )
    new_cursor = connection2.cursor()
    connection2.commit()

    #print("max user id")
    new_cursor.execute("SELECT MAX(user_id) from customer")
    res=new_cursor.fetchone()
    global user_id
    user_id =  res[0] + 1
    password_user = "'" + input("please enter a strong password within 45 characters ") + "'"
    phone_number = "'" + input("phone number : ") + "'"
    email = "'" + input("email : ") + "'"
    dob = "'" + input("date (YYYY-MM-DD): ") + "'"
    age = int(input('age : ')) 
    sex = "'" + input("sex (F/M): ") + "'"
    address_type = "'" + input("address type (work/home/other): ") + "'"
    place = "'" + input("place : ") + "'"
    pincode = int(input("pincode : "))
    city = "'" + input("city : ") + "'"
    print("****************************************************************")
    global query_insert_customer_details
    global query_insert_address_details
    query_insert_customer_details = "insert into customer (user_id,first_name,last_name,password_user,phone_number,email,dob,age,sex) values (%d, %s,%s,%s,%s,%s,%s,%d,%s)" % (user_id,fname,lname,password_user,phone_number,email,dob,age,sex)
    query_insert_address_details = "insert into address_type_customer (user_id, address_type,place, pincode,city) values (%d,%s,%s,%d,%s)" % (user_id, address_type, place,pincode,city)


def login(fname, lname):
    check_exists_query = "SELECT * FROM customer where first_name =  %s  and last_name =  %s  " % (fname,lname)
    my_cursor.execute(check_exists_query)
    q = my_cursor.fetchall()
    global known 
    known = 1
    if (q == [] ) :
        print("error : We can't seem to find you here! ")
        print("****************************************************************")
        print("Let's create a new profile for you!")
        print("****************************************************************")
        register_new(fname,lname)
        known = 0
       
    elif ( q != []): 
        check_exists_query = "SELECT * FROM customer where first_name =  %s  and last_name =  %s  " % (fname,lname)
        my_cursor.execute(check_exists_query)
        q = my_cursor.fetchall()
        global user_id
        user_id= q[0][0]
        #print(user_id)
        pass

def reserve_ride():
    book_type()
    k = my_cursor.execute("SELECT MAX(booking_id) from reservation")
    #print(k)
    global booking_id
    booking_id = int(((my_cursor.fetchall())[0])[0]) + 1 
    if booking_type == 'reservation' :
        date_of_booking = "'" + input("enter date of booking(yyyy-mm-dd) : ") + "'"
        time_of_booking= "'" + input("enter time of booking (hh:mm:ss): ") + "'"
    else:
        date_of_booking = payment_date
        time_of_booking= "'" +  input("enter time of booking (hh:mm:ss): ") + "'"
    bs = ["'cancelled'", "'successful'", "'delayed'"]
    booking_status =  random.choice(bs)
    if known == 0 :
        my_cursor.execute(query_insert_customer_details)
        my_cursor.execute(query_insert_address_details) 
        connection1.commit()

    reservation_query = "insert into reservation(booking_id,booking_type,date_of_booking,time_of_booking,booking_status,CUser_id) values(%d,'%s',%s,%s,%s,%d)" % (booking_id,booking_type,date_of_booking,time_of_booking,booking_status,user_id)
    my_cursor.execute(reservation_query)
    connection1.commit()


def book_ride():
    print("please enter your booking details : ")
    destination = "'" + input("final destination : ") + "'"
    starting_point = "'" + input("current location : ") + "'"
    distance = float(random.uniform(2.5, 25))
    travel_time = float(random.uniform(7.5, 75))             #minutes
    global trip_charge
    trip_charge = float(random.uniform(50, 400))            #rupees
    i =input("do you wish to leave now or reserve it? (now/reservation) : ") 
    global booking_type
    print (i)
    if i == "reservation" :
        booking_type="reservation"
    elif i =='now':
        print("why is this happening ")
        booking_type = "now"
        my_cursor.execute(query_insert_customer_details)
        my_cursor.execute(query_insert_address_details)


    global booking_id
    k = my_cursor.execute("SELECT MAX(booking_id) from reservation")
    #print(k)
    
    booking_id = int(((my_cursor.fetchall())[0])[0]) + 1
    #print("booking_id = ", booking_id)
    
    reservation_booking_id = booking_id

    my_cursor.execute("SELECT MAX(payment_id) from payment")
    global payment_id
    payment_id = int(((my_cursor.fetchall())[0])[0]) + 1
    reservation_payment_id = payment_id
    
    #print(user_id)
    date_of_booking = '"2023-04-22"'
    time_of_booking =  '"15:43:00"'
    booking_status =  '"now"'
    #print(booking_type)
    reservation_query = "insert into reservation(booking_id,booking_type,date_of_booking,time_of_booking,booking_status,CUser_id) values(%d,'%s',%s,%s,%s,%d)" % (booking_id,booking_type,date_of_booking,time_of_booking,booking_status,user_id)
    my_cursor.execute(reservation_query)
    connection1.commit()

    global query_fill_route_details
    query_fill_route_details = "insert into route_details(destination, starting_point, distance, travel_time, trip_charge,CUser_id, reservation_booking_id, reservation_payment_id) values (%s,%s,%f,%d,%f,%d,%d,%d)" % (destination, starting_point, distance, travel_time, trip_charge,user_id, reservation_booking_id, reservation_payment_id)


def payment():
    if booking_type =="reservation":
        book_ride()

    payment_method = "'" + input("choose method of payment(cash/card/UPI) : ") + "'"
    payment_date = "'" + input( "enter date of payment(yyyy-mm-dd) : ") + "'"
    refund = 0
    fare = trip_charge
    query_payment_insertion = "insert into payment(payment_method,payment_date,refund,payment_id,fare) values(%s, %s, %d, %d,%f)" % (payment_method, payment_date,refund,payment_id,fare)
    
    my_cursor.execute(query_payment_insertion)
    my_cursor.execute(query_fill_route_details)
    connection1.commit()



def leave_rating():
    choice = input("would you like to leave a review ? y/n?")
    if choice.lower() == 'y':
        feedback = input("pls give us your feedback : ")
        rating = int(input("pls give us a rating out of 5 : "))
        
        driver_user_id = random.randint(1,10) 
        query = "insert into reviews(feedback, rating, CUser_id, DUser_id) values ('%s', %d, %d, %d)" % (feedback, rating, user_id, driver_user_id)
        my_cursor.execute(query)
        connection1.commit()
    elif choice.lower()=='n':
        print("****************************************************************")
        ("thank you for your patience. ")


def show_price():
    print("****************************************************************")
    print("your trip costs : ", trip_charge)
    print("****************************************************************")






