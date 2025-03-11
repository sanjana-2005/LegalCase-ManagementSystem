import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Global variables
username = "admin"
password = "admin"

# Define entry_fields globally
entry_fields = {}

# Function to validate login credentials
def validate_login():
    entered_username = username_entry.get()
    entered_password = password_entry.get()
    
    if entered_username == username and entered_password == password:
        # If login successful, destroy login window and open data entry window
        login_window.destroy()
        open_data_entry_window()
    else:
        messagebox.showerror("Error", "Invalid username or password")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

# Function to submit data to MySQL..
def submit_data():
    try:
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="manager",
            database="case"
        )
        cursor = mydb.cursor()

        # Retrieve data from entry fields
        client_id = entry_fields["client_id"].get()
        first_name = entry_fields["first_name"].get()
        last_name = entry_fields["last_name"].get()
        client_contact = entry_fields["client'scontact"].get()
        attorney_id = entry_fields["attorney_id"].get()
        assigned_cases = entry_fields["assigned_cases"].get()
        attorney_contact = entry_fields["attorney'scontact"].get()
        court_id = entry_fields["court_id"].get()
        location = entry_fields["location"].get()
        assigned_judges = entry_fields["assigned_judges"].get()
        name = entry_fields["name"].get()
        case_id = entry_fields["case_id"].get()
        title = entry_fields["title"].get()
        hearing_dates = entry_fields["hearing_dates"].get()
        log_id = entry_fields["log_id"].get()
        evidence_id = entry_fields["evidence_id"].get()
        description = entry_fields["description"].get()
        photo = entry_fields["photo"].get()
        video = entry_fields["video"].get()
        date_obtained = entry_fields["date_obtained"].get()
        appeal_id = entry_fields["appeal_id"].get()
        status = entry_fields["status"].get()
        id = entry_fields["id"].get()
        terms = entry_fields["terms"].get()
        settlement = entry_fields["settlement"].get()
        settlement_details = entry_fields["settlement_details"].get()
        verdict_date = entry_fields["verdict_date"].get()

        # Insert data into MySQL tables
        cursor.execute("INSERT INTO client_files (client_id, first_name, last_name) VALUES (%s, %s, %s)", (client_id, first_name, last_name))
        cursor.execute("INSERT INTO clientnew (client_id, contact) VALUES (%s, %s)", (client_id, client_contact))
        cursor.execute("INSERT INTO attorney (attorney_id, first_name, last_name, assigned_cases, client_id) VALUES (%s, %s, %s, %s, %s)", (attorney_id, first_name, last_name, assigned_cases, client_id))
        cursor.execute("INSERT INTO attorneynew (attorney_id, contact) VALUES (%s, %s)", (attorney_id, attorney_contact))
        cursor.execute("INSERT INTO worksfor (client_id, attorney_id) VALUES (%s, %s)", (client_id, attorney_id))
        cursor.execute("INSERT INTO court (court_id, location, assigned_judges, name) VALUES (%s, %s, %s, %s)", (court_id, location, assigned_judges, name))
        cursor.execute("INSERT INTO case_conductedin (case_id, court_id, client_id, attorney_id, title) VALUES (%s, %s, %s, %s, %s)", (case_id, court_id, client_id, attorney_id, title))
        cursor.execute("INSERT INTO casenew (case_id, hearing_dates) VALUES (%s, %s)", (case_id, hearing_dates))
        cursor.execute("INSERT INTO hearning_includes (log_id, case_id, court_id) VALUES (%s, %s, %s)", (log_id, case_id, court_id))
        cursor.execute("INSERT INTO evidence_presentedwith (evidence_id, description, photo, video, date_obtained, case_id) VALUES (%s, %s, %s, %s, %s, %s)", (evidence_id, description, photo, video, date_obtained, case_id))
        cursor.execute("INSERT INTO documents_submittedwith (doc_id, case_id, contents, evidence_id) VALUES (%s, %s, %s, %s)", (id, case_id, description, evidence_id))
        cursor.execute("INSERT INTO appeal_on (appeal_id, case_id, status) VALUES (%s, %s, %s)", (appeal_id, case_id, status))
        cursor.execute("INSERT INTO grounds_on (id, terms, appeal_id) VALUES (%s, %s, %s)", (id, terms, appeal_id))
        cursor.execute("INSERT INTO verdict_leadsto (settlement, settlement_details, verdict_date, log_id) VALUES (%s, %s, %s, %s)", (settlement, settlement_details, verdict_date, log_id))

        mydb.commit()

        # Notify user that data has been submitted
        messagebox.showinfo("Success", "Data has been submitted successfully!")
    except mysql.connector.Error as error:
        # Rollback transaction on error
        mydb.rollback()
        messagebox.showerror("Error", f"Failed to insert data into MySQL: {error}")
    finally:
        # Close database connection
        mydb.close()

# Function to reset the form
def reset_form():
    for entry_field in entry_fields.values():
        entry_field.delete(0, 'end')

# Function to handle pressing Enter key
def on_enter(event):
    # Focus on the next entry field
    current_entry = data_entry_window.focus_get()
    current_index = list(entry_fields.values()).index(current_entry)
    next_index = (current_index + 1) % len(entry_fields)
    next_entry = list(entry_fields.values())[next_index]
    next_entry.focus()
    # If the last entry field is reached, submit the form
    if next_index == 0:
        submit_data()

# Function to open the data entry window
def open_data_entry_window():
    global data_entry_window
    data_entry_window = tk.Tk()
    data_entry_window.title("Data Entry")
    data_entry_window.configure(bg="skyblue")  # Set background color to sky blue

    # Create a canvas
    canvas = tk.Canvas(data_entry_window, bg="skyblue")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(data_entry_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the entry fields
    frame = ttk.Frame(canvas, style="My.TFrame")
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    # Function to resize the canvas scroll region
    def resize(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Bind the resize function to the frame and canvas
    frame.bind("<Configure>", resize)
    canvas.bind("<Configure>", resize)

    # Add labels and entry fields to the frame
    label_names_left = ["client_id", "first_name", "last_name", "client'scontact", "attorney_id", "assigned_cases", "attorney'scontact", "court_id", "location", "assigned_judges", "name", "case_id", "title", "hearing_dates", "log_id"]
    label_names_right = ["evidence_id", "description", "photo", "video", "date_obtained", "appeal_id", "status", "id", "terms", "settlement", "settlement_details", "verdict_date"]

    for idx, label_name in enumerate(label_names_left):
        ttk.Label(frame, text=label_name, style="My.TLabel").grid(row=idx, column=0, padx=10, pady=10, sticky="e")
        entry_fields[label_name] = ttk.Entry(frame, font=("Helvetica", 16))
        entry_fields[label_name].grid(row=idx, column=1, padx=10, pady=10, sticky="ew")
        # Bind Enter key to on_enter function for each entry field
        entry_fields[label_name].bind("<Return>", on_enter)

    for idx, label_name in enumerate(label_names_right):
        ttk.Label(frame, text=label_name, style="My.TLabel").grid(row=idx, column=2, padx=10, pady=10, sticky="e")
        entry_fields[label_name] = ttk.Entry(frame, font=("Helvetica", 16))
        entry_fields[label_name].grid(row=idx, column=3, padx=10, pady=10, sticky="ew")
        # Bind Enter key to on_enter function for each entry field
        entry_fields[label_name].bind("<Return>", on_enter)

    # Function to submit data
    submit_button = ttk.Button(data_entry_window, text="Submit", command=submit_data, style="My.TButton", cursor="hand2")
    submit_button.pack(side=tk.BOTTOM, padx=10, pady=5, fill=tk.X)

    # Function to reset the form
    reset_button = ttk.Button(data_entry_window, text="Reset", command=reset_form, style="My.TButton", cursor="hand2")
    reset_button.pack(side=tk.BOTTOM, padx=10, pady=5, fill=tk.X)

    # Bind arrow keys and mouse scroll event for canvas scrolling
    data_entry_window.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta/120), "units"))
    data_entry_window.bind_all("<Up>", lambda event: canvas.yview_scroll(-1, "units"))
    data_entry_window.bind_all("<Down>", lambda event: canvas.yview_scroll(1, "units"))

    # Center the window on the screen
    window_width = data_entry_window.winfo_reqwidth()
    window_height = data_entry_window.winfo_reqheight()
    position_right = int(data_entry_window.winfo_screenwidth()/2 - window_width/2)
    position_down = int(data_entry_window.winfo_screenheight()/2 - window_height/2)
    data_entry_window.geometry("+{}+{}".format(position_right, position_down))

    data_entry_window.mainloop()

# Create login window
login_window = tk.Tk()
login_window.title("Login")
login_window.configure(bg="purple")  # Set background color to purple

window_width = 400
window_height = 200
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
x_coordinate = (screen_width/2) - (window_width/2)
y_coordinate = (screen_height/2) - (window_height/2)
login_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Add label above the username field
label_title = ttk.Label(login_window, text="LEGAL CASE MANAGEMENT SYSTEM", style="My.TLabel", font=("Helvetica", 16))
label_title.pack(pady=10)

# Username label and entry
frame = ttk.Frame(login_window, style="My.TFrame")
frame.pack(pady=10)

username_label = ttk.Label(frame, text="Username:", style="My.TLabel")
username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

username_entry = ttk.Entry(frame, font=("Helvetica", 14), style="My.TEntry")
username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Password label and entry
password_label = ttk.Label(frame, text="Password:", style="My.TLabel")
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

password_entry = ttk.Entry(frame, show="*", font=("Helvetica", 14), style="My.TEntry")
password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Login button
login_button = ttk.Button(frame, text="Login", command=validate_login, style="My.TButton", cursor="hand2")
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Function to create MySQL tables
def create_tables():
    try:
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="manager",
            database="case"
        )
        cursor = mydb.cursor()

        # Start transaction
        cursor.execute("START TRANSACTION")

        # Create SQL table queries
        table_queries = ["""CREATE TABLE IF NOT EXISTS client_files (
                client_id INT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50)
            )""",
            """CREATE TABLE IF NOT EXISTS clientnew (
                client_id INT PRIMARY KEY,
                contact BIGINT(10)
            )""",
            """CREATE TABLE IF NOT EXISTS attorney (
                attorney_id INT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                contact BIGINT(10),
                assigned_cases VARCHAR(500),
                client_id INT,
                FOREIGN KEY (client_id) REFERENCES client_files(client_id)
            )""",
            """CREATE TABLE IF NOT EXISTS attorneynew (
                attorney_id INT PRIMARY KEY,
                contact BIGINT(10)
            )""",
            """CREATE TABLE IF NOT EXISTS worksfor (
                client_id INT,
                attorney_id INT,
                FOREIGN KEY (client_id) REFERENCES client_files(client_id),
                FOREIGN KEY (attorney_id) REFERENCES attorney(attorney_id)
            )""",
            """CREATE TABLE IF NOT EXISTS court (
                court_id INT PRIMARY KEY,
                location VARCHAR(50),
                assigned_judges VARCHAR(50),
                name VARCHAR(50)
            )""",
            """CREATE TABLE IF NOT EXISTS case_conductedin (
                case_id INT PRIMARY KEY,
                court_id INT,
                client_id INT,
                attorney_id INT,
                title VARCHAR(100),
                FOREIGN KEY (court_id) REFERENCES court(court_id),
                FOREIGN KEY (client_id) REFERENCES client_files(client_id),
                FOREIGN KEY (attorney_id) REFERENCES attorney(attorney_id)
            )""",
            """CREATE TABLE IF NOT EXISTS casenew (
                case_id INT PRIMARY KEY,
                hearing_dates DATE
            )""",
            """CREATE TABLE IF NOT EXISTS hearning_includes (
                log_id INT PRIMARY KEY,
                case_id INT,
                court_id INT,
                FOREIGN KEY (case_id) REFERENCES case_conductedin(case_id),
                FOREIGN KEY (court_id) REFERENCES court(court_id)
            )""",
            """CREATE TABLE IF NOT EXISTS evidence_presentedwith (
                evidence_id INT PRIMARY KEY,
                description VARCHAR(500),
                photo VARCHAR(50),
                video VARCHAR(50),
                date_obtained DATE,
                case_id INT,
                FOREIGN KEY (case_id) REFERENCES case_conductedin(case_id)
            )""",
            """CREATE TABLE IF NOT EXISTS documents_submittedwith (
                doc_id INT PRIMARY KEY,
                case_id INT,
                contents VARCHAR(500),
                evidence_id INT,
                FOREIGN KEY (case_id) REFERENCES case_conductedin(case_id),
                FOREIGN KEY (evidence_id) REFERENCES evidence_presentedwith(evidence_id)
            )""",
            """CREATE TABLE IF NOT EXISTS appeal_on (
                appeal_id INT PRIMARY KEY,
                case_id INT,
                status VARCHAR(200),
                FOREIGN KEY (case_id) REFERENCES case_conductedin(case_id)
            )""",
            """CREATE TABLE IF NOT EXISTS grounds_on (
                id INT PRIMARY KEY,
                terms VARCHAR(200),
                appeal_id INT,
                FOREIGN KEY (appeal_id) REFERENCES appeal_on(appeal_id)
            )""",
            """CREATE TABLE IF NOT EXISTS verdict_leadsto (
                settlement VARCHAR(600),
                settlement_details VARCHAR(200),
                verdict_date DATE,
                log_id INT,
                FOREIGN KEY (log_id) REFERENCES hearning_includes(log_id)
            )"""
            # SQL table creation queries here...
        ]

        # Execute table creation queries
        for query in table_queries:
            cursor.execute(query)

        # Commit transaction
        mydb.commit()

        # Notify user that tables have been created
        messagebox.showinfo("Success", "Database tables have been created successfully!")
    except mysql.connector.Error as error:
        # Rollback transaction on error
        mydb.rollback()
        messagebox.showerror("Error", f"Failed to create tables in MySQL: {error}")
    finally:
        # Close database connection
        mydb.close()

# Function to create tables
create_tables_button = ttk.Button(frame, text="Create Tables", command=create_tables, style="My.TButton", cursor="hand2")
create_tables_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Style settings
style = ttk.Style()
style.configure("My.TButton", background="lightblue", foreground="black", font=("Helvetica", 14))
style.configure("My.TLabel", foreground="black", font=("Helvetica", 14))  # Removed background color
style.configure("My.TEntry", fieldbackground="white", borderwidth=2, relief="solid", padding=(10, 10))
style.configure("My.TFrame", background="white", borderwidth=2, relief="solid", padding=(20, 20))  # Set frame color to white

# Center the login window on the screen
window_width = login_window.winfo_reqwidth()
window_height = login_window.winfo_reqheight()
position_right = int(login_window.winfo_screenwidth()/2 - window_width/2)
position_down = int(login_window.winfo_screenheight()/2 - window_height/2)
login_window.geometry("+{}+{}".format(position_right, position_down))

login_window.mainloop()
