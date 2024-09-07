import csv
import os
import random
import speech_recognition as sr
from datetime import datetime

# Define the CSV file path
csv_file_path = 'patients_registration.csv'
# Define the directories for patient records and audio files
patient_records_dir = 'PatientRecords'
audio_dir = 'Audio'

# List of doctors
doctors = ['Dr. Smith','Dr. Johnson','Dr. Williams','Dr. Brown','Dr. Jones']

def ensure_directory_exists(directory):
    """Ensure the directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_csv_if_not_exists(file_path):
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(['ID', 'Name', 'Gender', 'Age', 'Assigned Doctor'])

def add_patient_to_csv(file_path, patient_info):
    """Append a new patient record to the CSV file."""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(patient_info)

def get_patient_info():
    #Collect patient information from the user.
    patient_id = input("Enter Patient ID: ")
    name = input("Enter Name: ")
    gender = input("Enter Gender (M/F/Other): ")
    age = input("Enter Age: ")
    assigned_doctor = random.choice(doctors)
    # Return patient info
    return [patient_id, name, gender, age, assigned_doctor]

def create_patient_record_file(patient_id):
    #Create a CSV file for the patient to record therapy sessions and remarks.
    patient_file_path = os.path.join(patient_records_dir, f'{patient_id}.csv')
    if not os.path.exists(patient_file_path):
        with open(patient_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Session ID', 'Date', 'Doctor', 'Remark'])

def add_therapy_remark(patient_id, session_id, date, remark):
    #Add a remark to a specific therapy session in the patient's record file.
    patient_file_path = os.path.join(patient_records_dir, f'{patient_id}.csv')
    with open(patient_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([session_id, date, random.choice(doctors), remark])

def record_patient_audio(patient_id, session_id):
    #Record audio for a specific therapy session and save it to the patient's folder.s
    # Ensure the directory for patient audio exists
    patient_audio_dir = os.path.join(audio_dir, patient_id)
    ensure_directory_exists(patient_audio_dir)
    
    recognizer = sr.Recognizer()
    # Use only session number and date for the filename
    audio_filename = f"{session_id}_{datetime.now().strftime('%Y%m%d')}.wav"
    audio_file_path = os.path.join(patient_audio_dir, audio_filename)
    if session_id == '0':
        print("Try to say: How are you")
    elif session_id == '1':
        print("Try to say: I went to store.")
    elif session_id == '2':
        print("Try to say: The sun is hot today.")
    elif session_id == '3':
        print("Try to say: It's raining outside right now.")
    elif session_id == '4':
        print("Try to say: They went to park yesterday after dinner.")
    else:
        print("Try and speak: After sometime i will be able to speak fluently.")
    
    # print("Recording audio for session...")
    with sr.Microphone() as source:
        # print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source,duration=2)
        recognizer.energy_threshold = 40
        print("Recording...")
        audio_data = recognizer.record(source, duration=15)  # Record for 15 seconds
        with open(audio_file_path, "wb") as file:
            file.write(audio_data.get_wav_data())
    
    print(f"Audio saved to {audio_file_path}")
    return audio_file_path

def print_interface():
    """Print the application-like interface."""
    os.system('cls')
    print("\n" + "="*40)
    print("Speech Language Therapy System ")
    print("="*40)
    print("1. Register a new patient")
    print("2. Add or edit doctor's remark")
    print("3. View all patients")
    print("4. View patient's remarks")
    print("5. Record patient audio")
    print("6. Exit")
    print("="*40)

def list_patients():
    """List all patients in the main CSV file."""
    if not os.path.exists(csv_file_path):
        print("No patient records found.")
        return

    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        print("\nPatient List:")
        for row in reader:
            print(f"ID: {row[0]}, Name: {row[1]}, Assigned Doctor: {row[4]}")

def view_patient_remarks():
    """View remarks for a specific patient."""
    patient_id = input("Enter the Patient ID to view remarks: ")
    patient_file_path = os.path.join(patient_records_dir, f'{patient_id}.csv')
    
    if not os.path.exists(patient_file_path):
        print("No records found for this patient.")
        return

    with open(patient_file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        print("\n" + "="*40)
        print(f"Remarks for Patient ID: {patient_id}")
        print("="*40)
        for row in reader:
            print(f"Session ID: {row[0]}, Date: {row[1]}, Doctor: {row[2]}, Remark: {row[3]}")
        print("="*40)

def get_patient_id_for_remark():
    patient_id = input("Enter the Patient ID to add or edit remarks: ")
    return patient_id

def get_therapy_details():
    session_id = input("Enter Therapy Session ID: ")
    date = input("Enter Date (YYYY-MM-DD): ")
    remark = input("Enter the doctor's remark: ")
    return session_id, date, remark

def main():
    ensure_directory_exists(patient_records_dir)
    ensure_directory_exists(audio_dir)
    create_csv_if_not_exists(csv_file_path)

    while True:
        print_interface()
        choice = input("Enter your choice: ")

        if choice == '1':
            patient_info = get_patient_info()
            add_patient_to_csv(csv_file_path, patient_info)
            create_patient_record_file(patient_info[0])  # Create a separate file for the patient
            print("\nPatient information saved.")
        elif choice == '2':
            list_patients()
            patient_id = get_patient_id_for_remark()
            session_id, date, remark = get_therapy_details()
            add_therapy_remark(patient_id, session_id, date, remark)
            print("\nDoctor's remark added or updated.")
        elif choice == '3':
            list_patients()
        elif choice == '4':
            view_patient_remarks()
        elif choice == '5':
            patient_id = input("Enter Patient ID to record audio: ")
            session_id = input("Enter Therapy Session ID: ")
            record_patient_audio(patient_id, session_id)
        elif choice == '6':
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, 5, or 6.")

        

if __name__ == "__main__":
    main()
