"""
Quiz-enabled Student Management System with File Handling
--------------------------------------------------------
"""

import json
import os
import random
from datetime import datetime

USERS_FILE = "users.json"
SCORES_FILE = "scores.txt"


students = {}
curr_user = None      
curr_role = None      


ADMIN_CREDENTIALS = {
    "admin": "admin123"
}



QUIZ_QUESTIONS = {
    "DSA": [
        {
            "question": "Which data structure uses FIFO (First In First Out)?",
            "options": ["Stack", "Queue", "Tree", "Graph"],
            "answer": 2,
        },
        {
            "question": "What is the time complexity of binary search (on sorted array)?",
            "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"],
            "answer": 2,
        },
        {
            "question": "Which traversal of a binary search tree gives sorted order?",
            "options": ["Preorder", "Postorder", "Inorder", "Level order"],
            "answer": 3,
        },
        {
            "question": "Which data structure is used for function call management in memory?",
            "options": ["Queue", "Stack", "Array", "Linked List"],
            "answer": 2,
        },
        {
            "question": "Which of these is a linear data structure?",
            "options": ["Tree", "Graph", "Stack", "Trie"],
            "answer": 3,
        },
    ],
    "DBMS": [
        {
            "question": "What does SQL stand for?",
            "options": [
                "Structured Query Language",
                "Simple Query Language",
                "Sequential Query Language",
                "Standard Query List",
            ],
            "answer": 1,
        },
        {
            "question": "Which of the following is a primary key property?",
            "options": ["Can be NULL", "Can be duplicate", "Unique & Not NULL", "Always text"],
            "answer": 3,
        },
        {
            "question": "Which SQL command is used to remove a table and its data?",
            "options": ["DELETE", "DROP", "REMOVE", "TRUNCATE"],
            "answer": 2,
        },
        {
            "question": "Which normal form removes partial dependency?",
            "options": ["1NF", "2NF", "3NF", "BCNF"],
            "answer": 2,
        },
        {
            "question": "Which of these is a DML command?",
            "options": ["CREATE", "ALTER", "INSERT", "DROP"],
            "answer": 3,
        },
    ],
    "PYTHON": [
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["func", "def", "function", "lambda"],
            "answer": 2,
        },
        {
            "question": "What is the output of: len([1, 2, 3])?",
            "options": ["2", "3", "4", "Error"],
            "answer": 2,
        },
        {
            "question": "Which of these is used to handle exceptions in Python?",
            "options": ["if-else", "for", "try-except", "lambda"],
            "answer": 3,
        },
        {
            "question": "How do you start a comment in Python?",
            "options": ["//", "/*", "#", "<!--"],
            "answer": 3,
        },
        {
            "question": "Which data type is immutable?",
            "options": ["List", "Dictionary", "Set", "Tuple"],
            "answer": 4,
        },
    ],
}




def load_users():
    
    global students
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                students = json.load(f)
        except json.JSONDecodeError:
            students = {}
    else:
        students = {}


def save_users():
   
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4)


def append_score(enrollment, category, marks, total):
  
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = f"{enrollment},{category},{marks}/{total},{now}\n"
    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(record)


def get_user_scores(enrollment):
   
    results = []
    if not os.path.exists(SCORES_FILE):
        return results

    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 4:
                continue
            enr, category, marks, dt = parts[0], parts[1], parts[2], ",".join(parts[3:])
            if enr == enrollment:
                results.append((enr, category, marks, dt))
    return results


def get_all_scores():
   
    results = []
    if not os.path.exists(SCORES_FILE):
        return results
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 4:
                continue
            enr, category, marks, dt = parts[0], parts[1], parts[2], ",".join(parts[3:])
            results.append((enr, category, marks, dt))
    return results



def register():
    print("- REGISTER NEW STUDENT -")
    username = input(" Enter Username: ").strip()

    if not username:
        print(" Username cannot be empty.")
        return

    if username in students:
        print(" Username already exists.")
        return

    password = input(" Enter Password: ").strip()
    full_name = input(" Enter Full Name: ").strip()
    email = input(" Enter Email: ").strip()
    phoneno = input(" Enter Phone Number: ").strip()
    dob = input(" Date of Birth: ").strip()
    gender = input(" Gender: ").strip()
    address = input(" Enter your Address: ").strip()
    course = input(" Course / Branch: ").strip()
    year = input(" Year of Study: ").strip()
    student_id = input(" Enrollment / Student ID: ").strip()

    if not student_id:
        print(" Enrollment / Student ID cannot be empty.")
        return

    students[username] = {
        "username": username,
        "password": password,
        "full_name": full_name,
        "email": email,
        "phone": phoneno,
        "dob": dob,
        "gender": gender,
        "address": address,
        "course": course,
        "year": year,
        "student_id": student_id,
        "role": "user",
    }

    save_users()
    print(" Registration successful.")


def login():
    global curr_user, curr_role
    print("-LOGIN _")
    print(" 1. User Login")
    print(" 2. Admin Login")
    choice = input(" Choose option (1/2): ").strip()

    if choice == "2":
        username = input(" Admin Username: ").strip()
        password = input(" Admin Password: ").strip()
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            curr_user = username
            curr_role = "admin"
            print(f" Welcome Admin, {username}!")
        else:
            print(" Invalid admin credentials.")
        return

   
    username = input(" Username: ").strip()
    password = input(" Password: ").strip()

    user = students.get(username)
    if user and user.get("password") == password:
        curr_user = username
        curr_role = user.get("role", "user")
        print(f" Welcome, {user.get('full_name', username)}!")
    else:
        print(" Invalid username or password.")


def show_profile():
    if curr_user is None or curr_role != "user":
        print(" You must be logged in as a USER to view profile.")
        return

    user = students[curr_user]
    print("- YOUR PROFILE -")
    for key, value in user.items():
        if key in ["password", "role", "username"]:
            continue
        print(f" {key.replace('_', ' ').title()}: {value}")


def update_profile():
    if curr_user is None or curr_role != "user":
        print(" You must be logged in as a USER to update profile.")
        return

    print("\n--- UPDATE PROFILE ---")
    user = students[curr_user]

    editable_fields = ["full_name", "email", "phone", "course", "year", "address"]
    for key in editable_fields:
        old_val = user.get(key, "")
        new_val = input(f" {key.replace('_', ' ').title()} [{old_val}]: ").strip()
        if new_val:
            user[key] = new_val

    change_password = input(" Do you want to change your password (y/n): ").strip().lower()
    if change_password == "y":
        new_pass = input(" Enter new Password: ").strip()
        if new_pass:
            user["password"] = new_pass
            print(" Password updated successfully.")

    students[curr_user] = user
    save_users()
    print(" Profile updated.")


def logout():
    global curr_user, curr_role
    if curr_user:
        print(f" Logged out from '{curr_user}'.")
        curr_user = None
        curr_role = None
    else:
        print(" No user is currently logged in.")




def choose_category():
    print("- QUIZ CATEGORY -")
    print(" 1. DSA")
    print(" 2. DBMS")
    print(" 3. PYTHON")
    choice = input(" Choose category (1-3): ").strip()
    if choice == "1":
        return "DSA"
    elif choice == "2":
        return "DBMS"
    elif choice == "3":
        return "PYTHON"
    else:
        print(" Invalid category choice.")
        return None


def attempt_quiz():
    if curr_user is None or curr_role != "user":
        print(" You must be logged in as a USER to attempt quiz.")
        return

    category = choose_category()
    if category is None:
        return

    questions = QUIZ_QUESTIONS.get(category, [])
    if not questions:
        print(" No questions available for this category.")
        return

    
    temp_questions = questions[:]
    random.shuffle(temp_questions)
    num_questions = min(5, len(temp_questions))
    selected = temp_questions[:num_questions]

    score = 0
    print(f"-- {category} QUIZ -")
    for idx, q in enumerate(selected, start=1):
        print(f"\nQ{idx}. {q['question']}")
        for i, opt in enumerate(q["options"], start=1):
            print(f"  {i}. {opt}")
        try:
            ans = int(input(" Your answer (1-4): ").strip())
        except ValueError:
            ans = 0
        if ans == q["answer"]:
            score += 1
            print(" Correct!")
        else:
            print(f" Wrong! Correct option is {q['answer']}.")

    print(f"\nQuiz Completed. Your Score: {score}/{num_questions}")

    enrollment = students[curr_user].get("student_id", "NA")
    append_score(enrollment, category, score, num_questions)


def show_my_scores():
    if curr_user is None or curr_role != "user":
        print(" You must be logged in as a USER to view scores.")
        return

    enrollment = students[curr_user].get("student_id", "NA")
    records = get_user_scores(enrollment)

    print("\n--- YOUR QUIZ SCORES ---")
    if not records:
        print(" No quiz attempts found.")
        return

    print(" Enrollment | Category | Marks | Date & Time")
    print(" -------------------------------------------")
    for enr, category, marks, dt in records:
        print(f" {enr} | {category} | {marks} | {dt}")


def admin_view_all_scores():
    if curr_role != "admin":
        print(" Only ADMIN can view all scores.")
        return

    records = get_all_scores()
    print("\n--- ALL QUIZ SCORES (ADMIN) ---")
    if not records:
        print(" No quiz scores found.")
        return

    print(" Enrollment | Category | Marks | Date & Time")
    print(" -------------------------------------------")
    for enr, category, marks, dt in records:
        print(f" {enr} | {category} | {marks} | {dt}")




def main_menu():
    while True:
        print(" __STUDENT MANAGEMENT & QUIZ SYSTEM __")
        print("1. Register")
        print("2. Login (User/Admin)")
        print("3. Attempt Quiz")
        print("4. View My Profile")
        print("5. Update My Profile")
        print("6. View My Quiz Scores")
        print("7. Logout")
        print("8. Admin: View All Scores")
        print("9. Exit")

        choice = input(" Enter your choice (1-9): ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            attempt_quiz()
        elif choice == "4":
            show_profile()
        elif choice == "5":
            update_profile()
        elif choice == "6":
            show_my_scores()
        elif choice == "7":
            logout()
        elif choice == "8":
            admin_view_all_scores()
        elif choice == "9":
            print(" Exiting system. Goodbye!")
            break
        else:
            print(" Invalid option. Please enter a number between 1 and 9.")


load_users()
main_menu()
