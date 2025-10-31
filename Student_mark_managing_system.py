import sys
import math
import matplotlib.pyplot as plt

# Time order and maxima for normalization to percentage
time_order = ['Internal1', 'CAT1', 'Internal2', 'CAT2', 'Internal3', 'FAT']
MAX_SCORES = {'Internal1': 10, 'CAT1': 50, 'Internal2': 10, 'CAT2': 50, 'Internal3': 10, 'FAT': 80}

# Predefined subjects (edit as needed)
subjects_data = {
    'Multivariable Calculus and Differential Equations': {},
    'Applied Chemistry': {},
    'Computation Structures': {},
    'Basic Engineering': {},
    'Problem Solving using Python': {},
}

# ----------------- Grading and calculations -----------------

def assign_grade(percentage):
    if percentage >= 90:
        return 'S'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    elif percentage >= 40:
        return 'E'
    else:
        return 'F'

def calculate_subject_score(marks):
    # FAT fail rule: subject grade F if FAT < 50%
    fat_percentage = (marks['FAT'] / MAX_SCORES['FAT']) * 100
    if fat_percentage < 50:
        return 'F', 0.0
    total_percentage = (
        ((marks['CAT1'] / 50) * 15) +
        ((marks['CAT2'] / 50) * 15) +
        ((marks['FAT']  / 80) * 40) +
        ((marks['Internal1'] / 10) * 10) +
        ((marks['Internal2'] / 10) * 10) +
        ((marks['Internal3'] / 10) * 10)
    )
    grade = assign_grade(total_percentage)
    return grade, float(total_percentage)

# ----------------- Input helpers -----------------

def get_marks_input():
    print("Enter marks in the following order:", ' - '.join(time_order))
    marks = {}
    for exam_part in time_order:
        max_score = MAX_SCORES[exam_part]
        while True:
            try:
                score = float(input(f"{exam_part} (out of {max_score}): "))
                if 0 <= score <= max_score:
                    marks[exam_part] = score
                    break
                else:
                    print(f"Invalid input. Score should be between 0 and {max_score}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    return marks

# ----------------- Formatting utilities -----------------

def _num_len(val, decimals=2):
    s = f"{val:.{decimals}f}"
    return len(s)

def _max_len_str(values, header, min_w=0):
    return max(min_w, len(header), *(len(v) for v in values)) if values else max(min_w, len(header))

def _max_len_num(values, header, decimals=2, min_w=0):
    return max(min_w, len(header), *(_num_len(v, decimals) for v in values)) if values else max(min_w, len(header))

# ----------------- View: All students -----------------

def print_students_table(students):
    # Build data rows first
    rows = []
    for roll, info in students.items():
        total_all = 0.0
        total_percent_sum = 0.0
        for _, marks in info['subjects'].items():
            _, percent = calculate_subject_score(marks)
            total_all += sum(marks.values())
            total_percent_sum += percent
        avg_percent = total_percent_sum / max(1, len(info['subjects']))
        rows.append((roll, info['name'], total_all, avg_percent, assign_grade(avg_percent)))

    # Sort by avg percentage desc
    rows.sort(key=lambda x: x[3], reverse=True)

    # Compute dynamic widths
    roll_w = _max_len_str([r[0] for r in rows], "Roll Number", 10)
    name_w = _max_len_str([r[1] for r in rows], "Name", 28)
    tot_w  = _max_len_num([r[2] for r in rows], "Total Marks", 2, 12)
    avg_w  = _max_len_num([r[3] for r in rows], "Avg %", 2, 7)
    grade_w = _max_len_str([r[4] for r in rows], "Grade", 5)

    header_fmt = f"{{:<{roll_w}}}  {{:<{name_w}}}  {{:>{tot_w}}}  {{:>{avg_w}}}  {{:>{grade_w}}}"
    row_fmt    = f"{{:<{roll_w}}}  {{:<{name_w}}}  {{:>{tot_w}.2f}}  {{:>{avg_w}.2f}}  {{:>{grade_w}}}"

    total_width = roll_w + name_w + tot_w + avg_w + grade_w + 8
    print()
    print(header_fmt.format("Roll Number", "Name", "Total Marks", "Avg %", "Grade"))
    print("-" * total_width)
    for roll, name, total_all, avg_percent, grade in rows:
        print(row_fmt.format(roll, name, total_all, avg_percent, grade))
    print()

# ----------------- View: Individual student -----------------

def view_individual_student(students):
    roll = input("Enter the student's Roll Number: ").strip()
    if roll not in students:
        print("Student not found!")
        return
    info = students[roll]
    subjects = list(info['subjects'].keys())

    # Collect row data
    row_data = []
    subj_percents = []
    for subject, marks in info['subjects'].items():
        cat1_per = (marks['CAT1'] / 50) * 100
        cat2_per = (marks['CAT2'] / 50) * 100
        fat_per  = (marks['FAT']  / 80) * 100
        internal_total = marks['Internal1'] + marks['Internal2'] + marks['Internal3']

        cat1_grade = assign_grade(cat1_per)
        cat2_grade = assign_grade(cat2_per)
        fat_grade  = assign_grade(fat_per) if fat_per >= 50 else 'F'
        total_grade, subj_percent = calculate_subject_score(marks)

        row_data.append({
            "subject": subject,
            "cat1": marks['CAT1'], "gr1": cat1_grade,
            "cat2": marks['CAT2'], "gr2": cat2_grade,
            "fat": marks['FAT'],   "fatgr": fat_grade,
            "internal": internal_total, "total_grade": total_grade,
            "totpct": subj_percent
        })
        subj_percents.append(subj_percent)

    # Dynamic widths
    subj_w = _max_len_str([r["subject"] for r in row_data], "Subject", 30)
    n_w    = _max_len_num([r["cat1"] for r in row_data] + [r["cat2"] for r in row_data], "CAT1", 2, 6)
    n2_w   = _max_len_num([r["fat"] for r in row_data], "FAT", 2, 7)
    int_w  = _max_len_num([r["internal"] for r in row_data], "Internal", 2, 8)
    gr_w   = _max_len_str([r["gr1"] for r in row_data] + [r["gr2"] for r in row_data] + [r["fatgr"] for r in row_data], "Gr", 3)
    totpct_w = _max_len_num([r["totpct"] for r in row_data], "Tot%", 2, 6)
    tgrade_w = _max_len_str([r["total_grade"] for r in row_data], "Grade", 5)

    header_fmt = (
        f"{{:<{subj_w}}}  "
        f"{{:>{n_w}}} {{:>{gr_w}}}  "
        f"{{:>{n_w}}} {{:>{gr_w}}}  "
        f"{{:>{n2_w}}} {{:>{gr_w}}}  "
        f"{{:>{int_w}}} {{:>{tgrade_w}}}  "
        f"{{:>{totpct_w}}}"
    )
    row_fmt = (
        f"{{:<{subj_w}}}  "
        f"{{:>{n_w}.2f}} {{:>{gr_w}}}  "
        f"{{:>{n_w}.2f}} {{:>{gr_w}}}  "
        f"{{:>{n2_w}.2f}} {{:>{gr_w}}}  "
        f"{{:>{int_w}.2f}} {{:>{tgrade_w}}}  "
        f"{{:>{totpct_w}.2f}}"
    )

    total_width = subj_w + (n_w+gr_w)*2 + (n2_w+gr_w) + (int_w+tgrade_w) + totpct_w + 10
    print(f"\nDetails for {info['name']} (Roll: {roll}):\n")
    print(header_fmt.format("Subject", "CAT1", "Gr1", "CAT2", "Gr2", "FAT", "FATGr", "Internal", "Grade", "Tot%"))
    print("-" * total_width)

    for r in row_data:
        print(row_fmt.format(
            r["subject"],
            r["cat1"], r["gr1"],
            r["cat2"], r["gr2"],
            r["fat"],  r["fatgr"],
            r["internal"], r["total_grade"],
            r["totpct"]
        ))

    overall_avg = (sum(subj_percents) / max(1, len(subj_percents)))
    overall_grade = assign_grade(overall_avg)
    print(f"\nOverall Percentage (All Subjects): {overall_avg:.2f}%")
    print(f"Overall Grade: {overall_grade}")

    # Plots
    plot_performance_graphs(info)

# ----------------- Plots -----------------

def plot_performance_graphs(student_info):
    subjects = list(student_info['subjects'].keys())

    # Individual subjects (normalized to percentage)
    plt.figure()
    for subject in subjects:
        marks = student_info['subjects'][subject]
        vals_pct = [(marks[exam] / MAX_SCORES[exam]) * 100 for exam in time_order]
        plt.plot(time_order, vals_pct, marker='o', label=subject)
    plt.title('Individual Subject Performance Over Time (Percentage)')
    plt.xlabel('Exam')
    plt.ylabel('Percentage')
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Overall performance timeline (average percentage across subjects)
    overall_pct_series = []
    for exam_part in time_order:
        total_pct = 0.0
        count = 0
        for subject in subjects:
            marks = student_info['subjects'][subject]
            total_pct += (marks[exam_part] / MAX_SCORES[exam_part]) * 100
            count += 1
        overall_pct_series.append((total_pct / count) if count else 0.0)

    plt.figure()
    plt.plot(time_order, overall_pct_series, marker='o', color='black')
    plt.title('Overall Performance Over Semester (Percentage)')
    plt.xlabel('Exam')
    plt.ylabel('Average Percentage')
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ----------------- Class performance -----------------

def class_performance(students):
    if not students:
        print("No student records to calculate class performance.")
        return

    num_students = len(students)
    subjects = list(subjects_data.keys())

    # Sums per subject per exam
    subj_exam_sums = {subj: {exam: 0.0 for exam in time_order} for subj in subjects}
    for stu in students.values():
        for subj in subjects:
            marks = stu['subjects'][subj]
            for exam in time_order:
                subj_exam_sums[subj][exam] += marks[exam]

    # Averages
    subj_exam_avgs = {
        subj: {exam: subj_exam_sums[subj][exam] / num_students for exam in time_order}
        for subj in subjects
    }

    cat1_avgs = {subj: subj_exam_avgs[subj]['CAT1'] for subj in subjects}
    cat2_avgs = {subj: subj_exam_avgs[subj]['CAT2'] for subj in subjects}
    fat_avgs  = {subj: subj_exam_avgs[subj]['FAT']  for subj in subjects}
    internal_totals_avgs = {
        subj: subj_exam_avgs[subj]['Internal1'] + subj_exam_avgs[subj]['Internal2'] + subj_exam_avgs[subj]['Internal3']
        for subj in subjects
    }

    # Overall subject averages (percentage with weights)
    overall_subj_avgs = {}
    for subj in subjects:
        overall_subj_avgs[subj] = (
            ((subj_exam_avgs[subj]['CAT1'] / 50) * 15) +
            ((subj_exam_avgs[subj]['CAT2'] / 50) * 15) +
            ((subj_exam_avgs[subj]['FAT']  / 80) * 40) +
            (((subj_exam_avgs[subj]['Internal1'] + subj_exam_avgs[subj]['Internal2'] + subj_exam_avgs[subj]['Internal3']) / 30) * 30)
        )

    overall_semester_avg = sum(overall_subj_avgs.values()) / max(1, len(subjects))

    # Dynamic widths for table 1
    subj_w = _max_len_str(subjects, "Subject", 30)
    n_w    = _max_len_num(list(cat1_avgs.values()) + list(cat2_avgs.values()), "CAT Avg", 2, 10)
    fat_w  = _max_len_num(list(fat_avgs.values()), "FAT Avg", 2, 10)
    int_w  = _max_len_num(list(internal_totals_avgs.values()), "Cumulative Internals Avg", 2, 24)

    header_fmt = f"{{:<{subj_w}}}  {{:>{n_w}}}  {{:>{n_w}}}  {{:>{fat_w}}}  {{:>{int_w}}}"
    row_fmt    = f"{{:<{subj_w}}}  {{:>{n_w}.2f}}  {{:>{n_w}.2f}}  {{:>{fat_w}.2f}}  {{:>{int_w}.2f}}"
    total_width = subj_w + n_w*2 + fat_w + int_w + 8

    print("\nClass Performance:")
    print(header_fmt.format("Subject", "CAT1 Avg", "CAT2 Avg", "FAT Avg", "Cumulative Internals Avg"))
    print("-" * total_width)
    for subj in subjects:
        print(row_fmt.format(subj, cat1_avgs[subj], cat2_avgs[subj], fat_avgs[subj], internal_totals_avgs[subj]))

    # Dynamic widths for table 2
    pct_w = _max_len_num(list(overall_subj_avgs.values()), "Avg %", 2, 8)
    header2_fmt = f"{{:<{subj_w}}}  {{:>{pct_w}}}"
    row2_fmt    = f"{{:<{subj_w}}}  {{:>{pct_w}.2f}}"

    print("\nOverall Average per Subject (in %):")
    print(header2_fmt.format("Subject", "Avg %"))
    print("-" * (subj_w + pct_w + 2))
    for subj in subjects:
        print(row2_fmt.format(subj, overall_subj_avgs[subj]))

    print(f"\nOverall Semester Average: {overall_semester_avg:.2f}%")

    # Plots: class averages per subject over time (normalized to percentage)
    plt.figure()
    for subj in subjects:
        vals_pct = [(subj_exam_avgs[subj][exam] / MAX_SCORES[exam]) * 100 for exam in time_order]
        plt.plot(time_order, vals_pct, marker='o', label=subj)
    plt.title('Class Average per Subject Over Semester (Percentage)')
    plt.xlabel('Exam')
    plt.ylabel('Average Percentage')
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Overall class timeline (average across subjects at each exam)
    overall_class_timeline = []
    for exam in time_order:
        mean_pct = sum((subj_exam_avgs[subj][exam] / MAX_SCORES[exam]) * 100 for subj in subjects) / len(subjects)
        overall_class_timeline.append(mean_pct)

    plt.figure()
    plt.plot(time_order, overall_class_timeline, marker='o', color='black')
    plt.title('Class Overall Average Over Semester (Percentage)')
    plt.xlabel('Exam')
    plt.ylabel('Average Percentage')
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ----------------- Menu -----------------

def main():
    students = {}
    while True:
        print("\n--- VIT Student Marks Management ---")
        print("1. Add Student")
        print("2. View Individual Student Details")
        print("3. View All Students")
        print("4. Update Student Marks")
        print("5. Delete Student Record")
        print("6. Class Performance")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            roll = input("Enter Roll Number: ").strip()
            if roll in students:
                print("Student already exists!")
                continue
            name = input("Enter Name: ").strip()
            all_subjects_marks = {}
            for subject in subjects_data:
                print(f"\n-- Enter marks for: {subject} --")
                marks = get_marks_input()
                all_subjects_marks[subject] = marks
            students[roll] = {'name': name, 'subjects': all_subjects_marks}
            print("Student added successfully.")

        elif choice == "2":
            if not students:
                print("No student records available.")
            else:
                view_individual_student(students)

        elif choice == "3":
            if not students:
                print("No student records available.")
            else:
                print_students_table(students)

        elif choice == "4":
            roll = input("Enter Roll Number to update: ").strip()
            if roll not in students:
                print("Student not found!")
                continue
            print("Updating marks for student:", students[roll]['name'])
            for subject in students[roll]['subjects']:
                print(f"\n-- Enter new marks for: {subject} --")
                students[roll]['subjects'][subject] = get_marks_input()
            print("Marks updated successfully.")

        elif choice == "5":
            roll = input("Enter Roll Number to delete: ").strip()
            if roll in students:
                del students[roll]
                print("Student record deleted.")
            else:
                print("Student not found!")

        elif choice == "6":
            class_performance(students)

        elif choice == "7":
            print("Exiting.")
            sys.exit()

        else:
            print("Invalid choice. Try again.")

if _name_ == "_main_":
    main()
