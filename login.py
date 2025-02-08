#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pyodbc  # Import pyodbc for MS SQL Server connection
from tkinter import messagebox
from subprocess import call
from subprocess import Popen


class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")

        # Uncomment and set the correct path for the background image if needed
        # self.bg = ImageTk.PhotoImage(file=r"C:\Users\Sharwari\Desktop\DBMS MINI PROJECT\images\2.jpeg")
        # lbl_bg = Label(self.root, image=self.bg)
        # lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width=340, height=450)

        get_str = Label(frame, text="ADMIN LOGIN", font=("times new roman", 20, "bold"), fg="white", bg="black")
        get_str.place(x=80, y=100)

        # Labels
        username = Label(frame, text="Username", font=("times new roman", 15, "bold"), fg="white", bg="black")
        username.place(x=50, y=155)

        self.txtuser = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=40, y=180, width=270)

        password = Label(frame, text="Password", font=("times new roman", 15, "bold"), fg="white", bg="black")
        password.place(x=50, y=220)

        self.txtpass = ttk.Entry(frame, font=("times new roman", 15, "bold"), show="*")
        self.txtpass.place(x=40, y=250, width=270)

        loginbtn = Button(frame, text="Login", command=self.login, font=("times new roman", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="red", activeforeground="white", activebackground="red")
        loginbtn.place(x=110, y=300, width=120)



    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                # Using SQL Server Authentication (username and password)
                conn = pyodbc.connect('DRIVER={SQL Server};'
                                      'SERVER=192.168.0.159,49170;'  # Remote server IP and port
                                      'DATABASE=management;'  # Your database name
                                      'UID=admin@123;'  # Your SQL login username
                                      'PWD=police@7890'  # Replace with your actual SQL Server password
                                     )
                cursor = conn.cursor()

                # Execute the query
                cursor.execute("SELECT * FROM dbo.login WHERE userid=? AND password=?", 
                               (self.txtuser.get(), self.txtpass.get()))
                row = cursor.fetchone()

                if row is None:
                    messagebox.showerror("Error", "Invalid User ID or Password")
                else:
                    messagebox.showinfo("Successful", "Welcome")
                    self.root.destroy()
                    Popen(['python', 'crime_management_system.py'])  # Run the next script
                conn.close()
            except Exception as er:
                messagebox.showerror('Error', f'Due to {str(er)}')

# Assuming you have your Tkinter setup and main loop
if __name__ == "__main__":
    root = Tk()
    app = Login_Window(root)
    root.mainloop()


# In[ ]:




