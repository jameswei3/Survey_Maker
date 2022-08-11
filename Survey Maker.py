from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

#setup
root = Tk()
root.geometry("1000x500")
root.title("Survey Maker")

connection = mysql.connector.connect(host='<host>',database = '<database>', user='<user>',password='<password>')
cursor = connection.cursor(buffered=True)


#destroy all widgets
def ClrAllWidgets():
    for widget in root.winfo_children():  #all widgets in a frame
        widget.destroy()

#check connection
def PreStart():
    global connection
    try:
        if connection.is_connected():
            start()
    except:
        failtoconnect()

#connection fails
def failtoconnect():
    ClrAllWidgets()
    failLab = Label(root,text='Connection failed. Try again.',font=('Arial',42)).pack()
    failBut = Button(root,text='Reload',width=12,height=2,command=PreStart).pack()

#start
def start():
    ClrAllWidgets()
    ClrAllWidgets()
    startLabel = Label(root,text='Survey Creator',font=('Arial',50))
    startLabel.pack()

    startButton = Button(root, text='Start', width=25, height=4,command=Login)
    startButton.pack()

#Login & register
def Login():
    global userEntry
    global passEntry
    ClrAllWidgets()
    loginLab = Label(root,text='Login',font=('Arial',50)).place(x=450)
    userLab = Label(root,text='Username',font=('Arial',10)).place(x=400,y=100)
    userEntry = Entry(root)
    userEntry.place(x=470, y=100)
    passLab = Label(root, text='Password', font=('Arial', 10)).place(x=400, y=120)
    passEntry = Entry(root, show='*')
    passEntry.place(x=470, y=120)
    enterBut = Button(root, text='Submit',font=('Arial',15),width=10,height=3,command=LoginValidate).place(x=430,y=150)
    RegisBut = Button(root,text="Don't have an account? Register!",font=('Arial',7),command=Register).place(x=450,y=250)

def LoginValidate():
    global userget
    global passget
    userget = str(userEntry.get())
    passget = str(passEntry.get())

    sql_check = f"""SELECT password FROM profiles
                                    WHERE 
                                    username = '{userget}'"""
    cursor.execute(sql_check)
    connection.commit()

    try:
        sql_check_val = cursor.fetchall()[0][0]
        connection.commit()

        if passget != sql_check_val:
             messagebox.showerror(title='Error',message="Sorry. Username or password does not match, or no such username exists.")
        else:
            Menu()
    except:
        messagebox.showerror(title='Error',message="No username exists. Try again")

def Register():
    global userEntry
    global passEntry
    global cpassEntry
    ClrAllWidgets()
    registerLab = Label(root,text='Register',font=('Arial',50)).place(x=400)
    userLab = Label(root,text='Username',font=('Arial',10)).place(x=400,y=100)
    userEntry = Entry(root)
    userEntry.place(x=470,y=100)
    passLab = Label(root,text='Password',font=('Arial',10)).place(x=400,y=120)
    passEntry = Entry(root,show='*')
    passEntry.place(x=470,y=120)
    cpassLab = Label(root,text='Confirm Password',font=('Arial',10)).place(x=350,y=140)
    cpassEntry = Entry(root,show='*')
    cpassEntry.place(x=470,y=140)
    enterBut = Button(root, text='Submit',font=('Arial',12),width=10,height=3,command=RegisterValidate).place(x=430,y=170)
    LoginBut = Button(root, text="Back to Login", font=('Arial', 7), command=Login).place(x=450,y=250)

def RegisterValidate():
    global userget
    global passget
    global cpassget
    userget = str(userEntry.get())
    passget = str(passEntry.get())
    cpassget = str(cpassEntry.get())

    try:
        if passget != cpassget:
             messagebox.showerror(title='Error',message="Password does not match with confirmed password. Try again.")
        elif userget == '':
             messagebox.showerror(title='Error',message="Username can't be empty. Try again.")
        elif len(userget) > 15:
             messagebox.showerror(title='Error',message="Username is too long. Try again.")

        else:
            sql_register = f'''INSERT INTO profiles (username,password) 
                                       VALUES 
                                      ("{userget}","{passget}")'''
            cursor.execute(sql_register)
            connection.commit()
            Menu()
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror(title='Error',message="Sorry. The username is already taken.")

#The homepage
def Menu():
    username = StringVar()
    username.set(userget)
    ClrAllWidgets()
    Taskbar = Frame(root,height=50,width=1000,bg="red")
    Taskbar.pack(side=BOTTOM)
    usernameLab = Label(Taskbar,textvariable=username,font=('Arial',8))
    usernameLab.place(x=5)
    createBut = Button(Taskbar,text='Manage Survey',font=('Arial',7),width=50,height=4,command=Survey)
    createBut.place(x=67)
    homeBut = Button(Taskbar,text='Home',font=('Arial',7),width=50,height=4,command=Menu)
    homeBut.place(x=367)
    profileBut = Button(Taskbar,text='Logout',font=('Arial',7),width=50,height=4,command=Login)
    profileBut.place(x=667)

    #scrollbar
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH,expand=1)
    canvas = Canvas(main_frame)
    canvas.pack(side=LEFT,fill=BOTH,expand=1)
    scrollbar = ttk.Scrollbar(main_frame,orient=VERTICAL,command=canvas.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    second_frame = Frame(canvas)
    canvas.create_window((0,0),window=second_frame,anchor='nw')

    sql_survey_test = f"""SELECT surveyname FROM surveyq"""
    cursor.execute(sql_survey_test)
    asc = cursor.fetchall()
    for tuple in asc:
        for data in tuple:
            SurveyDoBut = Button(second_frame,text=data, font=('Arial', 15),
                                   command=lambda data=data:Fill(data))
            SurveyDoBut.pack()

def Survey():
    global surveynum
    global nd
    username = StringVar()
    username.set(userget)
    ClrAllWidgets()
    Taskbar = Frame(root, height=50, width=1000, bg="red")
    Taskbar.pack(side=BOTTOM)
    usernameLab = Label(Taskbar, textvariable=username, font=('Arial', 8))
    usernameLab.place(x=5)
    createBut = Button(Taskbar, text='Manage Survey', font=('Arial', 7), width=50, height=4,command=Survey)
    createBut.place(x=67)
    homeBut = Button(Taskbar, text='Home', font=('Arial', 7), width=50, height=4,command=Menu)
    homeBut.place(x=367)
    profileBut = Button(Taskbar, text='Logout', font=('Arial', 7), width=50, height=4,command=Login)
    profileBut.place(x=667)

    #Add&Delete Survey Frame
    surveyFrame = Frame(root,height=100,width=1000)
    surveyFrame.pack(side=BOTTOM)
    addsButton = Button(surveyFrame,text='Add',font=('Arial',15),width=25,height=5,command=Add)
    addsButton.place(x=20)
    delsButton = Button(surveyFrame,text='Delete',font=('Arial',15),width=25,height=5,command=Delete)
    delsButton.place(x=500)

    surveynum = 0

    sql_survey_test = f"""SELECT surveyname FROM surveys
                                                           WHERE 
                                                        username = '{userget}'"""
    cursor.execute(sql_survey_test)
    nd = cursor.fetchall()
    if nd != None:
        connection.commit()
        surveynum += len(nd)
    else:
        pass
    lin = 0
    labpos = 0

    try:
        for i in range(surveynum):
            snsv = nd[lin][0]
            snamelab = Button(root,text=snsv,font=('Arial',15),command=lambda snsv=snsv:Data(snsv))
            snamelab.place(x=50+labpos,y=10)
            lin += 1
            labpos += 200
    except:
        pass


def Add():
    global newEntry
    if surveynum > 5:
        messagebox.showerror(title='Error',message='You already have 5 surveys. Try deleting one.')
    else:
        ClrAllWidgets()
        backButton = Button(root, text='Back', font=('Arial', 7), command=Survey).place(x=0, y=0)
        addLab = Label(root, text='New Survey', font=('Arial', 50)).place(x=350)
        addinfoLab = Label(root, text='Please enter a survey name:', font=('Arial', 10)).place(x=400, y=100)
        newEntry = Entry(root)
        newEntry.place(x=420, y=150)
        enterBut = Button(root, text='Submit', font=('Arial', 15), width=10, height=3, command=PostAdd).place(x=430, y=180)


def Delete():
    ClrAllWidgets()
    backButton = Button(root, text='Back', font=('Arial', 7), command=Survey).place(x=0, y=0)
    for tuples in nd:
        for results in tuples:
            TKRESULTS = StringVar()
            TKRESULTS.set(results)
            butText = TKRESULTS.get()
            SurveyEditBut = Button(root, text=TKRESULTS.get(), font=('Arial', 7),
                                   command=lambda butText=butText: DeleteSurvey(butText))
            SurveyEditBut.pack()

def DeleteSurvey(survey):
    sql_delete_search = f"DELETE FROM surveys WHERE surveyname = '{survey}'"
    sql_delete_search2 = f"DELETE FROM surveyq WHERE surveyname = '{survey}'"
    sql_delete_search3 = f"DELETE FROM surveymc WHERE surveyname = '{survey}'"
    sql_delete_search4 = f"DELETE FROM surveya WHERE surveyname = '{survey}'"
    cursor.execute(sql_delete_search)
    cursor.execute(sql_delete_search2)
    cursor.execute(sql_delete_search3)
    cursor.execute(sql_delete_search4)
    connection.commit()
    messagebox.showinfo(title='Success',message='The survey is successfully deleted.')
    Survey()
def PostAdd():
    global newget
    newget = str(newEntry.get())
    moveon = True
    try:
        sql_survey_test = f"""SELECT surveyname FROM surveys
                                                                   WHERE 
                                                                username = '{userget}'"""
        cursor.execute(sql_survey_test)
        surveytest = cursor.fetchall()
        for results in surveytest:
            for survey in results:
                if newget == survey:
                    messagebox.showerror(title='Error',message='Another survey with the same name exists. Try again.')
                    moveon = False
                else:
                    pass
        if newget == '':
            messagebox.showerror(title='Error',message="Survey name can't be empty. Try again.")
            moveon = False

        if moveon == True:
            Edit(newget)
        else:
            pass


    except SyntaxError:
        messagebox.showerror(title='Error',message='Another survey with the same name exists. Try again.')

def Edit(surveyn):
    global delete
    global addq1choice1
    global addq1choice2
    global addqFrame1
    global addqFrame2
    global addqFrame3
    global addqFrame4
    global addqFrame5
    global pressBut

    pressBut = 0

    delete = False
    newname = StringVar()
    newname.set(surveyn)
    ClrAllWidgets()

    #scrollbar
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH,expand=1)
    canvas = Canvas(main_frame)
    canvas.pack(side=LEFT,fill=BOTH,expand=1)
    scrollbar = ttk.Scrollbar(main_frame,orient=VERTICAL,command=canvas.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    second_frame = Frame(canvas)
    canvas.create_window((0,0),window=second_frame,anchor='nw')

    titleFrame = Frame(second_frame,highlightbackground="black", highlightthickness=2)
    titleFrame.pack(side=TOP,padx=20,pady=20)
    addLab = Label(titleFrame, textvariable=newname, font=('Arial', 50)).pack()
    backButton = Button(second_frame,text='Back',font=('Arial',7),command=Survey).place(x=0,y=0)

    addqFrame1 = Frame(second_frame,width=500,highlightbackground='black',highlightthickness=2)
    addqFrame1.pack(side=TOP,pady=50)
    addqEntry1 = Entry(addqFrame1,font=('Arial',15))
    addqEntry1.pack()
    addq1choice1 = Button(addqFrame1,width=30,height=5,text='Multiple Choice',font=('Arial',10),command=lambda:multipleC(addqFrame1,addq1choice1,addq1choice2))
    addq1choice1.pack(side=LEFT)
    addq1choice2 = Button(addqFrame1, width=30, height=5, text='Short response', font=('Arial', 10),command=lambda: shortR(addq1choice1,addq1choice2))
    addq1choice2.pack(side=RIGHT)

    addqFrame2 = Frame(second_frame, width=500, highlightbackground='black', highlightthickness=2)
    addqFrame2.pack(side=TOP, pady=50)
    addqEntry2 = Entry(addqFrame2, font=('Arial', 15))
    addqEntry2.pack()
    addq2choice1 = Button(addqFrame2, width=30, height=5, text='Multiple Choice', font=('Arial', 10),
                          command=lambda: multipleC(addqFrame2, addq2choice1, addq2choice2))
    addq2choice1.pack(side=LEFT)
    addq2choice2 = Button(addqFrame2, width=30, height=5, text='Short response', font=('Arial', 10), command=lambda:  shortR(addq2choice1,addq2choice2))
    addq2choice2.pack(side=RIGHT)

    addqFrame3 = Frame(second_frame, width=500, highlightbackground='black', highlightthickness=2)
    addqFrame3.pack(side=TOP, pady=50)
    addqEntry3 = Entry(addqFrame3, font=('Arial', 15))
    addqEntry3.pack()
    addq3choice1 = Button(addqFrame3, width=30, height=5, text='Multiple Choice', font=('Arial', 10),
                          command=lambda: multipleC(addqFrame3, addq3choice1, addq3choice2))
    addq3choice1.pack(side=LEFT)
    addq3choice2 = Button(addqFrame3, width=30, height=5, text='Short response', font=('Arial', 10),
                          command=lambda: shortR(addq3choice1, addq3choice2))
    addq3choice2.pack(side=RIGHT)

    addqFrame4 = Frame(second_frame, width=500, highlightbackground='black', highlightthickness=2)
    addqFrame4.pack(side=TOP, pady=50)
    addqEntry4 = Entry(addqFrame4, font=('Arial', 15))
    addqEntry4.pack()
    addq4choice1 = Button(addqFrame4, width=30, height=5, text='Multiple Choice', font=('Arial', 10),
                          command=lambda: multipleC(addqFrame4, addq4choice1, addq4choice2))
    addq4choice1.pack(side=LEFT)
    addq4choice2 = Button(addqFrame4, width=30, height=5, text='Short response', font=('Arial', 10),
                          command=lambda: shortR(addq4choice1, addq4choice2))
    addq4choice2.pack(side=RIGHT)

    addqFrame5 = Frame(second_frame, width=500, highlightbackground='black', highlightthickness=2)
    addqFrame5.pack(side=TOP, pady=50)
    addqEntry5 = Entry(addqFrame5, font=('Arial', 15))
    addqEntry5.pack()
    addq5choice1 = Button(addqFrame5, width=30, height=5, text='Multiple Choice', font=('Arial', 10),
                          command=lambda: multipleC(addqFrame5, addq5choice1, addq5choice2))
    addq5choice1.pack(side=LEFT)
    addq5choice2 = Button(addqFrame5, width=30, height=5, text='Short response', font=('Arial', 10),
                          command=lambda: shortR(addq5choice1, addq5choice2))
    addq5choice2.pack(side=RIGHT)

    SubmitButton = Button(second_frame,text='Submit',font=('Arial',15),command=Save)
    SubmitButton.pack(pady=50)


#Multiple Choice
def multipleC(frame1,frame2,frame3):
    global pressBut
    frame2['state'] = DISABLED
    frame3['state'] = DISABLED
    addmcFrame = Frame(frame1)
    addmcFrame.pack(side=BOTTOM)
    textA = StringVar()
    textA.set('A')
    textB = StringVar()
    textB.set('B')
    textC = StringVar()
    textC.set('C')
    textD = StringVar()
    textD.set('D')
    choiceA = Entry(frame1, textvariable=textA)
    choiceA.pack(side=TOP)
    choiceB = Entry(frame1, textvariable=textB)
    choiceB.pack(side=TOP)
    choiceC = Entry(frame1, textvariable=textC)
    choiceC.pack(side=TOP)
    choiceD = Entry(frame1, textvariable=textD)
    choiceD.pack(side=TOP)
    pressBut += 1
    print(pressBut)

#Short response
def shortR(frame1,frame2):
    global pressBut
    frame1['state'] = DISABLED
    frame2['state'] = DISABLED
    pressBut += 1
    print(pressBut)

def Save():
    global questionlist1
    global questionlist2
    global questionlist3
    global questionlist4
    global questionlist5
    questionlist1 = []
    questionlist2 = []
    questionlist3 = []
    questionlist4 = []
    questionlist5 = []

    moveon2 = True
    sql_insert_survey_name = f"""INSERT INTO surveyq (surveyname) VALUES ('{newget}')"""
    sql_insert_survey_name2 = f"""INSERT INTO surveys (username,surveyname) VALUES ('{userget}','{newget}')"""
    cursor.execute(sql_insert_survey_name)
    cursor.execute(sql_insert_survey_name2)
    connection.commit()

    children_widgets = addqFrame1.winfo_children()
    children_widgets2 = addqFrame2.winfo_children()
    children_widgets3 = addqFrame3.winfo_children()
    children_widgets4 = addqFrame4.winfo_children()
    children_widgets5 = addqFrame5.winfo_children()

    for child_widget in children_widgets:
        if child_widget.winfo_class() == 'Entry':
            questionlist1.append(child_widget.get())

    for child_widget in children_widgets2:
        if child_widget.winfo_class() == 'Entry':
            questionlist2.append(child_widget.get())

    for child_widget in children_widgets3:
        if child_widget.winfo_class() == 'Entry':
            questionlist3.append(child_widget.get())

    for child_widget in children_widgets4:
        if child_widget.winfo_class() == 'Entry':
            questionlist4.append(child_widget.get())

    for child_widget in children_widgets5:
        if child_widget.winfo_class() == 'Entry':
            questionlist5.append(child_widget.get())

    all_questions = questionlist1 + questionlist2 + questionlist3 + questionlist4 + questionlist5

    for i in range(len(all_questions)):
        if all_questions[i] == '':
            messagebox.showerror(title='Error',message='All entries must have something in it.')
            moveon2 = False
            sql_cancel = f"DELETE FROM surveyq WHERE surveyname = '{newget}'"
            sql_cancel2 = f"DELETE FROM surveymc WHERE surveyname = '{newget}'"
            sql_cancel3 = f"DELETE FROM surveys WHERE surveyname = '{newget}'"
            cursor.execute(sql_cancel)
            cursor.execute(sql_cancel2)
            cursor.execute(sql_cancel3)
            connection.commit()
        elif pressBut < 5:
            messagebox.showerror(title='Error',message='All questions must be Multiple Choice or Short Response.')
            moveon2 = False
            sql_cancel = f"DELETE FROM surveyq WHERE surveyname = '{newget}'"
            sql_cancel2 = f"DELETE FROM surveymc WHERE surveyname = '{newget}'"
            sql_cancel3 = f"DELETE FROM surveys WHERE surveyname = '{newget}'"
            cursor.execute(sql_cancel)
            cursor.execute(sql_cancel2)
            cursor.execute(sql_cancel3)
            connection.commit()
        else:
            pass
    if moveon2 == True:
        Save2()
    else:
        pass

def Save2():
    all_question = []
    all_question.append(questionlist1)
    all_question.append(questionlist2)
    all_question.append(questionlist3)
    all_question.append(questionlist4)
    all_question.append(questionlist5)

    try:

        for i in range(0,5):
            savequestion = all_question[i]
            i2 = i+1
            if len(savequestion) == 1:
                sql_insert_question_type = f"UPDATE surveyq SET `Q{i2} type` = 'Sr',Q{i2} = '{savequestion[0]}' WHERE surveyname = '{newget}'"
                cursor.execute(sql_insert_question_type)
                connection.commit()
            elif len(savequestion) == 5:
                sql_insert_question_type = f"UPDATE surveyq SET `Q{i2} type` = 'Mc',Q{i2} = '{savequestion[0]}' WHERE surveyname = '{newget}'"
                sql_insert_question_mc = f"INSERT INTO surveymc (questionname,surveyname,`Choice 1`, `Choice 2`, `Choice 3`, `Choice 4`) VALUES ('{savequestion[0]}','{newget}','{savequestion[1]}','{savequestion[2]}','{savequestion[3]}','{savequestion[4]}')"
                print(sql_insert_question_mc)
                cursor.execute(sql_insert_question_type)
                cursor.execute(sql_insert_question_mc)
                connection.commit()
        messagebox.showinfo(title='Success',message='The survey is successfully added.')
        Menu()
    except:
        messagebox.showerror(title='Error',message='Duplicate names are found. Try again.')
        sql_cancel = f"DELETE FROM surveyq WHERE surveyname = '{newget}'"
        sql_cancel2 = f"DELETE FROM surveymc WHERE surveyname = '{newget}'"
        sql_cancel3 = f"DELETE FROM surveys WHERE surveyname = '{newget}'"
        cursor.execute(sql_cancel)
        cursor.execute(sql_cancel2)
        cursor.execute(sql_cancel3)
        connection.commit()

def Fill(sname):
    global fillFrame1
    global fillFrame2
    global fillFrame3
    global fillFrame4
    global fillFrame5

    global var1
    global var2
    global var3
    global var4
    global var5

    global sn

    ClrAllWidgets()

    sn = sname
    # scrollbar
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(main_frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor='nw')

    titleFrame = Frame(second_frame, highlightbackground="black", highlightthickness=2)
    titleFrame.pack(side=TOP, padx=20, pady=20)
    nameLab = Label(titleFrame, text=sname, font=('Arial', 50))
    nameLab.pack()
    backButton = Button(root, text='Back', font=('Arial', 7), command=Menu).place(x=0, y=0)

    sql_get_qname1 = f"SELECT Q1 FROM surveyq WHERE surveyname = '{sname}'"
    sql_get_qtype1 = f"SELECT `Q1 type` FROM surveyq WHERE surveyname = '{sname}'"
    sql_get_qname2 = f"SELECT Q2 FROM surveyq WHERE surveyname = '{sname}'"
    sql_get_qtype2 = f"SELECT `Q2 type` FROM surveyq WHERE surveyname = '{sname}'"
    sql_get_qname3 = f"SELECT Q3 FROM surveyq WHERE surveyname = '{sname}'"
    sql_get_qtype3 = f"SELECT `Q3 type` FROM surveyq WHERE surveyname = '{sname}'"
    sql_get_qname4 = f"SELECT Q4 FROM surveyq WHERE surveyname = '{sname}'"
    sql_get_qtype4 = f"SELECT `Q4 type` FROM surveyq WHERE surveyname = '{sname}'"
    sql_get_qname5 = f"SELECT Q5 FROM surveyq WHERE surveyname = '{sname}'"
    sql_get_qtype5 = f"SELECT `Q5 type` FROM surveyq WHERE surveyname = '{sname}'"
    cursor.execute(sql_get_qname1)
    res1 = cursor.fetchone()[0]
    cursor.execute(sql_get_qname2)
    res2 = cursor.fetchone()[0]
    cursor.execute(sql_get_qname3)
    res3 = cursor.fetchone()[0]
    cursor.execute(sql_get_qname4)
    res4 = cursor.fetchone()[0]
    cursor.execute(sql_get_qname5)
    res5 = cursor.fetchone()[0]

    cursor.execute(sql_get_qtype1)
    type1 = cursor.fetchone()[0]
    cursor.execute(sql_get_qtype2)
    type2 = cursor.fetchone()[0]
    cursor.execute(sql_get_qtype3)
    type3 = cursor.fetchone()[0]
    cursor.execute(sql_get_qtype4)
    type4 = cursor.fetchone()[0]
    cursor.execute(sql_get_qtype5)
    type5 = cursor.fetchone()[0]
    connection.commit()

    fillFrame1 = Frame(second_frame, width=500, highlightbackground='black', highlightthickness=2)
    fillFrame1.pack(side=TOP, pady=50)
    fillLabel = Label(fillFrame1, text=res1, font=('Arial', 10)).pack()
    var1 = Display(res1,type1,fillFrame1)

    fillFrame2 = Frame(second_frame, width=500, highlightbackground='black', highlightthickness=2)
    fillFrame2.pack(side=TOP, pady=50)
    fillLabel2 = Label(fillFrame2, text=res2, font=('Arial', 10)).pack()
    var2 = Display(res2,type2,fillFrame2)

    fillFrame3 = Frame(second_frame, width=500, highlightbackground='black', highlightthickness=2)
    fillFrame3.pack(side=TOP, pady=50)
    fillLabel3 = Label(fillFrame3, text=res3, font=('Arial', 10)).pack()
    var3 = Display(res3,type3,fillFrame3)

    fillFrame4 = Frame(second_frame, width=500, highlightbackground='black', highlightthickness=2)
    fillFrame4.pack(side=TOP, pady=50)
    fillLabel4 = Label(fillFrame4, text=res4, font=('Arial', 10)).pack()
    var4 = Display(res4,type4,fillFrame4)

    fillFrame5 = Frame(second_frame, width=500, highlightbackground='black', highlightthickness=2)
    fillFrame5.pack(side=TOP, pady=50)
    fillLabel5 = Label(fillFrame5, text=res5, font=('Arial', 10)).pack()
    var5 = Display(res5,type5,fillFrame5)

    SubmitButton = Button(second_frame, text='Submit', font=('Arial', 15), command=SaveFill)
    SubmitButton.pack(pady=50)

def Display(qname,qtype,qframe):
    global var
    if qtype == 'Mc':
        sql_choice1 = f"SELECT `Choice 1` from surveymc WHERE questionname = '{qname}'"
        sql_choice2 = f"SELECT `Choice 2` from surveymc WHERE questionname = '{qname}'"
        sql_choice3 = f"SELECT `Choice 3` from surveymc WHERE questionname = '{qname}'"
        sql_choice4 = f"SELECT `Choice 4` from surveymc WHERE questionname = '{qname}'"

        cursor.execute(sql_choice1)
        c1 = cursor.fetchone()[0]
        cursor.execute(sql_choice2)
        c2 = cursor.fetchone()[0]
        cursor.execute(sql_choice3)
        c3 = cursor.fetchone()[0]
        cursor.execute(sql_choice4)
        c4 = cursor.fetchone()[0]

        var = IntVar()

        R1 = Radiobutton(qframe,text=c1,variable=var,value=1)
        R1.pack(side=TOP)
        R2 = Radiobutton(qframe, text=c2, variable=var, value=2)
        R2.pack(side=TOP)
        R3 = Radiobutton(qframe, text=c3, variable=var, value=3)
        R3.pack(side=TOP)
        R4 = Radiobutton(qframe, text=c4, variable=var, value=4)
        R4.pack(side=TOP)
        return var
    elif qtype == 'Sr':
        WritingEntry = Entry(qframe, font=('Arial',15))
        WritingEntry.pack()
        return WritingEntry

def SaveFill():
    if var1.get() == 0 or var2.get() == 0 or var3.get() == 0 or var4.get() == 0 or var5.get() == 0 or var1.get() == None or var1.get() == None or var2.get() == None or var3.get() == None or var4.get() == None or var5.get() == None:
        messagebox.showerror(title='Error',message='Please fill all the answers.')
    else:
        sql_upload_answer = f"INSERT INTO surveya (surveyname,A1,A2,A3,A4,A5) VALUES ('{sn}','{var1.get()}','{var2.get()}','{var3.get()}','{var4.get()}','{var5.get()}')"
        cursor.execute(sql_upload_answer)
        connection.commit()
        messagebox.showinfo(title='Success',message='The results are recorded.')
        Menu()

def Data(survn):
    ClrAllWidgets()

    #scrollbar
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(main_frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor='nw')

    backButton = Button(second_frame, text='Back', font=('Arial', 7), command=Survey).place(x=0, y=0)
    sql_check_data = f"SELECT A1,A2,A3,A4,A5 FROM surveya WHERE surveyname = '{survn}'"
    cursor.execute(sql_check_data)
    datacollect = cursor.fetchall()
    if datacollect == []:
        messagebox.showerror(title='Error',message='No results are fetched.')
        Survey()
    else:
        for data in datacollect:
            resultLabel = Label(second_frame,text=str(data),font=('Arial',15)).pack(padx=250,pady=50)


PreStart()
root.mainloop()
