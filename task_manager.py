from datetime import date
from datetime import datetime

############################################### LOGGING IN #################################################################

task_file = open("tasks.txt","r+")
tasks = task_file.read()            #opening both task and users file to read them and put them into variables named tasks and users
task_file.close()

user_file = open("user.txt","r+")
users = user_file.read()
user_file.close()


users_list = users.split("\n")      #splitting the users string into a list using a new line as the separator. Each item in list will be in format (user, password) 
users_dict = {}                     #creating an open dictionary which will be populated by username: password
for n in users_list:                #iterating through the users list to convert each item (user, password) into a dictionary item (user:password).
    n = n.split(", ")                       #need to split each item at the point of the comma into two further items which can be separated when creating dictionary 
    users_dict[n[0]] = n[1]

logged_in = False 
while logged_in == False:
    user_username = input("Enter your username: ")          #login section. Using while loop to keep asking for login details until valid ones are entered 
    if user_username in users_dict:                         #checking if entered username is in dictionary as key. If not, will ask to try again. If in dictionary as key, will ask for password.
        user_password = input("Enter your password: ")      #if password is the right value for the key accessed in the dictionary - will log in and carry on to showing menu 
        if user_password == users_dict[user_username]:
            print("\n\nYou're logged in!")
            logged_in = True
        else:
            print("\n\nIncorrect password. Try again\n\n")
    else: 
        print("\n\nUsername not found. Try again\n\n")


########################################## DEFINING FUNCTIONS ################################################################


def reg_user():
    new_user_added = False
    if user_username == "admin":                            #check if username that has logged in is admin. If yes, will allow access. If not, will print statement saying no access
        while new_user_added == False:                              #using while loop to keep asking for details until passwords match. If they do not, while loop will cycle again.
            new_username = input("Enter a new username: ")
            while new_username in users_dict:               #using while loop to keep asking for another username is the one they picked is in the dictionary created from reading all current usernames and passwords
                new_username = input('\nThat username is already in use! Please choose another username: ')
            new_password = input("Enter a password: ")
            new_password_confirm = input("Enter the password again: ")
            if new_password_confirm == new_password: 
                with open("user.txt","a") as f:
                    f.write(f"\n{new_username}, {new_password}")        #opening the users file in a mode to add to it. will write the new details in the same format as previous ones 
                    f.close()
                    print("\n\nNew user has been added. Taking you back to menu.\n\n")
                    new_user_added = True
            else:
                    print("\n\nPasswords do not match. Try again\n\n")
    else: 
        print("\n\nYou do not have access to this! Returning to menu.\n\n") 


def add_task():
    task_user = input("Enter the username this task is assigned to: ")      
    task_title = input("Enter the title of the new task: ")
    task_description = input("Enter a description of the new task: ")
    task_due = input("Enter the due date of the task in the format dd/mm/yyyy: ")
    today = date.today()                                        #using datetime module to get todays date and convert into the same format that is requested by above input
    today = today.strftime("%d/%m/%Y")
    with open("tasks.txt", "a") as g:                           #opening task file in mode to add to it. writing the new task in the same order and format as previous ones. 
        g.write(f"{task_user}, {task_title}, {task_description}, {today}, {task_due}, No\n")
        print(f"\n{task_title} has been added for {task_user}!")


def view_all():
    with open("tasks.txt","r+") as n:                   #opening the tasks file to read it
        for line in n: 
            task = line.split(", ")                         #splitting each tasks by the comma to separate it into list of items. Using the format outlined above, can call certain indexes from list in print statement to show details of task.
            print(f"""                                      
_______________________________________________________

Task: {task[1]}
Assigned to: {task[0]}
Date assigned: {task[3]}                
Due date: {task[4]}
Task complete?: {task[5]}

Task description: {task[2]}

_______________________________________________________
""")
    n.close()



def view_mine():
    user_task = ""
    task_list = []
    task_dict = {}
    with open("tasks.txt","r+") as i:
        for line in i:              #opens file and puts all text into a text file         
            task_list.append(line)  #makes a list with each line of text being a separate item
    task_list_numbered = list(enumerate(task_list))  #enumerates the list - makes a nested list with each task being put together with a number starting from 0
    for n in task_list_numbered:         
        task = n[1].split(", ")     #iterates through list to make a dictionary which will show the task number as the key and the person assigned as the value
        task_num = n[0]             #dictionary will be used to check if the task number the user chooses to edit is their task. 
        task_dict[task_num] = task[0]
        if task[0] == user_username:            #when printing - will provide a task number next to 'task' which will be used for the user to call a task to edit 
            user_task = (f"""
_______________________________________________________

Task ({task_num + 1}): {task[1]}
Assigned to: {task[0]}
Date assigned: {task[3]}
Due date: {task[4]}
Task complete?: {task[5]}

Task description: {task[2]}

_______________________________________________________
""")        
            print(user_task)
    i.close()
    if user_task == "":                     #if the username logged in doesn't match any of the usernames that tasks are assigned to - prints you have no tasks
        print("\n\nYou have no tasks.\n\n")
    should_continue = True
    while should_continue:
        user_choice = int(input("\nPick a task you want to edit/complete. Type the number of the task from the above list OR type -1 to return to main menu: "))
        if user_choice == -1:           #using while loop to ask the user if they want to continue editing their tasks until they type -1
            should_continue = False
        elif task_dict[user_choice - 1] != user_username:       #if the number they chose is not a number that is assigned to one of their tasks, it will say error message and ask the question again
            print('\nThat task is not assigned to you.\n')
        else:
            for a,b in enumerate(task_list):
                if  a == user_choice - 1:                   #iterates through the task list to find the task the user wants to edit
                    task_check = b.split(', ')             
                    if task_check[5] == 'Yes\n':            #the 5th index of the the individal task (when split and named task_checker) is whether complete. If yes then error message saying can't edit it 
                        print('\nYou cannot edit a task that has been marked as complete')
                    else:
                        task_edit = int(input('\nType 1 to mark it as complete, 2 to edit the due date or 3 to change the user this task is assigned to: '))
                        if task_edit == 1:                      #asks for an input to see what user wants to do. If 1, will change the 5th index to Yes and join the list back into string form
                            task_check[5] = 'Yes\n'
                            task_check_string = ', '.join(task_check)
                            task_list[user_choice - 1] = task_check_string      #amends the overall task list replacing the task they selected with the changes
                            print('\nYour task has been marked as complete!\n')
                        elif task_edit == 2:
                            task_date = input('\nWhat should the new due date be? Type in dd/mm/yyyy format: ')
                            task_check[4] = task_date                       #allows user to change the 4th index of the individal task 'list' which is the due date. Joins it back into a string and inputs it into overall task list
                            task_check_string = ', '.join(task_check)
                            task_list[user_choice - 1] = task_check_string
                        elif task_edit == 3:
                            task_person = input('\nWho should this task be assigned to?: ') #allows user to change the 1st index of individual task 'list' which is the user assigned. 
                            while task_person not in users_dict:            #if the username they choose does not exist in the directory - will ask again to input a valid name
                                task_person = input('\nUnable to find user. Please ensure correct username inserted and username in use: ')
                            task_check[0] = task_person
                            task_check_string = ', '.join(task_check)       #rejoins the list as a string and inputs it into the overall task list in the right place 
                            task_list[user_choice - 1] = task_check_string
    task_text = ''.join(task_list)
    with open("tasks.txt",'w+') as f:
        f.write(task_text)                     #joins the overall task list into string format after all the changes and then overwrites the task file with the new string
    f.close()




def display_stats():
    if user_username == "admin":
        with open('task_overview.txt','r+') as r:
            for line in r:                      #opens the task overview file and prints what is in the file. Does same for user_overview file. ONLY IF ADMIN
                print(line)     
        r.close()
        with open('user_overview.txt','r+') as l:
            for line in l:
                print(line)
    else: 
        print("\n\nYou do not have access to this! Returning to menu.")


def generate_report():
    total_tasks = 0
    completed_tasks = 0                 #creates variables which will act as a counter for completed, incomplete, overdue tasks
    incomplete_tasks = 0
    tasks_overdue = 0
    total_users = 0
    user_overview_counter = {}
    user_overview_text = 'TASK MANAGER REPORT - USERS\n'
    if user_username == 'admin':                #can only be done as admin. 
        with open('user.txt','r+') as u:
            for line in u: 
                total_users += 1
                user_checker = line.split(', ')             #opens user file and uses counter to count how many users there are
                user_overview_counter[user_checker[0]] = []     #ADDS USERS TO A DICTIONARY - this will be used later to populate with a list per user counting whether tasks are complete, incomplete or overdue
        u.close()
        with open('tasks.txt','r+') as b:
            for line in b:                          #ITERATING THROUGH EACH TASK IN TASK FILE 
                total_tasks += 1
                task_checker = line.split(', ')                 #splits each line into a list from the task file. While iterating through each line(task) - will add to the counter of total tasks 
                if task_checker[5] == 'Yes\n':          
                    completed_tasks += 1                        
                    user_overview_counter[task_checker[0]] += 'y'   #if 5th index of task is yes, will add to counter of completed task. Will also add a y into the user_overview_counter dictionary - the key which it's added to is determined by the first index of task which is the user.
                elif task_checker[5] == 'No\n':
                    incomplete_tasks += 1
                    user_overview_counter[task_checker[0]] += 'n'   #same as above for incomplete tasks. 
                today_date = datetime.now()
                task_due_date = task_checker[4]
                task_due_formatted = datetime.strptime(task_due_date, '%d/%m/%Y')       #formats the string from the 4th index of the task (due date) using datetime module. This will allow comparison between that and todays date
                if today_date > task_due_formatted and task_checker[5] == 'No\n':
                    tasks_overdue += 1                                  #compares todays date to due date. If overdue, then will add to total overdue counter as well as adding an 'o' to the user_overview_counter dictionary (to the key defined in the 1st index of task)
                    user_overview_counter[task_checker[0]] += 'o'
        b.close()
        percentage_incomplete = (incomplete_tasks / total_tasks) * 100          #calculations to get percentage data. 
        percentage_overdue = (tasks_overdue / total_tasks) * 100
        with open('task_overview.txt','w+') as o:               #opens task_overview file and writes into it, the data as calculated from above lines. Will create new file if not present. Or overwrite previous file.
            o.write(f"""TASK MANAGER REPORT - TASKS

- Total number of tasks: {total_tasks}
- Completed tasks: {completed_tasks}
- Incomplete tasks: {incomplete_tasks}
- Tasks overdue: {tasks_overdue}
- Percentage incomplete: {percentage_incomplete}
- Percentage overdue: {percentage_overdue}
            
            """)
            o.close()
        for a in user_overview_counter: 
            user_completed_tasks = 0
            user_incomplete_tasks = 0                   #iterates through user_overview_counter dictionary which will look like {user: [y,n,o], user2: [n,n]} for example.
            user_overdue_tasks = 0 
            for b in user_overview_counter[a]: 
                if b == 'y':                        #iterates through the nested list in the keys (users) of dictionary. Will add to the counter of completed, incomplete and overdue tasks based on how many of each letter is in list.
                    user_completed_tasks += 1
                elif b == 'n':
                    user_incomplete_tasks += 1
                elif b == 'o':
                    user_overdue_tasks += 1   
            total_user_tasks = user_completed_tasks + user_incomplete_tasks     
            if total_user_tasks > 0:            #to avoid dividing by 0 error if there is a user but with no tasks assigned yet, will only carry on with calculations if total tasks is greater than 0. Otherwise will print no tasks for user.
                user_task_percentage = (total_user_tasks/total_tasks) * 100         
                user_task_completion_percentage = (user_completed_tasks/total_user_tasks) * 100
                user_task_incomplete_percentage = (user_incomplete_tasks/total_user_tasks) * 100            #calculations to get relevant data and will add to text string in a format that can be presented
                user_task_overdue_percentage = (user_overdue_tasks/total_user_tasks) * 100  
                user_overview_text += f''' 
User: {a}
    Total number of tasks assigned to user: {total_user_tasks}
    Percentage of total tasks assigned to user: {user_task_percentage}                      
    Percentage of tasks completed by user: {user_task_completion_percentage}
    Percentage of tasks incomplete by user: {user_task_incomplete_percentage}
    Percentage of tasks overdue for user: {user_task_overdue_percentage}
            '''
            else: 
                user_overview_text += f'''
User: {a}
    This user has no allocated tasks yet        
        ''' 
        with open('user_overview.txt','w+') as e:               #will open user_overview file and write into it the text that is produced from user_overview_text. Will overwrite or create new file if none present
            e.write(user_overview_text)
        e.close()
        print('\n\nReports have been generated in separate text files!\n')  
    else:
        print('\n\nYou do not have access to this! Returning to main menu.')    




####################################################### TASK MANAGER APP ##################################################################################



while logged_in == True:
    menu = input('''\n\nSelect one of the following Options below:
r - Registering a user (admin only)
a - Adding a task
va - View all tasks
vm - view my task
ds - display statistics (admin only)
gr - generate reports (admin only)
e - Exit
: ''').lower()
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':                 
        view_mine()
    elif menu == 'ds':
        generate_report()           #will generate report everytime before displaying it onto screen. 
        display_stats()
    elif menu == 'gr':
        generate_report()
    elif menu == 'e':
        print('\n\nGoodbye!!!\n\n')
        logged_in = False
        exit()
    else:
        print("\n\nYou have made a wrong choice, Please Try again\n\n")