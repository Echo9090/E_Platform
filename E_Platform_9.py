from abc import ABC, abstractmethod
import uuid
import json
import os

SAVE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Case3_json")

# Ensure the folder exists
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
print("Save folder initialized at:", SAVE_FOLDER)


print("Current Working Directory:", os.getcwd())


def load_json(filename):
    """
    Load JSON data from a file in SAVE_FOLDER.
    Handles file not existing or corrupted JSON gracefully.
    """
    filepath = os.path.join(SAVE_FOLDER, filename)
    if not os.path.exists(filepath):
        print(f"DEBUG: {filename} not found. Returning an empty list.")
        return []
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to decode {filename}. Error: {e}")
        return []
    except Exception as e:
        print(f"ERROR: Unexpected error loading {filename}. Error: {e}")
        return []

def save_json(filename, data):
    """
    Save JSON data to a file in SAVE_FOLDER.
    Handles any file-writing issues gracefully.
    """
    filepath = os.path.join(SAVE_FOLDER, filename)
    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
        print(f"DEBUG: Data successfully saved to {filepath}.")
    except Exception as e:
        print(f"ERROR: Failed to save data to {filename}. Error: {e}")



# Base Abstract Class: Person
class Person(ABC):
    def __init__(self, first_name, last_name, age, sex, birthdate, place_of_birth):
        self._id = self._generate_id()
        self._first_name = first_name
        self._last_name = last_name
        self._age = age
        self._sex = sex
        self._birthdate = birthdate
        self._place_of_birth = place_of_birth

    @abstractmethod
    def display_profile(self):
        pass

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())

    def __str__(self):
        return f"ID: {self._id}, Name: {self._first_name} {self._last_name}"
    
    def to_dict(self):
        """
        Converts the common Person attributes into a dictionary.
        """
        return {
            "id": self._id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "age": self._age,
            "sex": self._sex,
            "birthdate": self._birthdate,
            "place_of_birth": self._place_of_birth,
            "email": self.email,
            "password": self.password,
        }

# Subclass: Student
class Student(Person):
    def __init__(self, first_name, last_name, age, sex, birthdate, place_of_birth):
        super().__init__(first_name, last_name, age, sex, birthdate, place_of_birth)
        self._id = UserManager._generate_user_id("Student")  # Consistent ID
        self._enrolled_courses = []

    def enroll(self, course):
        self._enrolled_courses.append(course)

    def view_courses(self):
        return [course.name for course in self._enrolled_courses]

    def display_profile(self):
        enrolled_courses = (
            ", ".join(course._name for course in self._enrolled_courses)
            if self._enrolled_courses
            else "None"
        )
        print(f"Student Profile:\n"
              f"ID: {self._id}\n"
              f"Name: {self._first_name} {self._last_name}\n"
              f"Age: {self._age}\n"
              f"Sex: {self._sex}\n"
              f"Birthdate: {self._birthdate}\n"
              f"Place of Birth: {self._place_of_birth}\n"
              f"Email: {self.email}\n"
              f"Password: {self.password}\n"
              f"Enrolled Courses: {enrolled_courses}")
    
    # New JSON Deserialization Method
    def to_dict(self):
        """
        Converts the Student object into a dictionary for JSON serialization.
        """
        return {
            **super().to_dict(),
            "type": "Student",
            "enrolled_courses": [course._course_id for course in self._enrolled_courses]
        }

    @staticmethod
    def from_dict(data):
        """
        Rebuilds a Student object from a dictionary.
        """
        student = Student(
            data["first_name"],
            data["last_name"],
            data["age"],
            data["sex"],
            data["birthdate"],
            data["place_of_birth"]
        )
        student._id = data["id"]
        student.email = data.get("email", "")
        student.password = data.get("password", "")
        student._enrolled_courses = []  # Link courses after loading
        return student
    
    @classmethod
    def motivation_assignment(cls):
        """Motivation related to assignments."""
        print("\n📘 Don't procrastinate! Start your assignment today and give it your best shot!")

    @classmethod
    def motivation_exams(cls):
        """Motivation related to exams."""
        print("\n📖 Study hard, but don't forget to take breaks. You've got this!")

    @classmethod
    def motivation_grades(cls):
        """Motivation related to grades."""
        print("\n🎓 Grades are not the destination but part of the journey. Keep learning!")

    @classmethod
    def motivation_progress(cls):
        """Motivation about personal progress."""
        print("\n🚀 Every day is a new chance to improve yourself. Take it one step at a time!")

    @classmethod
    def motivation_balance(cls):
        """Motivation about balancing studies and personal life."""
        print("\n🧘‍♀️ Balance is key! Don't forget to take care of your mental and physical health.")

    @classmethod
    def motivation_teamwork(cls):
        """Motivation about teamwork and collaboration."""
        print("\n🤝 Collaboration makes us stronger. Share, learn, and grow together!")

# Subclass: Instructor
class Instructor(Person):
    def __init__(self, first_name, last_name, age, sex, birthdate, place_of_birth):
        super().__init__(first_name, last_name, age, sex, birthdate, place_of_birth)
        self._id = UserManager._generate_user_id("Instructor")  # Consistent ID
        self._assigned_courses = []

    def assign_course(self, course):
        if course not in self._assigned_courses:
            self._assigned_courses.append(course)


    def view_courses(self):
        return [course.name for course in self._assigned_courses]

    def display_profile(self):
        assigned_courses = (
            ", ".join(course._name for course in self._assigned_courses)
            if self._assigned_courses
            else "None"
        )
        print(f"Instructor Profile:\n"
              f"ID: {self._id}\n"
              f"Name: {self._first_name} {self._last_name}\n"
              f"Age: {self._age}\n"
              f"Sex: {self._sex}\n"
              f"Birthdate: {self._birthdate}\n"
              f"Place of Birth: {self._place_of_birth}\n"
              f"Email: {self.email}\n"
              f"Password: {self.password}\n"
              f"Assigned Courses: {assigned_courses}")
    
    def to_dict(self):
        """
        Converts the Instructor object into a dictionary for JSON serialization.
        """
        return {
            **super().to_dict(),
            "type": "Instructor",
            "assigned_courses": [course._course_id for course in self._assigned_courses],
        }

    @staticmethod
    def from_dict(data):
        """
        Rebuilds an Instructor object from a dictionary.
        """
        instructor = Instructor(
            data["first_name"],
            data["last_name"],
            data["age"],
            data["sex"],
            data["birthdate"],
            data["place_of_birth"],
        )
        instructor._id = data["id"]
        instructor.email = data.get("email", "")
        instructor.password = data.get("password", "")
        instructor._assigned_courses = []  # Link courses after loading
        return instructor
    
    @classmethod
    def motivation_teaching(cls):
        """Motivation about the teaching profession."""
        print("\n📚 Teaching is an art. Your knowledge empowers generations!")

    @classmethod
    def motivation_students(cls):
        """Motivation about working with students."""
        print("\n🎓 Every student you guide today will make a difference tomorrow. Keep inspiring!")

    @classmethod
    def motivation_grading(cls):
        """Motivation about grading."""
        print("\n✏️ Fair and constructive feedback helps students grow. You're shaping futures!")

    @classmethod
    def motivation_research(cls):
        """Motivation about professional development and research."""
        print("\n🔬 Keep innovating! Your work contributes to the ever-growing field of knowledge.")

    @classmethod
    def motivation_self_care(cls):
        """Motivation about self-care for instructors."""
        print("\n🧘 Teaching is rewarding but challenging. Remember to recharge and prioritize yourself.")

    @classmethod
    def motivation_collaboration(cls):
        """Motivation about collaboration with colleagues."""
        print("\n🤝 Collaboration among educators sparks creativity and innovation. Share your ideas!")

class Course:
    def __init__(self, course_id, name, start_date, end_date, description, capacity):
        self._course_id = course_id
        self._name = name
        self._start_date = start_date
        self._end_date = end_date
        self._description = description
        self._capacity = capacity
        self._enrolled_students = []
        self._instructor = None  # Assigned Instructor

    def assign_instructor(self, instructor):
        """Assigns an instructor to the course."""
        if self._instructor:
            print(f"Course {self._name} already has an assigned instructor.")
            return

        self._instructor = instructor
        if self not in instructor._assigned_courses:
            instructor._assigned_courses.append(self)  # Update instructor's assigned courses
        print(f"Instructor {instructor._first_name} {instructor._last_name} has been assigned to course {self._name}.")

    def __str__(self):
        instructor_name = f"{self._instructor._first_name} {self._instructor._last_name}" if self._instructor else "None"
        return (f"Course ID: {self._course_id}\nName: {self._name}\n"
                f"Start Date: {self._start_date}\nEnd Date: {self._end_date}\n"
                f"Description: {self._description}\nCapacity: {self._capacity}\n"
                f"Instructor: {instructor_name}\nEnrolled Students: {len(self._enrolled_students)} / {self._capacity}")
  
    def add_student(self, student):
        if len(self._enrolled_students) < self._capacity:
            self._enrolled_students.append(student)
            print(f"Student {student._first_name} {student._last_name} added to course {self._name}.")
        else:
            print(f"Course {self._name} is full. Cannot add student {student._first_name} {student._last_name}.")

    def to_dict(self):
        """
        Converts the Course object into a dictionary for JSON serialization.
        """
        return {
            "course_id": self._course_id,
            "name": self._name,
            "start_date": self._start_date,
            "end_date": self._end_date,
            "description": self._description,
            "capacity": self._capacity,
            "enrolled_students": [student._id for student in self._enrolled_students],
            "instructor": self._instructor._id if self._instructor else None,
        }

    @staticmethod
    def from_dict(data):
        """
        Rebuilds a Course object from a dictionary.
        """
        course = Course(
            course_id=data["course_id"],
            name=data["name"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data["description"],
            capacity=data["capacity"],
        )
        # Enrolled students and instructor will be linked separately
        return course

    def __str__(self):
        instructor_name = f"{self._instructor._first_name} {self._instructor._last_name}" if self._instructor else "None"
        return (
            f"Course ID: {self._course_id}\n"
            f"Name: {self._name}\n"
            f"Start Date: {self._start_date}\n"
            f"End Date: {self._end_date}\n"
            f"Description: {self._description}\n"
            f"Capacity: {self._capacity}\n"
            f"Instructor: {instructor_name}\n"
            f"Enrolled Students: {len(self._enrolled_students)} / {self._capacity}"
        )

# Class: Enrollment
class Enrollment:
    def __init__(self, student, course, payment_status="Pending", enrollment_status="Pending"):
        self._enrollment_id = self._generate_enrollment_id()
        self._student = student
        self._course = course
        self._payment_status = payment_status
        self._enrollment_status = enrollment_status

    def approve(self):
        """Approves the enrollment and adds the student to the course."""
        self._enrollment_status = "Approved"

        # Add student to the course's enrolled students list if not already present
        if self._student not in self._course._enrolled_students:
            self._course._enrolled_students.append(self._student)
            print(f"Student {self._student._first_name} {self._student._last_name} added to course {self._course._name}.")
        else:
            print(f"Student {self._student._first_name} {self._student._last_name} is already enrolled in course {self._course._name}.")
   
    def decline(self):
        self._enrollment_status = "Declined"

    def is_approved(self):
        return self._enrollment_status == "Approved"

    def __str__(self):
        return (f"Enrollment ID: {self._enrollment_id}\nStudent: {self._student._first_name} {self._student._last_name}\n"
                f"Course: {self._course._name}\nPayment Status: {self._payment_status}\n"
                f"Enrollment Status: {self._enrollment_status}")

    def to_dict(self):
        """
        Converts the Enrollment object into a dictionary for JSON serialization.
        """
        return {
            "enrollment_id": self._enrollment_id,
            "student_id": self._student._id if self._student else None,
            "course_id": self._course._course_id if self._course else None,
            "payment_status": self._payment_status,
            "enrollment_status": self._enrollment_status,
        }

    @staticmethod
    def from_dict(data):
        """
        Rebuilds an Enrollment object from a dictionary.
        Student and Course will be linked separately.
        """
        enrollment = Enrollment(
            student=None,  # Link later
            course=None,   # Link later
            payment_status=data["payment_status"],
            enrollment_status=data["enrollment_status"],
        )
        enrollment._enrollment_id = data["enrollment_id"]
        return enrollment
    
    @staticmethod
    def _generate_enrollment_id():
        return f"ENR-{str(uuid.uuid4())[:8]}"

# Class: Assignment
class Assignment:
    def __init__(self, assignment_id, course, due_date, description, max_grade):
        self._assignment_id = assignment_id
        self._course = course
        self._due_date = due_date
        self._description = description
        self._max_grade = max_grade
        self._submitted_students = {}   
        self._graded_students = {}

    def submit(self, student):
        """
        Allows a student to submit an assignment.
        """
        if student not in self._submitted_students:
            self._submitted_students[student] = "Submitted"
            print(f"Assignment submitted by {student._first_name} {student._last_name}.")
        else:
            print(f"Duplicate Submission: {student._first_name} {student._last_name} has already submitted this assignment.")


    def grade(self, student, grade):
        """
        Grades a student's submission, ensuring it doesn't exceed the max grade.
        """
        if student not in self._submitted_students:
            print(f"Error: {student._first_name} {student._last_name} has not submitted this assignment.")
            return

        if grade > self._max_grade:
            print(f"Error: Grade {grade} exceeds the maximum grade of {self._max_grade}.")
            return

        self._graded_students[student] = grade
        print(f"{student._first_name} {student._last_name} has been graded {grade}/{self._max_grade} for assignment {self._assignment_id}.") 

    def __str__(self):
        return (f"Assignment ID: {self._assignment_id}\n"
                f"Course: {self._course._name}\n"  # Accessing course name
                f"Due Date: {self._due_date}\n"
                f"Description: {self._description}\n"
                f"Submitted: {len(self._submitted_students)} students\n"
                f"Graded: {len(self._graded_students)} students")
    
    def to_dict(self):
        """
        Converts the Assignment object into a dictionary for JSON serialization.
        """
        return {
            "assignment_id": self._assignment_id,
            "course_id": self._course._course_id if self._course else None,
            "due_date": self._due_date,
            "description": self._description,
            "max_grade": self._max_grade,  # Include max grade
            "submitted_students": {student._id: status for student, status in self._submitted_students.items()},
            "graded_students": {student._id: grade for student, grade in self._graded_students.items()},
        }


    @staticmethod
    def from_dict(data, course):
        """
        Rebuilds an Assignment object from a dictionary.
        Submitted and graded students will be linked later.
        """
        max_grade = data.get("max_grade", 10.0)  # Default max grade to 10.0 if not present
        assignment = Assignment(
            assignment_id=data["assignment_id"],
            course=course,
            due_date=data["due_date"],
            description=data["description"],
            max_grade=max_grade  # Pass max grade to the constructor
        )
        assignment._submitted_students = {}  # Link later
        assignment._graded_students = {}    # Link later
        return assignment

# Class: Grade
class Grade:
    def __init__(self, student, course, grade_value):
        self._grade_id = self._generate_grade_id()
        self._student = student
        self._course = course
        self._grade_value = grade_value  # Use the passed grade argument


    def get_grade(self):
        return self._grade

    def update_grade(self, new_grade):
        self._grade = new_grade

    def __str__(self):
        return (f"Grade ID: {self._grade_id}\nStudent: {self._student._first_name} {self._student._last_name}\n"
                f"Course: {self._course._name}\nGrade: {self._grade}")

    @staticmethod
    def _generate_grade_id():
        return f"GRD-{str(uuid.uuid4())[:8]}"
    
    def to_dict(self):
        """
        Converts the Grade object into a dictionary for JSON serialization.
        """
        return {
            "grade_id": self._grade_id,
            "student_id": self._student._id if self._student else None,
            "course_id": self._course._course_id if self._course else None,
            "grade_value": self._grade_value,
        }

    @staticmethod
    def from_dict(data):
        """
        Rebuilds a Grade object from a dictionary.
        Student and Course will be linked separately.
        """
        grade = Grade(
            student=None,  # Link later
            course=None,   # Link later
            grade_value=data["grade_value"],
        )
        grade._grade_id = data["grade_id"]
        return grade

    def __str__(self):
        return (
            f"Grade ID: {self._grade_id}\n"
            f"Student: {self._student._first_name} {self._student._last_name} ({self._student._id})\n"
            f"Course: {self._course._name} ({self._course._course_id})\n"
            f"Grade: {self._grade_value}"
        )

class UserManager:
    _users = []

    @staticmethod
    def login(email, password):
        for user in UserManager._users:
            if user.email == email and user.password == password:
                print("Login successful!")
                return user
        print("Invalid credentials.")
        return None

    @staticmethod
    def sign_up(first_name, last_name, age, sex, birthdate, place_of_birth, account_type):
        email = f"{first_name.lower()}.{last_name.lower()}@email.com"
        password = UserManager._generate_password()
        if account_type == "Student":
            user_id = UserManager._generate_user_id("Student")
            user = Student(first_name, last_name, age, sex, birthdate, place_of_birth)
        elif account_type == "Instructor":
            user_id = UserManager._generate_user_id("Instructor")
            user = Instructor(first_name, last_name, age, sex, birthdate, place_of_birth)
        elif account_type == "Admin":
            user_id = UserManager._generate_user_id("Admin")
            user = PlatformAdmin(user_id, f"{first_name} {last_name}")
        else:
            print("Invalid account type.")
            return None
        user.email = email
        user.password = password
        UserManager._users.append(user)
        print(f"Account created! Email: {email} Password: {password}")
        return user

    @staticmethod
    def find_user_by_id(user_id):
        """Finds and returns a user by their ID."""
        for user in UserManager._users:
            if getattr(user, "_id", None) == user_id:  # Safely check _id attribute
                return user
        print("User not found.")
        return None


    @staticmethod
    def _generate_password():
        import random
        import string
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choices(chars, k=6))
    
    @staticmethod
    def _generate_user_id(account_type):
        from datetime import datetime
        year = datetime.now().year % 100  # Last two digits of the current year
        unique_part = str(uuid.uuid4().int)[:6]  # Generate a 6-digit unique number
        if account_type == "Student":
            return f"STU-{year}-{unique_part}"
        elif account_type == "Instructor":
            return f"INS-{year}-{unique_part}"
        elif account_type == "Admin":
            return f"ADM-{year}-{unique_part}"
        
    @staticmethod
    def view_all_users():
        """Displays all registered users."""
        if not UserManager._users:
            print("No users found.")
            return

        print("\n--- All Users ---")
        for user in UserManager._users:
            if isinstance(user, Student):
                user_type = "Student"
            elif isinstance(user, Instructor):
                user_type = "Instructor"
            elif isinstance(user, PlatformAdmin):
                user_type = "Admin"
                print(f"ID: {user._id}, Name: {user._admin_name}, Type: {user_type}")
                continue
            else:
                user_type = "Unknown"

            # Handle attributes gracefully
            user_id = getattr(user, "_id", "N/A")
            first_name = getattr(user, "_first_name", "N/A")
            last_name = getattr(user, "_last_name", "N/A")
            print(f"ID: {user_id}, Name: {first_name} {last_name}, Type: {user_type}")
    
    @staticmethod
    def remove_student(student_id):
        """
        Removes a student by their ID and updates JSON files.
        """
        for user in UserManager._users:
            if isinstance(user, Student) and user._id == student_id:
                UserManager._users.remove(user)
                print(f"Student with ID {student_id} has been removed.")
                UserManager.save_users()
                CourseManager.save_courses()  # Update courses JSON
                return
        print(f"Student with ID {student_id} not found.")


    @staticmethod
    def remove_instructor(instructor_id):
        """
        Removes an instructor by their ID and updates JSON files.
        """
        for user in UserManager._users:
            if isinstance(user, Instructor) and user._id == instructor_id:
                UserManager._users.remove(user)
                print(f"Instructor with ID {instructor_id} has been removed.")
                UserManager.save_users()
                CourseManager.save_courses()  # Update courses JSON
                return
        print(f"Instructor with ID {instructor_id} not found.")


    @staticmethod
    def drop_student_menu():
        """
        Handles dropping a student.
        """
        print("\n--- Drop Student Menu ---")
        print("1. Drop from Course")
        print("2. Delete Entirely")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            UserManager.drop_student_from_course()
        elif choice == "2":
            student_id = input("Enter Student ID to delete: ").strip()
            UserManager.remove_student(student_id)
        elif choice == "3":
            print("Returning to Drop User Menu...")
            return
        else:
            print("Invalid choice. Returning to the main menu.")


    @staticmethod
    def drop_instructor_menu():
        """
        Handles dropping an instructor.
        """
        print("\n--- Drop Instructor Menu ---")
        print("1. Drop from Course")
        print("2. Delete Entirely")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            UserManager.drop_instructor_from_course()
        elif choice == "2":
            instructor_id = input("Enter Instructor ID to delete: ").strip()
            UserManager.remove_instructor(instructor_id)
        elif choice == "3":
            print("Returning to Drop User Menu...")
            return
        else:
            print("Invalid choice. Returning to the main menu.")


    @staticmethod
    def drop_student_from_course():
        """
        Allows admin to drop a student from a specific course.
        """
        while True:
            course_id = input("Enter Course ID (or 'R' to return): ").strip()
            if course_id.lower() == 'r':
                print("Returning to Drop Student Menu...")
                return

            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
                continue

            if not course._enrolled_students:
                print(f"No students are enrolled in course {course._name}.")
                return

            print(f"\n--- Students in Course: {course._name} ---")
            for student in course._enrolled_students:
                print(f"Student ID: {student._id}, Name: {student._first_name} {student._last_name}")

            student_id = input("Enter Student ID to drop (or 'R' to return): ").strip()
            if student_id.lower() == 'r':
                print("Returning to Drop Student Menu...")
                return

            student = UserManager.find_user_by_id(student_id)
            if not student or student not in course._enrolled_students:
                print("Student not found in this course.")
            else:
                course._enrolled_students.remove(student)
                student._enrolled_courses.remove(course)
                print(f"Student {student._first_name} {student._last_name} has been dropped from course {course._name}.")
                return

    
    @staticmethod
    def drop_instructor_from_course():
        """
        Allows admin to unassign an instructor from a course.
        """
        while True:
            course_id = input("Enter Course ID (or 'R' to return): ").strip()
            if course_id.lower() == 'r':
                print("Returning to Drop Instructor Menu...")
                return

            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
                continue

            if not course._instructor:
                print(f"No instructor is assigned to the course {course._name}.")
                return

            print(f"Instructor {course._instructor._first_name} {course._instructor._last_name} is assigned to this course.")
            confirmation = input("Do you want to unassign this instructor? (yes/no or 'R' to return): ").strip().lower()

            if confirmation == "yes":
                instructor = course._instructor
                course._instructor = None
                instructor._assigned_courses.remove(course)
                print(f"Instructor {instructor._first_name} {instructor._last_name} has been unassigned from course {course._name}.")
                return
            elif confirmation == "no":
                print("Operation cancelled. Returning to Drop Instructor Menu...")
                return
            elif confirmation == 'r':
                print("Returning to Drop Instructor Menu...")
                return
            else:
                print("Invalid input. Please enter 'yes', 'no', or 'R'.")



    
    @staticmethod
    def load_users():
        """
        Load users from JSON and link assigned courses for instructors.
        """
        users_data = load_json("users.json")
        for user_data in users_data:
            if user_data["type"] == "Student":
                student = Student.from_dict(user_data)
                UserManager._users.append(student)
            elif user_data["type"] == "Instructor":
                instructor = Instructor.from_dict(user_data)
                UserManager._users.append(instructor)
            elif user_data["type"] == "Admin":
                admin = PlatformAdmin.from_dict(user_data)
                UserManager._users.append(admin)

        # Link assigned courses for instructors
        for user in UserManager._users:
            if isinstance(user, Instructor):
                user._assigned_courses = [
                    CourseManager.get_course_by_id(course_id)
                    for course_id in user_data.get("assigned_courses", [])
                    if CourseManager.get_course_by_id(course_id)
                ]


    @staticmethod
    def save_users():
        """Save users to JSON."""
        print("DEBUG: Saving users to users.json...")
        users_data = [user.to_dict() for user in UserManager._users]
        save_json("users.json", users_data)
        print("DEBUG: Users saved successfully.")

class PlatformAdmin:
    def __init__(self, admin_id, admin_name):
        self._id = admin_id  # Unique identifier for the admin
        self._admin_name = admin_name

    def display_profile(self):
        print(f"Admin Profile:\nID: {self._id}\nName: {self._first_name}")

    def __str__(self):
        return f"Admin: {self._first_name} (ID: {self._id})"
    
    @staticmethod
    def drop_user_menu():
        """
        Menu to handle dropping students or instructors.
        """
        print("\n--- Drop User Menu ---")
        print("1. Drop Student")
        print("2. Drop Instructor")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            UserManager.drop_student_menu()
        elif choice == "2":
            UserManager.drop_instructor_menu()
        elif choice == "3":
            print("Returning to Admin Menu...")
            return
        else:
            print("Invalid choice. Returning to the main menu.")

    
    def to_dict(self):
        return {
            "id": self._id,
            "type": "Admin",
            "name": self._admin_name,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def from_dict(data):
        admin = PlatformAdmin(data["id"], data["name"])
        admin.email = data.get("email", "")
        admin.password = data.get("password", "")
        return admin

class CourseManager:
    _courses = []
    _applications = {}  # Dictionary to track instructor applications by course ID


    @staticmethod
    def create_course(name, start_date, end_date, description, capacity):
        course_id = f"CRS-{str(uuid.uuid4())[:6]}"
        course = Course(course_id, name, start_date, end_date, description, capacity)
        CourseManager._courses.append(course)
        print(f"Course created: {course}")
        return course

    @staticmethod
    def remove_course(course_id):
        course = CourseManager.get_course_by_id(course_id)
        if course:
            CourseManager._courses.remove(course)
            print(f"Course {course_id} removed.")
        else:
            print("Course not found.")

    @staticmethod
    def get_course_by_id(course_id):
        """Retrieve a course by its ID."""
        for course in CourseManager._courses:
            if course._course_id == course_id:
                return course
        return None

    @staticmethod
    def view_all_courses():
        """
        Display all courses with their IDs, names, and capacities.
        """
        if not CourseManager._courses:
            print("No courses available.")
            return

        print("\n--- All Courses ---")
        for course in CourseManager._courses:
            print(f"Course ID: {course._course_id} | Course Name: {course._name} | Capacity: {len(course._enrolled_students)}/{course._capacity}")

    
    @staticmethod
    def view_available_courses(student):
        """
        Displays courses that the student is not already enrolled in.
        """
        available_courses = [
            course for course in CourseManager._courses
            if student not in course._enrolled_students
        ]

        if not available_courses:
            print("No available courses at the moment.")
            return
        
    @staticmethod
    def view_available_courses_for_instructor():
        """
        Displays courses that have no assigned instructor.
        """
        available_courses = [course for course in CourseManager._courses if course._instructor is None]

        if not available_courses:
            print("No available courses at the moment.")
            return

        print("\n--- Available Courses (Unassigned) ---")
        for course in available_courses:
            print(course)
    
    @staticmethod
    def view_enrolled_courses(student):
        """
        Display all courses the student is enrolled in.
        """
        if not student._enrolled_courses:
            print("You are not enrolled in any courses.")
            return

        print("\n--- Enrolled Courses ---")
        for course in student._enrolled_courses:
            print(f"Course ID: {course._course_id} | Course Name: {course._name} | Capacity: {len(course._enrolled_students)}/{course._capacity}")

    @staticmethod
    def view_applied_courses(instructor):
        """
        Display all courses the instructor has applied for or is assigned to.
        """
        applied_courses = CourseManager._applications.get(instructor._id, [])
        assigned_courses = instructor._assigned_courses

        if not applied_courses and not assigned_courses:
            print("You have not applied to or been assigned any courses.")
            return

        print("\n--- Applied/Assigned Courses ---")
        if applied_courses:
            print("\nApplied Courses:")
            for course in applied_courses:
                print(f"Course ID: {course._course_id} | Course Name: {course._name} | Capacity: {len(course._enrolled_students)}/{course._capacity}")

        if assigned_courses:
            print("\nAssigned Courses:")
            for course in assigned_courses:
                print(f"Course ID: {course._course_id} | Course Name: {course._name} | Capacity: {len(course._enrolled_students)}/{course._capacity}")



    @staticmethod
    def apply_to_course(instructor, course):
        """Allows an instructor to apply for a course if it has no assigned instructor."""
        if course._instructor:
            print(f"Course {course._name} already has an assigned instructor: {course._instructor._first_name} {course._instructor._last_name}. You cannot apply.")
            return

        if course._course_id not in CourseManager._applications:
            CourseManager._applications[course._course_id] = []

        # Check for duplicate applications
        if instructor in CourseManager._applications[course._course_id]:
            print(f"Instructor {instructor._first_name} {instructor._last_name} has already applied for this course.")
        else:
            CourseManager._applications[course._course_id].append(instructor)
            print(f"Instructor {instructor._first_name} {instructor._last_name} successfully applied for course {course._name}.")

    @staticmethod
    def view_applications_for_course(course):
        """Displays all applications for a specific course."""
        if course._course_id not in CourseManager._applications or not CourseManager._applications[course._course_id]:
            print(f"No applications found for course {course._name}.")
            return
        print(f"\n--- Applications for Course: {course._name} ---")
        for instructor in CourseManager._applications[course._course_id]:
            print(f"Instructor ID: {instructor._id}, Name: {instructor._first_name} {instructor._last_name}")

    @staticmethod
    def view_users_in_course(course_id):
        """Displays users (instructor and students) in a specific course."""
        course = CourseManager.get_course_by_id(course_id)
        if not course:
            print("Course not found.")
            return

        print(f"\n--- Users in Course: {course._name} ---")
        print(f"Course ID: {course._course_id}")
        print(f"Course Name: {course._name}")
        print(f"Capacity: {len(course._enrolled_students)}/{course._capacity}")
        print("\nInstructor:")
        if course._instructor:
            print(f"ID: {course._instructor._id}, Name: {course._instructor._first_name} {course._instructor._last_name}")
        else:
            print("No instructor assigned.")

        print("\nStudents:")
        if course._enrolled_students:
            for student in course._enrolled_students:
                print(f"ID: {student._id}, Name: {student._first_name} {student._last_name}")
        else:
            print("No students enrolled.")
    
    @staticmethod
    def view_students_in_course(course):
        """Displays all students enrolled in a specific course."""
        if not course._enrolled_students:
            print(f"No students are enrolled in the course: {course._name}")
            return

        print(f"\n--- Students in Course: {course._name} ---")
        print(f"Course ID: {course._course_id}, Course Name: {course._name}")
        for student in course._enrolled_students:
            print(f"Student ID: {student._id}, Student Name: {student._first_name} {student._last_name}")
    
    @staticmethod
    def load_courses():
        """
        Load courses from JSON and link instructors and students.
        """
        courses_data = load_json("courses.json")
        CourseManager._courses = []  # Clear existing courses to avoid duplication

        for course_data in courses_data:
            # Create Course objects
            course = Course.from_dict(course_data)
            CourseManager._courses.append(course)

            # Link instructor
            if course_data["instructor"]:
                instructor = UserManager.find_user_by_id(course_data["instructor"])
                if instructor:
                    course._instructor = instructor
                    if course not in instructor._assigned_courses:
                        instructor._assigned_courses.append(course)

            # Link enrolled students
            course._enrolled_students = [
                UserManager.find_user_by_id(student_id)
                for student_id in course_data["enrolled_students"]
                if UserManager.find_user_by_id(student_id)
            ]

    @staticmethod
    def save_courses():
        """
        Save all courses to JSON.
        """
        courses_data = [course.to_dict() for course in CourseManager._courses]
        save_json("courses.json", courses_data)

class EnrollmentManager:
    _enrollments = []

    
    @staticmethod
    def create_enrollment(student, course):
    # Check for duplicate enrollments
        for enrollment in EnrollmentManager._enrollments:
            if enrollment._student == student and enrollment._course == course:
                print(f"Student {student._first_name} {student._last_name} is already enrolled or has a pending enrollment in course {course._name}.")
                return None  # Exit if duplicate is found

    # Existing payment method logic
        print("Choose Payment Method:\n1. PayPal\n2. GCash\n3. Debit Card")
        payment_choice = input("Enter payment option (1, 2, or 3): ")
        payment_methods = { "1": "PayPal", "2": "GCash", "3": "Debit Card" }
        payment_status = "Paid" if payment_choice in payment_methods else "Pending"

        # Create and add the enrollment
        enrollment = Enrollment(student, course, payment_status)
        EnrollmentManager._enrollments.append(enrollment)
        print(f"Enrollment created: {enrollment}")
        return enrollment

    @staticmethod
    def approve_enrollment(enrollment_id):
        enrollment = EnrollmentManager.get_enrollment_by_id(enrollment_id)
        if enrollment:
            enrollment.approve()
            print(f"Enrollment with ID {enrollment_id} has been approved successfully.")
        else:
            print("Enrollment not found.")
    
    def approve(self):
        self._enrollment_status = "Approved"
        if self._student not in self._course._enrolled_students:
            self._course.add_student(self._student)
        print(f"Enrollment for {self._student._first_name} {self._student._last_name} in {self._course._name} approved.")


    @staticmethod
    def decline_enrollment(enrollment_id):
        enrollment = EnrollmentManager.get_enrollment_by_id(enrollment_id)
        if enrollment:
            enrollment.decline()
            print(f"Enrollment {enrollment_id} declined.")
        else:
            print("Enrollment not found.")

    @staticmethod
    def get_enrollment_by_id(enrollment_id):
        for enrollment in EnrollmentManager._enrollments:
            if enrollment._enrollment_id == enrollment_id:
                return enrollment
        print("Enrollment not found.")
        return None
    
    @staticmethod
    def view_enrollments_by_course(course):
        enrollments = [enrollment for enrollment in EnrollmentManager._enrollments if enrollment._course == course]
        if not enrollments:
            print(f"No enrollments found for course: {course._name}")
            return
        print(f"Enrollments for Course: {course._name}")
        for enrollment in enrollments:
            print(enrollment)

    @staticmethod
    def load_enrollments():
        """
        Load enrollments from JSON and link students and courses.
        Ensure student and course relationships are updated.
        """
        enrollments_data = load_json("enrollments.json")
        print(f"DEBUG: Loading {len(enrollments_data)} enrollments from enrollments.json")

        EnrollmentManager._enrollments = []  # Clear existing enrollments to avoid duplication

        for enrollment_data in enrollments_data:
            student = UserManager.find_user_by_id(enrollment_data["student_id"])
            course = CourseManager.get_course_by_id(enrollment_data["course_id"])

            if not student or not course:
                print(f"WARNING: Skipping enrollment {enrollment_data['enrollment_id']} due to missing student or course.")
                continue

            # Create and link enrollment
            enrollment = Enrollment.from_dict(enrollment_data)
            enrollment._student = student
            enrollment._course = course
            EnrollmentManager._enrollments.append(enrollment)

            # Update relationships
            if course not in student._enrolled_courses:
                student._enrolled_courses.append(course)  # Link course to student
            if student not in course._enrolled_students:
                course._enrolled_students.append(student)  # Link student to course

            print(f"DEBUG: Enrollment {enrollment._enrollment_id} linked: {student._id} -> {course._course_id}")


    @staticmethod
    def save_enrollments():
        """
        Save all enrollments to JSON.
        """
        enrollments_data = [enrollment.to_dict() for enrollment in EnrollmentManager._enrollments]
        print(f"DEBUG: Saving {len(enrollments_data)} enrollments to enrollments.json")
        for enrollment in enrollments_data:
            print(f"DEBUG: {enrollment}")  # Log each enrollment
        save_json("enrollments.json", enrollments_data)

class AssignmentManager:
    _assignments = []

    @staticmethod
    def add_assignment(course_id, assignment_id, due_date, description, max_grade):
        """
        Add an assignment to a course with a specified maximum grade.
        """
        if max_grade <= 0:
            print("Max grade must be greater than 0.")
            return

        course = CourseManager.get_course_by_id(course_id)
        if not course:
            print("Course not found. Assignment not created.")
            return

        assignment = Assignment(assignment_id, course, due_date, description, max_grade)
        AssignmentManager._assignments.append(assignment)
        print(f"Assignment added:\n{assignment}")



    @staticmethod
    def submit_assignment(student, assignment_id):
        assignment = AssignmentManager.get_assignment_by_id(assignment_id)
        if assignment:
            assignment.submit(student)
        else:
            print("Assignment not found.")

    @staticmethod
    def grade_assignment(assignment_id, student_id, grade):
        """
        Grade a student's assignment using the assignment's predefined max grade.
        """
        assignment = AssignmentManager.get_assignment_by_id(assignment_id)
        if not assignment:
            print("Assignment not found.")
            return

        student = UserManager.find_user_by_id(student_id)
        if not student or not isinstance(student, Student):
            print("Student not found.")
            return

        assignment.grade(student, grade)


    @staticmethod
    def get_assignment_by_id(assignment_id):
        """Retrieves an assignment by its ID."""
        for assignment in AssignmentManager._assignments:
            if assignment._assignment_id == assignment_id:
                return assignment
        return None
    
    @staticmethod
    def view_all_assignments(course):
        """Displays all assignments for a specific course."""
        assignments_for_course = [assignment for assignment in AssignmentManager._assignments if assignment._course == course]
        if not assignments_for_course:
            print(f"No assignments found for course: {course._name}")
            return

        print(f"\n--- Assignments for Course: {course._name} ---")
        for assignment in assignments_for_course:
            print(assignment)
    
    @staticmethod
    def view_assignment_grades(student, course):
        """Displays the assignment grades for a student in a specific course."""
        assignments_for_course = [assignment for assignment in AssignmentManager._assignments if assignment._course == course]

        if not assignments_for_course:
            print(f"No assignments found for course: {course._name}")
            return

        print(f"\n--- Assignment Grades for Course: {course._name} ---")
        for assignment in assignments_for_course:
            grade = assignment._graded_students.get(student, "None")
            print(f"Assignment ID: {assignment._assignment_id}, "
                  f"Assignment Name: {assignment._description}, "
                  f"Assignment Grade: {grade}")
    
    @staticmethod
    def view_passed_assignments(course, passing_grade=5):
        """
        Displays all assignments and the students who passed them in a specific course.
        Highlights ungraded submissions for the instructor's attention.
        """
        assignments_for_course = [assignment for assignment in AssignmentManager._assignments if assignment._course == course]

        if not assignments_for_course:
            print(f"No assignments found for course: {course._name}")
            return

        print(f"\n--- Passed Assignments for Course: {course._name} ---")
        print(f"Course ID: {course._course_id}, Course Name: {course._name}\n")

        for assignment in assignments_for_course:
            print(f"Assignment ID: {assignment._assignment_id}, Description: {assignment._description}")

            # Identify passed students
            passed_students = [student for student, grade in assignment._graded_students.items() if grade is not None and grade >= passing_grade]

            # Identify ungraded students
            ungraded_students = [student for student in assignment._submitted_students.keys() if student not in assignment._graded_students]

            if ungraded_students:
                print("\nWarning: The following students have submitted but not yet been graded:")
                for student in ungraded_students:
                    print(f"Student Name: {student._first_name} {student._last_name}")

            if not passed_students:
                print("\nNo students passed this assignment.\n")
            else:
                print("\nPassed Students:")
                for student in passed_students:
                    print(f"Student Name: {student._first_name} {student._last_name}")
                print()
    
    @staticmethod
    def view_all_assignments(course, student=None):
        """
        Displays all assignments for a specific course and optionally shows the passing status for a student.
        """
        assignments_for_course = [
            assignment for assignment in AssignmentManager._assignments if assignment._course == course
        ]
        if not assignments_for_course:
            print(f"No assignments found for course: {course._name}")
            return

        print(f"\n--- Assignments for Course: {course._name} ---")
        for assignment in assignments_for_course:
            if student:
                passed_status = (
                    "Passed" if student in assignment._graded_students and assignment._graded_students[student] >= 5 else "Not Passed"
                )
                print(
                    f"Assignment ID: {assignment._assignment_id}, Due Date: {assignment._due_date}, "
                    f"Passed: {passed_status}, Description: {assignment._description}"
                )
            else:
                print(
                    f"Assignment ID: {assignment._assignment_id}, Due Date: {assignment._due_date}, "
                    f"Description: {assignment._description}"
                )



    @staticmethod
    def load_assignments():
        """
        Load assignments from JSON and link courses, students, and grades.
        """
        assignments_data = load_json("assignments.json")
        for assignment_data in assignments_data:
            course = CourseManager.get_course_by_id(assignment_data["course_id"])
            if not course:
                print(f"WARNING: Skipping assignment {assignment_data['assignment_id']} due to missing course.")
                continue

            if "max_grade" not in assignment_data:
                print(f"ERROR: Assignment {assignment_data['assignment_id']} is missing 'max_grade'. Skipping.")
                continue

            assignment = Assignment.from_dict(assignment_data, course)

            # Link submitted students
            assignment._submitted_students = {
                UserManager.find_user_by_id(student_id): status
                for student_id, status in assignment_data["submitted_students"].items()
                if UserManager.find_user_by_id(student_id)
            }

            # Link graded students
            assignment._graded_students = {
                UserManager.find_user_by_id(student_id): grade
                for student_id, grade in assignment_data["graded_students"].items()
                if UserManager.find_user_by_id(student_id)
            }

            AssignmentManager._assignments.append(assignment)


    @staticmethod
    def save_assignments():
        """
        Save all assignments to JSON.
        """
        assignments_data = [assignment.to_dict() for assignment in AssignmentManager._assignments]
        save_json("assignments.json", assignments_data)

class GradeManager:
    _grades = []

    @staticmethod
    def assign_grade(student, course, grade_value):
        """
        Assign a course grade to a student using a 1-5 scale.
        """
        grade = Grade(student, course, grade_value)
        GradeManager._grades.append(grade)
        print(f"Grade assigned: {grade}")
        return grade



    @staticmethod
    def view_student_grades(student):
        """View all grades assigned to a student."""
        student_grades = [grade for grade in GradeManager._grades if grade._student == student]
        if not student_grades:
            print(f"No grades found for {student._first_name} {student._last_name}.")
            return
        for grade in student_grades:
            print(grade)

    @staticmethod
    def grade_course(course_id, instructor):
        """Allows an instructor to grade all students in a course with proper grading flow."""
        course = CourseManager.get_course_by_id(course_id)
        if not course:
            print("Course not found.")
            return

        if course._instructor != instructor:
            print("You are not assigned to this course.")
            return

        if not course._enrolled_students:
            print(f"No students are enrolled in the course {course._name}.")
            return

        print(f"\n--- Grading Course: {course._name} ---")
        print(f"Course ID: {course._course_id}, Course Name: {course._name}\n")

        # Display students with their current grading status
        for student in course._enrolled_students:
            existing_grade = next(
                (grade._grade_value for grade in GradeManager._grades 
                if grade._student == student and grade._course == course),
                "Not Yet Graded"
            )
            print(f"Student ID: {student._id}, Name: {student._first_name} {student._last_name}, Grade: {existing_grade}")

        print("\nChoose students to grade.")
        
        # Grade each student
        for student in course._enrolled_students:
            existing_grade = next(
                (grade._grade_value for grade in GradeManager._grades 
                if grade._student == student and grade._course == course),
                None
            )
            if existing_grade is not None:
                print(f"{student._first_name} {student._last_name} is already graded with {existing_grade}. Skipping...")
                continue

            # Input grade for the student
            try:
                grade_value = float(input(f"Enter grade (1.0 - 5.0) for {student._first_name} {student._last_name}: "))
                if 1.0 <= grade_value <= 5.0:
                    GradeManager.assign_grade(student, course, grade_value)
                else:
                    print(f"Invalid grade. Please enter a grade between 1.0 and 5.0. Skipping {student._first_name} {student._last_name}.")
            except ValueError:
                print(f"Invalid input. Skipping {student._first_name} {student._last_name}.")

    @staticmethod
    def load_grades():
        """
        Load grades from JSON and link students and courses.
        """
        grades_data = load_json("grades.json")
        print(f"DEBUG: Found {len(grades_data)} grades in the file.")
        GradeManager._grades = []  # Clear existing grades

        for grade_data in grades_data:
            student = UserManager.find_user_by_id(grade_data["student_id"])
            course = CourseManager.get_course_by_id(grade_data["course_id"])

            if not student or not course:
                print(f"WARNING: Skipping grade {grade_data['grade_id']} due to missing student or course.")
                continue

            grade = Grade.from_dict(grade_data)
            grade._student = student
            grade._course = course
            GradeManager._grades.append(grade)

    @staticmethod
    def save_grades():
        """
        Save all grades to JSON.
        """
        grades_data = [grade.to_dict() for grade in GradeManager._grades]
        save_json("grades.json", grades_data)

def general_menu():
    while True:
        print("\n--- General Menu ---")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            email = input("Enter email: ")
            password = input("Enter password: ")
            user = UserManager.login(email, password)
            if user:
                if isinstance(user, Student):
                    student_menu(user)
                elif isinstance(user, Instructor):
                    instructor_menu(user)
                elif isinstance(user, PlatformAdmin):  # Redirect to Admin Menu
                    admin_menu(user)

        elif choice == "2":  # Sign Up
            print("\n--- Sign Up ---")
            print("Account Type:\n1. Student\n2. Instructor\n3. Admin")
            account_type_choice = input("Choose account type (1, 2, or 3): ")
            account_type = (
                "Student" if account_type_choice == "1" else
                "Instructor" if account_type_choice == "2" else "Admin"
            )

            if account_type == "Admin":
                admin_name = input("Enter Admin Name: ")
                admin_id = UserManager._generate_user_id("Admin")
                email = f"admin-{admin_id.lower()}@platform.com"
                password = UserManager._generate_password()
                admin = PlatformAdmin(admin_id, admin_name)
                admin.email = email  # Adding email to admin
                admin.password = password  # Adding password to admin
                UserManager._users.append(admin)
                print(f"Admin account created!\nEmail: {email}\nPassword: {password}\nID: {admin_id}")

            else:  # Student or Instructor
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                age = int(input("Age: "))
                print("Sex:\n1. Male\n2. Female")
                sex_choice = input("Choose your sex (1 or 2): ")
                sex = "Male" if sex_choice == "1" else "Female"

                birthdate = input("Birthdate (MM/DD/YYYY): ")
                place_of_birth = input("Place of Birth: ")

                email = f"{first_name.lower()}.{last_name.lower()}@platform.com"
                password = UserManager._generate_password()

                if account_type == "Student":
                    user_id = UserManager._generate_user_id("Student")
                    user = Student(first_name, last_name, age, sex, birthdate, place_of_birth)
                elif account_type == "Instructor":
                    user_id = UserManager._generate_user_id("Instructor")
                    user = Instructor(first_name, last_name, age, sex, birthdate, place_of_birth)

                user.email = email
                user.password = password
                UserManager._users.append(user)
                print(f"{account_type} account created!\nEmail: {email}\nPassword: {password}\nID: {user_id}")



        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def student_menu(student):
    while True:

        # Randomly choose a motivational method from the Student class
        import random
        motivational_methods = [
            Student.motivation_assignment,
            Student.motivation_exams,
            Student.motivation_grades,
            Student.motivation_progress,
            Student.motivation_balance,
            Student.motivation_teamwork
        ]
        random.choice(motivational_methods)()  # Call a random method

        print(f"\n--- Student Menu ({student._first_name} {student._last_name}) ---")
        print("1. View Profile")
        print("2. View All Courses")
        print("3. View Enrolled Courses")
        print("4. Enroll in Course")
        print("5. View Grades")
        print("6. View Assignments")
        print("7. Submit Assignment")
        print("8. View Assignment Grades")
        print("9. Notifications")
        print("10. Logout")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            student.display_profile()
        elif choice == "2":
            CourseManager.view_all_courses  # Pass the current student

        elif choice == "3":
            CourseManager.view_enrolled_courses(student)

        elif choice == "4":  # Enroll in Course
            print("\n--- Available Courses ---")
            CourseManager.view_available_courses(student)  # Pass the student here

            course_id = input("\nEnter Course ID to enroll: ").strip()
            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
            elif len(course._enrolled_students) >= course._capacity:
                print("Course is full. Cannot enroll.")
            elif course in student._enrolled_courses:
                print(f"You are already enrolled in the course: {course._name}.")
            else:
                EnrollmentManager.create_enrollment(student, course)


        elif choice == "5":
            GradeManager.view_student_grades(student)

        elif choice == "6":  # View Assignments
            course_id = input("Enter Course ID to view assignments: ").strip()
            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
            else:
                AssignmentManager.view_all_assignments(course)

        elif choice == "7":  # Submit Assignment
            # Prompt for course selection
            print("\n--- Your Enrolled Courses ---")
            if not student._enrolled_courses:
                print("You are not enrolled in any courses.")
                continue

            for course in student._enrolled_courses:
                print(f"Course ID: {course._course_id}, Course Name: {course._name}")

            course_id = input("Enter Course ID to submit an assignment: ").strip()
            course = CourseManager.get_course_by_id(course_id)

            if not course:
                print("Course not found.")
                continue

            if course not in student._enrolled_courses:
                print(f"You are not enrolled in course {course._name}.")
                continue

            # Use the class method to display assignments
            AssignmentManager.list_assignments_for_student(student, course)

            assignment_id = input("\nEnter Assignment ID to submit: ").strip()
            assignment = AssignmentManager.get_assignment_by_id(assignment_id)

            if not assignment or assignment._course != course:
                print(f"Invalid Assignment ID or the assignment is not part of course {course._name}.")
                continue

            AssignmentManager.submit_assignment(student, assignment_id)

        
        elif choice == "8":  # View Assignment Grades
            course_id = input("Enter Course ID to view assignment grades: ").strip()
            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
            elif course not in student._enrolled_courses:
                print(f"You are not enrolled in course: {course._name}.")
            else:
                AssignmentManager.view_assignment_grades(student, course)

        elif choice == "9":
            print("Feature not implemented: Notifications will be handled later.")
        elif choice == "10":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def instructor_menu(instructor):
    while True:

         # Randomly choose a motivational method from the Instructor class
        import random
        motivational_methods = [
            Instructor.motivation_teaching,
            Instructor.motivation_students,
            Instructor.motivation_grading,
            Instructor.motivation_research,
            Instructor.motivation_self_care,
            Instructor.motivation_collaboration
        ]
        random.choice(motivational_methods)()  # Call a random method

        print(f"\n--- Instructor Menu ({instructor._first_name} {instructor._last_name}) ---")
        print("1. View Profile")
        print("2. View All Courses")
        print("3. View Applied/Assigned Courses")
        print("4. Apply to Course")
        print("5. View Students Enrolled in Your Course")
        print("6. Add Assignment")
        print("7. Grade Assignment")
        print("8. Grade Course")
        print("9. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            instructor.display_profile()
            
        elif choice == "2":
            CourseManager.view_all_courses()

        elif choice == "3":
            CourseManager.view_applied_courses(instructor)

        elif choice == "4":  # Apply to Course
            CourseManager.view_available_courses_for_instructor()

            course_id = input("Enter Course ID to apply for: ").strip()
            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
            else:
                CourseManager.apply_to_course(instructor, course)


        elif choice == "5":  # View All Students in Course
            course_id = input("Enter Course ID: ").strip()
            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
            elif course._instructor != instructor:
                print("You are not assigned to this course.")
            else:
                CourseManager.view_students_in_course(course)


        elif choice == "6":  # Add Assignment
            course_id = input("Enter Course ID: ")
            assignment_id = input("Enter Assignment ID: ")
            due_date = input("Enter Due Date (MM/DD/YYYY): ")
            description = input("Enter Assignment Description: ")
            max_grade = float(input("Enter Maximum Grade: "))
            AssignmentManager.add_assignment(course_id, assignment_id, due_date, description, max_grade)


        elif choice == "7":  # View Passed Assignments
            course_id = input("Enter Course ID: ").strip()
            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
            elif course._instructor != instructor:
                print("You are not assigned to this course.")
            else:
                AssignmentManager.view_passed_assignments(course)


        elif choice == "8":  # Grade Assignment
            assignment_id = input("Enter Assignment ID: ").strip()
            student_id = input("Enter Student ID to grade: ").strip()
            grade = float(input("Enter Grade to assign: "))  # Prompt only for the grade
            AssignmentManager.grade_assignment(assignment_id, student_id, grade)  # Pass only grade



        elif choice == "9":  # Grade Course
            course_id = input("Enter Course ID to grade: ").strip()
            GradeManager.grade_course(course_id, instructor)


        elif choice == "9": # Log out
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def admin_menu(admin):
    while True:
        print(f"\n--- Admin Menu ({admin._admin_name}) ---")
        print("1. Create Course")
        print("2. Drop Course")
        print("3. View All Users")
        print("4. View User in specified Course")
        print("5. Assign Instructor to Course")
        print("6. Approve/Reject Student Enrollments")
        print("7. Drop Student/Instructor")
        print("8. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":  # Create Course
            name = input("Course Name: ")
            start_date = input("Start Date (MM/DD/YYYY): ")
            end_date = input("End Date (MM/DD/YYYY): ")
            description = input("Description: ")
            capacity = int(input("Capacity: "))
            course = CourseManager.create_course(name, start_date, end_date, description, capacity)
            print(f"Course created: {course}")

        elif choice == "2":  # Drop Course
            course_id = input("Enter Course ID to drop: ")
            CourseManager.remove_course(course_id)

        elif choice == "3":  # View All Users
            UserManager.view_all_users()

        elif choice == "4":  # View Users in a Specific Course
            course_id = input("Enter Course ID: ").strip()
            CourseManager.view_users_in_course(course_id)

        elif choice == "5":  # Assign Instructor to Course
            course_id = input("Enter Course ID: ")
            course = CourseManager.get_course_by_id(course_id)
            if course:
                CourseManager.view_applications_for_course(course)
                instructor_id = input("Enter Instructor ID to approve: ")
                instructor = UserManager.find_user_by_id(instructor_id)  # Look up by consistent ID
                if instructor:
                    course.assign_instructor(instructor)
                    print(f"Instructor {instructor._first_name} {instructor._last_name} assigned to course {course._name}.")
                    # Clear applications after assigning
                    CourseManager._applications[course._course_id] = []
                else:
                    print("Instructor not found.")

        elif choice == "6":  # Approve/Reject Enrollments
            course_id = input("Enter Course ID to manage enrollments: ")
            course = CourseManager.get_course_by_id(course_id)
            if course:
                EnrollmentManager.view_enrollments_by_course(course)
                print("Options:\n1. Approve Enrollment\n2. Reject Enrollment")
                sub_choice = input("Choose an option: ")
                enrollment_id = input("Enter Enrollment ID: ")
                if sub_choice == "1":
                    EnrollmentManager.approve_enrollment(enrollment_id)
                elif sub_choice == "2":
                    EnrollmentManager.decline_enrollment(enrollment_id)

        elif choice == "7":  # Drop Student/Instructor
            PlatformAdmin.drop_user_menu()

        elif choice == "8":  # Logout
            print("Logging out...")
            break  # Exits the loop cleanly

        else:
            print("Invalid choice. Please try again.")



def main():
    print("Welcome to the E-Learning Platform!")

    # Debugging: Check the current working directory and save folder
    print(f"DEBUG: Current Working Directory: {os.getcwd()}")
    print(f"DEBUG: JSON Save Folder: {SAVE_FOLDER}")

    # Debugging: Check JSON file names and intended paths
    print("\nDEBUG: JSON Files:")
    print(f"Users File: {os.path.join(SAVE_FOLDER, 'users.json')}")
    print(f"Courses File: {os.path.join(SAVE_FOLDER, 'courses.json')}")
    print(f"Enrollments File: {os.path.join(SAVE_FOLDER, 'enrollments.json')}")
    print(f"Assignments File: {os.path.join(SAVE_FOLDER, 'assignments.json')}")
    print(f"Grades File: {os.path.join(SAVE_FOLDER, 'grades.json')}")

    # Load data at the beginning
    print("\nDEBUG: Loading Data...")
    UserManager.load_users()
    CourseManager.load_courses()
    EnrollmentManager.load_enrollments()
    AssignmentManager.load_assignments()
    GradeManager.load_grades()

    # Debugging: Confirmation that loading is complete
    print("\nDEBUG: Data Loaded Successfully.")

    try:
        general_menu()  # Main program logic (this handles menu inputs)
    finally:
        # Save data before exiting
        print("\nDEBUG: Saving Data...")
        UserManager.save_users()
        CourseManager.save_courses()
        EnrollmentManager.save_enrollments()
        AssignmentManager.save_assignments()
        GradeManager.save_grades()
        print("DEBUG: Data Saved Successfully.")

    print("Exiting program. Goodbye!")





# Entry Point
if __name__ == "__main__":
    main()
