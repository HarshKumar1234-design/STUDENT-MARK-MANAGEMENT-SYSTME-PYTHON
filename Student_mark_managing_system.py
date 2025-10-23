students = {}

def add_student():
    """Add a new student with marks"""
    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")
    
    marks = {}
    marks['Math'] = float(input("Enter Math marks: "))
    marks['Science'] = float(input("Enter Science marks: "))
    marks['English'] = float(input("Enter English marks: "))
    
    # Calculate total and average
    total = sum(marks.values())
    average = total / len(marks)
    
    students[roll_no] = {
        'name': name,
        'marks': marks,
        'total': total,
        'average': average,
        'grade': calculate_grade(average)
    }
    
    print(f"Student {name} added successfully!")

def calculate_grade(average):
    """Calculate grade based on average"""
    if average >= 90:
        return 'A+'
    elif average >= 80:
        return 'A'
    elif average >= 70:
        return 'B'
    elif average >= 60:
        return 'C'
    elif average >= 50:
        return 'D'
    else:
        return 'F'

def view_student():
    """View details of a specific student"""
    roll_no = input("Enter roll number: ")
    
    if roll_no in students:
        student = students[roll_no]
        print("\n" + "="*50)
        print(f"Name: {student['name']}")
        print(f"Roll Number: {roll_no}")
        print("Marks:")
        for subject, mark in student['marks'].items():
            print(f"  {subject}: {mark}")
        print(f"Total: {student['total']}")
        print(f"Average: {student['average']:.2f}")
        print(f"Grade: {student['grade']}")
        print("="*50 + "\n")
    else:
        print("Student not found!")

def view_all_students():
    """Display all students"""
    if not students:
        print("No students in the system!")
        return
    
    print("\n" + "="*70)
    print(f"{'Roll No':<10} {'Name':<20} {'Total':<10} {'Average':<10} {'Grade':<10}")
    print("="*70)
    for roll_no, student in students.items():
        print(f"{roll_no:<10} {student['name']:<20} {student['total']:<10} "
              f"{student['average']:<10.2f} {student['grade']:<10}")
    print("="*70 + "\n")

def update_student():
    """Update student marks"""
    roll_no = input("Enter roll number: ")
    
    if roll_no not in students:
        print("Student not found!")
        return
    
    print(f"Updating marks for {students[roll_no]['name']}")
    marks = {}
    marks['Math'] = float(input("Enter new Math marks: "))
    marks['Science'] = float(input("Enter new Science marks: "))
    marks['English'] = float(input("Enter new English marks: "))
    
    total = sum(marks.values())
    average = total / len(marks)
    
    students[roll_no]['marks'] = marks
    students[roll_no]['total'] = total
    students[roll_no]['average'] = average
    students[roll_no]['grade'] = calculate_grade(average)
    
    print("Marks updated successfully!")

def delete_student():
    """Delete a student record"""
    roll_no = input("Enter roll number: ")
    
    if roll_no in students:
        del students[roll_no]
        print("Student deleted successfully!")
    else:
        print("Student not found!")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("   STUDENT MARKS MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Student")
        print("2. View Student")
        print("3. View All Students")
        print("4. Update Student Marks")
        print("5. Delete Student")
        print("6. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_student()
        elif choice == '3':
            view_all_students()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()