
student_file = "students.txt"
teacher_file = "teachers.txt"


def get_input(message):
    value = input(message).strip()

    if value.lower() == "exit":
        print("\nHave a nice day!")
        raise SystemExit

    return value


def create_files():
    for file_name in [student_file, teacher_file]:
        try:
            with open(file_name, "r") as file:
                pass
        except FileNotFoundError:
            with open(file_name, "w") as file:
                pass


def authenticate(email):
    username, separator, domain = email.partition("@")

    if not separator or not username:
        return None

    if domain == "bennett.student.edu.in":
        return "student"

    elif domain == "bennett.faculty.edu.in":
        return "faculty"

    elif domain == "bennett.programcoordinator.edu.in":
        return "coordinator"

    return None


def save_teacher(name, cabin, available):
    with open(teacher_file, "r") as file:
        records = file.readlines()

    records = [
        record for record in records
        if record.strip().partition("|")[0].lower() != name.lower()
    ]

    with open(teacher_file, "w") as file:
        file.writelines(records)
        file.write(f"{name}|{cabin}|{available}\n")


def faculty_login():
    print("\n========== FACULTY REGISTRATION ==========")

    name = get_input("Enter your name: ")
    cabin = get_input("Enter your cabin details: ")

    print("\nEnter your available days and time slots.")
    print("Format: Day HH:MM-HH:MM")
    print("Example: Monday 11:00-12:00")
    print("For multiple slots, separate them using semicolons.")
    print("Example: Monday 11:00-12:00; Tuesday 14:00-15:00")
    print("Use 24-hour time format.")

    available = get_input("\nEnter your available times: ")

    if not name or not cabin or not available:
        print("\nAll details are required.")
        return

    save_teacher(name, cabin, available)

    print("\nFaculty details successfully saved!")


def load_teachers():
    with open(teacher_file, "r") as file:
        records = [
            line.strip().split("|", 2)
            for line in file if line.strip()
        ]

    return [record for record in records if len(record) == 3]


def find_teacher(name):
    teachers = load_teachers()

    matches = [
        teacher for teacher in teachers
        if teacher[0].lower() == name.lower()
    ]

    return matches[0] if matches else None


def time_to_minutes(time):
    hour, separator, minute = time.partition(":")

    if not separator or not hour.isdigit() or not minute.isdigit():
        return None

    hour = int(hour)
    minute = int(minute)

    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return None

    return hour * 60 + minute


def check_availability(available, requested):
    day, separator, requested_time = requested.strip().partition(" ")

    if not separator or not day:
        return False, "INVALID"

    requested_minutes = time_to_minutes(requested_time)

    if requested_minutes is None:
        return False, "INVALID"

    slots = available.split(";")
    next_available = None

    for slot in slots:
        slot_day, separator, time_range = slot.strip().partition(" ")

        if not separator:
            continue

        start, separator, end = time_range.partition("-")

        if not separator:
            continue

        start_minutes = time_to_minutes(start)
        end_minutes = time_to_minutes(end)

        if start_minutes is None or end_minutes is None:
            continue

        if end_minutes <= start_minutes:
            if start_minutes >= 12 * 60 and end_minutes < 12 * 60:
                end_minutes += 12 * 60
            else:
                continue

        if slot_day.lower() == day.lower():

            if start_minutes <= requested_minutes < end_minutes:
                return True, None

            if start_minutes > requested_minutes:
                if next_available is None or start_minutes < next_available[0]:
                    next_available = (start_minutes, slot_day, start)

    if next_available:
        return False, next_available[1] + " " + next_available[2]

    return False, "No later available time recorded"


def save_student(email, faculty, requested, status, resolution):
    with open(student_file, "a") as file:
        file.write(
            f"{email}|{faculty}|{requested}|{status}|{resolution}\n"
        )


def student_login(email):
    print("\n========== STUDENT PORTAL ==========")
    print(
        "\nHi student! Welcome to Campus Faculty Locator "
        "& Office Hour Scheduler. I'm Priyanshu, here to help you."
    )

    faculty_name = get_input("\nWhich faculty details do you need? ")

    teacher = find_teacher(faculty_name)

    if teacher is None:
        print("\nSorry Student, faculty details are not available.")
        return

    name, cabin, available = teacher

    print("\nYes! Faculty is present in our directory.")
    print("Faculty Name:", name)
    print("Cabin Details:", cabin)
    print("Available Times:", available)

    print("\nEnter the day and time when you want to visit.")
    print("Format: Day HH:MM")
    print("Examples:")
    print("Monday 11:30")
    print("Tuesday 14:00")
    print("Friday 16:30")
    print("Use 24-hour time format.")
    print("Remember: 1:20 PM must be entered as 13:20.")

    requested = get_input("\nEnter your required day and time: ")

    is_available, next_time = check_availability(available, requested)

    if next_time == "INVALID":
        print("\nInvalid time format. Please use Day HH:MM.")
        return

    if is_available:
        print("\nGood news Student! The faculty is available.")
        print("You may visit the faculty at:", cabin)
        status = "Faculty available"

    else:
        print("\nSorry Student, the faculty is currently busy.")
        print("You may visit at:", next_time)
        status = "Faculty busy"

    resolution = get_input(
        "\nWas your query resolved? (Yes/No/Pending): "
    )

    if resolution.lower() not in ["yes", "no", "pending"]:
        resolution = "Pending"

    save_student(email, name, requested, status, resolution)

    print("\nYour interaction has been recorded.")


def coordinator_login():
    print("\n========== PROGRAM COORDINATOR PORTAL ==========")

    name = get_input("Enter your name: ")

    print("\nWelcome", name)
    print("\n========== STUDENT INTERACTION HISTORY ==========")

    with open(student_file, "r") as file:
        records = [
            line.strip().split("|", 4)
            for line in file if line.strip()
        ]

    if not records:
        print("\nNo student interactions recorded yet.")
        return

    for record in records:
        if len(record) == 5:
            email, faculty, requested, status, resolution = record

            print("\nStudent Email:", email)
            print("Faculty:", faculty)
            print("Requested Time:", requested)
            print("Faculty Status:", status)
            print("Problem Resolved:", resolution)
            print("----------------------------------------")


def main():
    create_files()

    while True:
        print("\n========================================")
        print(" CAMPUS FACULTY LOCATOR & OFFICE HOUR SCHEDULER")
        print("========================================")

        print("\n1. Student Login")
        print("2. Faculty Login")
        print("3. Program Coordinator Login")
        print("4. Exit")

        print("\nWrite 'exit' at any time to close the program.")

        choice = get_input("\nEnter your choice: ")

        if choice == "4":
            print("\nHave a nice day!")
            break

        elif choice in ["1", "2", "3"]:
            email = get_input("\nEnter your Bennett email: ")

            role = authenticate(email)

            if role == "student" and choice == "1":
                student_login(email)

            elif role == "faculty" and choice == "2":
                faculty_login()

            elif role == "coordinator" and choice == "3":
                coordinator_login()

            else:
                print("\nInvalid email or login category.")

        else:
            print("\nInvalid choice. Please select 1, 2, 3 or 4.")


main()
