import mysql.connector
import self_library as lib 




print("WELCOME TO SAARTHI, INDIA'S NUMBER ONE ONLINE CAB SERVICE")

while (1):
    fname = "'" + input("Please enter your first name  :    ") + "'"
    lname = "'" + input("Please enter your last name  :     ") + "'"
    lib.login(fname,lname)

    i = int(input("Press 1 to book a cab or 0 to exit:      "))
    if(i==1):
        r = int(input("Press 1 to reserve or 0 to book now:     "))
        if(r==1):
            
            
            lib.reserve_ride()
            lib.payment()
            lib.show_price()
            lib.leave_rating()
            print("****************************************************************")

            print("Thank you for using Saarthi!")

            exit(0)
        else:
            lib.book_ride()    
            lib.payment()
            lib.show_price()
            lib.leave_rating()
            print("****************************************************************")

            print("Thank you for using Saarthi!")

            exit(0)
    else:
        print("****************************************************************")
        print("Thank you for using Saarthi!")
        exit(0)        




