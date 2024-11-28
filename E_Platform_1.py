from abc import ABC, abstractmethod
from datetime import datetime
import json

# User Class
class User(ABC):    
    def __init__(self, user_id, name, email, phone_number, password):
        self.__id = user_id
        self.name = name
        self._email = email
        self._phone_number = phone_number
        self._password = password

    @abstractmethod
    def get_details(self):
        pass

    def get_id(self):
        return self.__id

    def set_email(self, email):
        self._email = email

    def get_email(self):
        return self._email


# Student Class
class Student(User):
    def __init__(self, user_id, name, email, phone_number, student_id):
        super().__init__(user_id, name, email, phone_number)
        self.student_id = student_id
        self._enrolled_courses = []

    def enroll_in_course(self, course):
        if course not in self._enrolled_courses:
            self._enrolled_courses.append(course)
        else:
            raise ValueError(f"Already enrolled in course: {course.title}")

    def drop_course(self, course):
        if course in self._enrolled_courses:
            self._enrolled_courses.remove(course)
        else:
            raise ValueError("Course not found in enrolled courses.")

    def get_enrolled_courses(self):
        return self._enrolled_courses

    def get_details(self):
        return (f"Student ID: {self.get_id()}, Name: {self.name}, "
                f"Email: {self._email}, Phone: {self._phone_number}")


# Instructor Class
class Instructor(User):
    def __init__(self, user_id, name, email, phone_number, instructor_id):
        super().__init__(user_id, name, email, phone_number)
        self.instructor_id = instructor_id
        self._assigned_courses = []

    def assign_course(self, course):
        if course not in self._assigned_courses:
            self._assigned_courses.append(course)
        else:
            raise ValueError(f"Course {course.title} is already assigned.")

    def remove_assigned_course(self, course):
        if course in self._assigned_courses:
            self._assigned_courses.remove(course)
        else:
            raise ValueError("Course not found in assigned courses.")

    def get_assigned_courses(self):
        return self._assigned_courses

    def get_details(self):
        return (f"Instructor ID: {self.get_id()}, Name: {self.name}, "
                f"Email: {self._email}, Phone: {self._phone_number}")


# Enrollment Class
class Enrollment:
    def __init__(self, student, course):
        self.student = student
        self.course = course
        self.enrollment_date = datetime.now()
        self.grade = None  # Link to a Grade object later if needed

    def __str__(self):
        return f"Enrollment: {self.student.name} in {self.course.title} on {self.enrollment_date}"

class Grade:
    def __init__(self, student, course):
        self.student = student
        self.course = course
        self.assignments = {}  # {assignment_id: grade_details}

    def add_grade(self, assignment_id, grade_value):
        if assignment_id in self.assignments:
            raise ValueError("Grade for this assignment already exists.")
        self.assignments[assignment_id] = {
            "grade_value": grade_value,
            "date_assigned": datetime.now(),
        }

    def update_grade(self, assignment_id, grade_value):
        if assignment_id in self.assignments:
            self.assignments[assignment_id]["grade_value"] = grade_value
            self.assignments[assignment_id]["date_updated"] = datetime.now()
        else:
            raise ValueError("No grade found for this assignment.")

    def get_grade(self, assignment_id):
        return self.assignments.get(assignment_id, None)

    def get_all_grades(self):
        return self.assignments

    def __str__(self):
        return f"Grades for {self.student.name} in {self.course.title}: {self.assignments}"


# Course Class
class Course:
    def __init__(self, course_id, title, description, instructor=None, schedule=None):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.instructor = instructor
        self.students_enrolled = []
        self.assignments = []
        self.schedule = schedule

    def add_student(self, student):
        if student not in self.students_enrolled:
            self.students_enrolled.append(student)
            student.enroll_in_course(self)
        else:
            raise ValueError(f"Student {student.name} is already enrolled in this course.")

    def remove_student(self, student):
        if student in self.students_enrolled:
            self.students_enrolled.remove(student)
            student.drop_course(self)
        else:
            raise ValueError(f"Student {student.name} is not enrolled in this course.")

    def add_assignment(self, assignment):
        if assignment not in self.assignments:
            self.assignments.append(assignment)
        else:
            raise ValueError(f"Assignment {assignment.title} already exists.")

    def set_instructor(self, instructor):
        self.instructor = instructor
        instructor.assign_course(self)

    def get_course_details(self):
        return {
            "course_id": self.course_id,
            "title": self.title,
            "description": self.description,
            "instructor": self.instructor.name if self.instructor else "No instructor assigned",
            "students_enrolled": [student.name for student in self.students_enrolled],
            "assignments": [assignment.title for assignment in self.assignments],
            "schedule": self.schedule if self.schedule else "No schedule set",
        }

from datetime import datetime

class Assignment:
    def __init__(self, assignment_id, title, description, due_date, max_score):
        self.assignment_id = assignment_id  # Unique identifier for the assignment
        self.title = title  # Title of the assignment
        self.description = description  # Brief description of the assignment
        self.due_date = due_date  # Deadline for submission
        self.max_score = max_score  # Maximum score for the assignment
        self.submissions = {}  # Stores submissions as {student_id: {"submission": str, "score": int, "date_submitted": datetime}}

    def submit_assignment(self, student_id, submission_text):
        if student_id not in self.submissions:
            if datetime.now() <= self.due_date:
                self.submissions[student_id] = {
                    "submission": submission_text,
                    "score": None,  # Score is assigned later by the instructor
                    "date_submitted": datetime.now(),
                }
            else:
                raise ValueError("Submission deadline has passed.")
        else:
            raise ValueError(f"Student ID {student_id} has already submitted this assignment.")

    def grade_submission(self, student_id, score):
        if student_id in self.submissions:
            if score <= self.max_score:
                self.submissions[student_id]["score"] = score
            else:
                raise ValueError(f"Score exceeds the maximum score of {self.max_score}.")
        else:
            raise ValueError(f"No submission found for student ID {student_id}.")

    def get_submission(self, student_id):
        if student_id in self.submissions:
            return self.submissions[student_id]
        else:
            raise ValueError(f"No submission found for student ID {student_id}.")

    def get_all_submissions(self):
        return self.submissions

    def __str__(self):
        return (f"Assignment ID: {self.assignment_id}, Title: {self.title}, "
                f"Description: {self.description}, Due Date: {self.due_date}, "
                f"Max Score: {self.max_score}, Submissions: {len(self.submissions)}")

class Schedule:
    def __init__(self, course_id, start_date, end_date, sessions):
        """
        :param course_id: The course ID the schedule is associated with.
        :param start_date: The start date of the course.
        :param end_date: The end date of the course.
        :param sessions: A list of session timings, e.g., ["Monday 10:00-12:00", "Wednesday 14:00-16:00"]
        """
        self.course_id = course_id
        self.start_date = start_date
        self.end_date = end_date
        self.sessions = sessions

    def update_schedule(self, new_sessions):
        """Update the session timings."""
        self.sessions = new_sessions

    def get_schedule_details(self):
        """Return schedule information."""
        return {
            "course_id": self.course_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "sessions": self.sessions,
        }

    def __str__(self):
        return (f"Course ID: {self.course_id}, Start: {self.start_date}, "
                f"End: {self.end_date}, Sessions: {', '.join(self.sessions)}")
            
class PlatformAdmin:
    def __init__(self, admin_id, name, email, phone_number):
        self.admin_id = admin_id
        self.name = name
        self._email = email
        self._phone_number = phone_number
        self.created_courses = []

    def create_course(self, course_id, title, description, schedule=None):
        course = Course(course_id, title, description, schedule=schedule)
        self.created_courses.append(course)
        return course

    def update_course(self, course, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(course, attr):
                setattr(course, attr, value)

    def delete_course(self, course, all_courses):
        if course in self.created_courses:
            self.created_courses.remove(course)
            all_courses.remove(course)  # Assuming `all_courses` is a global list of courses
        else:
            raise ValueError("Course not found in admin's created courses.")

    def create_user(self, user_type, **kwargs):
        if user_type == "Student":
            return Student(**kwargs)
        elif user_type == "Instructor":
            return Instructor(**kwargs)
        else:
            raise ValueError("Invalid user type.")

    def delete_user(self, user, all_users):
        if user in all_users:
            all_users.remove(user)
        else:
            raise ValueError("User not found.")

    def view_logs(self):
        # Optional: Add logic for viewing system logs
        pass

    def __str__(self):
        return f"Admin ID: {self.admin_id}, Name: {self.name}, Email: {self._email}"
    
class UserManager:
    def __init__(self):
        self.users = []  # List to store all user objects

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
        else:
            raise ValueError("User not found.")

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email

    @classmethod
    def count_users(cls, users):
        return len(users)

    def get_all_users(self):
        return [user.get_details() for user in self.users]

class Login:
    def __init__(self, users,):
        self.users = users  
        self.current_user = None

    def authenticate(self, email, password):
        user = self.users.get(email)
        if user and user._password == password:  
            return True
        return False


    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user
    
import os

class JSONHandler:
    @staticmethod
    def save_to_file(data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, default=str)

    @staticmethod
    def load_from_file(filename):
        if not os.path.exists(filename):  # Check if the file exists
            with open(filename, 'w') as file:
                json.dump([], file)  # Create an empty file
        with open(filename, 'r') as file:
            return json.load(file)


class MenuSystem:
    def __init__(self, users, all_courses):
        self.users = users  # Dictionary of users (email: user_object)
        self.all_courses = all_courses  # List of all course objects
        self.login = Login(users)

    def prepopulate_data(users, all_courses):
        # Add instructors
        instructor1 = Instructor(user_id=1, name="Alice", email="alice@example.com", phone_number="1234567890", instructor_id=101)
        instructor2 = Instructor(user_id=2, name="Bob", email="bob@example.com", phone_number="0987654321", instructor_id=102)
        users[instructor1.get_email()] = instructor1
        users[instructor2.get_email()] = instructor2

        # Add students
        student1 = Student(user_id=3, name="Charlie", email="charlie@example.com", phone_number="1112223333", student_id=201)
        student2 = Student(user_id=4, name="Diana", email="diana@example.com", phone_number="4445556666", student_id=202)
        users[student1.get_email()] = student1
        users[student2.get_email()] = student2

        # Add courses
        course1 = Course(course_id="C101", title="Python Basics", description="Learn Python from scratch.", instructor=instructor1)
        course2 = Course(course_id="C102", title="Data Science", description="Intro to Data Science concepts.", instructor=instructor2)
        all_courses.append(course1)
        all_courses.append(course2)

        # Enroll students in courses
        course1.add_student(student1)
        course2.add_student(student2)

    print("Data prepopulated successfully!")


    def main_menu(self):
        while True:
            print("\n=== E-Learning Platform ===")
            print("1. Login")
            print("2. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.login_menu()
            elif choice == "2":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    def login_menu(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

        if self.login.authenticate(email, password):
            user = self.login.get_current_user()
            if isinstance(user, Instructor):
                self.instructor_menu(user)
            elif isinstance(user, Student):
                self.student_menu(user)
        else:
            print("Invalid email or password. Please try again.")

    def instructor_menu(self, instructor):
        while True:
            print(f"\n=== Instructor Menu: {instructor.name} ===")
            print("1. View Assigned Courses")
            print("2. Create New Course")
            print("3. Add Assignment")
            print("4. Grade Assignment")
            print("5. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                courses = instructor.get_assigned_courses()
                if courses:
                    print("\nAssigned Courses:")
                    for course in courses:
                        print(f"- {course.title}")
                else:
                    print("No assigned courses yet.")
            elif choice == "2":
                self.create_course(instructor)
            elif choice == "3":
                self.add_assignment(instructor)
            elif choice == "4":
                self.grade_assignment(instructor)
            elif choice == "5":
                self.login.logout()
                print("Logged out.")
                break
            else:
                print("Invalid choice. Try again.")

    def student_menu(self, student):
        while True:
            print(f"\n=== Student Menu: {student.name} ===")
            print("1. View Enrolled Courses")
            print("2. Enroll in a Course")
            print("3. Submit Assignment")
            print("4. View Grades")
            print("5. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                courses = student.get_enrolled_courses()
                if courses:
                    print("\nEnrolled Courses:")
                    for course in courses:
                        print(f"- {course.title}")
                else:
                    print("No courses enrolled yet.")
            elif choice == "2":
                self.enroll_course(student)
            elif choice == "3":
                self.submit_assignment(student)
            elif choice == "4":
                self.view_grades(student)
            elif choice == "5":
                self.login.logout()
                print("Logged out.")
                break
            else:
                print("Invalid choice. Try again.")

    def create_course(self, instructor):
        course_id = input("Enter course ID: ")
        title = input("Enter course title: ")
        description = input("Enter course description: ")
        course = Course(course_id, title, description, instructor=instructor)
        self.all_courses.append(course)
        instructor.assign_course(course)
        print(f"Course '{title}' created successfully!")

    def add_assignment(self, instructor):
        courses = instructor.get_assigned_courses()
        if not courses:
            print("No assigned courses. Create a course first.")
            return

        print("\nAssigned Courses:")
        for i, course in enumerate(courses):
            print(f"{i + 1}. {course.title}")

        choice = int(input("Select a course to add assignment (1-N): ")) - 1
        if 0 <= choice < len(courses):
            course = courses[choice]
            assignment_id = input("Enter assignment ID: ")
            title = input("Enter assignment title: ")
            description = input("Enter description: ")
            due_date = datetime.strptime(input("Enter due date (YYYY-MM-DD): "), "%Y-%m-%d")
            max_score = int(input("Enter max score: "))
            assignment = Assignment(assignment_id, title, description, due_date, max_score)
            course.add_assignment(assignment)
            print(f"Assignment '{title}' added to course '{course.title}'!")
        else:
            print("Invalid selection.")

    def grade_assignment(self, instructor):
        courses = instructor.get_assigned_courses()
        if not courses:
            print("No assigned courses. Create a course first.")
            return

        print("\nAssigned Courses:")
        for i, course in enumerate(courses):
            print(f"{i + 1}. {course.title}")

        choice = int(input("Select a course to grade (1-N): ")) - 1
        if 0 <= choice < len(courses):
            course = courses[choice]
            assignments = course.assignments
            if not assignments:
                print("No assignments in this course.")
                return

            print("\nAssignments:")
            for i, assignment in enumerate(assignments):
                print(f"{i + 1}. {assignment.title}")

            assignment_choice = int(input("Select an assignment to grade (1-N): ")) - 1
            if 0 <= assignment_choice < len(assignments):
                assignment = assignments[assignment_choice]
                student_id = input("Enter student ID: ")
                score = int(input("Enter score: "))
                assignment.grade_submission(student_id, score)
                print(f"Student {student_id} graded for assignment '{assignment.title}'!")
            else:
                print("Invalid selection.")
        else:
            print("Invalid selection.")

    def enroll_course(self, student):
        course_id = input("Enter course ID to enroll: ")
        course = next((c for c in self.all_courses if c.course_id == course_id), None)
        if course:
            try:
                course.add_student(student)
                print(f"Enrolled in course '{course.title}' successfully!")
            except ValueError as e:
                print(e)
        else:
            print("Course not found.")

    def submit_assignment(self, student):
        courses = student.get_enrolled_courses()
        if not courses:
            print("No enrolled courses. Enroll in a course first.")
            return

        print("\nEnrolled Courses:")
        for i, course in enumerate(courses):
            print(f"{i + 1}. {course.title}")

        choice = int(input("Select a course to submit assignment (1-N): ")) - 1
        if 0 <= choice < len(courses):
            course = courses[choice]
            assignments = course.assignments
            if not assignments:
                print("No assignments in this course.")
                return

            print("\nAssignments:")
            for i, assignment in enumerate(assignments):
                print(f"{i + 1}. {assignment.title}")

            assignment_choice = int(input("Select an assignment to submit (1-N): ")) - 1
            if 0 <= assignment_choice < len(assignments):
                assignment = assignments[assignment_choice]
                submission_text = input("Enter your submission: ")
                assignment.submit_assignment(student.student_id, submission_text)
                print(f"Submitted assignment '{assignment.title}' successfully!")
            else:
                print("Invalid selection.")
        else:
            print("Invalid selection.")

    def view_grades(self, student):
        print("\nYour Grades:")
        for course in student.get_enrolled_courses():
            grades = Grade(student, course).get_all_grades()
            print(f"Course: {course.title}")
            for assignment, details in grades.items():
                print(f"  Assignment: {assignment}, Grade: {details.get('grade_value', 'Not graded')}")

if __name__ == "__main__":
    users = {}  # Dictionary for user storage
    all_courses = []  # List for course storage
    

 
    # Initialize and run the menu system
    menu = MenuSystem(users, all_courses)
    menu.main_menu()

