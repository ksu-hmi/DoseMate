import tkinter as tk
from tkinter import ttk
import datetime
import csv
from tkinter import messagebox
import pyttsx3
import dateutil.parser
import sqlite3
from geopy.geocoders import Nominatim # start of SOS integration, Zainab's comment 

def speak_text(command):
    text = pyttsx3.init()
    text.say(command)
    text.runAndWait()

# Constants
MEDICATION_FILE = 'medication.csv'

# Function to load medication data from CSV
def load_medication_data():
    medication_data = []
    with open(MEDICATION_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            medication_data.append(row)
    return medication_data

# Function to display medication information
def display_medication_info():
    medication_data = load_medication_data()
    for row in medication_data:
        label_medication_name = tk.Label(top, text=row, font=("Arial", 12), fg="#FFFFFF", bg="#333333") 
        label_medication_name.pack(pady=10)

# Function to set reminders for medication
def set_medication_reminders():
    medication_data = load_medication_data()
    current_time = datetime.datetime.now().strftime("%H:%M")
    messagebox.showinfo("Medication Reminder", "Reminders have been set.")
    speak_text("Medication reminders have been set.") #Anita

    for row in medication_data:
        medication_name = row[0]
        frequency = row[2]
        schedule_time_str = row[3]

        # Parse the schedule time string to a datetime object
        schedule_time = dateutil.parser.parse(schedule_time_str).strftime("%H:%M")

        if current_time == schedule_time:
            messagebox.showinfo("Medication Reminder", f"It's time to take {medication_name}.")
            print(f"Reminder: Take {medication_name}!") #Anita

# Function to add medication to the schedule
def add_medication_schedule():
    medication_name = entry_medication_name.get()
    dosage = entry_dosage.get()
    frequency = entry_frequency.get()
    schedule_time = entry_schedule_time.get()
    quantity = entry_quantity.get() # Entry field for quantity - Anita 

    # Append the medication schedule to the CSV file
    with open(MEDICATION_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([medication_name, dosage, frequency, schedule_time])
    messagebox.showinfo("Success", "Medication schedule added successfully.")

# Function to get the current location, SOS integration, Zainab's Change 
def get_current_location():
    geolocator = Nominatim(user_agent="med_reminder_app")
    location = geolocator.geocode("Your City, Your Country")  # Replace with default location
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Function to send emergency alert, this feature will include an SOS feature that in case of an emergency can alert designated contacts or even emergency services with the user's location and relevant mewdication, Zainab's change
def send_emergency_alert():
    current_location = get_current_location()
    if current_location:
        latitude, longitude = current_location
        alert_message = f"EMERGENCY! User needs assistance. Location: {latitude}, {longitude}"

        # You can customize this part to send the alert through SMS, email, or any other service.
        # For demonstration purposes, we'll display a messagebox.
        messagebox.showinfo("Emergency Alert", alert_message)
    else:
        messagebox.showwarning("Location Error", "Unable to retrieve current location. Please check your internet connection.") 
        
    
def add_medication():
    top1 = tk.Toplevel()
    top1.title("Add Medication")
    top1.geometry("400x500") #Brianna
    top1.config(bg='#333333')
    top1.after(500, speak_text, "You have selected Add Medication. Please enter your Medication, Dosage, Frequency, schedule time and Quantity.")
    global entry_medication_name
    global entry_dosage
    global entry_frequency
    global entry_schedule_time
    global entry_quantity #Anita


    # Medication Schedule Form
    label_medication_name = tk.Label(top1, text="Medication Name:", font=("Arial", 12), fg="#FFFFFF", bg="#333333")
    label_medication_name.pack(pady=5)
    entry_medication_name = tk.Entry(top1, font=("Arial", 12))
    entry_medication_name.pack(pady=5)

    label_dosage = tk.Label(top1, text="Dosage:", font=("Arial", 12), fg="#FFFFFF", bg="#333333")
    label_dosage.pack(pady=5)
    entry_dosage = tk.Entry(top1, font=("Arial", 12))
    entry_dosage.pack(pady=5)

    label_frequency = tk.Label(top1, text="Frequency:", font=("Arial", 12), fg="#FFFFFF", bg="#333333")
    label_frequency.pack(pady=5)
    entry_frequency = tk.Entry(top1, font=("Arial", 12))
    entry_frequency.pack(pady=5)

    label_schedule_time = tk.Label(top1, text="Schedule Time:", font=("Arial", 12), fg="#FFFFFF", bg="#333333")
    label_schedule_time.pack(pady=5)
    entry_schedule_time = tk.Entry(top1, font=("Arial", 12))
    entry_schedule_time.pack(pady=5)

    button_add_medication = tk.Button(top1, text="Add Medication", command=add_medication_schedule, font=("Arial", 12), fg="#000000", bg="#117A65")
    button_add_medication.pack(pady=5)
    top1.after(500, speak_text, "You have selected Add Medication. Kindly enter your Medication, Dosage, Frequency, and schedule time") #Brianna 
    top1.mainloop()

    label_quantity = tk.Label(top1, text="Quantity:", font=("Arial", 12), fg="#FFFFFF", bg="#333333")
    label_quantity.pack(pady=5)
    entry_quantity = tk.Entry(top1, font=("Arial", 12))
    entry_quantity.pack(pady=5)


def display_medication():
    top = tk.Toplevel()
    top.title("Display Medication Reminder")
    top.geometry("400x500") #Brianna
    top.config(bg='#333333')
    top.after(500, speak_text, "You have clicked on Display Medication successfully.") #Anita

    # Medication Schedule Form
    label_medication_name = tk.Label(top, text='Display Medication', font=("Arial", 16), fg="#FFFFFF", bg="#333333")
    label_medication_name.pack(pady=10)

    label_medication_info_btn = tk.Button(top, text='Click to view Medication', command=display_medication_info, font=("Arial", 12), fg="#000000", bg="#117A65")
    label_medication_info_btn.pack(pady=10)

    top.after(500, speak_text, "You have clicked on Display Medication App successfully")
    top.mainloop()

def delete_medication(medication_id): # Brianna Deletetion of medication 
    # Connect to the SQLite database (replace 'your_database.db' with the actual database file)
    connection = sqlite3.connect('your_database.db')
    cursor = connection.cursor()

    try:
        # Execute the SQL command to delete the medication with the given ID
        cursor.execute('DELETE FROM medications WHERE id = ?', (medication_id,))
        # Commit the changes to the database
        connection.commit()
        print(f'Medication with ID {medication_id} deleted successfully.')
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f'Error deleting medication: {e}')
    finally:
        # Close the database connection
        connection.close()


def close():
    window.destroy()

# Create the main window
window = tk.Tk()
window.title("Med Reminder") #Brianna 
window.geometry("400x500") #Brianna
window.config(bg='#333333')

# Create a label with custom styling
label = tk.Label(window, text="Medication Reminder App", font=("Arial", 20), pady=20, bg='#333333', fg='#FFFFFF')
label.pack()

# Create a styled frame for buttons
button_frame = ttk.Frame(window, padding=20)
button_frame.pack()

# Create three styled buttons vertically aligned
button1 = ttk.Button(button_frame, text="Add Medication", command=add_medication, style="Custom.TButton")
button1.pack(pady=10)

button2 = ttk.Button(button_frame, text="Display Medication", command=display_medication, style="Custom.TButton")
button2.pack(pady=10)

button3 = ttk.Button(button_frame, text="Delete Medication", command= delete_medication, style="Custom.TButton")
button3.pack(pady=10)

button4 = ttk.Button(button_frame, text="Set Reminder", command=set_medication_reminders, style="Custom.TButton")
button4.pack(pady=10)

button5 = ttk.Button(button_frame, text="Quantity", command=add_medication_schedule, style="Custom.TButton")
 #Anita

button6 = ttk.Button(button_frame, text="Exit/Close", command=close, style="Custom.TButton")
button6.pack(pady=10)

# Define custom styling for the buttons
style = ttk.Style()
style.configure("Custom.TButton", font=("Arial", 12), foreground="#000000", background="#117A65", relief="raised")
style.map("Custom.TButton", foreground=[('active', 'red'), ('disabled', 'gray')], background=[('active', '#0E4C3C'), ('disabled', 'gray')])


window.after(500, speak_text, "Welcome to Med Reminder. Explore the capabilities of our cutting-edge Medication Reminder App, providing easy functionalities for adding, displaying, setting reminders, and exiting with ease") #Brianna

# Start the main event loop
window.mainloop()
