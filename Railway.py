GUI WITH DATABASE(RAIWAY APPLICATION):

CREATE DATABASE:

create database railway1;

use  railway1;

CREATE TABLE:

CREATE TABLE users (
       user_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
         email VARCHAR(100) NOT NULL
     );



 CREATE TABLE trains (
         train_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
         price DECIMAL(10, 2) NOT NULL
     );




CODE:


import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk


trains = [
    {"name": "Express Train", "price": 300.0},
    {"name": "Shatabdi Express", "price": 500.0},
    {"name": "Rajdhani Express", "price": 700.0},
    {"name": "Superfast Train", "price": 400.0},
    {"name": "Duronto Express", "price": 600.0},
]


user_name = None
user_email = None
order = []
total_price = 0.0


def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      
            password="root",  
            database="railway1"  
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None


def save_user_details(name, email):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        ''', (name, email))
        conn.commit()
        conn.close()


def login_page():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg="#A8D0E6")

   
    tk.Label(login_window, text="Login to Railway Ticket Booking", font=("Arial", 24, "bold"), bg="#3B9A96", fg="white", relief="raised", padx=10, pady=10).pack(pady=20)

   
    tk.Label(login_window, text="Enter User ID:", bg="#A8D0E6", font=("Arial", 14)).pack(pady=5)
    user_id_entry = tk.Entry(login_window, width=30, font=("Arial", 12))
    user_id_entry.pack(pady=5)

   
    def login():
        user_id = user_id_entry.get()
        if not user_id:
            messagebox.showerror("Input Error", "User ID must be provided.")
            return
        save_user_details(user_id, "N/A")  
        login_window.destroy()  
        personal_details_page()  

    tk.Button(login_window, text="Login", command=login, bg="#FF8C00", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    login_window.mainloop()


def personal_details_page():
    global personal_window, user_name, user_email
    personal_window = tk.Tk()
    personal_window.title("Enter Personal Details")
    personal_window.configure(bg="#A8D0E6")

   
    tk.Label(personal_window, text="Enter Your Personal Details", font=("Arial", 24, "bold"), bg="#3B9A96", fg="white", relief="raised", padx=10, pady=10).pack(pady=20)

    tk.Label(personal_window, text="Enter Your Name:", bg="#A8D0E6", font=("Arial", 12)).pack(pady=5)
    name_entry = tk.Entry(personal_window, width=30, font=("Arial", 12))
    name_entry.pack(pady=5)

    tk.Label(personal_window, text="Enter Your Email:", bg="#A8D0E6", font=("Arial", 12)).pack(pady=5)
    email_entry = tk.Entry(personal_window, width=30, font=("Arial", 12))
    email_entry.pack(pady=5)

   
    def next_page():
        global user_name, user_email
        user_name = name_entry.get()
        user_email = email_entry.get()

        if not user_name or not user_email:
            messagebox.showerror("Input Error", "Both name and email must be provided.")
            return
       
       
        save_user_details(user_name, user_email)
       
        personal_window.destroy()
        menu_page()

    tk.Button(personal_window, text="Next", command=next_page, bg="#FF8C00", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    personal_window.mainloop()


def menu_page():
    global menu_window, order, total_price
    menu_window = tk.Tk()
    menu_window.title("Select Your Train")
    menu_window.configure(bg="#A8D0E6")

   
    tk.Label(menu_window, text="Available Trains", font=("Arial", 24, "bold"), bg="#3B9A96", fg="white", relief="raised", padx=10, pady=10).pack(pady=20)

    train_listbox = tk.Listbox(menu_window, selectmode=tk.MULTIPLE, height=6, width=50, font=("Arial", 12))
    train_listbox.pack(pady=10)

   
    for train in trains:
        train_listbox.insert(tk.END, f"{train['name']} - RS:{train['price']}")

   
    def add_to_order():
        global order, total_price
        selected_items = train_listbox.curselection()

        if not selected_items:
            messagebox.showerror("Selection Error", "Please select at least one train.")
            return

        order = []
        total_price = 0.0

        for item in selected_items:
            train = trains[item]
            order.append(train)
            total_price += train['price']

        amount_details_page()

    tk.Button(menu_window, text="Book Ticket", command=add_to_order, bg="#FF8C00", fg="white", font=("Arial", 14, "bold")).pack(pady=20)

    menu_window.mainloop()


def amount_details_page():
    global amount_window

    amount_window = tk.Tk()
    amount_window.title("Amount Details")
    amount_window.configure(bg="#A8D0E6")

   
    tk.Label(amount_window, text="Amount Details", font=("Arial", 24, "bold"), bg="#3B9A96", fg="white", relief="raised", padx=10, pady=10).pack(pady=20)

   
    if order:
        tk.Label(amount_window, text="Your Ticket(s):", bg="#A8D0E6", font=("Arial", 14, "bold")).pack(pady=5)
        for train in order:
            tk.Label(amount_window, text=f"{train['name']} - RS:{train['price']}", bg="#A8D0E6", font=("Arial", 12)).pack(pady=5)

        tk.Label(amount_window, text=f"Total Price: RS:{total_price}", bg="#A8D0E6", font=("Arial", 16, "bold")).pack(pady=10)

    def modify_order():
        amount_window.destroy()
        menu_page()  

    def confirm_ticket():
        confirmation_page()  

    tk.Button(amount_window, text="Modify the available train", command=modify_order, bg="#FF8C00", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(amount_window, text="Confirm Ticket", command=confirm_ticket, bg="#FF8C00", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    amount_window.mainloop()


def confirmation_page():
    global confirmation_window

    confirmation_window = tk.Tk()
    confirmation_window.title("Ticket Confirmation")
    confirmation_window.configure(bg="#A8D0E6")

   
    tk.Label(confirmation_window, text="Ticket Confirmation", font=("Arial", 24, "bold"), bg="#3B9A96", fg="white", relief="raised", padx=10, pady=10).pack(pady=20)

    if order:
        tk.Label(confirmation_window, text="Your Ticket(s):", bg="#A8D0E6", font=("Arial", 14, "bold")).pack(pady=5)
        for train in order:
            tk.Label(confirmation_window, text=f"{train['name']} - RS:{train['price']}", bg="#A8D0E6", font=("Arial", 12)).pack(pady=5)

        tk.Label(confirmation_window, text=f"Total Price: RS:{total_price}", bg="#A8D0E6", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(confirmation_window, text=f"Name: {user_name}", bg="#A8D0E6", font=("Arial", 12)).pack(pady=5)
    tk.Label(confirmation_window, text=f"Email: {user_email}", bg="#A8D0E6", font=("Arial", 12)).pack(pady=5)

    confirmation_window.mainloop()


login_page()

