"""
SCHOOL PORTAL DATA SEEDER
Populate database with realistic demo data for all school portal modules.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from school_portal_helpers import *

DB_PATH = Path(__file__).resolve().parent / "abdul_project.db"


class SchoolPortalSeeder:
    """Seed school portal with demo data."""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)
    
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def seed_all(self):
        """Seed all data."""
        print("🌱 Starting School Portal Data Seeding...\n")
        
        self.seed_students()
        print("✓ Students seeded")
        
        self.seed_teachers()
        print("✓ Teachers seeded")
        
        self.seed_classes()
        print("✓ Classes seeded")
        
        self.seed_subjects()
        print("✓ Subjects seeded")
        
        self.seed_attendance()
        print("✓ Attendance records seeded")
        
        self.seed_exams()
        print("✓ Exams seeded")
        
        self.seed_exam_results()
        print("✓ Exam results seeded")
        
        self.seed_assignments()
        print("✓ Assignments seeded")
        
        self.seed_assignment_submissions()
        print("✓ Assignment submissions seeded")
        
        self.seed_fees()
        print("✓ Fees seeded")
        
        self.seed_payments()
        print("✓ Payments seeded")
        
        self.seed_timetable()
        print("✓ Timetable seeded")
        
        self.seed_libraries()
        print("✓ Library books seeded")
        
        self.seed_book_transactions()
        print("✓ Book transactions seeded")
        
        self.seed_transports()
        print("✓ Transport records seeded")
        
        self.seed_hostels()
        print("✓ Hostel records seeded")
        
        self.seed_ai_logs()
        print("✓ AI logs seeded")
        
        self.seed_analytics()
        print("✓ Analytics data seeded")
        
        print("\n✅ All data seeded successfully!")
    
    def seed_students(self):
        """Seed student data."""
        students = []
        classes = ["10-A", "10-B", "9-A", "9-B", "8-A", "8-B"]
        
        for i in range(1, 201):
            class_name = random.choice(classes)
            first_name, last_name = generate_random_name()
            student_id = generate_student_id(class_name, i % 40 + 1)
            
            students.append((
                student_id,
                1,  # school_id
                first_name,
                last_name,
                i % 40 + 1,
                class_name,
                random.choice(["A", "B"]),
                f"{first_name.lower()}{i}@student.school.com",
                generate_random_phone(),
                f"Parent {last_name}",
                generate_random_phone(),
                f"parent{i}@email.com",
                (datetime.now() - timedelta(days=random.randint(4000, 6500))).strftime("%Y-%m-%d"),
                f"{i} Main Street, City",
                (datetime.now() - timedelta(days=random.randint(200, 500))).strftime("%Y-%m-%d"),
                None,
                "Active"
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_students 
                (student_id, school_id, first_name, last_name, roll_number, class, section, 
                 email, phone, parent_name, parent_phone, parent_email, date_of_birth, 
                 address, admission_date, photo_url, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                students
            )
            conn.commit()
    
    def seed_teachers(self):
        """Seed teacher data."""
        teachers = []
        subjects = ["Mathematics", "English", "Science", "History", "Computer Science"]
        qualifications = ["B.Ed", "M.Ed", "B.Tech", "M.Sc"]
        
        for i in range(1, 51):
            first_name, last_name = generate_random_name("M" if i % 2 == 0 else "F")
            teacher_id = generate_teacher_id()
            
            teachers.append((
                teacher_id,
                1,  # school_id
                first_name,
                last_name,
                f"teacher{i}@school.com",
                generate_random_phone(),
                random.choice(subjects),
                random.randint(2, 20),
                random.choice(qualifications),
                f"{i} Teacher Lane, City",
                (datetime.now() - timedelta(days=random.randint(8000, 12000))).strftime("%Y-%m-%d"),
                None,
                "Active"
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_teachers 
                (teacher_id, school_id, first_name, last_name, email, phone, 
                 subject_expertise, experience_years, qualification, address, 
                 date_of_birth, photo_url, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                teachers
            )
            conn.commit()
    
    def seed_classes(self):
        """Seed class data."""
        classes = []
        class_names = ["8", "9", "10", "11", "12"]
        
        for class_name in class_names:
            for section in ["A", "B"]:
                class_id = generate_class_id(class_name, section)
                classes.append((
                    class_id,
                    1,  # school_id
                    f"Class {class_name}-{section}",
                    None,
                    section,
                    random.randint(35, 45),
                    "2024",
                    "Active"
                ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_classes 
                (class_id, school_id, class_name, class_teacher_id, section, 
                 total_students, academic_year, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                classes
            )
            conn.commit()
    
    def seed_subjects(self):
        """Seed subject data."""
        subjects = []
        subject_list = [
            ("MATH", "Mathematics"),
            ("ENG", "English"),
            ("SCI", "Science"),
            ("HIST", "History"),
            ("GEO", "Geography"),
            ("CS", "Computer Science"),
            ("PE", "Physical Education"),
            ("ART", "Art")
        ]
        
        for i, (code, name) in enumerate(subject_list * 10):
            subject_id = generate_subject_id(code, str(i % 5 + 8))
            subjects.append((
                subject_id,
                1,  # school_id
                name,
                code,
                None,
                f"CLASS-{i % 5 + 8}-A",
                random.randint(3, 5),
                "Active"
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_subjects 
                (subject_id, school_id, subject_name, subject_code, teacher_id, 
                 class_id, credits, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                subjects
            )
            conn.commit()
    
    def seed_attendance(self):
        """Seed attendance records."""
        attendance_records = []
        
        with self._connect() as conn:
            students = conn.execute("SELECT student_id FROM portal_students LIMIT 100").fetchall()
        
        for student in students:
            student_id = student[0]
            for day in range(1, 31):
                date = f"2024-04-{day:02d}"
                status = random.choice(["Present", "Present", "Present", "Absent", "Leave"])
                attendance_records.append((
                    1,  # school_id
                    student_id,
                    date,
                    status,
                    "Teacher",
                    ""
                ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_attendance 
                (school_id, student_id, attendance_date, status, marked_by, remarks)
                VALUES (?, ?, ?, ?, ?, ?)""",
                attendance_records
            )
            conn.commit()
    
    def seed_exams(self):
        """Seed exam data."""
        exams = []
        exam_types = ["Unit Test", "Mid-Term", "Final Exam", "Quiz"]
        classes = ["10-A", "10-B", "9-A", "9-B"]
        
        for i in range(1, 26):
            exam_id = generate_exam_id()
            exams.append((
                exam_id,
                1,  # school_id
                f"{random.choice(exam_types)} - {i}",
                random.choice(exam_types),
                f"CLASS-{random.choice(classes)}",
                f"SUB-MATH-10-A",
                100,
                (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                60,
                40,
                "Scheduled",
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_exams 
                (exam_id, school_id, exam_name, exam_type, class_id, subject_id, 
                 total_marks, exam_date, duration_minutes, passing_marks, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                exams
            )
            conn.commit()
    
    def seed_exam_results(self):
        """Seed exam results."""
        results = []
        
        with self._connect() as conn:
            exams = conn.execute("SELECT exam_id FROM portal_exams LIMIT 10").fetchall()
            students = conn.execute("SELECT student_id FROM portal_students LIMIT 100").fetchall()
        
        for exam in exams:
            exam_id = exam[0]
            for student in students[:50]:
                student_id = student[0]
                obtained_marks = random.uniform(20, 100)
                percentage = calculate_percentage(obtained_marks, 100)
                grade = format_grade(percentage)
                
                results.append((
                    1,  # school_id
                    exam_id,
                    student_id,
                    obtained_marks,
                    percentage,
                    grade,
                    random.choice(["Pending", "Published"]),
                    ""
                ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_exam_results 
                (school_id, exam_id, student_id, obtained_marks, percentage, 
                 grade, status, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                results
            )
            conn.commit()
    
    def seed_assignments(self):
        """Seed assignment data."""
        assignments = []
        classes = ["10-A", "10-B", "9-A", "9-B"]
        
        for i in range(1, 21):
            assignment_id = generate_assignment_id()
            deadline = (datetime.now() + timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d")
            
            assignments.append((
                assignment_id,
                1,  # school_id
                f"CLASS-{random.choice(classes)}",
                "SUB-MATH-10-A",
                "TCH-2024-ABC1",
                f"Assignment {i}",
                f"Description for assignment {i}",
                random.uniform(10, 50),
                deadline,
                "Active"
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_assignments 
                (assignment_id, school_id, class_id, subject_id, teacher_id, 
                 title, description, total_marks, deadline, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                assignments
            )
            conn.commit()
    
    def seed_assignment_submissions(self):
        """Seed assignment submissions."""
        submissions = []
        
        with self._connect() as conn:
            assignments = conn.execute("SELECT assignment_id FROM portal_assignments LIMIT 15").fetchall()
            students = conn.execute("SELECT student_id FROM portal_students LIMIT 100").fetchall()
        
        for assignment in assignments:
            assignment_id = assignment[0]
            for student in students[:40]:
                student_id = student[0]
                submission_date = datetime.now().strftime("%Y-%m-%d")
                marks = random.uniform(5, 40)
                plagiarism = round(random.uniform(0, 25), 2)
                
                submissions.append((
                    1,  # school_id
                    assignment_id,
                    student_id,
                    submission_date,
                    marks,
                    f"Good work! Score: {marks:.0f}/50",
                    plagiarism,
                    random.choice(["Submitted", "Graded"]),
                ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_assignment_submissions 
                (school_id, assignment_id, student_id, submission_date, marks_obtained, 
                 ai_feedback, plagiarism_score, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                submissions
            )
            conn.commit()
    
    def seed_fees(self):
        """Seed fee data."""
        fees = []
        fee_types = ["Tuition Fee", "Transport Fee", "Library Fee", "Lab Fee", "Sports Fee"]
        amounts = [25000, 5000, 1500, 2000, 1000]
        
        with self._connect() as conn:
            students = conn.execute("SELECT student_id FROM portal_students LIMIT 150").fetchall()
        
        for student in students:
            student_id = student[0]
            for fee_type, amount in zip(fee_types, amounts):
                fee_id = generate_fee_id(student_id)
                due_date = (datetime.now() + timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d")
                
                fees.append((
                    fee_id,
                    1,  # school_id
                    student_id,
                    fee_type,
                    amount,
                    due_date,
                    0,
                    0,
                    random.choice(["Pending", "Paid", "Partial"]),
                    None,
                    None,
                    ""
                ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_fees 
                (fee_id, school_id, student_id, fee_name, amount, due_date, 
                 fine_amount, paid_amount, payment_status, payment_date, receipt_number, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                fees
            )
            conn.commit()
    
    def seed_payments(self):
        """Seed payment records."""
        payments = []
        
        with self._connect() as conn:
            students = conn.execute("SELECT student_id FROM portal_students LIMIT 100").fetchall()
        
        for i, student in enumerate(students):
            student_id = student[0]
            payment_id = generate_payment_id()
            amount = random.choice([5000, 25000, 30000])
            
            payments.append((
                payment_id,
                1,  # school_id
                student_id,
                None,
                amount,
                random.choice(["Cash", "Check", "Online Transfer"]),
                f"TXN-{random.randint(100000, 999999)}",
                random.choice(["Pending", "Verified"]),
                "Admin" if random.random() > 0.7 else None,
                None,
                datetime.now().strftime("%Y-%m-%d")
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_payments 
                (payment_id, school_id, student_id, fee_id, amount, payment_method, 
                 transaction_id, verification_status, verified_by, verified_date, payment_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                payments
            )
            conn.commit()
    
    def seed_timetable(self):
        """Seed timetable data."""
        timetable = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        periods = list(range(1, 5))
        classes = ["10-A", "10-B", "9-A", "9-B"]
        subjects = ["Mathematics", "English", "Science", "History"]
        
        for day in days:
            for period in periods:
                for cls in classes:
                    timetable_id = f"TT-{cls}-{day}-{period}"
                    timetable.append((
                        timetable_id,
                        1,  # school_id
                        f"CLASS-{cls}",
                        day,
                        period,
                        None,
                        None,
                        f"{8 + period}:00",
                        f"{8 + period + 1}:00",
                        f"Room-{random.randint(101, 205)}",
                    ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_timetable 
                (timetable_id, school_id, class_id, day_of_week, period_number, 
                 subject_id, teacher_id, start_time, end_time, room_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                timetable
            )
            conn.commit()
    
    def seed_libraries(self):
        """Seed library books."""
        books = []
        book_titles = [
            ("Calculus", "Author 1", "Mathematics"),
            ("Physics", "Author 2", "Science"),
            ("English Literature", "Author 3", "English"),
            ("World History", "Author 4", "History"),
            ("Python Programming", "Author 5", "Computer Science"),
            ("Biology", "Author 6", "Science"),
            ("Chemistry", "Author 7", "Science"),
            ("Economics", "Author 8", "Social Studies")
        ]
        
        for i, (title, author, category) in enumerate(book_titles * 5):
            book_id = generate_book_id()
            books.append((
                book_id,
                1,  # school_id
                title,
                author,
                f"ISBN-{i}",
                category,
                random.randint(2, 10),
                random.randint(1, 10),
                random.choice(["Available", "Low Stock"]),
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_libraries 
                (book_id, school_id, title, author, isbn, category, 
                 quantity, available_quantity, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                books
            )
            conn.commit()
    
    def seed_book_transactions(self):
        """Seed book borrowing transactions."""
        transactions = []
        
        with self._connect() as conn:
            books = conn.execute("SELECT book_id FROM portal_libraries LIMIT 20").fetchall()
            students = conn.execute("SELECT student_id FROM portal_students LIMIT 100").fetchall()
        
        for i in range(50):
            transaction_id = f"BRW-{i}"
            book_id = random.choice(books)[0]
            student_id = random.choice(students)[0]
            borrow_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            due_date = (datetime.now() + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")
            return_date = None if random.random() > 0.7 else (datetime.now() - timedelta(days=random.randint(0, 5))).strftime("%Y-%m-%d")
            
            transactions.append((
                transaction_id,
                1,  # school_id
                book_id,
                student_id,
                borrow_date,
                return_date,
                due_date,
                random.choice(["Borrowed", "Returned", "Overdue"]),
                0,
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_book_transactions 
                (transaction_id, school_id, book_id, student_id, borrow_date, 
                 return_date, due_date, status, fine_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                transactions
            )
            conn.commit()
    
    def seed_transports(self):
        """Seed transport data."""
        transports = []
        
        for i in range(1, 11):
            transport_id = generate_transport_id()
            transports.append((
                transport_id,
                1,  # school_id
                f"BUS-{i:03d}",
                f"Driver {i}",
                f"Driver{i}Phone",
                f"Route-{chr(64 + i)}",
                random.randint(40, 55),
                random.randint(35, 50),
                "Active",
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_transports 
                (transport_id, school_id, bus_number, driver_name, driver_phone, 
                 route_name, capacity, total_students, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                transports
            )
            conn.commit()
    
    def seed_hostels(self):
        """Seed hostel data."""
        hostels = []
        
        hostel_types = [
            ("Boys Hostel", "Boys", 150),
            ("Girls Hostel A", "Girls", 100),
            ("Girls Hostel B", "Girls", 80)
        ]
        
        for i, (name, hostel_type, capacity) in enumerate(hostel_types):
            hostel_id = generate_hostel_id()
            hostels.append((
                hostel_id,
                1,  # school_id
                name,
                hostel_type,
                random.randint(30, 50),
                capacity,
                f"Warden {i + 1}",
                "Active",
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_hostels 
                (hostel_id, school_id, hostel_name, hostel_type, room_count, 
                 total_capacity, warden_name, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                hostels
            )
            conn.commit()
    
    def seed_ai_logs(self):
        """Seed AI processing logs."""
        ai_logs = []
        
        for i in range(50):
            ai_log_id = f"AI-LOG-{i}"
            ai_logs.append((
                ai_log_id,
                1,  # school_id
                random.choice(["Grading", "OCR", "Plagiarism", "Prediction"]),
                f"Input data {i}",
                f"Output data {i}",
                round(random.uniform(0.85, 0.99), 3),
                random.uniform(100, 5000),
                random.choice(["Success", "Failed"]),
                "",
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_ai_logs 
                (ai_log_id, school_id, process_type, input_data, output_data, 
                 confidence_score, processing_time_ms, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                ai_logs
            )
            conn.commit()
    
    def seed_analytics(self):
        """Seed analytics data."""
        analytics = []
        
        metrics = [
            ("total_students", 200),
            ("total_teachers", 50),
            ("total_classes", 10),
            ("avg_attendance", round(random.uniform(85, 98), 1)),
            ("assignment_submission_rate", round(random.uniform(80, 98), 1)),
            ("fee_collection_rate", round(random.uniform(75, 95), 1)),
            ("ai_grading_requests", random.randint(1000, 5000)),
            ("ocr_processing_success_rate", round(random.uniform(90, 99), 1))
        ]
        
        for metric_name, metric_value in metrics:
            analytics_id = f"ANALYTICS-{metric_name}"
            analytics.append((
                analytics_id,
                1,  # school_id
                metric_name,
                metric_value,
                datetime.now().strftime("%Y-%m-%d"),
                json.dumps({"details": f"Details for {metric_name}"}),
            ))
        
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO portal_analytics 
                (analytics_id, school_id, metric_name, metric_value, metric_date, details_json)
                VALUES (?, ?, ?, ?, ?, ?)""",
                analytics
            )
            conn.commit()


def main():
    """Run seeder."""
    seeder = SchoolPortalSeeder()
    seeder.seed_all()


if __name__ == "__main__":
    main()
