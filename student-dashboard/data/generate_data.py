"""
data/generate_data.py

Generates a realistic synthetic dataset for 200 students with marks across 5 subjects,
attendance, total, percentage, and assigned grades.
Uses standard library modules so it runs without dependencies.
"""

import csv
import math
import os
import random


def generate_student_data(num_students: int = 200, seed: int = 42):
    """Generates realistic student performance records as a list of dictionaries.

    Args:
        num_students (int): Number of student records to generate.
        seed (int): Random seed for reproducibility.

    Returns:
        list[dict]: List of generated student record dictionaries.
    """
    random.seed(seed)

    first_names = [
        "Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Sneha", "Aditya", "Diya",
        "Karan", "Isha", "Rahul", "Meera", "Siddharth", "Riya", "Dev", "Kavya",
        "Arjun", "Anushka", "Nikhil", "Pooja", "Varun", "Tanvi", "Yash", "Neha",
        "Amit", "Shreya", "Raj", "Simran", "Manish", "Kritika"
    ]
    last_names = [
        "Sharma", "Verma", "Patel", "Gupta", "Rao", "Nair", "Reddy", "Singh",
        "Joshi", "Kumar", "Bhat", "Mehta", "Deshmukh", "Chopra", "Kulkarni",
        "Mishra", "Agarwal", "Saxena", "Shah", "Pandey"
    ]

    departments = [
        "Computer Science",
        "Data Science",
        "Artificial Intelligence",
        "Information Technology"
    ]
    genders = ["Male", "Female"]
    semesters = [3, 4, 5, 6]

    subjects = ["Maths", "Python", "DBMS", "Data Structures", "Java"]

    records = []

    for i in range(1, num_students + 1):
        student_id = f"DS{2024000 + i}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        gender = random.choice(genders)
        department = random.choice(departments)
        semester = random.choice(semesters)

        # Realistic attendance centered around 82%
        attendance = round(random.gauss(82, 9), 1)
        attendance = max(50.0, min(100.0, attendance))

        # Marks correlated with attendance
        base_performance = (attendance / 100.0) * 18

        subject_marks = {}
        for sub in subjects:
            mark = int(random.gauss(62 + base_performance, 11))
            mark = max(28, min(100, mark))
            subject_marks[sub] = mark

        total = sum(subject_marks.values())
        percentage = round(total / 5.0, 2)

        # Grade assignment logic
        if percentage >= 85:
            grade = "A+"
        elif percentage >= 75:
            grade = "A"
        elif percentage >= 65:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        elif percentage >= 40:
            grade = "D"
        else:
            grade = "F"

        record = {
            "student_id": student_id,
            "name": name,
            "gender": gender,
            "department": department,
            "semester": semester,
            "attendance_percent": attendance,
            "Maths": subject_marks["Maths"],
            "Python": subject_marks["Python"],
            "DBMS": subject_marks["DBMS"],
            "Data Structures": subject_marks["Data Structures"],
            "Java": subject_marks["Java"],
            "total": total,
            "percentage": percentage,
            "grade": grade
        }
        records.append(record)

    return records


def save_to_csv(records, output_path):
    """Saves records list to CSV file."""
    if not records:
        return
    fieldnames = list(records[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "students.csv")

    students = generate_student_data(num_students=200)
    save_to_csv(students, csv_path)
    print(f"Successfully generated {len(students)} student records at '{csv_path}'.")
