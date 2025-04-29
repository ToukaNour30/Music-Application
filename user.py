from tkinter import messagebox, END
import pymysql
from tkinter import *
from PIL import Image, ImageTk
import pygame


class user():
    def __init__(self):
        self.playlist_list = None
        self.user_id = 0
        self.user_window= None
        self.bgLabel=None
        self.main_frame=None
        self.search_frame=None
        self.playlist_frame=None
        self.bgimage = None
        self.exploreicon = None
        self.searchicon=None
        self.playlisticon=None
        self.search_entry=None
        self. artist_ids=[]
        self.scrollable_frame=None
        self.scrollable_search_frame=None
        self.scrollable_playlist_frame=None
        self.songs_photo=[]
        self.songs_name=[]
        self.image_references=[]
        self.image_references_albums=[]
        self.image_references_play = []
        self.album_photo_list=[]
        self.album_name_list=[]
        self.album_ids=[]
        self.play_single_songs=[]
        self.stopicon=None
        self.playicon=None
        self.song_bar=None
        self.current_pos=0
        self.selected_album=0
        self.song_album_photo=[]
        self.song_album_name=[]
        self.image_references_songs=[]
        self.scrollable_album_frame=None
        self.song_album_frame=None
        self.play_album_song=[]
        self.current_song = None
        self.song_name=""
        self.photo_path=""
        self.song_path=""
        self.selected_somg_name=""
        self.selected_photo_path = ""
        self.selected_song_path = ""
        self.songs_name_search=[]
        self.songs_photo_search=[]
        self.play_single_songs_search=[]
        self.stop_flag=True
        self.play_flag=True
        self.song_path=""
        pygame.mixer.init()
        self.img=None
        self.add_window=None
        self.playlist_name_entry=None
        self.delete_window=None
        self.playlist_name_delete_entry = None
        self.playlist_name=None
        self.playlist_name_list=[]
        self.add_in_playlist_window=None
        self.selected_song_id=None
        self.song_id_list=[]
        self.song_id=""
        self.selected_playlist=""
        self.playlist_id_list=[]
        self.playlist_label=None
        self.bglabel_playlist=None
        self.add_playlist = None
        self.delete_playlist = None
        self.label = None
        self.user_name_label = None
        self.playlist_name_button = None
        self.selected_playlist_id=None
        self.songs_in_playlist=[]
        self.songs_namelist=[]
        self.songs_pathlist=[]
        self.song_pathphoto=[]
        self.song_frame=None
        self.song_id_list_search=[]
        self.song_id_list_main=[]





    def get_image(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'select * from user where user_id=%s'
            mycursor.execute(query, (self.user_id,))
            artist_row = mycursor.fetchone()
            if artist_row:
                img_path = artist_row[4]
                user_name = artist_row[2]
                return img_path, user_name
        except pymysql.Error as e:
            print(f"error:{str(e)}")
        return None
    def create_playlist_table(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='******')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please try again')
            return
        query = 'CREATE DATABASE IF NOT EXISTS musicapp'
        mycursor.execute(query)
        query = 'USE musicapp'
        mycursor.execute(query)
        query_playlist = 'create table IF NOT EXISTS playlist(playlist_id INT AUTO_INCREMENT PRIMARY KEY,playlist_name varchar (20),' \
                        'user_id int, foreign key (user_id) references user(user_id) )'
        mycursor.execute(query_playlist)
        if con:
            con.close()

    def create_playlist_track_table(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='******')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please try again')
            return
        query = 'CREATE DATABASE IF NOT EXISTS musicapp'
        mycursor.execute(query)
        query = 'USE musicapp'
        mycursor.execute(query)
        query_playlist = '''CREATE TABLE IF NOT EXISTS playlist_track (
                        playlist_id INT,
                        song_id INT,
                        FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id),
                        FOREIGN KEY (song_id) REFERENCES song(song_id),
                        PRIMARY KEY (playlist_id, song_id)
                    )'''

        mycursor.execute(query_playlist)
        if con:
            con.close()


    def search(self):
        self.songs_name_search.clear()
        self.songs_photo_search.clear()
        self.play_single_songs_search.clear()
        self.song_id_list_search.clear()
        try:
            con = pymysql.connect(host='localhost', user='root', password='******')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please try again')
            return
        query = 'use musicapp'
        mycursor.execute(query)
        query = 'select * from song where song_name=%s '
        mycursor.execute(query, (self.search_entry.get()))
        rows = mycursor.fetchall()
        if rows == None:
            messagebox.showerror('ERROR', 'artist not found')
        elif rows:
            for row in rows:
                self.songs_name_search.append(row[1])
                self.songs_photo_search.append(row[3])
                self.play_single_songs_search.append(row[4])
                self.song_id_list_search.append(row[0])


    def on_enter(self,event):
        if event.keycode==13:
            self.search()
        y_axis = 60
        y_axis_label = 130
        widgets_to_keep = [self.bglabel, self.search_entry]
        for widget in self.scrollable_search_frame.winfo_children():
            if widget not in widgets_to_keep:
                 widget.destroy()

        for i in range(len(self.songs_name_search)):
            self.song_name = self.songs_name_search[i]
            self.photo_path = self.songs_photo_search[i].strip("'").replace("/", "\\")
            self.song_path = self.play_single_songs_search[i]
            song_id = self.song_id_list_search[i]

            # (song_name, photo_path)
            try:
                img_label = Image.open(self.photo_path)
                img_label = img_label.resize((100, 100))
                img_label = ImageTk.PhotoImage(img_label)
                self.image_references_songs.append(img_label)
                song_button = Button(self.scrollable_search_frame, image=img_label, width=100, height=60,
                                     command=lambda path=self.song_path, photo=self.photo_path, name=self.song_name:
                                     self.selected(path, photo, name, self.search_frame)
                                     )
                song_button.place(x=1, y=y_axis)
                song_name_label = Label(self.scrollable_search_frame, text=self.song_name,font=('times', 15, 'bold'),
                                     bg='purple', fg='lavenderblush1', highlightthickness=0)
                song_name_label.place(x=1, y=y_axis_label)
                add_song_button = Button(self.scrollable_search_frame, text="...", font=('times', 10, 'bold'), width=1,
                                         height=1,
                                         bg='purple', fg='lavenderblush1', highlightthickness=0,
                                         command=lambda song=song_id:
                                         self.add_in_playlist(song)
                                         )
                add_song_button.place(x=100, y=y_axis)
                y_axis += 110
                y_axis_label += 110
            except Exception as e:
                print(f"Error loading image for {self.song_name}: {str(e)}")

    def createplaylist(self):
        # self.add_window = Toplevel(self.user_window)
        # self.add_window.geometry('200x150')
        # self.add_window.title("Add in playlist")
        #
        # playlist_name_label = Label(self.add_window, text="playlist Name", bg='purple', fg='lavenderblush1')
        # playlist_name_label.place(x=20, y=20)
        # self.playlist_name_entry = Entry(self.add_window, bg='cadetblue')
        # self.playlist_name_entry.place(x=20, y=45)
        # add_button = Button(self.add_window, text="Add", command=self.createplaylist, bg='purple',
        #                     fg='lavenderblush1')
        # add_button.place(x=50, y=100)
        try:
            con = pymysql.connect(host='localhost', user='root', password='******')
            mycursor = con.cursor()
            query = 'CREATE DATABASE IF NOT EXISTS musicapp'
            mycursor.execute(query)
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'insert into playlist (playlist_name,user_id) VALUES (%s,%s)'
            mycursor.execute(query, (self.playlist_name_entry.get(), self.user_id))
            con.commit()
            messagebox.showinfo("Success", f"Playlist '{self.playlist_name_entry.get()}' created successfully!")
            if hasattr(self, 'add_window'):
                self.add_window.destroy()
                self.create_playlist_frame()
        except pymysql.Error as e:
            print(f"error:{str(e)}")

    def get_songs(self):
        # self.songs_name.clear()
        # self.songs_photo.clear()
        # self.play_single_songs.clear()
        # self.song_id_list.clear()
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'SELECT * FROM SONG WHERE album_id is NULL ORDER BY RAND() LIMIT 5'
            mycursor.execute(query)
            songs_rows = mycursor.fetchall()
            if songs_rows:
                # print(songs_rows)
                for song in songs_rows:
                    self.songs_name.append(song[1])
                    self.songs_photo.append(song[3])
                    self.play_single_songs.append(song[4])
                    self.song_id_list_main.append(song[0])
                    # print(self.play_single_songs)

        except pymysql.Error as e:
            print(f"error:{str(e)}")

    def get_albums(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'SELECT * FROM album ORDER BY RAND() LIMIT 5 '
            mycursor.execute(query)
            album_rows = mycursor.fetchall()
            if album_rows:
                for album_row in album_rows:
                    img_path = album_row[3]
                    album_name = album_row[1]
                    album_id = album_row[0]
                    self.album_photo_list.append(img_path)
                    self.album_name_list.append(album_name)
                    self.album_ids.append(album_id)
                return True
            else:
                print("No albums found for the artist.")
                return False
        except pymysql.Error as e:
            print(f"error:{str(e)}")

        return None

    def get_album_songs(self):
        self.song_album_photo.clear()
        self.song_album_name.clear()
        self.song_id_list.clear()
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'SELECT * FROM song WHERE album_id = %s'
            mycursor.execute(query, (self.selected_album,))
            song_ids = mycursor.fetchall()
            # print(song_ids)
            for song_id in song_ids:
                if song_id:
                    img_path = song_id[3]
                    song_name = song_id[1]
                    self.play_album_song.append(song_id[4])
                    self.song_album_photo.append(img_path)
                    self.song_album_name.append(song_name)
                    self.song_id_list.append(song_id[0])
                    # print(self.play_album_song)
            if song_ids:
                return True
            else:
                print("No albums found for the artist.")
                return False
        except pymysql.Error as e:
            print(f"error:{str(e)}")
        return None

    def show_playlist(self):
        self.playlist_name_list.clear()
        try:
            con = pymysql.connect(host='localhost', user='root', password='******')
            mycursor = con.cursor()
            query = 'CREATE DATABASE IF NOT EXISTS musicapp'
            mycursor.execute(query)
            query = 'USE musicapp'
            mycursor.execute(query)
            query= 'select * from playlist where user_id=%s'
            mycursor.execute(query,self.user_id)
            playlists=mycursor.fetchall()
            if playlists:
                for playlist in playlists:
                    self.playlist_name_list.append(playlist[1])
                    self.playlist_id_list.append(playlist[0])
                    print(self.playlist_name_list)
                return True
            else:
                print("No playlists found for the user.")
                return False
        except pymysql.Error as e:
            print(f"error:{str(e)}")
        finally:
            if con:
                con.close()

    def insert_into_playlist_track(self, playlist_name, song_id):
        self.selected_song_id = song_id
        self.selected_playlist = playlist_name
        print(self.selected_song_id, self.selected_playlist)
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'select playlist_id from playlist where playlist_name=%s'
            mycursor.execute(query, self.selected_playlist)
            playlist_id = mycursor.fetchone()
            print(playlist_id)
            query = 'INSERT INTO playlist_track (playlist_id, song_id) VALUES (%s, %s)'
            mycursor.execute(query, (playlist_id, self.selected_song_id))
            con.commit()
            messagebox.showinfo("Success", f"Song added to '{self.selected_playlist}' playlist successfully!")
        except pymysql.Error as e:
            print(f"error: {str(e)}")
            messagebox.showerror("Error", f"Database Error: {str(e)}. Please try again")
    def deletplaylist(self):

        try:
            con = pymysql.connect(host='localhost', user='root', password='emy123')
            mycursor = con.cursor()
            query = 'CREATE DATABASE IF NOT EXISTS musicapp'
            mycursor.execute(query)
            query = 'USE musicapp'
            mycursor.execute(query)
            delete_quere='delete from playlist where playlist_name=%s and user_id=%s'
            mycursor.execute(delete_quere,(self.playlist_name_delete_entry.get(),self.user_id))
            con.commit()
            messagebox.showinfo("Success", f"Playlist '{self.playlist_name_delete_entry.get()}' deleted successfully!")
            if hasattr(self, 'delete_window'):
                self.delete_window.destroy()
                self.create_playlist_frame()
        except pymysql.Error as e:
                print(f"error:{str(e)}")
        finally:
                if con:
                    con.close()
    def get_songs_in_playlist(self):
        self.songs_namelist.clear()
        self.songs_pathlist.clear()
        self.song_pathphoto.clear()
        self.song_id_list.clear()
        try:
            con = pymysql.connect(host='localhost', user='root', password='*****')
            mycursor = con.cursor()
            query = 'CREATE DATABASE IF NOT EXISTS musicapp'
            mycursor.execute(query)
            query = 'USE musicapp'
            mycursor.execute(query)
            query = 'select song_id from playlist_track where playlist_id=%s'
            mycursor.execute(query, self.selected_playlist_id)
            playlists = mycursor.fetchall()

            if playlists:
                for playlist in playlists:
                    print(playlist)
                    query='select song_name,song_path,song_photo,song_id from song where song_id=%s'
                    mycursor.execute(query,playlist)
                    song_info = mycursor.fetchone()
                    if song_info:
                        song_name, song_path,song_photo,song_id = song_info
                        self.songs_namelist.append(song_name)
                        self.songs_pathlist.append(song_path)
                        self.song_pathphoto.append(song_photo)
                        self.song_id_list.append(song_id)
                    else:
                        print(f"No songs found ")

                return True
            else:
                print("No playlists found for the user.")
                return False
        except pymysql.Error as e:
            print(f"error:{str(e)}")
        finally:
            if con:
                con.close()


    def show_songs_playlist(self,id):
        y_axis = 50
        y_axis_label = 130
        self.selected_playlist_id=id
        self.get_songs_in_playlist()
        self.song_frame = Frame(self.scrollable_playlist_frame, width=540, height=700)
        self.song_frame.place(x=10, y=310)
        bglabel = Label(self.song_frame, image=self.bgimage)
        bglabel.pack()
        for i in range(len(self.songs_namelist)):
            self.song_name = self.songs_namelist[i]
            self.photo_path = self.song_pathphoto[i].strip("'").replace("/", "\\")
            self.song_path = self.songs_pathlist[i]
            # (song_name, photo_path)
            try:
                img_label = Image.open(self.photo_path)
                img_label = img_label.resize((100, 100))
                img_label = ImageTk.PhotoImage(img_label)
                self.image_references_songs.append(img_label)
                song_button = Button(self.song_frame, image=img_label, width=100, height=60,
                                     command=lambda path=self.song_path, photo=self.photo_path, name=self.song_name:
                                     self.selected(path, photo, name, self.playlist_frame)
                                     )
                song_button.place(x=1, y=y_axis)
                song_name_label = Label(self.song_frame, text=self.song_name,bg='purple',
                            fg='lavenderblush1')
                song_name_label.place(x=1, y=y_axis_label)
                y_axis += 110
                y_axis_label += 110
            except Exception as e:
                print(f"Error loading image for {self.song_name}: {str(e)}")


    def add_in_playlist(self,song_id):
        self.selected_song_id=song_id
        self.show_playlist()
        self.add_in_playlist_window = Toplevel(self.user_window)
        self.add_in_playlist_window.geometry('200x150')
        y_axis=50
        print(self.playlist_name_list)
        for playlist_name in self.playlist_name_list:
            playlist_button = Button(self.add_in_playlist_window, text=playlist_name, bg='purple',
                            fg='lavenderblush1',
                                     command=lambda name=playlist_name,song=song_id:
                                     self.insert_into_playlist_track(name,song))
            playlist_button.place(x=50,y=y_axis)
            y_axis+=30



    def set_user_id(self,received_user_id):

        self.user_id=received_user_id

    def create_song_bar(self,song_path,photo,name,frame):
        self.selected_song_path=song_path
        self.selected_photo_path=photo
        self.selected_somg_name=name
        self.song_bar = Frame(frame, bg='white', height=50, width=546)
        self.song_bar.place(relx=0, rely=0.85)
        img = Image.open(photo)
        img = img.resize((50, 50))
        img = ImageTk.PhotoImage(img)
        self.image_references_play.append(img)
        photo_label = Label(self.song_bar, image=img)
        photo_label.place(relx=0.04, rely=0)
        name_label = Label(self.song_bar, text=name)
        name_label.place(relx=0.15, rely=0)
        if self.play_flag:
            self.stopicon = PhotoImage(file='play_icon.png')
            stop_button = Button(self.song_bar, image=self.stopicon, bd=0, bg='white', activebackground='white',
                                 command=self.stop)
            stop_button.place(relx=0.9, rely=0)
        else:
            self.stop()
    def selected(self,path,photo,name,frame):
        print(path)
        self.selected_song_path = path
        pygame.mixer.music.load(self.selected_song_path)
        pygame.mixer.music.play(loops=0, start=self.current_pos)
        self.create_song_bar(self.song_path,photo,name,frame)

    def stop(self):
        self.stop_flag=True
        self.play_flag = False
        self.current_pos = pygame.mixer.music.get_pos()
        pygame.mixer.music.stop()
        self.playicon = PhotoImage(file='stop_icon.png')
        play_button = Button(self.song_bar, image=self.playicon, bd=0, bg='white', activebackground='white',
                               command=self.play)
        play_button.place(relx=0.9, rely=0)
    def play(self):
        #print(self.current_pos)
        self.play_flag=True
        self.stop_flag = False
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.selected_song_path)
            pygame.mixer.music.play(loops=0, start=self.current_pos// 1000)
        stop_button = Button(self.song_bar, image=self.stopicon, bd=0, bg='white', activebackground='white',
                             command=self.stop)
        stop_button.place(relx=0.9, rely=0)

    def on_add(self):
        self.add_window = Toplevel(self.user_window)
        self.add_window.geometry('200x150')
        self.add_window.title("Add a playlist")

        playlist_name_label = Label(self.add_window, text="playlist Name", bg='purple', fg='lavenderblush1')
        playlist_name_label.place(x=20, y=20)
        self.playlist_name_entry = Entry(self.add_window, bg='cadetblue')
        self.playlist_name_entry.place(x=20, y=45)
        add_button = Button(self.add_window, text="Add", command=self.createplaylist, bg='purple',
                            fg='lavenderblush1')
        add_button.place(x=50, y=100)

    def on_delet(self):
        self.delete_window = Toplevel(self.user_window)
        self.delete_window.geometry('200x150')
        self.delete_window.title("delete a playlist")

        playlist_name_label = Label(self.delete_window, text="playlist Name", bg='purple', fg='lavenderblush1')
        playlist_name_label.place(x=20, y=20)
        self.playlist_name_delete_entry = Entry(self.delete_window, bg='cadetblue')
        self.playlist_name_delete_entry.place(x=20, y=45)
        add_button = Button(self.delete_window, text="DELETE", command=self.deletplaylist, bg='purple',
                            fg='lavenderblush1')
        add_button.place(x=50, y=100)

    def explore(self):
        if self.search_frame:
            self.search_frame.pack_forget()
        if self.playlist_frame:
            self.playlist_frame.pack_forget()
        if self.song_album_frame:
            self.song_album_frame.destroy()
        if self.bgimage:
            self.bgimage=None
        self.create_main_frame()

    def show_album_songs(self,id):
        #print(id)
        self.selected_album = id

        songs = self.get_album_songs()

        if songs:
            if self.main_frame:
                self.main_frame.destroy()
            if self.song_album_frame:
                self.song_album_frame.destroy()

            self.song_album_frame = Frame(self.user_window, width=540, height=700)
            self.song_album_frame.pack()
            try:
                self.bgimage = ImageTk.PhotoImage(file='background.jpg')
                print("Image loaded successfully.")
            except Exception as e:
                print("Error loading image:", e)
            canvas = Canvas(self.song_album_frame, width=530, height=700)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)

            scrollbar = Scrollbar(self.song_album_frame, orient=VERTICAL)
            scrollbar.pack(side=RIGHT, fill=Y)

            scrollbar.config(command=canvas.yview)
            canvas.config(yscrollcommand=scrollbar.set)

            self.scrollable_album_frame = Frame(canvas)
            canvas.create_window((0, 0), window=self.scrollable_album_frame, anchor='nw')
            bglabel = Label(self.scrollable_album_frame, image=self.bgimage)
            bglabel.pack()
            y_axis = 60
            y_axis_label = 130
            # print(len(self.song_name_label))
            for i in range(len(self.song_album_name)):
                self.song_name = self.song_album_name[i]
                self.photo_path = self.song_album_photo[i].strip("'").replace("/", "\\")
                self.song_path = self.play_album_song[i]
                self.song_id = self.song_id_list[i]

                try:
                    img_label = Image.open(self.photo_path)
                    img_label = img_label.resize((100, 100))
                    img_label = ImageTk.PhotoImage(img_label)
                    self.image_references_songs.append(img_label)
                    song_button =Button(self.song_album_frame, image=img_label, width=100, height=60,
                                        command=lambda path=self.song_path,photo=self.photo_path, name=self.song_name:
                                        self.selected(path,photo, name,self.song_album_frame)
                                        )
                    song_button.place(x=1, y=y_axis)
                    song_name_label = Label(self.scrollable_album_frame, text=self.song_name,bg='purple',
                            fg='lavenderblush1')
                    song_name_label.place(x=1, y=y_axis_label)
                    add_song_button = Button(self.song_album_frame, text="...", font=('times', 10, 'bold'), width=1,
                                             height=1,
                                             bg='purple', fg='lavenderblush1', highlightthickness=0,
                                             command=lambda song=self.song_id:
                                             self.add_in_playlist(song)
                                             )
                    add_song_button.place(x=100, y=y_axis)
                    y_axis += 110
                    y_axis_label += 110
                except Exception as e:
                    print(f"Error loading image for {self.song_name}: {str(e)}")
            if self.song_bar:
                self.create_song_bar(self.selected_song_path, self.selected_photo_path, self.selected_somg_name,
                                     self.song_album_frame)
            self.buttom_bar(self.song_album_frame)
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            scrollbar.config(command=canvas.yview)

    def create_playlist_frame(self):
        playlist=self.show_playlist()
        if self.main_frame:
            self.main_frame.pack_forget()
        if self.search_frame:
            self.search_frame.pack_forget()
        if self.playlist_frame:
            self.playlist_frame.destroy()
        if self.song_album_frame:
            self.song_album_frame.destroy()
        if self.bgimage:
            self.bgimage = None
        self.playlist_frame = Frame(self.user_window, width=546, height=700)
        self.playlist_frame.pack()
        try:
            self.bgimage = ImageTk.PhotoImage(file='background.jpg')
            print("Image loaded successfully.")
        except Exception as e:
            print("Error loading image:", e)
        canvas = Canvas(self.playlist_frame, width=530, height=700)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.playlist_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        self.scrollable_playlist_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.scrollable_playlist_frame, anchor='nw')
        self.bglabel_playlist = Label(self.scrollable_playlist_frame, image=self.bgimage)
        self.bglabel_playlist.pack()
        self.playlist_label=Label(self.scrollable_playlist_frame,text="your playlists",bg='purple',
                            fg='lavenderblush1')
        self.playlist_label.place(x=5,y=200)
        self.add_playlist=Button(self.scrollable_playlist_frame,text="+Add playlist",font=('times', 15, 'bold'),
                                 bg='lavenderblush1', fg='cadetblue', highlightthickness=0,command=self.on_add)
        self.add_playlist.place(x=360,y=50)
        self.delete_playlist=Button(self.scrollable_playlist_frame,text="-Delete playlist",font=('times', 15, 'bold'),
                                 bg='lavenderblush1', fg='cadetblue', highlightthickness=0,command=self.on_delet)
        self.delete_playlist.place(x=360,y=100)
        img_path, user_name = self.get_image()
        if img_path:
            try:
                self.img = Image.open(img_path)
                self.img = ImageTk.PhotoImage(self.img)
                self.label = Label(self.scrollable_playlist_frame, image=self.img, bg='black')
                self.label.place(x=50, y=50)
            except Exception as e:
                print("Error loading artist image:", e)
        self.user_name_label = Label(self.scrollable_playlist_frame, text=user_name, font=('times', 15, 'bold'),
                                  bg='purple', fg='lavenderblush1', highlightthickness=0)
        self.user_name_label.place(x=50, y=120)

        x_axis=1
        if playlist:
            for i in range(len(self.playlist_name_list)):
                print(self.playlist_name_list[i])
                self.playlist_name = self.playlist_name_list[i]
                playlist_id=self.playlist_id_list[i]
                self.playlist_name_button = Button(self.scrollable_playlist_frame, text=self.playlist_name,font=('times', 15, 'bold'),
                                  bg='purple', fg='lavenderblush1', highlightthickness=0,
                                              command=lambda id=playlist_id:
                                              self.show_songs_playlist(id)
                                              )

                self.playlist_name_button.place(x=x_axis, y=250)

                x_axis += 110

            if self.song_bar:
                self.create_song_bar(self.selected_song_path, self.selected_photo_path, self.selected_somg_name, self.playlist_frame)
            self.buttom_bar(self.playlist_frame)
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            scrollbar.config(command=canvas.yview)

    def create_search_frame(self):
        if self.main_frame:
            self.main_frame.pack_forget()
        if self.playlist_frame:
            self.playlist_frame.pack_forget()
        if self.song_album_frame:
            self.song_album_frame.destroy()


        if self.bgimage:
            self.bgimage = None
        self.search_frame=Frame(self.user_window, width=546, height=700)
        self.search_frame.pack()
        try:
            self.bgimage = ImageTk.PhotoImage(file='background.jpg')
            print("Image loaded successfully.")
        except Exception as e:
            print("Error loading image:", e)

        canvas = Canvas(self.search_frame, width=530, height=700)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.search_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        self.scrollable_search_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.scrollable_search_frame, anchor='nw')
        self.bglabel = Label(self.scrollable_search_frame, image=self.bgimage)
        self.bglabel.pack()
        self.search_entry = Entry(self.scrollable_search_frame, width=30)
        self.search_entry.place(x=160, y=10)
        self.search_entry.bind('<KeyPress>', self.on_enter)

        if self.song_bar:
            self.create_song_bar(self.selected_song_path, self.selected_photo_path, self.selected_somg_name, self.search_frame)
        self.buttom_bar(self.search_frame)
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        scrollbar.config(command=canvas.yview)


    def create_main_frame(self):
        self.create_playlist_table()
        self.create_playlist_track_table()
        if not self.songs_name :
            self.get_songs()
        self.main_frame = Frame(self.user_window, width=546, height=700)
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


        songs=Label(self.scrollable_frame,text="songs:",font=('times', 15, 'bold'),
                                     bg='purple', fg='lavenderblush1', highlightthickness=0)
        songs.place(x=5,y=50)
        x_axis = 1
        for i in range(len(self.songs_name)):
            self.song_name = self.songs_name[i]
            self.photo_path = self.songs_photo[i].strip("'").replace("/", "\\")
            self.song_path = self.play_single_songs[i]
            song_id=self.song_id_list_main[i]
            #print(self.song_path)

            try:
                img_button = Image.open(self.photo_path)
                img_button = img_button.resize((100, 100))
                img_button = ImageTk.PhotoImage(img_button)
                self.image_references.append(img_button)
                #print(str(self.song_path))
                song_button = Button(self.scrollable_frame, image=img_button, width=100, height=60,
                                     font=('times', 15, 'bold'),
                                     bg='purple', fg='lavenderblush1', highlightthickness=0,
                                     command=lambda path=self.song_path,photo=self.photo_path,name=self.song_name:
                                     self.selected(path,photo,name,self.main_frame))
                song_button.place(x=x_axis, y=100)
                song_name_label = Label(self.scrollable_frame, text=self.song_name, font=('times', 10, 'bold'),
                                     bg='purple', fg='lavenderblush1', highlightthickness=0)
                song_name_label.place(x=x_axis, y=170)
                add_song_button=Button(self.scrollable_frame,text="...",font=('times', 10, 'bold'),width=1,height=1,
                                     bg='purple', fg='lavenderblush1', highlightthickness=0,
                                       command=lambda song=song_id:
                                       self.add_in_playlist(song))

                add_song_button.place(x=x_axis+100,y=100)
                x_axis += 130
            except Exception as e:
                print(f"Error loading image for {self.song_name}: {str(e)}")
        if self.song_bar:
            self.create_song_bar(self.selected_song_path, self.selected_photo_path, self.selected_somg_name, self.main_frame)
        if not self.album_name_list:
            self.get_albums()
        albums = Label(self.scrollable_frame, text="albums:",font=('times', 15, 'bold'),
                                     bg='purple', fg='lavenderblush1', highlightthickness=0)
        albums.place(x=10, y=250)
        x_axis = 1
        for i in range(len(self.album_name_list)):
            album_name = self.album_name_list[i]
            photo_path = self.album_photo_list[i].strip("'").replace("/", "\\")
            album_id = self.album_ids[i]
            try:
                img_button = Image.open(photo_path)
                img_button = img_button.resize((100, 100))
                img_button = ImageTk.PhotoImage(img_button)
                self.image_references_albums.append(img_button)
                album_button = Button(self.scrollable_frame, image=img_button, width=100, height=60,
                                      font=('times', 15, 'bold'),
                                      bg='purple', fg='lavenderblush1', highlightthickness=0,
                                      command=lambda id=album_id: self.show_album_songs(id))
                album_button.place(x=x_axis, y=300)
                print(album_name,"here")
                album_name_label = Label(self.scrollable_frame, text=album_name,  bg='purple',
                                         fg='lavenderblush1', highlightthickness=0)
                album_name_label.place(x=x_axis, y=370)
                x_axis += 110
            except Exception as e:
                print(f"Error loading image for {album_name}: {str(e)}")
        #print(self.album_name_list,self.album_photo_list)
        self.buttom_bar(self.main_frame)
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        scrollbar.config(command=canvas.yview)

    def buttom_bar(self,frame):
        if self.searchicon or self.exploreicon or self.playlisticon:
            self.searchicon=None
            self.exploreicon=None
            self.playlisicon=None


        button_bar = Frame(frame, bg='white', height=50, width=546)
        button_bar.place(relx=0, rely=0.93)
        self.exploreicon = PhotoImage(file='exploreicon.png')
        explore_button = Button(button_bar, image=self.exploreicon, bd=0,
                                font=('times', 15, 'bold'),
                                bg='purple', fg='lavenderblush1', highlightthickness=0,
                                command=self.explore)
        explore_button.place(relx=0.05, rely=0)
        explore_label = Label(button_bar, text="explore", font=('Open Sans', 7, 'bold'),
                              fg='black', bg='white')
        explore_label.place(relx=0.05, rely=0.5)
        self.searchicon = PhotoImage(file='searchicon.png')
        search_button = Button(button_bar, image=self.searchicon, bd=0, font=('times', 15, 'bold'),
                                  bg='purple', fg='lavenderblush1', highlightthickness=0,
                               command=self.create_search_frame)
        search_button.place(relx=0.4, rely=0)
        search_label = Label(button_bar, text="search", font=('Open Sans', 7, 'bold'),
                             fg='black', bg='white')
        search_label.place(relx=0.4, rely=0.6)

        self.playlisticon = PhotoImage(file='playlisticon.png')
        playlist_button = Button(button_bar, image=self.playlisticon, bd=0,font=('times', 15, 'bold'),
                                  bg='purple', fg='lavenderblush1', highlightthickness=0,
                                 command=self.create_playlist_frame)
        playlist_button.place(relx=0.8, rely=0)
        playlist_label = Label(button_bar, text="playlist", font=('Open Sans', 7, 'bold'),
                               fg='black', bg='white')
        playlist_label.place(relx=0.8, rely=0.6)



    def run_user(self):

        self.user_window = Tk()
        self.user_window.geometry('546x700+50+50')
        self.user_window.resizable(0, 0)
        self.user_window.title('USER PAGE')
        self.create_main_frame()
        self.buttom_bar(self.main_frame)
        self.user_window.mainloop()