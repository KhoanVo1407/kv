import happybase

connection = happybase.Connection('172.17.0.2')
table = connection.table('People')

#Create
def create_user(index, user_id, first_name, last_name, sex, email, phone, dob, job_title):
    row_key = str(index)
    if table.row(row_key):
        print(f"User with Index {index} already exists.")
        return
    
    user_data = {
        'info:user_id': user_id,
        'info:first_name': first_name,
        'info:last_name': last_name,
        'info:sex': sex,
        'info:email': email,
        'info:phone': phone,
        'info:dob': dob,
        'info:job_title': job_title
    }
    table.put(row_key, user_data)
    print(f"User {first_name} {last_name} added successfully.")

#Read
def read_user(index=None):
    if index:
        row = table.row(str(index))
        if row:
            print_user(index, row)
        else:
            print(f"No user found with Index {index}")
    else:
        users = [(int(key.decode("utf-8")), data) for key, data in table.scan()]
        sorted_users = sorted(users, key=lambda x: x[0])

        for user_index, user_data in sorted_users:
            print_user(user_index, user_data)

def print_user(index, data):
    print(f"\nIndex: {index},")
    print(f"User ID: {data.get(b'info:user_id', b'').decode('utf-8')},")
    print(f"First Name: {data.get(b'info:first_name', b'').decode('utf-8')},")
    print(f"Last Name: {data.get(b'info:last_name', b'').decode('utf-8')},")
    print(f"Sex: {data.get(b'info:sex', b'').decode('utf-8')},")
    print(f"Email: {data.get(b'info:email', b'').decode('utf-8')},")
    print(f"Phone: {data.get(b'info:phone', b'').decode('utf-8')},")
    print(f"DOB: {data.get(b'info:dob', b'').decode('utf-8')},")
    print(f"Job Title: {data.get(b'info:job_title', b'').decode('utf-8')}\n")
#Update
def update_user(index, **kwargs):
    row_key = str(index)
    if not table.row(row_key):
        print(f"No user found with Index {index}")
        return

    user_data = {f"info:{k}": v for k, v in kwargs.items()}
    table.put(row_key, user_data)
    print(f"User with Index {index} updated successfully.")

#Delete
def delete_user(index):
    table.delete(str(index))
    print(f"User with Index {index} deleted successfully.")

#Menu
def main():
    while True:
        print("\n--- HBase User Management ---")
        print("1. Add User")
        print("2. View User")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            index = input("Index: ")
            user_id = input("User ID: ")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            sex = input("Sex: ")
            email = input("Email: ")
            phone = input("Phone: ")
            dob = input("Date of Birth: ")
            job_title = input("Job Title: ")
            create_user(index, user_id, first_name, last_name, sex, email, phone, dob, job_title)

        elif choice == '2':
            view_choice = input("Choose to (1) View a single user or (2) View all users: ")

            if view_choice == '1':
                user_index = input("Enter User Index to view: ")
                read_user(user_index)
            elif view_choice == '2':
                read_user()
            else:
                print("Invalid choice. Please choose either 1 or 2.")

        elif choice == '3':
            index = input("Enter User Index to update: ")
            print("Enter new values (leave blank to keep unchanged):")
            user_id = input("User ID: ")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            sex = input("Sex: ")
            email = input("Email: ")
            phone = input("Phone: ")
            dob = input("Date of Birth: ")
            job_title = input("Job Title: ")

            update_data = {k: v for k, v in {
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'sex': sex,
                'email': email,
                'phone': phone,
                'dob': dob,
                'job_title': job_title
            }.items() if v}

            update_user(index, **update_data)

        elif choice == '4':
            index = input("Enter User Index to delete: ")
            delete_user(index)

        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

    connection.close()

if __name__ == "__main__":
    main()
