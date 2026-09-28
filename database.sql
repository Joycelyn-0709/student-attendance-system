CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    register_no TEXT UNIQUE NOT NULL,
    department TEXT
);

CREATE TABLE attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    attendance_date TEXT,
    status TEXT,
    FOREIGN KEY (student_id)
    REFERENCES students(student_id)
);

INSERT INTO students
(name, register_no, department)
VALUES
('Joycelyn', 'IT001', 'IT'),
('Serena', 'IT002', 'IT'),
('Sanjana', 'IT003', 'IT');