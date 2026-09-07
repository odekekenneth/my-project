import os

FILENAME = "study_log.txt"
sessions = []


def classify_session(duration):
    """Classifies session duration as Short, Medium, or Long."""
    if duration < 30:
        return "Short"
    elif 30 <= duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session():
    """Prompts for details, validates input, and logs a new session."""
    print("\n--- Add a Study Session ---")
    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date_label = input("Enter date/day label (e.g., 2026-08-31 or Mon): ").strip()

    # Input validation for positive number duration
    while True:
        try:
            duration = float(input("Enter duration in minutes: "))
            if duration > 0:
                break
            else:
                print("Duration must be a positive number. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number for duration.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date_label,
        "duration": duration,
    }
    sessions.append(session)
    print(f"Session for '{subject}' added successfully!")


def view_sessions():
    """Displays all logged study sessions in a formatted table."""
    if not sessions:
        print("\nNo study sessions logged yet.")
        return

    print("\n" + "=" * 65)
    print(
        f"{'Date/Day':<12} | {'Subject':<15} | {'Topic':<15} | {'Mins':<6} | {'Category':<8}"
    )
    print("=" * 65)

    for s in sessions:
        category = classify_session(s["duration"])
        print(
            f"{s['date']:<12} | {s['subject']:<15} | {s['topic']:<15} | {s['duration']:<6.1f} | {category:<8}"
        )
    print("=" * 65)


def search_by_subject():
    """Searches sessions by subject (case-insensitive) and computes total time."""
    if not sessions:
        print("\nNo sessions available to search.")
        return

    search_term = input("\nEnter subject to search: ").strip().lower()
    matches = [s for s in sessions if s["subject"].lower() == search_term]

    if not matches:
        print(f"\nNo sessions found for subject: '{search_term}'")
        return

    total_minutes = sum(s["duration"] for s in matches)

    print(f"\n--- Search Results for '{search_term}' ---")
    print("=" * 65)
    print(
        f"{'Date/Day':<12} | {'Subject':<15} | {'Topic':<15} | {'Mins':<6} | {'Category':<8}"
    )
    print("=" * 65)
    for s in matches:
        category = classify_session(s["duration"])
        print(
            f"{s['date']:<12} | {s['subject']:<15} | {s['topic']:<15} | {s['duration']:<6.1f} | {category:<8}"
        )
    print("=" * 65)
    print(
        f"Total time spent on '{search_term}': {total_minutes:.1f} minutes ({total_minutes / 60:.2f} hours)"
    )


def study_statistics():
    """Computes overall statistics, subject totals, weakest subject, and longest session."""
    if not sessions:
        print("\nNo study sessions logged to calculate statistics.")
        return

    total_mins = sum(s["duration"] for s in sessions)
    total_hours = total_mins / 60

    # Aggregate by subject
    subject_totals = {}
    for s in sessions:
        subj = s["subject"]
        subject_totals[subj] = subject_totals.get(subj, 0) + s["duration"]

    # Subject with least study time (weakest area)
    weakest_subject = min(subject_totals, key=subject_totals.get)
    weakest_hours = subject_totals[weakest_subject] / 60

    # Longest single session
    longest_session = max(sessions, key=lambda s: s["duration"])

    print("\n--- Study Statistics & Analysis ---")
    print(f"Total time studied overall : {total_hours:.2f} hours ({total_mins:.1f} mins)")
    print("\nTotal Hours Studied per Subject:")
    for subj, mins in subject_totals.items():
        print(f"  - {subj}: {mins / 60:.2f} hrs ({mins:.1f} mins)")

    print(
        f"\nWeakest Subject (Least Studied): {weakest_subject} ({weakest_hours:.2f} hrs)"
    )
    print(
        f"Longest Session Recorded      : {longest_session['subject']} - '{longest_session['topic']}' ({longest_session['duration']:.1f} mins)"
    )


def load_sessions():
    """Loads saved sessions from study_log.txt if the file exists."""
    if not os.path.exists(FILENAME):
        return

    try:
        with open(FILENAME, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split("|")
                    if len(parts) == 4:
                        sessions.append(
                            {
                                "subject": parts[0],
                                "topic": parts[1],
                                "date": parts[2],
                                "duration": float(parts[3]),
                            }
                        )
    except Exception as e:
        print(f"Error loading saved data: {e}")


def save_sessions():
    """Saves all logged sessions to study_log.txt."""
    try:
        with open(FILENAME, "w") as file:
            for s in sessions:
                file.write(
                    f"{s['subject']}|{s['topic']}|{s['date']}|{s['duration']}\n"
                )
        print("All sessions successfully saved to file.")
    except Exception as e:
        print(f"Error saving data: {e}")


def main():
    """Main menu loop."""
    load_sessions()

    while True:
        print("\n=========================================")
        print("          SMART STUDY PLANNER            ")
        print("=========================================")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        print("=========================================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session()
        elif choice == "2":
            view_sessions()
        elif choice == "3":
            search_by_subject()
        elif choice == "4":
            study_statistics()
        elif choice == "5":
            save_sessions()
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose a number between 1 and 5.")


if __name__ == "__main__":
    main()