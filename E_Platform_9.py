from abc import ABC, abstractmethod
import uuid
import json

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
        
# Subclass: Instructor
class Instructor(Person):
    def __init__(self, first_name, last_name, age, sex, birthdate, place_of_birth):
        super().__init__(first_name, last_name, age, sex, birthdate, place_of_birth)
        self._id = UserManager._generate_user_id("Instructor")  # Consistent ID
        self._assigned_courses = []

    def assign_course(self, course):
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
# Class: Course
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
        self._instructor = instructor
        print(f"Instructor {instructor._first_name} {instructor._last_name} assigned to course {self._name}.")

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

# Class: Enrollment
class Enrollment:
    def __init__(self, student, course, payment_status="Pending", enrollment_status="Pending"):
        self._enrollment_id = self._generate_enrollment_id()
        self._student = student
        self._course = course
        self._payment_status = payment_status
        self._enrollment_status = enrollment_status

    def approve(self):
        self._enrollment_status = "Approved"
        if self._student not in self._course._enrolled_students:
            self._student._enrolled_courses.append(self._course)  # Updates course's student list
        print(f"Enrollment for {self._student._first_name} {self._student._last_name} in course {self._course._name} approved.")

    def decline(self):
        self._enrollment_status = "Declined"

    def is_approved(self):
        return self._enrollment_status == "Approved"

    def __str__(self):
        return (f"Enrollment ID: {self._enrollment_id}\nStudent: {self._student._first_name} {self._student._last_name}\n"
                f"Course: {self._course._name}\nPayment Status: {self._payment_status}\n"
                f"Enrollment Status: {self._enrollment_status}")

    @staticmethod
    def _generate_enrollment_id():
        return f"ENR-{str(uuid.uuid4())[:8]}"

# Class: Assignment
class Assignment:
    def __init__(self, assignment_id, course, due_date, description):
        self._assignment_id = assignment_id
        self._course = course
        self._due_date = due_date
        self._description = description
        self._submitted_students = {}
        self._graded_students = {}

    def submit(self, student):
        if student not in self._submitted_students:
            self._submitted_students[student] = "Submitted"
            print(f"Assignment submitted by {student._first_name} {student._last_name}.")
        else:
            print(f"{student._first_name} {student._last_name} has already submitted this assignment.")

    def grade(self, student, grade, max_grade):
        """Grades a student's submission with validation."""
        if student not in self._submitted_students:
            print(f"{student._first_name} {student._last_name} has not submitted this assignment.")
            return

        if grade > max_grade:
            print(f"Error: Grade {grade} exceeds the maximum grade of {max_grade}.")
            return

        # Update or add the grade
        self._graded_students[student] = grade
        print(f"{student._first_name} {student._last_name} has been graded {grade}/{max_grade} for assignment {self._assignment_id}.")

    def __str__(self):
        return (f"Assignment ID: {self._assignment_id}\n"
                f"Course: {self._course._name}\n"  # Accessing course name
                f"Due Date: {self._due_date}\n"
                f"Description: {self._description}\n"
                f"Submitted: {len(self._submitted_students)} students\n"
                f"Graded: {len(self._graded_students)} students")

# Class: Grade
class Grade:
    def __init__(self, student, course, grade):
        self._grade_id = self._generate_grade_id()
        self._student = student
        self._course = course
        self._grade = grade
        

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
        """Removes a student by their ID."""
        for user in UserManager._users:
            if isinstance(user, Student) and user._id == student_id:
                UserManager._users.remove(user)
                print(f"Student with ID {student_id} has been removed.")
                return
        print(f"Student with ID {student_id} not found.")

    @staticmethod
    def remove_instructor(instructor_id):
        """Removes an instructor by their ID."""
        for user in UserManager._users:
            if isinstance(user, Instructor) and user._id == instructor_id:
                UserManager._users.remove(user)
                print(f"Instructor with ID {instructor_id} has been removed.")
                return
        print(f"Instructor with ID {instructor_id} not found.")

class PlatformAdmin:
    def __init__(self, admin_id, admin_name):
        self._id = admin_id  # Unique identifier for the admin
        self._admin_name = admin_name

    def display_profile(self):
        print(f"Admin Profile:\nID: {self._id}\nName: {self._first_name}")

    def __str__(self):
        return f"Admin: {self._first_name} (ID: {self._id})"

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
        if not CourseManager._courses:
            print("No courses available.")
            return
        for course in CourseManager._courses:
            print(course)
    
    @staticmethod
    def view_available_courses():
        """Displays courses not assigned to any instructor."""
        available_courses = [course for course in CourseManager._courses if course._instructor is None]
        if not available_courses:
            print("No available courses at the moment.")
            return
        print("\n--- Available Courses ---")
        for course in available_courses:
            print(course)
    @staticmethod
    def apply_to_course(instructor, course):
        """Allows an instructor to apply for a course."""
        if course._instructor:
            print(f"Course {course._name} already has an assigned instructor: {course._instructor._first_name} {course._instructor._last_name}.")
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

class EnrollmentManager:
    _enrollments = []

    
    @staticmethod
    def create_enrollment(student, course):
    # Check for duplicate enrollments
        for enrollment in EnrollmentManager._enrollments:
            if enrollment._student == student and enrollment._course == course:
                print(f"Student {student._first_name} {student._last_name} is already enrolled or has a pending enrollment in course {course._name}.")
            return None

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
    
class AssignmentManager:
    _assignments = []

    @staticmethod
    def add_assignment(course_id, assignment_id, due_date, description):
        course = CourseManager.get_course_by_id(course_id)
        if not course:
            print("Course not found. Assignment not created.")
            return

        assignment = Assignment(assignment_id, course, due_date, description)
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
    def grade_assignment(assignment_id, student_id, grade, max_grade):
        """Grades a student's submitted assignment with max grade validation."""
        assignment = AssignmentManager.get_assignment_by_id(assignment_id)
        if not assignment:
                print("Assignment not found.")
                return

        student = UserManager.find_user_by_id(student_id)
        if not student or not isinstance(student, Student):
                print("Student not found.")
                return

        assignment.grade(student, grade, max_grade)

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

class GradeManager:
    _grades = []

    @staticmethod
    def assign_grade(student, course, grade_value):
        """Assign a grade to a specific student for a course."""
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
        """Allows an instructor to grade all students in a course."""
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
        for student in course._enrolled_students:
            try:
                grade_value = float(input(f"Enter grade for {student._first_name} {student._last_name}: "))
                GradeManager.assign_grade(student, course, grade_value)  # Reuse assign_grade method
            except ValueError:
                print(f"Invalid input. Skipping {student._first_name} {student._last_name}.")

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
        print(f"\n--- Student Menu ({student._first_name} {student._last_name}) ---")
        print("1. View Profile")
        print("2. View Available Courses")
        print("3. Enroll in Course")
        print("4. View Grades")
        print("5. View Assignments")
        print("6. Submit Assignment")
        print("7. Notifications")
        print("8. Logout")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            student.display_profile()
        elif choice == "2":
            CourseManager.view_all_courses()
        elif choice == "3":
            course_id = input("Enter Course ID to enroll: ")
            course = CourseManager.get_course_by_id(course_id)
            if course:
                EnrollmentManager.create_enrollment(student, course)
        elif choice == "4":
            GradeManager.view_student_grades(student)

        elif choice == "5":  # View Assignments
            course_id = input("Enter Course ID to view assignments: ").strip()
            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
            else:
                AssignmentManager.view_all_assignments(course)

        elif choice == "6":
            assignment_id = input("Enter Assignment ID to submit: ")
            AssignmentManager.submit_assignment(student, assignment_id)
        elif choice == "7":
            print("Feature not implemented: Notifications will be handled later.")
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def instructor_menu(instructor):
    while True:
        print(f"\n--- Instructor Menu ({instructor._first_name} {instructor._last_name}) ---")
        print("1. View Profile")
        print("2. View Available Courses")
        print("3. Apply to Course")
        print("4. Add Assignment")
        print("5. Grade Assignment")
        print("6. Grade Course")
        print("7. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            instructor.display_profile()
        elif choice == "2":
            CourseManager.view_available_courses()

        elif choice == "3":  # Apply to Course
            course_id = input("Enter Course ID to apply for: ").strip()
            course = CourseManager.get_course_by_id(course_id)
            if not course:
                print("Course not found.")
            else:
                CourseManager.apply_to_course(instructor, course)


        elif choice == "4":  # Add Assignment
            course_id = input("Enter Course ID: ")
            assignment_id = input("Enter Assignment ID: ")
            due_date = input("Enter Due Date (MM/DD/YYYY): ")
            description = input("Enter Assignment Description: ")
            AssignmentManager.add_assignment(course_id, assignment_id, due_date, description)

        elif choice == "5":  # Grade Assignment
            assignment_id = input("Enter Assignment ID: ").strip()
            student_id = input("Enter Student ID to grade: ").strip()
            max_grade = float(input("Enter Maximum Grade: "))  # Prompt for maximum grade
            grade = float(input("Enter Grade to assign: "))  # Prompt for grade
            AssignmentManager.grade_assignment(assignment_id, student_id, grade, max_grade)  # Pass max_grade


        elif choice == "6":  # Grade Course
            course_id = input("Enter Course ID to grade: ").strip()
            GradeManager.grade_course(course_id, instructor)


        elif choice == "7":
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
        print("4. Assign Instructor to Course")
        print("5. Approve/Reject Student Enrollments")
        print("6. Drop Student/Instructor")
        print("7. Logout")
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

        elif choice == "4":  # Assign Instructor to Course
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


        elif choice == "5":  # Approve/Reject Enrollments
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

        elif choice == "6":  # Drop Student/Instructor
            print("Options:\n1. Drop Student\n2. Drop Instructor")
            sub_choice = input("Choose an option: ")
            user_id = input("Enter User ID: ")

            if sub_choice == "1":
                UserManager.remove_student(user_id)
            elif sub_choice == "2":
                UserManager.remove_instructor(user_id)
            else:
                print("Invalid option.")

        elif choice == "7":  # Logout
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    print("Welcome to the E-Learning Platform!")
    general_menu()

# Entry Point
if __name__ == "__main__":
    main()
