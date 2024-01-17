import os
from cryptography.fernet import Fernet

# Load the key from a file or other source
# with open('key.key', 'rb') as f:
# key = f.read()

found_key = False
while not found_key:
    key = input("Enter the key to decrypt this video: ")
    with open('C:/Users/Jay_s/PycharmProjects/IRP/key.key') as fopen:
        if fopen.read().strip() == key:
            found_key = True
        else:
            print("Incorrect Key, please try again")

found_vid = False
while not found_vid:
    time = input("Enter date and time in the format (day-month-year-hour-minute-second): ")
    folder_name = 'C:/Users/Jay_s/PycharmProjects/IRP/Recorded_Videos/'
    file_name = f'{time}_encrypted.mp4'
    file_path = os.path.join(folder_name, file_name)
    if os.path.exists(file_path):
        found_vid = True
    else:
        print("Video not found, please try again")

# Load the encrypted video file
with open(file_path, 'rb') as f:
    encrypted_data = f.read()

# Create a Fernet object with the key
f = Fernet(key)

# Decrypt the video data
decrypted_data = f.decrypt(encrypted_data)

# Save the decrypted data to a new file
with open(f'C:/Users/Jay_s/PycharmProjects/IRP/Decrypted_Videos/{time}_decrypted.mp4', 'wb') as f:
    f.write(decrypted_data)
