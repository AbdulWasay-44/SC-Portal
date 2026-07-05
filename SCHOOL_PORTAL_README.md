# 🏫 SCHOOL PORTAL - COMPLETE USER GUIDE

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Features](#features)
4. [Module Descriptions](#module-descriptions)
5. [Database Schema](#database-schema)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Overview

The **School Portal** is a comprehensive, enterprise-level school management system built with Streamlit, Python, and SQLite. It provides complete management of all aspects of school operations including students, teachers, classes, attendance, exams, assignments, fees, and AI-powered grading.

### Key Features
- ✅ Modern, responsive UI with Streamlit
- ✅ 14 major management modules
- ✅ AI-powered grading integration
- ✅ Real-time analytics and reporting
- ✅ Secure payment management
- ✅ Complete audit trails
- ✅ Multi-role access control
- ✅ Advanced search and filtering

---

## Quick Start

### Installation

1. **Ensure dependencies are installed:**
```bash
pip install streamlit pandas plotly
```

2. **Seed the database with sample data:**
```bash
python school_portal_data_seeder.py
```

3. **Start the application:**
```bash
streamlit run app.py
```

4. **Navigate to School Portal:**
   - Click "🏫 School Portal" button in the sidebar
   - You'll see the dashboard immediately

### First Steps
1. Dashboard - View system overview
2. Students - Add/manage student records
3. Teachers - Add/manage teacher records
4. Attendance - Mark daily attendance
5. Exams - Create and manage exams
6. Fees - Manage fee collection

---

## Features

### 1. 📊 Dashboard
**Overview of entire school system**

Displays:
- 8 KPI metric cards (students, teachers, classes, etc.)
- Monthly attendance trends
- Revenue collection charts
- Recent activity feed
- Quick actions panel

Use Cases:
- Principal/Admin daily check-ins
- System health monitoring
- Quick access to key metrics
- Activity tracking

---

### 2. 👨‍🎓 Student Management
**Complete student lifecycle management**

Features:
- ✅ Add new students with profile photos
- ✅ Edit student information
- ✅ Search and filter by name, class, ID
- ✅ View individual student profiles
- ✅ Track attendance and grades
- ✅ Manage fee status
- ✅ View performance analytics

Student Profile Includes:
- Personal information
- Contact details
- Parent information
- Academic history
- Attendance records
- Fee payment status
- Performance metrics

Roll Number Generation:
- Automatic based on class and rank
- Format: STU-YYYY-CLASS-ROLL

---

### 3. 👨‍🏫 Teacher Management
**Teacher recruitment and performance tracking**

Features:
- ✅ Add teachers with qualifications
- ✅ Subject specialization tracking
- ✅ Class assignment management
- ✅ Experience and qualification records
- ✅ AI grading usage analytics
- ✅ Teaching performance ratings

Teacher Metrics:
- AI grading adoption rate
- Average rating (1-5 scale)
- Classes assigned
- Subject expertise
- Years of experience

---

### 4. 📚 Classes & Subjects
**Curriculum and class structure management**

Features:
- ✅ Create classes (8-12)
- ✅ Manage sections (A, B, C, etc.)
- ✅ Add subjects to classes
- ✅ Assign teachers to subjects
- ✅ Manage course credits
- ✅ Weekly timetable view

Timetable Features:
- Period-wise scheduling
- Room number assignment
- Teacher assignment
- Subject mapping
- Weekly view
- Class-wise view

---

### 5. 📋 Attendance Management
**Track student and class attendance**

Features:
- ✅ Mark daily attendance
- ✅ Bulk attendance entry
- ✅ View attendance records
- ✅ Monthly attendance reports
- ✅ Low attendance alerts
- ✅ Attendance analytics

Statuses:
- Present
- Absent
- Leave
- Medical Leave

Analytics:
- Class-wise attendance %
- Monthly trends
- Low attendance alerts
- Student performance correlation

---

### 6. 📝 Exams & Results
**Comprehensive examination management**

Features:
- ✅ Create exams (Unit Test, Mid-Term, Final)
- ✅ Schedule exams
- ✅ Upload results in bulk
- ✅ Generate report cards
- ✅ Calculate GPA
- ✅ Grade mapping

Grade Calculation:
- A+ (90-100%)
- A (80-90%)
- B (70-80%)
- C (60-70%)
- D (50-60%)
- F (<50%)

Report Card Features:
- Subject-wise marks
- Percentage calculation
- Grade display
- GPA calculation
- Comparative analysis
- PDF generation (ready)

---

### 7. 🤖 AI Grading & Analytics
**AI-powered automated grading system**

Features:
- ✅ Submit assignments for AI grading
- ✅ Automatic plagiarism detection
- ✅ Confidence score tracking
- ✅ AI feedback generation
- ✅ Accuracy metrics
- ✅ Historical grading data

AI Metrics:
- Average confidence score
- Total submissions graded
- AI accuracy rate
- Grade distribution
- Confidence score distribution
- Processing time

Plagiarism Detection:
- Text similarity analysis
- Original work verification
- Duplicate detection
- Source matching

---

### 8. 📝 Assignment Management
**Complete assignment lifecycle**

Features:
- ✅ Create assignments
- ✅ Set deadlines
- ✅ Track submissions
- ✅ Mark late submissions
- ✅ Grade submissions
- ✅ Generate feedback
- ✅ Analytics and reports

Assignment Analytics:
- Submission rate by assignment
- On-time vs late submissions
- Average scores
- Performance trends
- Student comparison

---

### 9. 💰 Fees & Payments
**Complete payment management system**

Fee Structure:
- Tuition Fee (₹25,000/month)
- Transport Fee (₹5,000/month)
- Library Fee (₹1,500/year)
- Lab Fee (₹2,000/year)
- Sports Fee (₹1,000/year)

Payment Processing:
- ✅ Student fee status tracking
- ✅ Payment verification
- ✅ Receipt generation
- ✅ Late fee calculation
- ✅ Scholarship approval
- ✅ Discount management
- ✅ Collection analytics

Payment Methods:
- Cash
- Check
- Online Transfer
- Card Payment

Fee Analytics:
- Monthly collection trend
- Collection rate %
- Pending fees tracking
- Payment status distribution
- Revenue forecasting

---

### 10. 📢 Announcements & Notifications
**School-wide communication system**

Features:
- ✅ Create announcements
- ✅ Set priority levels
- ✅ Multi-channel delivery
- ✅ Recipient targeting
- ✅ Schedule announcements
- ✅ Track delivery status
- ✅ View notification history

Channels:
- Email
- SMS
- In-App Notification
- Push Notification

Announcement Types:
- General announcements
- Exam notifications
- Fee reminders
- Event updates
- Emergency alerts
- Achievement recognition

---

### 11. 📚 Library Management
**Book inventory and borrowing system**

Features:
- ✅ Add books to inventory
- ✅ Track book availability
- ✅ Manage borrowing
- ✅ Track due dates
- ✅ Calculate fines
- ✅ Book search
- ✅ Category management

Book Categories:
- Fiction
- Reference
- Science
- Mathematics
- History
- Computer Science

Borrowing:
- Borrow period: 14 days
- Fine: ₹10/day overdue
- Renewal: Once per book
- Holds: Available
- Reservation: Available

---

### 12. 🚌 Transport & Hostel
**Transportation and accommodation management**

Transport Features:
- ✅ Bus/vehicle management
- ✅ Driver information
- ✅ Route management
- ✅ Student allocation
- ✅ Capacity tracking
- ✅ Attendance on routes

Hostel Features:
- ✅ Room allocation
- ✅ Occupancy tracking
- ✅ Warden assignment
- ✅ Hostel fee management
- ✅ Student records
- ✅ Complaints tracking

---

### 13. 📊 Reports & Analytics
**Generate comprehensive reports**

Report Types:
- Student Report (individual or bulk)
- Teacher Performance Report
- Class Analytics Report
- Attendance Summary
- Fee Collection Report
- Academic Performance Report
- AI Grading Report

Export Formats:
- PDF
- Excel
- CSV

Reports Include:
- Statistical summaries
- Trend analysis
- Comparative data
- Recommendations
- Charts and graphs

---

### 14. ⚙️ Settings
**System configuration and customization**

School Information:
- School name
- School code
- Principal details
- Contact information
- Address
- Website

Academic Settings:
- Academic year
- Semester structure
- Grading scale
- Holiday calendar
- Term dates

System Settings:
- Theme (Light/Dark)
- Language
- Time format
- Date format
- Currency
- Timezone

Advanced Settings:
- AI grading enable/disable
- OCR processing
- Maintenance mode
- Security settings
- Backup settings

---

## Database Schema

### Core Tables

#### portal_students
```sql
student_id (PK)
first_name, last_name
roll_number
class, section
email, phone
parent_name, parent_phone, parent_email
date_of_birth
address
admission_date
photo_url
status (Active/Suspended/Left)
created_at, updated_at
```

#### portal_teachers
```sql
teacher_id (PK)
first_name, last_name
email, phone
subject_expertise
experience_years
qualification
address
date_of_birth
photo_url
status
created_at, updated_at
```

#### portal_classes
```sql
class_id (PK)
class_name
class_teacher_id (FK)
section
total_students
academic_year
status
created_at
```

#### portal_subjects
```sql
subject_id (PK)
subject_name
subject_code
teacher_id (FK)
class_id (FK)
credits
status
created_at
```

#### portal_attendance
```sql
id (PK)
student_id (FK)
attendance_date
status (Present/Absent/Leave)
marked_by
remarks
created_at
```

#### portal_exams
```sql
exam_id (PK)
exam_name
exam_type
class_id (FK)
subject_id (FK)
total_marks
exam_date
duration_minutes
passing_marks
status
created_at
```

#### portal_exam_results
```sql
id (PK)
exam_id (FK)
student_id (FK)
obtained_marks
percentage
grade
status
remarks
created_at
```

#### portal_assignments
```sql
assignment_id (PK)
class_id (FK)
subject_id (FK)
teacher_id (FK)
title
description
total_marks
deadline
status
created_at
```

#### portal_assignment_submissions
```sql
id (PK)
assignment_id (FK)
student_id (FK)
submission_date
marks_obtained
ai_feedback
plagiarism_score
status
created_at
```

#### portal_fees
```sql
fee_id (PK)
student_id (FK)
fee_name
amount
due_date
fine_amount
paid_amount
payment_status
payment_date
receipt_number
remarks
created_at
```

#### portal_payments
```sql
payment_id (PK)
student_id (FK)
fee_id (FK)
amount
payment_method
transaction_id
verification_status
verified_by
verified_date
payment_date
created_at
```

#### Additional Tables
- portal_timetable
- portal_libraries
- portal_book_transactions
- portal_transports
- portal_hostels
- portal_ai_logs
- portal_analytics

---

## Configuration

### Environment Variables
No external environment variables required. All configuration is in-app through Settings page.

### Database
- Location: `abdul_project.db`
- Type: SQLite3
- Auto-initialization: Yes

### Streamlit Configuration
Edit `.streamlit/config.toml` to customize:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#31333F"

[client]
showErrorDetails = true
```

---

## Troubleshooting

### Common Issues

**1. Database connection error**
```
Solution: Ensure abdul_project.db is in the project root directory
Run: python school_portal_data_seeder.py
```

**2. Missing helper functions**
```
Solution: Ensure school_portal_helpers.py is in project root
Install: pip install school_portal_helpers
```

**3. Streamlit not responding**
```
Solution: Clear cache and restart
Run: streamlit cache clear
Then: streamlit run app.py
```

**4. Data not appearing**
```
Solution: Seed database with sample data
Run: python school_portal_data_seeder.py
```

**5. Charts not loading**
```
Solution: Ensure Plotly is installed
Run: pip install plotly
```

---

## FAQ

### Q: How do I add a new student?
**A:** Go to Students → Add Student tab, fill in details, and click "Add Student".

### Q: Can I import students in bulk?
**A:** Currently manual entry only. Bulk import is planned for v2.0.

### Q: How are fees calculated?
**A:** Fees = (Fee Amount) + (Late Fees if applicable) - (Discounts/Scholarships)

### Q: Can teachers grade using AI?
**A:** Yes! Go to AI Grading & Analytics → Submit for AI Grading.

### Q: How is GPA calculated?
**A:** GPA = (Average Percentage) / 10

### Q: Can I generate report cards?
**A:** Yes! Exams & Results → Report Cards → Select student → Generate PDF

### Q: Is data automatically backed up?
**A:** Yes, automatic daily backups in Settings → Advanced Settings

### Q: Can I customize the grading scale?
**A:** Yes, in Settings → Academic Settings → Grading Scale

### Q: How do I track attendance trends?
**A:** Go to Attendance → Analytics → View Monthly Trend

### Q: Can I export reports?
**A:** Yes! Reports & Analytics → Export → Choose format (PDF/Excel/CSV)

---

## Support & Contact

For issues or feature requests, contact:
- School Admin Email
- Technical Support: support@school.com
- Emergency: 1800-XXXX-XXXX

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | May 2024 | Initial release with 14 modules |
| 1.1.0 | June 2024 | Added AI analytics (planned) |
| 1.2.0 | July 2024 | Mobile app support (planned) |
| 2.0.0 | Aug 2024 | Advanced features (planned) |

---

## License & Copyright

© Abdul's School Portal - All Rights Reserved 2024

Built with ❤️ for modern education management
