from tkinter import messagebox, END
from PIL import Image, ImageTk
from tkinter import *


import pymysql


class forget():
    def __init__(self):
        self.forgetpass_window = None
        self.resized_img = None
        self.bglabel = None
        self.emailEntry = None
        self.PasswordEntry = None
        self.confirmEntry=None

    def clear(self):
        self.emailEntry.delete(0, END)
        self.PasswordEntry.delete(0, END)
        self.confirmEntry.delete(0, END)

    def submit(self):
      if  self.emailEntry.get() == '' or self.PasswordEntry.get() == '' or self.confirmEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')
      elif self.PasswordEntry.get() != self.confirmEntry.get():
            messagebox.showerror('Error', 'Password Mismatch')
      else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='*****')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Database Connectivity Issue, Please try again')
                return
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'select * from account where email=%s'
            mycursor.execute(query,(self.emailEntry.get()))
            row = mycursor.fetchone()
            if row==None:
                messagebox.showerror('Error', 'Incorrect Email')
            else:
                try:
                    query_account = 'update account set password=%s where email=%s'
                    mycursor.execute(query_account, (self.PasswordEntry.get(), self.emailEntry.get()))
                    query_artist = 'update artist set password=%s where email=%s'
                    mycursor.execute(query_artist, (self.PasswordEntry.get(),self.emailEntry.get()))
                    query_user = 'update user set password=%s where email=%s'
                    mycursor.execute(query_user, (self.PasswordEntry.get(), self.emailEntry.get()))

                    con.commit()
                except pymysql.IntegrityError as e:
                    print(f"IntegrityError: {e}")
                finally:
                    con.close()

                messagebox.showinfo('Succsess', 'password is reset')
                self.clear()
                self.loginPage()

    def confirm_entry(self, event):
        if self.confirmEntry.get() == 'Confirm New Pass':
            self.confirmEntry.delete(0, END)


    def password_entry(self, event):
        if self.PasswordEntry.get() == 'New Password':
            self.PasswordEntry.delete(0, END)

    def email_entry(self, event):
        if self.emailEntry.get() == 'Email':
            self.emailEntry.delete(0, END)

    def loginPage(self):
        self.forgetpass_window.destroy()
        import login as log
        l = log.login()
        l.run_login()

    def forget_pass(self):
        self.forgetpass_window = Tk()
        self.forgetpass_window.geometry('546x700+50+50')
        self.forgetpass_window.resizable(0, 0)
        self.forgetpass_window.title('CHANGE password')

        bgimage = ImageTk.PhotoImage(file='background.jpg')

        bglabel = Label(self.forgetpass_window, image=bgimage)
        bglabel.place(x=0, y=0)

        self.forgetpass_circular_frame = Frame(self.forgetpass_window, width=400, height=400,
                                               highlightbackground='purple',
                                               highlightcolor='purple', highlightthickness=2)
        self.forgetpass_circular_frame.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)

        heading = Label(self.forgetpass_window, text='Reset Password',
                        font=('times', 23, 'bold'), bg='purple', fg='lavenderblush1')
        heading.place(x=160, y=70)

        self.emailEntry = Entry(self.forgetpass_window, width=20, font=('times', 14, 'bold'), bd=0, bg='purple',
                                fg='CadetBlue2')
        self.emailEntry.place(x=180, y=240)
        self.emailEntry.insert(0, "Email")
        self.emailEntry.bind('<FocusIn>', self.email_entry)

        self.PasswordEntry = Entry(self.forgetpass_window, width=20, font=('times', 14, 'bold'), bd=0, bg='purple',
                                   fg='CadetBlue2')
        self.PasswordEntry.place(x=180, y=300)
        self.PasswordEntry.insert(0, "New Password")
        self.PasswordEntry.bind('<FocusIn>', self.password_entry)

        self.confirmEntry = Entry(self.forgetpass_window, width=20, font=('times', 14, 'bold'), bd=0, bg='purple',
                                  fg='CadetBlue2')
        self.confirmEntry.place(x=180, y=360)
        self.confirmEntry.insert(0, "Confirm New Pass")
        self.confirmEntry.bind('<FocusIn>', self.confirm_entry)

        submit_Button = Button(self.forgetpass_window, text='Submit', font=('open sans', 16, 'bold underline'),
                               fg='CadetBlue2', bg='purple', command=self.submit)
        # command=submit)
        submit_Button.place(x=240, y=450)

        self.forgetpass_window.mainloop()
