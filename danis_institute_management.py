import psycopg2
import hashlib
import matplotlib.pyplot as plt

# Database Manager Class
class DatabaseManager:
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Pakaka@132",
            database="Danis"
        )
        self.cur = self.con.cursor()
     
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        self.cur.execute(query, params or ())
        if fetch_one:
            return self.cur.fetchone()
        if fetch_all:
            return self.cur.fetchall()
        self.con.commit()
        return None

    def fetch_data(self, query, params=None):
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def close_connection(self):
        self.cur.close()
        self.con.close()

# Base User Class
class User:
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role

    def view_profile(self):
        print(f"\nUser ID: {self.user_id}, Username: {self.username}, Role: {self.role}")

#faculty class
class Faculty(User):
    
    def remove_student(self, student_id):
        db = DatabaseManager()
        try:
            query = "DELETE FROM student WHERE student_id = %s"
            db.execute_query(query, (student_id,))
            print(f"Student ID {student_id} removed.")
        except Exception as e:
            print("Failed to remove :", e)
        finally:
            db.close_connection()


    def update_student(self, new_name, student_id):
        db = DatabaseManager()
        try:
            query = "UPDATE student SET name = %s WHERE student_id = %s"
            db.execute_query(query, (new_name, student_id))
            print(f"Student ID {student_id} name updated.")
        except Exception as e:
            print("Failed to update name:", e)
        finally:
            db.close_connection() 

    def view_student_marks(self, student_id):
        db = DatabaseManager()
        query = "SELECT subject, marks FROM marks WHERE student_id = %s"
        data = db.fetch_data(query, (student_id,))
        print(f"\nMarks for Student ID {student_id}:")
        for subject, marks in data:
            print(f"{subject}: {marks}")
        db.close_connection()

    def view_student(self):
        db = DatabaseManager()
        query = "SELECT * FROM student"
        data = db.fetch_data(query)
        print("\n---student List ---")
        for row in data:
            print(f"ID: {row[0]}, Name: {row[1]}")
        db.close_connection()

    def insert_student_marks(self, subject, marks, student_id):
        db = DatabaseManager()
        query = "INSERT into marks (subject, marks, student_id) VALUES (%s, %s, %s)"
        db.execute_query(query, (subject, marks, student_id))
        print(f"Student ID {student_id} marks inserted.")
        db.close_connection()
        
    def update_student_marks(self, marks, subject, student_id):
        db = DatabaseManager()
        try:
            query = "UPDATE marks set marks = %s where subject = %s AND student_id = %s"
            db.execute_query(query, (marks, subject, student_id))
            print(f"Student ID {student_id} marks updated.")
        except Exception as e:
            print("Failed to update marks:", e)
        finally:
            db.close_connection() 

# Principal Class
class Principal(Faculty):
    def __init__(self, user_id, username, role):
        super().__init__(user_id, username, role)
        
    def update_salary(self, faculty_id, new_salary):
        db = DatabaseManager()
        try:
            query = "UPDATE faculty SET salary = %s WHERE faculty_id = %s"
            db.execute_query(query, (new_salary, faculty_id))
            print(f"Salary updated for Faculty ID: {faculty_id}")
        except Exception as e:
            print("Failed to update salary:", e)
        finally:
            db.close_connection() 

    def remove_faculty(self, faculty_id):
        db = DatabaseManager()
        try:
            query = "DELETE FROM faculty WHERE faculty_id = %s"
            db.execute_query(query, (faculty_id,))
            print(f"Faculty ID {faculty_id} removed.")
        except Exception as e:
            print("Failed to remove faculty:", e)
        finally:
            db.close_connection()

    def view_faculty(self):
        db = DatabaseManager()
        query = "SELECT * FROM faculty"
        data = db.fetch_data(query)
        print("\n--- Faculty List ---")
        for row in data:
            print(f"ID: {row[0]}, Name: {row[1]}, Salary: {row[2]}")
        db.close_connection()

# Student Class
class Student(User):
    def view_marks(self):
        
        subjects1 = []
        marks1 = []
        
        db = DatabaseManager()
        query = "SELECT subject, marks FROM marks WHERE student_id = %s"
        data = db.fetch_data(query, (self.user_id,))

        if not data:
            print(f"No marks found for Student ID {student_id}.")
            return
            
        print("\nYour Marks:")
        for subject, marks in data:
            print(f"{subject}: {marks}")
            subjects1.append(subject)
            marks1.append(marks)
        
        # Plotting the graph
        plt.figure(figsize=(7, 3))
        plt.bar(subjects1, marks1, color='green')
        plt.xlabel('Subjects')
        plt.ylabel('Marks')
        plt.title(f'Marks for Student ID {self.user_id}')
        plt.show()
        db.close_connection()

# Authentication Class
class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, username, password):
        hashed_password = self.hash_password(password)
        query = "SELECT user_id, role_id FROM users WHERE username = %s AND password = %s"
        result = self.db.fetch_data(query, (username, hashed_password))
        if result:
            user_id, role = result[0]
            print("Login Successful!")
            return self.create_user_instance(user_id, username, role)
        else:
            print("Invalid Credentials.")
            return None

    def create_user_instance(self, user_id, username, role):
        role_map = {
            1: 'Principal',
            2: 'Faculty',
            3: 'Student'
        }
        role_name = role_map.get(role)
        
        if role_name == 'Principal':
            return Principal(user_id, username, role_name)
        elif role_name == 'Faculty':
            if user_id == "38":
                return Principal(user_id, username, role_name)
            else:
                return Faculty(user_id, username, role_name)
                
        elif role_name == 'Student':
            return Student(user_id, username, role_name)
        else:
            return None

    def register_user(self, username, password, role):
        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (username, password, role_id) VALUES (%s, %s, %s) RETURNING user_id"
        self.db.execute_query(query, (username, hashed_password, role))
        print("User registered successfully.")
        
        # Fetch the newly created user ID
        query = "SELECT user_id FROM users WHERE username = %s"
        result = self.db.fetch_data(query, (username,))
        
        if result:
            user_id = result[0][0]
            return self.create_user_instance(user_id, username, int(role))
        else:
            print("Registration failed.")
            return None


# Menus for each role
def principal_menu(principal):
    while True:
        print("\n--- Principal Menu ---")
        print("1. add any user")
        print("2. View All Faculty")
        print("3. Update Faculty Salary")
        print("4. Remove Faculty")
        print("5. view all student")
        print("6. update student name")  
        print("7. view student marks")
        print("8. insert student marks")
        print("9. update student marks")
        print("10. remove student")
        print("11. Exit")
        choice = input("Enter choice: ")

        auth_manager = AuthManager()
        
        if choice == "1":
            role = input("Enter Role \n (1) for admin \n (2) for Faculty \n (3) for Student: ")
            auth_manager = AuthManager()  # Create an instance of AuthManager
            
            if role == "1":
                username = input("Enter New Principal Username: ")
                    
                while True:
                    password = input("Enter Password (at least 5 characters): ").strip()
                    if len(password) >= 5:
                        break
                    print("Password must be at least 5 characters long.")
                        
                hashed_password = auth_manager.hash_password(password)
                    
                # Register the Principal in the users table
                db = DatabaseManager()
                query = "INSERT INTO users (username, password, role_id) VALUES (%s, %s, %s)"
                db.execute_query(query, (username, hashed_password, 1))
                print("New Principal added successfully.")
                
            elif role == "2":
                username = input("Enter Username: ")
                while(True):
                    password = input("enter password (atleast 5 characters)").strip()
                    if len(password) >= 5:
                        break
                    print("password must be atleast 5 char long")
                salary = int(input("Enter Salary: "))
        
                # Hash the password
                hashed_password = auth_manager.hash_password(password)
                
                # Register the user in the users table
                db = DatabaseManager()  # Create an instance of DatabaseManager
                user_query = "INSERT INTO users (username, password,role_id) VALUES (%s, %s, %s) RETURNING user_id"
                user_id = db.execute_query(user_query, (username, hashed_password, role), fetch_one=True)[0]
        
                # Now link the user to the faculty table
                faculty_query = "INSERT INTO faculty (faculty_id, name, salary) VALUES (%s, %s, %s)"
                db.execute_query(faculty_query, (user_id, username, salary))
                
                print("Faculty registered successfully.")

            elif role == "3":
                username = input("Enter Username: ")
                while(True):
                    password = input("enter password (atleast 5 characters)").strip()
                    if len(password) >= 5:
                        break
                    print("password must be atleast 5 char long")
        
                # Hash the password
                hashed_password = auth_manager.hash_password(password)

                # to register and  Create an instance of DatabaseManager
                db = DatabaseManager() 
                user_query = "INSERT INTO users (username, password,role_id) VALUES (%s, %s, %s) RETURNING user_id"
                user_id = db.execute_query(user_query, (username, hashed_password, role), fetch_one=True)[0]
        
                # Now link the user to the faculty table
                faculty_query = "INSERT INTO student (student_id, name) VALUES (%s, %s)"
                db.execute_query(faculty_query, (user_id, username))
                
                print("Student registered successfully.")
        elif choice == "2":
            principal.view_faculty()
        elif choice == "3":
            faculty_id = input("Enter Faculty ID: ")
            new_salary = input("Enter New Salary: ")
            principal.update_salary(faculty_id, new_salary)
        elif choice == "4":
            faculty_id = input("Enter Faculty ID: ")
            principal.remove_faculty(faculty_id)
        elif choice == "5":
            principal.view_student()
        elif choice == "6":
            student_id = input("Enter Student ID: ")
            new_name = input("enter new name od student")
            principal.update_student(new_name,student_id)
        elif choice == "7":
            student_id = input("Enter Student ID: ")
            principal.view_student_marks(student_id)
        elif choice == "8":
            subject = input("enter subject")
            marks = input("enter marks")
            student_id = input("Enter Student ID: ")
            principal.insert_student_marks(subject,marks,student_id)
        elif choice == "9":
            marks = input("enter marks")
            subject = input("enter subject")
            student_id = input("Enter Student ID: ")
            principal.update_student_marks(marks, subject, student_id)
        elif choice == "10":
            student_id = input("Enter Student ID: ")
            principal.remove_student(student_id)
        elif choice == "11":
            print("thank you bye..")
            break
        else:
            print("Invalid choice. Try again.")
            
def faculty_menu(faculty):
    while True:
        print("\n--- Faculty Menu ---")
        print("1. View All Students")
        print("2. View Student Marks")
        print("3. Update Student Name")
        print("4. insert student marks")
        print("5. update student marks")
        print("6. Remove Student")
        print("7. Logout") 
        choice = input("Enter choice: ")
        
        if choice == "1":
            faculty.view_student()
        elif choice == "2":
            student_id = input("Enter Student ID: ")
            faculty.view_student_marks(student_id)
        elif choice == "3":
            student_id = input("Enter Student ID: ")
            new_name = input("Enter New Name of Student: ")
            faculty.update_student(new_name,student_id)
        elif choice == "4":
            subject = input("enter subject")
            marks = input("enter marks")
            student_id = input("Enter Student ID: ")
            faculty.insert_student_marks(subject,marks,student_id)
        elif choice == "5":
            marks = input("enter marks")
            subject = input("enter subject")
            student_id = input("Enter Student ID: ")
            faculty.update_student_marks(marks, subject, student_id)
        elif choice == "6":
            student_id = input("Enter Student ID: ")
            faculty.remove_student(student_id)
        elif choice == "7":
            print("Logging out...")  # Message for Logout
            break  # Exits the menu loop
        else:
            print("Invalid choice. Try again.")
            
def student_menu(student):
    while True:
        print("\n---Student Menu ---")
        print("1. view your marks")
        print("2. exit")
        choice = input("Enter choice: ")
      
        if choice == "1":
            student.view_marks()
        elif choice == "2":
            print("thank you bye..")
            break
        else:
            print("Invalid choice. Try again.")

# Main Program Flow
def main():
    auth_manager = AuthManager()
    print("1. Login \n2. Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        user = auth_manager.authenticate_user(username, password)
        
        if isinstance(user, Principal):
            principal_menu(user)
        elif isinstance(user, Faculty):
            faculty_menu(user)
        elif isinstance(user, Student):
            student_menu(user)
        else:
            print("Access Denied or Role Not Implemented Yet.")

    elif choice == "2":
        print("Exiting. Thank you!")

if __name__ == "__main__":
    main()