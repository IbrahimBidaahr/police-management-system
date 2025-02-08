#!/usr/bin/env python
# coding: utf-8

# In[39]:


from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pyodbc
from tkinter import messagebox
import os
import json



class YourApplication:
    def __init__(self):
        self.load_config()  # Call the method to load the configuration

    def load_config(self):
        """Load database configuration from config.json"""
        with open('config.json', 'r') as config_file:
            self.config = json.load(config_file)  # Load JSON data from the file

    def search_data(self): 
        if self.var_com_search.get() == "":
            messagebox.showerror('Error', 'All fields are required') 
        else:
            try:
                # Create the connection string using values from the config.json file
                connection_string = (
                    f"DRIVER={self.config['driver']};"
                    f"SERVER={self.config['server']};"
                    f"DATABASE={self.config['database']};"
                )

                # Add authentication method to the connection string
                if self.config['trusted_connection'].lower() == 'yes':
                    connection_string += "Trusted_Connection=yes;"
                else:
                    connection_string += f"UID={self.config['username']};PWD={self.config['password']};"

                # Connect to the database
                conn = pyodbc.connect(connection_string)
                my_cursor = conn.cursor()

                # SQL query based on user input
                my_cursor.execute('SELECT * FROM dbo.criminal WHERE ' + str(self.var_com_search.get()) + " LIKE '%" + str(self.var_search.get()) + "%'")
                rows = my_cursor.fetchall()

                if len(rows) != 0:
                    self.criminal_table.delete(*self.criminal_table.get_children())
                    for row in rows:
                        self.criminal_table.insert('', END, values=row)  # Directly insert the row

                conn.commit()
                conn.close()

            except Exception as es:
                messagebox.showerror('Error', f'Due to {str(es)}')



class Criminal:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1530x790+0+0')
        self.root.title('POLICE MANAGEMENT SYSTEM')

        # Variables
        self.var_case_id = StringVar()
        self.var_criminal_no = StringVar()
        self.var_name = StringVar()
        self.var_nickname = StringVar()
        self.var_arrest_date = StringVar()
        self.var_date_of_crime = StringVar()
        self.var_address = StringVar()
        self.var_age = StringVar()
        self.var_occupation = StringVar()
        self.var_birthMark = StringVar()
        self.var_crime_type = StringVar()
        self.var_father_name = StringVar()
        self.var_gender = StringVar()
        self.var_wanted = StringVar()

        # Create a frame for the images
        img_frame = Frame(self.root, bd=5, relief='solid', bg="white")
        img_frame.place(x=10, y=10, width=1530, height=200)  # Adjusted to fit the original size

        # Load images
        self.load_images(img_frame)


        # Title Label
        lbl_title = Label(self.root, text='POLICE MANAGEMENT SYSTEM SOFTWARE', font=('times new roman', 35, 'bold'), bg='black', fg='gold')
        lbl_title.place(x=0, y=0, width=1530, height=70)

        # Load images
        self.load_images(img_frame)

        # Main frame
        Main_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        Main_frame.place(x=10, y=200, width=1500, height=560)

        # Upper frame
        upper_frame = LabelFrame(Main_frame, bd=2, relief=RIDGE, text='Criminal Information', font=('times new roman', 11, 'bold'), fg='red', bg='white')
        upper_frame.place(x=10, y=10, width=1480, height=270)

        # Labels Entry
        self.create_entry_fields(upper_frame)

        # Buttons
        self.create_buttons(upper_frame)

        # Down frame
        down_frame = LabelFrame(Main_frame, bd=2, relief=RIDGE, text='Criminal Information Table', font=('times new roman', 11, 'bold'), fg='red', bg='white')
        down_frame.place(x=10, y=280, width=1480, height=270)

        # Search frame
        self.create_search_frame(down_frame)

        # Table Frame
        self.create_table_frame(down_frame)

        self.fetch_data()

    def load_images(self, img_frame):
        print("Loading images...")  # Debugging statement
        # Create a list to hold references to the images
        self.image_references = []  # Store references to avoid garbage collection

        # Load images from 1 to 4
        images = ['C:\\Users\\surface\\police_logo.jpg', 'C:\\Users\\surface\\8.jpg', 'C:\\Users\\surface\\7.jpg']
        
        # Interchange police_logo and image3
        images[0], images[2] = images[2], images[0]  # Swap the first and third images

        for image_path in images:
            if not os.path.exists(image_path):
                print(f"Warning: Image file '{image_path}' does not exist. Skipping.")
                continue  # Skip to the next iteration if the image does not exist

            try:
                img = Image.open(image_path)
                img = img.resize((600, 160), Image.LANCZOS)  # Resize images to fit the frame
                photo = ImageTk.PhotoImage(img)

                # Create a label for each image
                label = Label(img_frame, image=photo)
                label.image = photo  # Keep a reference to avoid garbage collection
                
                # Store the reference to the image
                self.image_references.append(photo)  # Append the photo to the list
                
                # Pack the label to display the image
                label.pack(side='left', padx=10, pady=10)  # Horizontally align the images
                print(f"Image loaded successfully from {image_path}.")
            except Exception as e:
                print(f"Error loading image from {image_path}: {e}")


    



    def create_entry_fields(self, upper_frame):
        # Create entry fields for criminal information
        labels = [
            ('Case ID:', self.var_case_id),
            ('Criminal NO:', self.var_criminal_no),
            ('Criminal Name:', self.var_name),
            ('NickName:', self.var_nickname),
            ('Arrest Date:', self.var_arrest_date),
            ('Date Of Crime:', self.var_date_of_crime),
            ('Address:', self.var_address),
            ('Age:', self.var_age),
            ('Occupation:', self.var_occupation),
            ('BirthMark:', self.var_birthMark),
            ('Crime Type:', self.var_crime_type),
            ('Father Name:', self.var_father_name),
            ('Gender:', self.var_gender),
            ('Most Wanted:', self.var_wanted)
        ]

        for i, (text, var) in enumerate(labels):
            row = i // 4
            col = i % 4
            lbl = Label(upper_frame, text=text, font=('arial', 12, 'bold'), bg='white')
            lbl.grid(row=row, column=col * 2, padx=2, pady=7, sticky=W)
            entry = ttk.Entry(upper_frame, textvariable=var, width=22, font=('arial', 11, 'bold'))
            entry.grid(row=row, column=col * 2 + 1, padx=2, pady=7, sticky=W)

        # Radio buttons for gender and wanted status
        self.create_radio_buttons(upper_frame)

    def create_radio_buttons(self, upper_frame):
        # Gender Radio Buttons
        radio_frame_gender = Frame(upper_frame, bd=2, relief=RIDGE, bg='white')
        radio_frame_gender.place(x=100, y=150, width=190, height=30)

        male = Radiobutton(radio_frame_gender, variable=self.var_gender, text='Male', value='male', font=('arial', 9, 'bold'), bg='white')
        male.grid(row=0, column=0, pady=2, padx=5, sticky=W)
        self.var_gender.set('male')

        female = Radiobutton(radio_frame_gender, variable=self.var_gender, text='Female', value='female', font=('arial', 9, 'bold'), bg='white')
        female.grid(row=0, column=1, pady=2, padx=5, sticky=W)

        # Wanted Radio Buttons
        radio_frame_wanted = Frame(upper_frame, bd=2, relief=RIDGE, bg='white')
        radio_frame_wanted.place(x=410, y=150, width=190, height=30)

        yes = Radiobutton(radio_frame_wanted, variable=self.var_wanted, text='Yes', value='yes', font=('arial', 9, 'bold'), bg='white')
        yes.grid(row=0, column=0, pady=2, padx=5, sticky=W)
        self.var_wanted.set('yes')

        no = Radiobutton(radio_frame_wanted, variable=self.var_wanted, text='No', value='no', font=('arial', 9, 'bold'), bg='white')
        no.grid(row=0, column=1, pady=2, padx=5, sticky=W)

    def create_buttons(self, upper_frame):
        # Buttons for actions
        button_frame = Frame(upper_frame, bd=2, relief=RIDGE, bg='white')
        button_frame.place(x=5, y=200, width=620, height=45)

        btn_add = Button(button_frame, command=self.add_data, text='Save', font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
        btn_add.grid(row=0, column=0, padx=3, pady=5)

        btn_update = Button(button_frame, command=self.update_data, text='Update', font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
        btn_update.grid(row=0, column=1, padx=3, pady=5)

        btn_delete = Button(button_frame, command=self.delete_data, text='Delete', font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
        btn_delete.grid(row=0, column=2, padx=3, pady=5)

        btn_clear = Button(button_frame, command=self.clear_data, text='Clear', font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
        btn_clear.grid(row=0, column=3, padx=3, pady=5)

    def create_search_frame(self, down_frame):
        search_frame = LabelFrame(down_frame, bd=2, relief=RIDGE, text='Search Criminal Record', font=('times new roman', 11, 'bold'), fg='red', bg='white')
        search_frame.place(x=0, y=0, width=1470, height=60)

        search_by = Label(search_frame, font=("arial", 11, "bold"), text="Search By:", bg="red", fg="white")
        search_by.grid(row=0, column=0, sticky=W, padx=5)

        self.var_com_search = StringVar()
        combo_search_box = ttk.Combobox(search_frame, textvariable=self.var_com_search, font=("arial", 11, "bold"), width=18, state='readonly')
        combo_search_box['value'] = ('Select Option', 'Case_id', 'Criminal_no')
        combo_search_box.current(0)
        combo_search_box.grid(row=0, column=1, sticky=W, padx=5)

        self.var_search = StringVar()
        search_txt = ttk.Entry(search_frame, textvariable=self.var_search, width=18, font=("arial", 11, "bold"))
        search_txt.grid(row=0, column=2, sticky=W, padx=5)

        btn_search = Button(search_frame, command=self.search_data, text='Search', font=("arial", 13, "bold"), width=14, bg='blue')
        btn_search.grid(row=0, column=3, padx=3, pady=5)

        btn_all = Button(search_frame, command=self.fetch_data, text='Show All', font=("arial", 13, "bold"), width=14, bg='blue')
        btn_all.grid(row=0, column=4, padx=3, pady=5)

    def create_table_frame(self, down_frame):
        table_frame = Frame(down_frame, bd=2, relief=RIDGE)
        table_frame.place(x=0, y=60, width=1470, height=170)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.criminal_table = ttk.Treeview(table_frame, column=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.criminal_table.xview)
        scroll_y.config(command=self.criminal_table.yview)

        headings = [
            "Case Id", "Crime No", "Criminal Name", "Nick name", "Arrest Date",
            "Date of crime", "Address", "Age", "Occupation", "Birth Mark",
            "Crime Type", "Father Name", "Gender", "Wanted"
        ]

        for i, heading in enumerate(headings, start=1):
            self.criminal_table.heading(str(i), text=heading)
            self.criminal_table.column(str(i), width=100)

        self.criminal_table['show'] = 'headings'
        self.criminal_table.pack(fill=BOTH, expand=1)

        self.criminal_table.bind("<ButtonRelease>", self.get_cursor)

    # Add function
    def add_data(self):
        if self.var_case_id.get() == "":
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                conn = pyodbc.connect('DRIVER={SQL Server};'
                                      'SERVER=HajiDaud\\SQLEXPRESS;'  # Replace with your server name
                                      'DATABASE=management;'  # Your database name
                                      'Trusted_Connection=yes')  # Use Windows Authentication

                my_cursor = conn.cursor()
                my_cursor.execute('INSERT INTO dbo.criminal (Case_id, Criminal_id, Criminal_name, Nick_name, arrest_date, dateOfcrime, address, age, occupation, BirthMark, crimeType, fatherName, gender, wanted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                    self.var_case_id.get(),
                    self.var_criminal_no.get(),
                    self.var_name.get(),
                    self.var_nickname.get(),
                    self.var_arrest_date.get(),
                    self.var_date_of_crime.get(),
                    self.var_address.get(),
                    self.var_age.get(),
                    self.var_occupation.get(),
                    self.var_birthMark.get(),
                    self.var_crime_type.get(),
                    self.var_father_name.get(),
                    self.var_gender.get(),
                    self.var_wanted.get()
                ))
                conn.commit()
                self.fetch_data()
                self.clear_data()
                conn.close()
                messagebox.showinfo('Successful', 'Criminal record has been added')
            except Exception as es:
                messagebox.showerror('Error', f'Due to {str(es)}')

    # Fetch data
    def fetch_data(self):
        try:
            conn = pyodbc.connect('DRIVER={SQL Server};'
                              'SERVER=HajiDaud\\SQLEXPRESS;'  # Replace with your server name
                              'DATABASE=management;'  # Your database name
                              'Trusted_Connection=yes')  # Use Windows Authentication
            my_cursor = conn.cursor()
            my_cursor.execute('SELECT * FROM dbo.criminal')
            data = my_cursor.fetchall()
        
            if len(data) != 0:
                self.criminal_table.delete(*self.criminal_table.get_children())
                for row in data:
                    # Clean the data by replacing extra quotes with spaces
                    cleaned_row = tuple(str(item).replace('"', ' ').replace("'", ' ') if isinstance(item, str) else item for item in row)
                    self.criminal_table.insert('', END, values=cleaned_row)  # Insert the cleaned row
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror('Error', f'Due to {str(e)}')

  

    # Get cursor
    def get_cursor(self, event=""):
        cursor_row = self.criminal_table.focus()
        content = self.criminal_table.item(cursor_row)
        data = content['values']

        self.var_case_id.set(data[0])
        self.var_criminal_no.set(data[1])
        self.var_name.set(data[2])
        self.var_nickname.set(data[3])
        self.var_arrest_date.set(data[4])
        self.var_date_of_crime.set(data[5])
        self.var_address.set(data[6])
        self.var_age.set(data[7])
        self.var_occupation.set(data[8])
        self.var_birthMark.set(data[9])
        self.var_crime_type.set(data[10])
        self.var_father_name.set(data[11])
        self.var_gender.set(data[12])
        self.var_wanted.set(data[13])

    # Update
    def update_data(self):
        if self.var_case_id.get() == "":
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                update = messagebox.askyesno('Update', "Are you sure you want to update this record?")
                if update > 0:
                    conn = pyodbc.connect('DRIVER={SQL Server};'
                                      'SERVER=HajiDaud\\SQLEXPRESS;'  # Replace with your server name
                                      'DATABASE=management;'  # Your database name
                                      'Trusted_Connection=yes')  # Use Windows Authentication
                
                    my_cursor = conn.cursor() 
                    my_cursor.execute('UPDATE dbo.criminal SET Criminal_id=?, Criminal_name=?, Nick_name=?, arrest_date=?, dateOfcrime=?, address=?, age=?, occupation=?, BirthMark=?, crimeType=?, fatherName=?, gender=?, wanted=? WHERE Case_id=?', (
                        self.var_criminal_no.get(),
                        self.var_name.get(),
                        self.var_nickname.get(),
                        self.var_arrest_date.get(),
                        self.var_date_of_crime.get(),
                        self.var_address.get(),
                        self.var_age.get(),
                        self.var_occupation.get(),
                        self.var_birthMark.get(),
                        self.var_crime_type.get(),
                        self.var_father_name.get(),
                        self.var_gender.get(),
                        self.var_wanted.get(),
                        self.var_case_id.get()
                    ))    
                else:
                    if not update:
                        return
                conn.commit()
                self.fetch_data()
                self.clear_data()
                conn.close()
                messagebox.showinfo('Successful', 'Criminal record has been updated')
            except Exception as es:
                messagebox.showerror('Error', f'Due to {str(es)}')   
    
    # Delete
    def delete_data(self):
        if self.var_case_id.get() == "":
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                delete = messagebox.askyesno('Delete', "Are you sure you want to delete this record?")
                if delete > 0:
                    conn = pyodbc.connect('DRIVER={SQL Server};'
                                      'SERVER=HajiDaud\\SQLEXPRESS;'  # Replace with your server name
                                      'DATABASE=management;'  # Your database name
                                      'Trusted_Connection=yes')  # Use Windows Authentication
               
                    my_cursor = conn.cursor() 
                    sql = "DELETE FROM dbo.criminal WHERE Case_id=?"
                    value = (self.var_case_id.get(),)
                    my_cursor.execute(sql, value)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                self.clear_data()
                conn.close()
                messagebox.showinfo('Successful', 'Criminal record has been deleted')
            except Exception as es:
                messagebox.showerror('Error', f'Due to {str(es)}')   

    # Clear
    def clear_data(self):
        self.var_case_id.set("")
        self.var_criminal_no.set("")
        self.var_name.set("")
        self.var_nickname.set("")
        self.var_arrest_date.set("")
        self.var_date_of_crime.set("")
        self.var_address.set("")
        self.var_age.set("")
        self.var_occupation.set("")
        self.var_birthMark.set("")
        self.var_crime_type.set("")
        self.var_father_name.set("")
        self.var_gender.set("")
        self.var_wanted.set("")

    # Search
    # Search
    def search_data(self): 
        if self.var_com_search.get() == "":
            messagebox.showerror('Error', 'All fields are required') 
        else:
            try:
                conn = pyodbc.connect('DRIVER={SQL Server};'
                                  'SERVER=HajiDaud\\SQLEXPRESS;'  # Replace with your server name
                                  'DATABASE=management;'  # Your database name
                                  'Trusted_Connection=yes')  # Use Windows Authentication
            
                my_cursor = conn.cursor()
                my_cursor.execute('SELECT * FROM dbo.criminal WHERE ' + str(self.var_com_search.get()) + " LIKE '%" + str(self.var_search.get()) + "%'")
                rows = my_cursor.fetchall()
                if len(rows) != 0:
                    self.criminal_table.delete(*self.criminal_table.get_children())
                    for row in rows:
                        # Clean the data by replacing extra quotes with spaces
                        cleaned_row = tuple(str(item).replace('"', ' ').replace("'", ' ') if isinstance(item, str) else item for item in row)
                        self.criminal_table.insert('', END, values=cleaned_row)  # Insert the cleaned row
                else:
                    messagebox.showinfo('Info', 'No records found')  # Optional feedback for no results
                conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror('Error', f'Due to {str(es)}')


if __name__ == "__main__":
    root = Tk()
    obj = Criminal(root)
    root.mainloop()


# In[ ]:





# In[ ]:




