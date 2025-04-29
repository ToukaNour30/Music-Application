from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import ImageTk

class login():
    def __init__(self):

        self.login_frame = None
        self.user_id=0
        self.login_window=0
        self.eyebutton=0
        self.password_entry=0
        self.closeeye=0
        self.username_entry=0
        self.password_entry=0
        self.eyebutton=0
        self.artist_id=0


    def login_user(self):

        if self.username_entry.get()== '' or self.password_entry.get() == '':
            messagebox.showerror('Error', 'All Fields Are Required')
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='*****')
                mycursor = con.cursor()

            except:
                messagebox.showerror('Error', 'Database Connectivity Issue, Please try again')
                return
            query = 'USE musicapp'
            mycursor.execute(query)
            query='use musicapp'
            mycursor.execute(query)
            query='select * from account where email=%s and password=%s'
            print("Query:", query)
            mycursor.execute(query,(self.username_entry.get(),self.password_entry.get()))
            row=mycursor.fetchone()
            query='select * from user where email=%s and password=%s'
            mycursor.execute(query,(self.username_entry.get(),self.password_entry.get()))
            user_row=mycursor.fetchone()
            artist_query='select * from artist where email=%s and password=%s'
            mycursor.execute(artist_query,(self.username_entry.get(),self.password_entry.get()))
            artits_row=mycursor.fetchone()
            print(artits_row)
            if row==None:
                messagebox.showerror('ERROR','Invalid username or password')
            elif user_row:

                con.close()
                messagebox.showinfo('Welcome', 'login is Successful')

                self.user_id = user_row[0]
                print(self.user_id)
                self.login_window.destroy()
                import user as user_window
                u= user_window.user()
                u.set_user_id(self.user_id)
                u.run_user()
            elif artits_row:
                print("fr")
                con.close()
                messagebox.showinfo('Welcome', 'login is Successful')
                self.artist_id=artits_row[0]
                self.login_window.destroy()
                import Artist as artist_window
                a=artist_window.Artist()
                a.set_artist_id(self.artist_id)
                a.run_artist()

            else:
                messagebox. showinfo('Welcome','login is Successful')


    def forget_pass(self):
        self.login_window.destroy()
        import forgetpass as forr
        f=forr.forget()
        f.forget_pass()


    def signupPage(self):
        self.login_window.destroy()
        import signup as sign
        s=sign.signup()
        s.run_signup()
    def signupPageartist(self):
        self.login_window.destroy()
        import signupartist as signart
        s=signart. signup_artist()
        s.signup_artist()
    def user_enter(self,event):
        if self.username_entry.get()=='Email':
            self.username_entry.delete(0,END)
    def password_enter(self,event):
        if self.password_entry.get()=='Password':
            self.password_entry.delete(0,END)
    def hide(self):
        self.closeeye.config(file='closeye.png')
        self.password_entry.config(show='*')
        self.eyebutton.config(command=self.show)

    def show(self):
        self.closeeye.config(file='openeye.png')
        self.password_entry.config(show='')
        self.eyebutton.config(command=self.hide)

    def run_login(self):
        self.login_window=Tk()
        self.login_window.geometry('546x700+50+50')
        self.login_window.resizable(0,0)
        self.login_window.title('LOGIN PAGE')
        bgimage=ImageTk.PhotoImage(file='background.jpg')
        canvas = Canvas(self.login_window)
        canvas.create_image(0, 0, image=bgimage, anchor=NW)
        canvas.pack(fill="both", expand=True)

        bglabel=Label(self.login_window,image=bgimage)
        bglabel.place(x=0,y=0)

        self.login_frame = Frame(self.login_window, width=400, height=400, highlightbackground='purple',highlightcolor='purple', highlightthickness=2)
        self.login_frame.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)

        heading=Label(self.login_window,text='USER LOGIN',font=('times',23,'bold'),bg='purple',fg='lavenderblush1')
        heading.place(x=185,y=70)
        self.username_entry=Entry(self.login_window,width=20,font=('times',11,'bold'),bd=0,fg='lavenderblush1',bg='purple')
        self.username_entry.place(x=200,y=210)
        self.username_entry.insert(0,'Email')

        self.username_entry.bind('<FocusIn>',self.user_enter)
        #Frame(login_window,width=250,height=2,bg='black').place(x=200,y=325)


        self.password_entry=Entry(self.login_window,width=20,font=('times',11,'bold'),bd=0,fg='lavenderblush1',bg='purple',show='*')
        self.password_entry.place(x=200,y=250)
        self.password_entry.insert(0,'Password')
        self.password_entry.bind('<FocusIn>',self.password_enter)
        self.closeeye=PhotoImage(file='closeye.png')
        self.eyebutton=Button(self.login_window,image=self.closeeye,bd=0,bg='white',activebackground='white',
                         cursor='hand2',command=self.hide)
        self.eyebutton.place(x=390,y=250)



        forgett_button=Button(self.login_window,text='Forgot Password..?',bd=0,bg='purple',activebackground='white',
                         cursor='hand2',font=('Open Sans',9,'bold'),
                         fg='white',activeforeground='purple',command=self.forget_pass)
        forgett_button.place(x=300,y=400)

        loginbutton=Button(self.login_window,text='login',font=('Open Sans',16,'bold'),
                           fg='white',bg='purple',activeforeground='white',
                           activebackground='purple',cursor='hand2',bd=0,command = self.login_user)
        # , command = self.login_user
        loginbutton.place(x=250,y=320)

        signuplabel=Label(self.login_window,text='Dont have an account?',font=('Open Sans',9,'bold'),
                          fg='white',bg='purple')
        signuplabel.place(x=140,y=400)

        newaccountbuttonuser=Button(self.login_window,text='Create new one as a user',font=('Open Sans',9,'bold underline'),
                           fg='CadetBlue2',bg='purple',activeforeground='blue',
                           activebackground='purple',cursor='hand2',bd=0,command=self.signupPage)
        newaccountbuttonuser.place(x=215,y=460)
        newaccountbuttonartist=Button(self.login_window,text='Create new one as an artist',font=('Open Sans',9,'bold underline'),
                           fg='CadetBlue2',bg='purple',activeforeground='blue',
                           activebackground='purple',cursor='hand2',bd=0,command=self.signupPageartist)
        newaccountbuttonartist.place(x=210,y=490)
        self.login_window.mainloop()


