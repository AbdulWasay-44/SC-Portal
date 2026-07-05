# 🚀 SCHOOL PORTAL - QUICK START GUIDE

Get your School Portal running in 5 minutes!

---

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (1 min)
```bash
pip install streamlit pandas plotly
```

### Step 2: Seed Database (1 min)
```bash
python school_portal_data_seeder.py
```

**Output should show:**
```
✓ Students seeded
✓ Teachers seeded
✓ Classes seeded
✓ Subjects seeded
✓ Attendance records seeded
... (more items)
✅ All data seeded successfully!
```

### Step 3: Start Application (1 min)
```bash
streamlit run app.py
```

**Browser opens to:** http://localhost:8501

### Step 4: Access School Portal (1 min)
1. Click **🏫 School Portal** in the sidebar
2. You'll see the Dashboard with sample data

### Step 5: Explore Features (1 min)
- ✅ View Dashboard
- ✅ Check Student List
- ✅ Mark Attendance
- ✅ View Reports

---

## 📋 First Time Checklist

- [ ] Database seeded with sample data
- [ ] Application running without errors
- [ ] Can access School Portal from sidebar
- [ ] Dashboard displays KPI metrics
- [ ] Can view student list
- [ ] Can navigate between modules

---

## 🎯 Quick Actions (2-3 min each)

### Add a New Student
1. Go to: **Students** → **Add Student**
2. Fill in:
   - First Name
   - Last Name
   - Email
   - Phone
   - Class (select from dropdown)
   - Roll Number
3. Click: **✅ Add Student**

### Mark Attendance
1. Go to: **Attendance** → **Mark Attendance**
2. Select:
   - Attendance Date
   - Class
   - Subject
3. Check/Uncheck students: **Present**, **Absent**, **Leave**
4. Click: **💾 Save Attendance**

### View Student Performance
1. Go to: **Students** → **Student Profile**
2. Select a student
3. View:
   - Attendance %
   - GPA
   - Fee Status
   - Assignment completion

### Generate Report Card
1. Go to: **Exams & Results** → **Report Cards**
2. Select a student
3. View:
   - Subject-wise marks
   - Grades
   - GPA
4. Click: **📄 Generate PDF Report**

### Process Payment
1. Go to: **Fees & Payments** → **Payments**
2. Fill in:
   - Student
   - Amount
   - Payment Method
   - Transaction ID
3. Click: **✅ Verify & Process Payment**

### Create Assignment
1. Go to: **Assignments** → **Create Assignment**
2. Fill in:
   - Title
   - Class
   - Subject
   - Total Marks
   - Deadline
3. Click: **✅ Create Assignment**

### AI Grade Submissions
1. Go to: **AI Grading** → **AI Grading**
2. Select:
   - Assignment
   - Class
   - Subject
3. Upload: Student submissions
4. Click: **🤖 Grade with AI**
5. View: Marks, Feedback, Confidence

---

## 📊 Dashboard Overview

**KPI Cards (Top):**
- 👨‍🎓 Total Students
- 👨‍🏫 Total Teachers
- 📚 Total Classes
- 📖 Active Courses
- 📊 Attendance Rate
- ✅ Assignments
- 💰 Pending Fees
- 🤖 AI Requests

**Charts (Middle):**
- Monthly Attendance Trend (line chart)
- Revenue Collection (bar chart)

**Activity Feed (Bottom):**
- Recent actions
- User activities
- System updates

---

## 🔍 Navigation Map

```
School Portal (Home Page)
├── 📊 Dashboard (KPIs & Charts)
├── 👨‍🎓 Students
│   ├── View Students
│   ├── Add Student
│   ├── Student Profile
│   └── Student Analytics
├── 👨‍🏫 Teachers
│   ├── View Teachers
│   ├── Add Teacher
│   └── Teacher Analytics
├── 📚 Classes & Subjects
│   ├── View Classes
│   ├── Manage Subjects
│   └── Timetable
├── 📋 Attendance
│   ├── Mark Attendance
│   ├── View Records
│   └── Analytics
├── 📝 Exams & Results
│   ├── Create Exam
│   ├── View Exams
│   ├── Upload Results
│   └── Report Cards
├── 🤖 AI Grading
│   ├── AI Grading
│   ├── Grading History
│   └── AI Analytics
├── 📝 Assignments
│   ├── Create Assignment
│   ├── View Submissions
│   └── Assignment Analytics
├── 💰 Fees & Payments
│   ├── Fee Structure
│   ├── Student Fees
│   ├── Payments
│   └── Fee Analytics
├── 📢 Announcements
│   ├── Send Announcement
│   └── Notification History
├── 📚 Library
│   ├── Book Inventory
│   └── Book Borrowing
├── 🚌 Transport & Hostel
│   ├── Transport
│   └── Hostel
├── 📊 Reports
│   ├── Generate Report
│   ├── View Reports
│   └── Export
└── ⚙️ Settings
    ├── School Info
    ├── Academic Settings
    ├── System Settings
    └── Advanced
```

---

## 🎓 Module Highlights

| Module | Purpose | Key Actions |
|--------|---------|------------|
| 📊 Dashboard | System overview | Monitor KPIs |
| 👨‍🎓 Students | Student management | Add, edit, view profiles |
| 👨‍🏫 Teachers | Teacher management | Add, assign subjects |
| 📋 Attendance | Track attendance | Mark daily attendance |
| 📝 Exams | Manage exams | Create, grade, report cards |
| 💰 Fees | Payment management | Track, verify, collect fees |
| 🤖 AI | AI grading | Auto-grade assignments |
| 📊 Reports | Analytics & reports | Generate, export reports |

---

## 💡 Pro Tips

### 1. Use Search & Filter
- Search students by name or ID
- Filter by class or status
- Faster navigation

### 2. Bulk Operations
- Mark attendance for entire class at once
- Upload multiple exam results
- Process batch payments

### 3. Export Data
- Download reports as PDF
- Export to Excel for analysis
- Share data with stakeholders

### 4. Customize Settings
- Configure school info
- Set grading scale
- Adjust fee structure

### 5. Use Analytics
- Track attendance trends
- Monitor revenue
- Analyze student performance
- Predict dropouts

---

## ⚙️ Configuration Tips

### Recommended Settings

**School Info:**
- School Name: Your School Name
- School Code: Unique identifier
- Principal: Principal Name

**Academic Settings:**
- Academic Year: 2024-2025
- Semesters: 2 or 3
- Grading Scale: A-F (or customize)

**System Settings:**
- Theme: Choose Light or Dark
- Language: English (default)
- Time Format: 24-hour

---

## 🔐 User Roles

Different modules may be available based on user role:

| Role | Access |
|------|--------|
| Admin | All modules, Settings |
| Principal | All modules, Dashboard |
| Teacher | Students, Classes, Attendance, AI Grading, Assignments |
| Student | Personal Profile, Assignments, Results |
| Parent | Child Profile, Attendance, Results |

---

## 📱 Common Workflows

### Daily Workflow (Teacher)
1. **Morning:** Check Dashboard for alerts
2. **During Class:** Mark Attendance
3. **After Class:** View Submissions, Grade Assignments
4. **End of Day:** Review Analytics

### Weekly Workflow (Admin)
1. **Monday:** Review Attendance Report
2. **Mid-Week:** Process Payments
3. **Thursday:** Create Announcements
4. **Friday:** Generate Weekly Report

### Monthly Workflow (Principal)
1. **Start of Month:** Review KPIs
2. **Mid-Month:** Analyze Performance Data
3. **End of Month:** Generate Reports, Review Fees
4. **Next Day:** Plan improvements

---

## ❓ Quick Troubleshooting

**Q: Data not showing?**
- Ensure database is seeded: `python school_portal_data_seeder.py`

**Q: Streamlit not starting?**
- Check Python version (3.8+)
- Reinstall: `pip install -r requirements.txt`

**Q: Charts not loading?**
- Install Plotly: `pip install plotly`
- Refresh page (F5)

**Q: Very slow?**
- Clear Streamlit cache: `streamlit cache clear`
- Reduce date range for analytics

**Q: Permission denied?**
- Run with admin privileges
- Check file permissions

---

## 📞 Need Help?

**Check the full documentation:**
- Read: `SCHOOL_PORTAL_README.md`
- Architecture: `SCHOOL_PORTAL_ARCHITECTURE.md`

**Common issues:**
- See: `Troubleshooting` section in README

**Feature requests:**
- Contact: your-email@school.com

---

## 🎉 You're Ready!

You now have a fully functional School Portal!

**Next Steps:**
1. ✅ Explore each module
2. ✅ Customize settings
3. ✅ Import real data
4. ✅ Train staff
5. ✅ Go live!

---

**Version:** 1.0.0 | **Last Updated:** May 2024 | **Status:** ✅ Ready to Use
