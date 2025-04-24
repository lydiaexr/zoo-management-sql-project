import	PySimpleGUI  as	sg
import sqlite3
import base64
import time

##-------------------------------------------------------------------------------------------------------------------------------------
## Υπάρχουσες Καταχωρήσεις
def open_window_current_input():
    global conn
    global c
    animal = base64.b64encode(open("icons\See_Animals.png","rb").read())
    caring = base64.b64encode(open("icons\Caring.png","rb").read())
    feeds = base64.b64encode(open("icons\Feeds.png","rb").read())
    is_fed = base64.b64encode(open("icons\Is_fed.png","rb").read())
    is_next_to = base64.b64encode(open("icons\Is_next_to.png","rb").read())
    is_sick = base64.b64encode(open("icons\See_Is_sick.png","rb").read())
    living_space = base64.b64encode(open("icons\Living_space.png","rb").read())
    staff = base64.b64encode(open("icons\Staff.png","rb").read())
    treats = base64.b64encode(open("icons\See_Treats.png","rb").read())
    vet = base64.b64encode(open("icons\Vets.png","rb").read())
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [
                [sg.Button('',image_data=animal,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Animal'),
                sg.Button('',image_data=caring,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Caring'),
                sg.Button('',image_data=feeds,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Feeds'),
                sg.Button('',image_data=is_fed,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Is_fed')],
                [sg.Button('',image_data=is_next_to,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Is_next_to'),
                sg.Button('',image_data=is_sick,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Is_sick'),
                sg.Button('',image_data=living_space,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Living_space'),
                sg.Button('',image_data=treats,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Treats')],
                [sg.Button('',image_data=staff,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Staff'),
                sg.Button('',image_data=vet,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Vet')],
                [sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]              
              ]

    window = sg.Window("Δεδομένα Βάσης",layout,finalize=True,element_justification='c',resizable=True)
    
    while True:
        event,values = window.read()
        table = event
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == "Animal": 
            c.execute("Select * from Animal")
        elif event == "Caring":
            c.execute("Select * from Caring")
        elif event == "Feeds":
            c.execute("Select * from Feeds")
        elif event == "Is_fed":
            c.execute("Select * from Is_fed")
        elif event == "Is_next_to":
            c.execute("Select * from Is_next_to")
        elif event == "Is_sick":
            c.execute("Select * from Is_sick")
        elif event == "Living_space":
            c.execute("Select * from Living_space")
        elif event == "Staff":
            c.execute("Select * from Staff join Employee on SSN_staff=SSN_employee")
            table="Staff join Employee on SSN_staff=SSN_employee"
        elif event == "Treats":
            c.execute("Select * from Treats")
        elif event == "Vet":
            c.execute("Select * from Vet join Employee on SSN_vet=SSN_employee")
            table="Vet join Employee on SSN_vet=SSN_employee"
        data = c.fetchall()
        field_names = [i[0] for i in c.description]
        show_data(data,field_names,table)
    
    window.close()

## Συναρτήσεις για εκτύπωση και αναζήτηση δεδομένων
def show_data(x,headings,table,Q=False):
    save = base64.b64encode(open("icons\GO.png","rb").read())
    
    if Q:
        layout = [
                    [sg.Table(values=x,headings=headings,max_col_width=30,auto_size_columns=True,bind_return_key=True,justification='c',num_rows=20,alternating_row_color='lightgray',font=("Calibri",12))]
                ] 
    else:
        layout = [
                    [sg.Text('Αναζήτηση',size=(12,1)),
                    sg.Combo(headings,size=20,readonly=True,key='combo'),  
                    sg.InputText(), 
                    sg.Button('',image_data=save,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Search')], 
                    [sg.Text('Ταξινόμηση ανά',size=(12, 1)), 
                    sg.Combo(headings,size=20,readonly=True,key='sort_it'),
                    sg.Checkbox('Φθίνουσα σειρά',default=False,key="Desc")],
                    [sg.Table(values=x,headings=headings,max_col_width=60,auto_size_columns=True,bind_return_key=True,justification='c',num_rows=35,alternating_row_color='lightgray',font=("Calibri",12))]
                ] 
    
    window = sg.Window('Δεδομένα Βάσης',layout,ttk_theme='clam',resizable=True,finalize=True,return_keyboard_events=True)

    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Search'or event == "\r":
            combo = values['combo']
            sort_it = values['sort_it']
            Desc = values["Desc"]
            window.close()
            Search_in_data(values[0],table,combo,sort_it,Desc)
            
    window.close()

def Search_in_data(num,table,combo,sort_it,d):
    global c
    if (d == True): d = "DESC" 
    else: d = "ASC"
    if (num == "" or combo == ""):
        if (sort_it == ""):
            c.execute("SELECT * FROM " + table)
        else: c.execute("SELECT * FROM " + table + " ORDER BY " + sort_it + " " + d)
    else:
        if (sort_it == ""):
            c.execute("SELECT * FROM " + table + " WHERE " + combo + "=?",[(num)])
        else: c.execute("SELECT * FROM " + table + " WHERE " + combo + "=? ORDER BY " + sort_it + " " + d,[(num)])
    data = c.fetchall()
    field_names = [i[0] for i in c.description]
    show_data(data,field_names,table)

##-------------------------------------------------------------------------------------------------------------------------------------
## Νέες Καταχωρήσεις
def open_window_input():
    animal = base64.b64encode(open("icons\Animal.png","rb").read())
    food = base64.b64encode(open("icons\Food.png","rb").read())
    treats = base64.b64encode(open("icons\Treats.png","rb").read())
    is_sick = base64.b64encode(open("icons\sick.png","rb").read())
    caring = base64.b64encode(open("icons\Cage.png","rb").read())
    employee = base64.b64encode(open("icons\employee.png","rb").read())
    death = base64.b64encode(open("icons\Death.png","rb").read())
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [  
                [sg.Button('',image_data=animal,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Animal'),
                sg.Button('',image_data=food,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Food'),
                sg.Button('',image_data=treats,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Treats'),
                sg.Button('',image_data=is_sick,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Is_sick')],
                [sg.Button('',image_data=caring,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Caring'),
                sg.Button('',image_data=employee,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Employee')], 
                [sg.Button('',image_data=death,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Die')],
                [sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')] 
            ]
    
    window = sg.Window("Νέα Καταχώρηση",layout,finalize=True,element_justification='c',resizable=True) 
    choice = None
    
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Animal": open_window_animal()
        elif event == "Food": open_food_window()
        elif event == "Food": open_food_window()
        elif event == "Treats": open_treats_window()
        elif event == "Is_sick": open_sick_window()
        elif event == "Caring": open_caring_window()
        elif event == "Employee": open_employee_window()
        elif event == "Die": open_death_window()
        
    window.close()

## Συναρτήσεις για κάθε ένα παραθύρο καταχώρησης στοιχείων
def open_window_animal():
    global conn
    save = base64.b64encode(open("icons\SUBMIT.png","rb").read())
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [
                [sg.Text('Παρακαλώ εισάγετε τα στοιχεία του ζώου',text_color='black',font=("Calibri",25))],
                [sg.Text('Κωδικός Ζώου',size=(25,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Όνομα Ζώου',size=(25,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Είδος Ζώου',size =(25,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Κωδικός Κλουβιού Διαμονής',size=(25,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Ημερομηνία Γέννησης',size=(25,1),text_color='black',font=("Calibri",15)),
                sg.Text('Ημέρα',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)),
                sg.Text('Μήνας',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)),
                sg.Text('Χρόνος',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(4,1))],
                [sg.Text('Φύλο',size=(25,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Βάρος',size=(25,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Button('',image_data=save,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Save_Animal'),
                sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]
            ]
    
    window = sg.Window( "Νέο Ζώο", layout, finalize=True, element_justification='c',resizable=True, return_keyboard_events=True)
    
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event=='Exit':
            break
        elif event == 'Save_Animal' or event=='\r':
            error=check_error(values)
            if error == 0:
                values[4]=values[6]+"-"+values[5]+"-"+values[4]
                try:
                    conn.execute('''INSERT  INTO Animal VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',(int(values[0]), values[2], int(values[3]), values[1], values[4], values[7], int(values[8]), "NULL"))
                    conn.commit()
                    break 
                except ValueError as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)   
                except sqlite3.Error as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
            else: error_message("Παρακαλώ εισάγετε τιμές")      
    
    window.close()

def open_food_window():
    global conn
    save = base64.b64encode(open("icons\SUBMIT.png","rb").read()) 
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [
                [sg.Text('Παρακαλώ εισάγετε τα στοιχεία του ζώου και της τροφης του',text_color='black',font=("Calibri",25))],
                [sg.Text('Κωδικός Ζώου',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Είδος Τροφής',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('AΦΜ προσωπικού',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Ημερομηνία Ταΐσματος',size=(20,1),text_color='black',font=("Calibri",15)),
                sg.Text('Ημέρα',size=(5,1),text_color='black',font=("Calibri", 15)),sg.InputText(size=(2,1)),
                sg.Text('Μήνας',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)),
                sg.Text('Χρόνος',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(4,1)),
                sg.Text('Ώρα',size=(3,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)),
                sg.Text(":",size=(1,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1))],
                [sg.Text('Ποσότητα',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Button('',image_data=save,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Save_Food'),
                sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]
            ]
    window = sg.Window("Νέα Καταχώρηση",layout,finalize=True,element_justification='c',resizable=True,return_keyboard_events=True) 
    
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save_Food' or event == '\r':
            error = check_error(values)
            if error == 0:
                values[3] = values[5] + "-" + values[4] + "-" + values[3]
                values[6] = values[6] + ":" + values[7]
                try :
                    conn.execute('''INSERT  INTO Feeds VALUES (?, ?, ?, ?, ?, ?);''',(values[1],int(values[2]),int(values[0]),values[3],values[6],int(values[8])))
                    conn.commit()
                    break
                except ValueError as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
                except sqlite3.Error as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message) 
            else: error_message("Παρακαλώ εισάγετε τιμές")      
    
    window.close()

def open_treats_window():
    global conn
    save = base64.b64encode(open("icons\SUBMIT.png","rb").read())
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [
                [sg.Text('Παρακαλώ εισάγετε τα στοιχεια για την περίθαλψη',text_color='black',font=("Calibri",25))],
                [sg.Text('Κωδικός Ζώου',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Όνομα ασθένειας',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('AΦΜ κτηνιάτρου',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Ημερομηνία Περίθαλψης',size=(32,1),text_color='black',font=("Calibri",15)),
                sg.Text('Ημέρα',size=(5,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)),
                sg.Text('Μήνας',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)),
                sg.Text('Χρόνος',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(4,1))], 
                [sg.Text('Φάρμακο',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Button('',image_data=save,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Save_Treats'),
                sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]
            ]
    
    window = sg.Window("Νέα Καταχώρηση",layout,finalize=True,element_justification='c',resizable=True,return_keyboard_events=True) 
    
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save_Treats' or event == '\r':
            error = check_error(values)
            if error == 0:
                values[3] = values[5] + "-" + values[4] + "-" + values[3]
                try :
                    conn.execute('''INSERT  INTO Treats VALUES (?, ?, ?, ?, ?);''',(values[1],int(values[0]),int(values[2]),int(values[6]),values[3]))
                    conn.commit()
                except ValueError as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
                except sqlite3.Error as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
            else : error_message("Παρακαλώ εισάγετε τιμές")
                
            break          
    
    window.close()

def open_sick_window():
    global conn
    save = base64.b64encode(open("icons\SUBMIT.png","rb").read())
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [
                [sg.Text('Παρακαλώ εισάγετε τα στοιχεια για την ασθένεια του ζώου',text_color='black',font=("Calibri",25))],
                [sg.Text('Κωδικός Ζώου',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Όνομα ασθένειας',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Ημερομηνία Διάγνωσης',size=(32,1),text_color='black',font=("Calibri",15)),
                sg.Text('Ημέρα',size=(5,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)),
                sg.Text('Μήνας',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)), 
                sg.Text('Χρόνος',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(4,1))], 
                [sg.Button('',image_data=save,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Save_sick'),
                sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]
            ]
    
    window = sg.Window("Νέα Καταχώρηση",layout,finalize=True,element_justification='c',resizable=True,return_keyboard_events=True) 
    
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save_sick' or event == "\r":
            error=check_error(values)
            if error == 0:
                values[2] = values[4] + "-" + values[3] + "-" + values[2]
                try:
                    conn.execute('''INSERT  INTO Is_sick VALUES (?, ?, ?);''',(int(values[0]),values[1],values[2]))
                    conn.commit()
                    break 
                except ValueError as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
                except sqlite3.Error as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
            else: error_message("Παρακαλώ εισάγετe τιμές")    
    
    window.close()

def open_caring_window():
    global conn
    save = base64.b64encode(open("icons\SUBMIT.png","rb").read())
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [
                [sg.Text('Παρακαλώ εισάγετε τα στοιχεια για την περιποίηση του κελιού',text_color='black',font=("Calibri",25))],
                [sg.Text('Κωδικός Κελιού',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('ΑΦΜ προσωπικού',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Ημερομηνία Περιποίησης',size=(32,1),text_color='black',font=("Calibri",15)),
                sg.Text('Ημέρα',size=(5,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)),
                sg.Text('Μήνας',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)), 
                sg.Text('Χρόνος',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(4,1))], 
                [sg.Button('',image_data=save,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Save_caring'),
                sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]
            ]
    
    window = sg.Window("Νέα Καταχώρηση",layout,finalize=True,element_justification='c',resizable=True,return_keyboard_events=True) 
    
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save_caring' or event == '\r':
            error=check_error(values)
            if error == 0:
                values[2] = values[4] + "-" + values[3] + "-" + values[2]
                try:
                    conn.execute('''INSERT  INTO Caring VALUES (?, ?, ?);''',(int(values[1]),int(values[0]),values[2]))
                    conn.commit()
                    break   
                except ValueError as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
                except sqlite3.Error as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
            else: error_message("Παρακαλώ εισάγετε τιμές")     
    
    window.close()

def open_employee_window():
    global conn
    save = base64.b64encode(open("icons\SUBMIT.png","rb").read())
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [
                [sg.Text('Παρακαλώ εισάγετε τα στοιχεια του υπαλλήλου',text_color='black',font=("Calibri",25))],
                [sg.Text('Όνομα',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Επώνυμο',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('ΑΦΜ',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Τηλέφωνο',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Διεύθυνση',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Radio('Κτηνίατρος',"RADIO1",font=("Calibri",15),default=False,key="5"),
                sg.Radio('Προσωπικό',"RADIO1",font=("Calibri",15),default=False,key="6")],
                [sg.Button('',image_data=save,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Save_employee'),
                sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]
                
            ]
    
    window = sg.Window("Νέα Καταχώρηση",layout,finalize=True,element_justification='c',resizable=True,return_keyboard_events=True) 
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event =='Exit':
            break
        elif event == 'Save_employee' or event == "\r":
            error = check_error(values)
            if error == 0:
                try :
                    if (values['5']==False and values['6']==False): error_message("Παρακαλώ εισάγετε την ειδικότητα του νέου υπαλλήλου")
                    else:
                        conn.execute('''INSERT  INTO Employee VALUES (?, ?, ?, ?, ?);''',(int(values[2]),int(values[3]),values[0],values[1],values[4]))
                        if values['5'] == 1:
                            conn.execute('''INSERT  INTO Vet VALUES (?)''',(int(values[2]),))
                            conn.commit()
                            break
                        elif values['6'] == 1:
                            conn.execute('''INSERT  INTO Staff VALUES (?)''',(int(values[2]),))
                            conn.commit()
                            break
                except ValueError as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
                except sqlite3.Error as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)
            else: error_message("Παρακαλώ εισάγετε τιμές")
    
    window.close()   

def open_death_window():
    global conn
    save = base64.b64encode(open("icons\SUBMIT.png","rb").read())
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [
                [sg.Text('Παρακαλώ εισάγετε τα παρακάτω στοιχεία',text_color='black',font=("Calibri",25))],
                [sg.Text('Κωδικός Ζώου',size=(30,1),text_color='black',font=("Calibri",15)),sg.InputText()],
                [sg.Text('Ημερομηνία Θανάτου',size =(32, 1), text_color='black', font=("Calibri", 15)),
                sg.Text('Ημέρα',size=(5,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)), 
                sg.Text('Μήνας',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(2,1)), 
                sg.Text('Χρόνος',size=(6,1),text_color='black',font=("Calibri",15)),sg.InputText(size=(4,1))],
                [sg.Button('',image_data=save,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Save_Death'),
                sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]
            ]
    
    window = sg.Window("Νέα Καταχώρηση",layout,finalize=True,element_justification='c',resizable=True,return_keyboard_events=True) 
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save_Death' or event == '\r':
            error = check_error(values)
            if error == 0:
                values[1] = values[3] + "-" + values[2] + "-" + values[1]
                try:
                    conn.execute("UPDATE Animal SET Death_date = ? WHERE Animal_id=?",[values[1],(int(values[0]))])
                    conn.commit()
                    if c.rowcount < 1 :
                        message = "Παρακαλώ εισάγετε σωστές τιμές, δεν υπάρχει το primary key"
                        error_message(message)
                    break   
                except ValueError as error:
                    message = "Παρακαλώ εισάγετε σωστές τιμές, " + str(error)
                    error_message(message)                
            else: error_message("Σφάλμα! Παρακαλώ εισάγετε τιμές")      
    
    window.close()

## Συναρτήσεις για διαχείριση Error
def check_error(values):
    for i in range (len(values)):
        if i in values:
            if (values[i] == ""):
                return 1
        return 0      
            
def error_message(str):
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    layout = [[sg.Text(str,text_color='red',font=("Calibri",25)),
    sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]]  
    
    window = sg.Window("ΕRROR",layout,finalize=True,element_justification='c',resizable=True) 
    
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break 
    
    window.close()

##-------------------------------------------------------------------------------------------------------------------------------------
## Queries
def open_query_window():
    go = base64.b64encode(open("icons\go2.png","rb").read())
    cancel = base64.b64encode(open("icons\cancel.png","rb").read())
    
    layout = [
                [sg.Text('Παρακαλώ διαλέξτε Query',text_color='black',font=("Calibri",15))],                
                [sg.Radio('Ποιο κλουβί έχει τα περισσότερα διπλανά κλουβιά;',"RADIO1",default=False,key="1")],
                [sg.Radio('Ποια είδη ζώων υπάρχουν στον κήπο και πόσα ζώα υπάρχουν από το καθέ ένα;',"RADIO1",default=False,key="2")],
                [sg.Radio('Ποιος είναι ο μεσος όρος ηλικίας των ζωντανών ζώων;',"RADIO1",default=False,key='3')],
                [sg.Radio('Ποια ζώα που εχουν πεθάνει είχαν αρρωστήσει πάνω από 2 φορές τον ίδιο χρόνο;',"RADIO1",default=False,key='4')],
                [sg.Radio('Ποιοι υπάλληλοι ταίζουν τα ζώα περισσότερο από το επιθυμητό;',"RADIO1",default=False,key='5')],
                [sg.Radio('Ποιο είδος ζώου μένει σε κλουβί χωρίς να συμβιώνει με άλλο είδος;',"RADIO1",default=False,key='6')],
                [sg.Radio('Ανάμεσα στα μακροβιότερα ζώα του κήπου, ποιες τροφές είναι οι πιο συνηθισμένες;',"RADIO1",default=False,key="7")],
                [sg.Button('',image_data=go,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Go'),
                sg.Button('',image_data=cancel,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='Exit')]
            ]
    
    window = sg.Window("Queries",layout,finalize=True,element_justification='c',resizable=True,return_keyboard_events=True) 
    
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Go':
            index2=None
            if values["1"] == True: 
                index = "Create index ind1 on Feeds(Animal_id)"
                sql = "select Cage_id_is, count(Cage_id_near) as maxim FROM Is_next_to group by Cage_id_is having maxim= (SELECT MAX(next) FROM (  SELECT Cage_id_is, count(cage_id_near) as next FROM Is_next_to GROUP by Cage_id_is))"
            if values["2"] == True:
                index = "Create index ind1 on Species(Species_name)"
                sql = "Select Species_name,COUNT(Species_name) FROM Animal GROUP BY Species_name"
            if values["3"] == True: 
                index = "Create index ind1 on Feeds(Animal_id)"
                sql = "Select AVG(date('now')-Birthday) as Average_Age from Animal where Death_date is NULL"
            if values["4"] == True:
                index = "Create index ind1 on Animal(Animal_id)"
                index2 = "Create index ind2 on Is_sick(Animal_id)"
                sql = "Select Animal_id,Species_name from Animal natural join Is_sick where Death_date is not Null and strftime('%Y',Death_date)=strftime('%Y',Diagnosis_date) group by Animal_id HAVING count(Animal_id)>1"
            if values["5"] == True:
                index = "Create index ind1 on Is_fed(Animal_id)"
                index2 = "Create index ind2 on Feeds(Animal_id)"
                sql = "Select Employee_name,Surname,SSN_staff from Animal NATURAL JOIN Feeds NATURAL join Is_fed join Employee on SSN_staff=SSN_employee where Ideal_quantity<Quantity group by SSN_staff"
            if values["6"] == True:
                index = "Create index ind1 on Animal(Animal_id)"
                sql = "Select Species_name from(Select * FROM Animal GROUP by Species_name) GROUP by Cage_id HAVING count(Cage_id)=1"
            if values["7"] == True:
                index = "Create index ind1 on Animal(Animal_id)"
                sql = "select Food_name, count(Food_name) as Fr from Is_fed where Animal_id in (select Animal_id from (Select Animal_id, date('now')-Birthday as age from Animal where Death_date is NULL UNION select Animal_id, Death_date-Birthday from Animal where Death_date is not NULL) where age =(select max(age) as old from (Select date('now')-Birthday as age from Animal where Death_date is NULL UNION select Death_date-Birthday from Animal where Death_date is not NULL order by age desc))) group by Food_name having Fr>1 order by Fr Desc"
            query(sql,index,index2)
                    
    window.close()

def query(sql,index, index2):
    global c
    
    c.execute("drop index if exists ind1")
    c.execute("drop index if exists ind2")
    t1 = time.perf_counter()
    c.execute(sql)
    sql_time = time.perf_counter() - t1
    print(f'Eκτέλεση εντολής χωρίς ευρετήριο σε {sql_time:.5f} sec')
    c.execute(index)
    if index2 is not None:
        c.execute(index2)
    t2 = time.perf_counter()
    c.execute(sql)
    sql_time_index = time.perf_counter() - t2
    print(f'Eκτέλεση εντολής με ευρετήριο σε {sql_time_index:.5f} sec')
     
    data = c.fetchall()
    field_names = [i[0] for i in c.description]
    show_data(data,field_names,None,True)

##-------------------------------------------------------------------------------------------------------------------------------------

## Main 
def main():
    global conn
    global c
    conn = sqlite3.connect("zoo_db.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    sg.theme('LightGreen3')
    inputdata = base64.b64encode(open("icons\insert_data.png","rb").read())
    readydata = base64.b64encode(open("icons\ReadData.png","rb").read())
    query  = base64.b64encode(open("icons\query.png","rb").read())
    
    layout = [	
                [sg.Text('Καλώς Ορίσατε!',size=(50,0),font=("Calibri",20),justification='center',text_color='black')],[sg.VPush()],
                [sg.Text('Σύστημα διαχείρισης ζώων ζωολογικού κήπου',size=(50,1),font=("Calibri",15),justification='center',text_color='black')],
                [sg.Image('icons\Zoo-PNG-Transparent-Image.png',size=(800,210))],
                [sg.Button("",image_data=readydata,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key="curr_input"),
                sg.Button("",image_data=inputdata,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key="new_input"),
                sg.Button("",image_data=query,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key="query")]
            ]
    window = sg.Window("Ζωολογικός κήπος",layout,finalize=True,element_justification='c',resizable=True) 
    
    while True:
        event,values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "new_input":
            open_window_input()
        elif event == "curr_input":
            open_window_current_input()
        elif event == "query":
            open_query_window()
    
    conn.close()
    window.close()
    
if __name__ == "__main__":
    main()