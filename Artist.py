
import pymysql
from tkinter import *
from tkinter import Tk, Canvas, Frame, PhotoImage, messagebox, filedialog
from PIL import Image, ImageTk

class Artist():
    def __init__(self):
        self.artist_window= None
        self.main_frame=None
        self.bgimage = None
        self.circular_img=None
        self.img=None
        self.artist_id=0
        self.artist_name=""
        self.scrollable_frame =None

        self.photo_entry_album=None
        self.album_name_entry=None
        self.song_Text_album=None
        self.artist_window = None
        self.album_window=None
        self.album_name=""
        self.photo_path_album=""
        self.song_name_album=""
        self.songs_list=[]

        self.song_photo_entry = None
        self.song_name_entry = None
        self.song_window = None
        self.song_name = ""
        self.photo_path_song= ""
        self.album_name_list=[]
        self.album_photo_list=[]
        self.scrollable_frame_hor =None
        self.button=[]
        self.image_references = []
        self.image_references_songs = []
        self.song_frame=None
        self.song_photo=[]
        self.song_name_label=[]
        self.label=[]
        self.song_album_frame=None
        self.album_ids=[]
        self.selected_album=0
        self.song_album_photo=[]
        self.song_album_name=[]
        self.song_download_Entry = ""
        self.song_download_album = []
        self.song_download_album_entry = None
        self.song_download_entry = None
        self.song_download=""
        self.akbums=False




    def set_artist_id(self,artist_id):
            self.artist_id=artist_id

    def get_image(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'select * from artist where artist_id=%s'
            mycursor.execute(query,(self.artist_id,))
            artist_row = mycursor.fetchone()
            if artist_row:
                img_path = artist_row[4]
                artist_name=artist_row[2]
                return img_path,artist_name
        except pymysql.Error as e:
            print(f"error:{str(e)}")
        return None


    def create_album(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Database Connectivity Issue: {str(e)}. Please try again')
            return
        try:
            query = 'CREATE DATABASE IF NOT EXISTS musicapp'
            mycursor.execute(query)

            query = 'USE musicapp'
            mycursor.execute(query)

            query = '''CREATE TABLE IF NOT EXISTS album(
                                album_id INT AUTO_INCREMENT PRIMARY KEY,
                                album_name VARCHAR(20),
                                artist_id INT,
                                album_photo varchar(100),
                                FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
                            )'''
            mycursor.execute(query)
            con.commit()
        except pymysql.Error as e:
            con.rollback()
            messagebox.showerror('Error', f'Database Error: {str(e)}. Please try again')
        finally:
            con.close()
    def create_song(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
        except pymysql.Error as e:
            messagebox.showerror('Error',f'Database connectivity Issue:{str(e)}. please try again')
            return
        try:
            query= 'create database if not exists musicapp'
            mycursor.execute(query)
            query = 'USE musicapp'
            mycursor.execute(query)
            query= '''CREATE TABLE IF NOT EXISTS song(
                                song_id INT AUTO_INCREMENT PRIMARY KEY,
                                song_name VARCHAR(20),
                                album_id INT,
                                song_photo varchar(100),
                                song_path varchar(100),
                                FOREIGN KEY (album_id) REFERENCES album(album_id)
                            )'''
            mycursor.execute(query)
            con.commit()
        except pymysql.Error as e:
            con.rollback()
            messagebox.showerror('Error',f'databse connectivity issue:{str(e)}. please try again')
            return
        finally:
            con.close()
    def create_sing_a_song(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='****')
            mycursor = con.cursor()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Database connectivity Issue:{str(e)}. please try again')
            return
        try:
            query = 'create database if not exists musicapp'
            mycursor.execute(query)
            query = 'USE musicapp'
            mycursor.execute(query)
            query = '''CREATE TABLE IF NOT EXISTS sing_a_song(
                                       song_id INT,
                                       artist_id INT,
                                       FOREIGN KEY (artist_id) REFERENCES artist(artist_id),
                                       FOREIGN KEY(song_id) REFERENCES song(song_id),
                                       PRIMARY KEY (song_id, artist_id)

                                   )'''
            mycursor.execute(query)
            con.commit()
        except pymysql.Error as e:
            con.rollback()
            messagebox.showerror('Error', f'databse connectivity issue:{str(e)}. please try again')
            return
        finally:
            con.close()

    def open_file_dialog_album(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.photo_entry_album.delete(0, "end")  # Clear the entry if there's any text
            self.photo_entry_album.insert(0, file_path)

    def open_file_dialog_album_songs(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            #self.song_download_album_entry.delete("1.0", "end")  # Clear the entry if there's any text
            self.song_download_album_entry.insert("1.0", file_path)

    def open_file_dialog_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.song_photo_entry.delete(0, "end")  # Clear the entry if there's any text
            self.song_photo_entry.insert(0, file_path)

    def open_file_dialog_song_downloaded(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            self.song_download_entry.delete(0, "end")  # Clear the entry if there's any text
            self.song_download_entry.insert(0, file_path)
    def insert_in_album(self):
        #print(self.songs_list)
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Database Connectivity Issue: {str(e)}. Please try again')
            return
        try:
            query = 'use musicapp'
            mycursor.execute(query)
            query = 'insert into album (album_name, artist_id, album_photo) values (%s, %s, %s)'
            mycursor.execute(query, (self.album_name, self.artist_id, self.photo_path_album))
            con.commit()
            album_id=mycursor.lastrowid
            for song, downloaded_song in zip(self.songs_list[0], self.song_download_album[0]):
                song = song.replace("\"", "")
                downloaded_song = downloaded_song.replace('"', '')
                #print(song,album_id,self.photo_path_album)
                query_song = 'insert into song(song_name,album_id,song_photo,song_path) values(%s,%s,%s,%s)'
                mycursor.execute(query_song,(song,album_id,self.photo_path_album,downloaded_song))
            con.commit()
            messagebox.showinfo("Success", f"album '{self.album_name}' created successfully!")
            if hasattr(self, 'album_window'):
                self.get_albums()
                self.album_window.destroy()
                self.create_main_frame()
        except pymysql.Error as e:
            con.rollback()
            messagebox.showerror('Error', f'Database Error: {str(e)}. Please try again')
        finally:
            con.close()
    def insert_in_song(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Database Connectivity Issue: {str(e)}. Please try again')
            return
        try:
            query = 'use musicapp'
            mycursor.execute(query)
            query = 'insert into song (song_name, album_id,song_photo,song_path) values (%s, %s, %s,%s)'
            mycursor.execute(query, (self.song_name,None, self.photo_path_song,self.song_download))
            con.commit()
            song_id = mycursor.lastrowid
            query_song = 'insert into sing_a_song(song_id,artist_id) values(%s,%s)'
            mycursor.execute(query_song, (song_id, self.artist_id))
            con.commit()
            messagebox.showinfo("Success", f"song '{self.song_name}' created successfully!")
            if hasattr(self, 'song_window'):
                self.get_songs()
                self.song_window.destroy()
                self.create_main_frame()
        except pymysql.Error as e:
            con.rollback()
            messagebox.showerror('Error', f'Database Error: {str(e)}. Please try again')
        finally:
            con.close()
    def get_albums(self):
        self.album_photo_list.clear()
        self.album_name_list.clear()
        self.album_ids.clear()
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'select * from album where artist_id=%s'
            mycursor.execute(query,(self.artist_id,))
            album_rows = mycursor.fetchall()
            if album_rows:
                for album_row in album_rows:
                    img_path = album_row[3]
                    album_name=album_row[1]
                    album_id=album_row[0]
                    self.album_photo_list.append(img_path)
                    self.album_name_list.append(album_name)
                    self.album_ids.append(album_id)
                    print(self.album_ids)
                return True
            else:
                print("No albums found for the artist.")
                return False
        except pymysql.Error as e:
            print(f"error:{str(e)}")

        return None

    def get_single_songs(self):
        self.song_photo.clear()
        self.song_name_label.clear()
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'SELECT song_id FROM sing_a_song WHERE artist_id = %s'
            mycursor.execute(query, (self.artist_id,))
            song_ids = mycursor.fetchall()
            #print(song_ids)
            for song_id in song_ids:
                query = 'SELECT song_name, song_photo FROM song WHERE song_id = %s'
                mycursor.execute(query, (song_id,))
                song_rows = mycursor.fetchone()
                if song_rows:
                    img_path = song_rows[1]
                    song_name = song_rows[0]
                    self.song_photo.append(img_path)
                    self.song_name_label.append(song_name)
            if song_ids:
                return True
            else:
                print("No albums found for the artist.")
                return False
        except pymysql.Error as e:
            print(f"error:{str(e)}")
        return None
    def get_songs(self):
        self.song_album_photo.clear()
        self.song_album_name.clear()
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'SELECT * FROM song WHERE album_id = %s'
            mycursor.execute(query, (self.selected_album,))
            song_ids = mycursor.fetchall()
            #print(song_ids)
            for song_id in song_ids:
                if song_id:
                    img_path = song_id[3]
                    song_name = song_id[1]
                    self.song_album_photo.append(img_path)
                    self.song_album_name.append(song_name)
            if song_ids:
                return True
            else:
                print("No albums found for the artist.")
                return False
        except pymysql.Error as e:
            print(f"error:{str(e)}")
        return None


    def on_add_clicked_album(self):
        self.album_name = self.album_name_entry.get()
        self.photo_path_album = self.photo_entry_album.get()
        songs_text = self.song_Text_album.get("1.0", "end-1c")
        self.songs_list.append(songs_text.split('\n'))
        songs_text=self.song_download_album_entry.get("1.0","end-1c")
        self.song_download_album.append(songs_text.split('\n'))
        self.insert_in_album()
    def on_add_clicked_song(self):
        self.song_name=self.song_name_entry.get()
        self.photo_path_song=self.song_photo_entry.get()
        self.song_download=self.song_download_entry.get()
        self.insert_in_song()

    def open_album_window(self):
        self.album_window = Toplevel(self.artist_window)
        self.album_window.geometry('400x300')
        self.album_window.title('Add Album')
        # bg_image = PhotoImage(file="colorful.jpg")
        #
        # # Create a Label to hold the background image
        # bg_label = Label(self.album_window, image=bg_image)
        # bg_label.place(relwidth=1, relheight=1)

        album_name_label = Label(self.album_window, text='Album Name:',bg='purple',fg='lavenderblush1')
        album_name_label.place(x=20,y=20)

        self.album_name_entry = Entry(self.album_window,bg='cadetblue')
        self.album_name_entry.place(x=115,y=25)

        photo_label = Label(self.album_window, text='Album Photo:',bg='purple',fg='lavenderblush1')
        photo_label.place(x=20,y=55)
        photo_button = Button(self.album_window, text='Select Image', command=self.open_file_dialog_album,bg='purple',fg='Cadetblue2')
        photo_button.place(x=110,y=85)

        self.photo_entry_album = Entry(self.album_window,bg='cadetblue')
        self.photo_entry_album.place(x=110,y=55)
        # ///////////////////////////////////////////////////
        song_label = Label(self.album_window, text='Songs:',bg='purple',fg='lavenderblush1')
        song_label.place(x=20,y=110)

        self.song_Text_album = Text(self.album_window, height=2, width=30,bg='cadetblue')
        self.song_Text_album.place(x=20,y=135)

        song_download_button = Button(self.album_window, text='insert the songs', command=self.open_file_dialog_album_songs,bg='purple',fg='lavenderblush1')
        song_download_button.place(x=20,y=180)
        self.song_download_album_entry = Text(self.album_window, height=2, width=30,bg='cadetblue')
        self.song_download_album_entry.place(x=20,y=210)

        add_button = Button(self.album_window, text='Add', command=self.on_add_clicked_album,bg='purple',fg='lavenderblush1')
        add_button.place(x=160,y=250)

    def open_song_window(self):

        self.song_window = Toplevel(self.artist_window)
        self.song_window.geometry('400x200')
        self.song_window.title("Add a song")

        song_name_label = Label(self.song_window, text="Song Name",bg='purple',fg='lavenderblush1')
        song_name_label.place(x=20,y=20)
        self.song_name_entry = Entry(self.song_window,bg='cadetblue')
        self.song_name_entry.place(x=20,y=45)
        photo_label = Label(self.song_window, text="Song Photo:",bg='purple',fg='lavenderblush1')
        photo_label.place(x=20,y=70)
        photo_button = Button(self.song_window, text="Select Image", command=self.open_file_dialog_song,bg='purple',fg='lavenderblush1')
        photo_button.place(x=150,y=90)
        self.song_photo_entry = Entry(self.song_window,bg='cadetblue')
        self.song_photo_entry.place(x=20,y=95)

        song_download_button = Button(self.song_window, text='insert the song', command=self.open_file_dialog_song_downloaded,bg='purple',fg='lavenderblush1')
        song_download_button.place(x=20,y=120)
        self.song_download_entry = Entry(self.song_window,bg='cadetblue')
        self.song_download_entry.place(x=20,y=150)

        add_button = Button(self.song_window, text="Add", command=self.on_add_clicked_song,bg='purple',fg='lavenderblush1')
        add_button.place(x=190,y=170)
    def sel(self,id):
        print(id)
        self.selected_album=id
        if self.song_frame:
            self.song_frame.destroy()
        if self.song_album_frame:
            self.song_album_frame.destroy()
        songs=self.get_songs()

        if songs:
            self.song_album_frame = Frame(self.scrollable_frame, width=540, height=700)
            self.song_album_frame.place(x=10,y=510)
            bglabel = Label(self.song_album_frame, image=self.bgimage)
            bglabel.pack()
            song_button = Button(self.song_album_frame, text="Back to your songs",
                                 font=('times', 15, 'bold'),
                                 bg='lavenderblush1', fg='cadetblue', highlightthickness=0,command=self.create_song_frame)
            song_button.place(x=1, y=5)
            y_axis = 60
            y_axis_label = 130
            # print(len(self.song_name_label))
            for i in range(len(self.song_album_name)):
                song_name = self.song_album_name[i]
                photo_path = self.song_album_photo[i].strip("'").replace("/", "\\")
                # (song_name, photo_path)
                try:
                    img_label = Image.open(photo_path)
                    img_label = img_label.resize((100, 100))
                    img_label = ImageTk.PhotoImage(img_label)
                    self.image_references_songs.append(img_label)
                    song_label = Label(self.song_album_frame, image=img_label, width=100, height=60)
                    song_label.place(x=1, y=y_axis)
                    song_name_label = Label(self.song_album_frame, text=song_name, font=('times', 15, 'bold'),
                               bg='lavenderblush1', fg='cadetblue', highlightthickness=0)
                    song_name_label.place(x=1, y=y_axis_label)
                    y_axis += 110
                    y_axis_label += 110
                except Exception as e:
                    print(f"Error loading image for {song_name}: {str(e)}")

    def create_song_frame(self):
        if self.song_album_frame:
            self.song_album_frame.destroy()
        songs = self.get_single_songs()
        if songs:
            self.song_frame=Frame(self.scrollable_frame,width=540,height=700)
            self.song_frame.place(x=10,y=510)
            bglabel = Label(self.song_frame, image=self.bgimage)
            bglabel.pack()
            song_Label = Label(self.song_frame, text="your songs",
                               font=('times', 15, 'bold'),
                               bg='lavenderblush1', fg='cadetblue', highlightthickness=0)
            song_Label.place(x=1, y=5)
            y_axis = 60
            y_axis_label=130
            #print(len(self.song_name_label))
            for i in range(len(self.song_name_label)):
                song_name = self.song_name_label[i]
                photo_path = self.song_photo[i].strip("'").replace("/", "\\")
                #(song_name, photo_path)
                try:
                    img_label= Image.open(photo_path)
                    img_label = img_label.resize((100, 100))
                    img_label = ImageTk.PhotoImage(img_label)
                    self.image_references_songs.append(img_label)
                    song_label = Label(self.song_frame, image=img_label, width=100, height=60)
                    song_label.place(x=1, y=y_axis)
                    song_name_label = Label(self.song_frame, text=song_name, font=('times', 15, 'bold'),
                                 bg='purple', fg='lavenderblush1',highlightthickness=0)
                    song_name_label.place(x=1, y=y_axis_label)
                    y_axis += 110
                    y_axis_label += 110
                except Exception as e:
                    print(f"Error loading image for {song_name}: {str(e)}")

    def create_horizontal_frame(self):
        if not self.album_name_list:
            self.albums = self.get_albums()
        if self.albums:
            horizontal_frame = Frame(self.scrollable_frame, width=530, height=150)
            horizontal_frame.place(x=10, y=300)
            canvas = Canvas(horizontal_frame, width=520, height=150)
            canvas.pack(side=TOP, fill=X)

            scrollbar = Scrollbar(horizontal_frame, orient=HORIZONTAL)
            scrollbar.pack(side=BOTTOM, fill=X)

            scrollbar.config(command=canvas.xview)
            canvas.config(yscrollcommand=scrollbar.set)

            self.scrollable_frame_hor = Frame(canvas)
            canvas.create_window((0, 0), window=self.scrollable_frame_hor, anchor='nw')

            bglabel = Label(self.scrollable_frame_hor, image=self.bgimage)
            bglabel.pack()
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            scrollbar.config(command=canvas.xview)
            albums_label = Label(self.scrollable_frame_hor, text="your albums",
                                 font=('times', 15, 'bold'),
                                 bg='lavenderblush1', fg='cadetblue', highlightthickness=0)
            albums_label.place(x=1, y=5)
            x_axis = 5

            for i in range(len(self.album_name_list)):
                album_name = self.album_name_list[i]
                photo_path = self.album_photo_list[i].strip("'").replace("/", "\\")
                album_id = self.album_ids[i]
                try:
                    img_button = Image.open(photo_path)
                    img_button = img_button.resize((100, 100))
                    img_button = ImageTk.PhotoImage(img_button)
                    self.image_references.append(img_button)
                    album_button = Button(self.scrollable_frame_hor, image=img_button, width=100, height=60,
                                          command=lambda id=album_id: self.sel(id))
                    #self.selected_album = self.album_ids[i]
                    album_button.place(x=x_axis, y=50)
                    album_name_label = Label(self.scrollable_frame_hor, text=album_name, font=('times', 15, 'bold'),
                                 bg='purple', fg='lavenderblush1',highlightthickness=0)
                    album_name_label.place(x=x_axis, y=120)
                    x_axis += 120
                except Exception as e:
                    print(f"Error loading image for {album_name}: {str(e)}")



    def create_main_frame(self):
        if self.main_frame:
            self.main_frame.destroy()
        self.main_frame = Frame(self.artist_window, width=546, height=700)
        self.main_frame.pack()
        try:
            self.bgimage = ImageTk.PhotoImage(file='background.jpg')
            print("Image loaded successfully.")
        except Exception as e:
            print("Error loading image:", e)
        canvas = Canvas(self.main_frame, width=530, height=700)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.main_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        self.scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        bglabel = Label(self.scrollable_frame, image=self.bgimage)
        bglabel.pack()
        img_path,artist_name=self.get_image()
        if img_path:
            try:
                self.img = Image.open(img_path)
                self.img = ImageTk.PhotoImage(self.img)
                label = Label(self.scrollable_frame, image=self.img,bg='black')
                label.place(x=50,y=50)
            except Exception as e:
                print("Error loading artist image:", e)
        self.create_song_frame()
        self.artist_name=artist_name
        artist_name_label = Label(self.scrollable_frame, text=self.artist_name,  font=('times', 15, 'bold'),
                                 bg='purple', fg='lavenderblush1',highlightthickness=0)
        artist_name_label.place(x=50,y=240)
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        scrollbar.config(command=canvas.yview)

        self.create_album()
        add_album_button=Button(self.scrollable_frame,text="+Add album",font=('times', 14, 'bold'),
                                                                               command=self.open_album_window, fg='CadetBlue2', bg='purple')
        add_album_button.place(x=300,y=100)
        self.create_song()
        self.create_sing_a_song()
        add_song_button=Button(self.scrollable_frame,text="+Add song",font=('times', 14, 'bold'),
                                                                               command=self.open_song_window, fg='CadetBlue2', bg='purple')
        add_song_button.place(x=300,y=150)
        self.create_horizontal_frame()


    def run_artist(self):

        self.artist_window = Tk()
        self.artist_window.geometry('546x700+50+50')
        self.artist_window.resizable(0, 0)
        self.artist_window.title('artist PAGE')
        self.create_main_frame()
        self.artist_window.mainloop()