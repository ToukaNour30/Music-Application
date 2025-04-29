from tkinter import messagebox, END
from PIL import Image, ImageTk
from tkinter import *
import pymysql


class signup():
    def __init__(self):
        self.emailEntry = None
        self.signup_window = None
        self.confirmEntry = None
        self.usernameEntry = None
        self.PasswordEntry = None
        self.resized_img = None
        self.bgLabel = None
        self.check = None

    def clear(self):
        self.emailEntry.delete(0, END)
        self.usernameEntry.delete(0, END)
        self.PasswordEntry.delete(0, END)
        self.confirmEntry.delete(0, END)
        self.check.set(0)

    def connect_database(self):
        if self.emailEntry.get()=='' or self.usernameEntry.get()=='' or self.PasswordEntry.get()=='' or \
                self.confirmEntry.get()=='':
            messagebox.showerror('Error','All Fields Are Required')
        elif self.PasswordEntry.get()!=self.confirmEntry.get():
            messagebox.showerror('Error', 'Password Mismatch')
        elif self.check.get()==0:
            messagebox.showerror('Error', 'Please Accept Terms & Conditions')
        else:
            try:
                con= pymysql.connect(host='localhost',user='root',password='*****')
                mycursor=con.cursor()
            except :
                messagebox.showerror('Error','Database Connectivity Issue, Please try again')
                return
            query='CREATE DATABASE IF NOT EXISTS musicapp'
            mycursor.execute(query)
            query='USE musicapp'
            mycursor.execute(query)
            query_account='create table IF NOT EXISTS account(email varchar(50),password varchar (20),' \
                          'Constraint composite_key primary key (email,password))'
            mycursor.execute(query_account)
            query_user='create table IF NOT EXISTS user(user_id INT AUTO_INCREMENT PRIMARY KEY,email varchar(50),' \
                       'username varchar(100),password varchar (20),profile_image varchar(100),' \
                       'FOREIGN KEY (email,password) REFERENCES account(email, password))'
            mycursor.execute(query_user)
            query='select * from account where email=%s and password=%s'
            mycursor.execute(query,(self.emailEntry.get(),self.PasswordEntry.get()))
            existinr_record=mycursor.fetchone()
            if existinr_record:
                messagebox.showerror('info','This email-password combination already exists')

            else:
                query_account = 'insert into account(email,password) values(%s,%s)'
                mycursor.execute(query_account, (self.emailEntry.get(), self.PasswordEntry.get()))
                query_user = 'insert into user(email,username,password,profile_image ) values(%s,%s,%s,%s)'
                profile_image_path = r'C:\user_pictures\profile_picture.jpg'
                mycursor.execute(query_user,(self.emailEntry.get(),self.usernameEntry.get(),
                                             self.PasswordEntry.get(),profile_image_path))

                con.commit()
                con.close()
                messagebox.showinfo('Succsess','Registration is successful')
                self.clear()
                self.loginPage()


    def user_Entry(self, event):
        # to delete the word written in the label
        # for method bind
        if self.usernameEntry.get() == 'UserName':
            self.usernameEntry.delete(0, END)

    def password_Entry(self, event):
        # to delete the word written in the label
        # for method bind
        if self.PasswordEntry.get() == 'Password':
            self.PasswordEntry.delete(0, END)

    def email_Entry(self, event):
        # to delete the word written in the label
        # for method bind
        if self.emailEntry.get() == 'Email':
            self.emailEntry.delete(0, END)

    def confirm_Entry(self, event):
        # to delete the word written in the label
        # for method bind
        if self.confirmEntry.get() == 'Confirm Pass':
            self.confirmEntry.delete(0, END)

    def loginPage(self):
        self.signup_window.destroy()
        import login as log
        l = log.login()
        l.run_login()

    def run_signup(self):
        self.signup_window = Tk()
        self.signup_window.geometry('546x700+50+50')
        self.signup_window.resizable(0, 0)
        self.signup_window.title('sign up page')

        bgimage = ImageTk.PhotoImage(file='background.jpg')

        bglabel = Label(self.signup_window, image=bgimage)
        bglabel.place(x=0, y=0)

        self.signup_frame = Frame(self.signup_window, width=400, height=400, highlightbackground='purple',
                                  highlightcolor='purple', highlightthickness=2)
        self.signup_frame.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)

        heading = Label(self.signup_window, text='Create an Account', font=('times', 23, 'bold'),
                        bg='purple', fg='lavenderblush1')
        heading.place(x=160, y=70)

        self.emailEntry = Entry(self.signup_window, width=20, font=('times', 14, 'bold'), bd=0, bg='purple',
                                fg='lavenderblush1')
        self.emailEntry.place(x=180, y=180)
        self.emailEntry.insert(0, "Email")
        self.emailEntry.bind('<FocusIn>', self.email_Entry)

        self.usernameEntry = Entry(self.signup_window, width=20, font=('times', 14, 'bold'), bd=0, bg='purple',
                                   fg='lavenderblush1')
        self.usernameEntry.place(x=180, y=220)
        self.usernameEntry.insert(0, "UserName")
        self.usernameEntry.bind('<FocusIn>', self.user_Entry)

        self.PasswordEntry = Entry(self.signup_window, width=20, font=('times', 14, 'bold'), bd=0, bg='purple',fg='lavenderblush1')
        self.PasswordEntry.place(x=180, y=260)
        self.PasswordEntry.insert(0, "Password")
        self.PasswordEntry.bind('<FocusIn>', self.password_Entry)

        self.confirmEntry = Entry(self.signup_window, width=20, font=('times', 14, 'bold'), bd=0, bg='purple',
                                  fg='lavenderblush1')
        self.confirmEntry.place(x=180, y=300)
        self.confirmEntry.insert(0, "Confirm Pass")
        self.confirmEntry.bind('<FocusIn>', self.confirm_Entry)

        self.check = IntVar()
        terms_and_conditions = Checkbutton(self.signup_window, text='terms and conditions',
                                           font=('times', 9, 'bold'), fg='CadetBlue2', bg='purple',
                                           variable=self.check)
        terms_and_conditions.place(x=280, y=450)

        signup_Button = Button(self.signup_window, text='Signup', font=('times', 16, 'bold'),
                               bg='purple', fg='lavenderblush1',command = self.connect_database)

        # , command = self.connect_databse)

        signup_Button.place(x=240, y=365)

        alreadyaccount = Label(self.signup_window, text='have an account?', font=('open sans', 9, 'bold'),
                               fg='CadetBlue2', bg='purple')
        alreadyaccount.place(x=160, y=450)

        Login_Button = Button(self.signup_window, text='Login', font=('open sans', 9, 'bold underline'),
                              fg='CadetBlue2', bg='purple', command=self.loginPage)
        Login_Button.place(x=255, y=500)

        self.signup_window.mainloop()


