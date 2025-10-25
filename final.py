class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = can_teach_subjects
        self.assigned_subjects = set()

    def __repr__(self):
        return f"Teacher({self.first_name} {self.last_name}, {self.age} років)"

def create_schedule(subjects, teachers):
    uncovered_subjects = subjects.copy()

    selected_teachers = []
    available_teachers = teachers.copy()

    while uncovered_subjects:
        best_teacher = None
        best_covered_subjects = set()

        for teacher in available_teachers:
            covered = teacher.can_teach_subjects & uncovered_subjects

            if len(covered) > len(best_covered_subjects):
                best_teacher = teacher
                best_covered_subjects = covered
            elif len(covered) == len(best_covered_subjects) and covered:
                if best_teacher is None or teacher.age < best_teacher.age:
                    best_teacher = teacher
                    best_covered_subjects = covered

        if best_teacher is None or not best_covered_subjects:
            return None

        best_teacher.assigned_subjects = best_covered_subjects.copy()
        selected_teachers.append(best_teacher)

        uncovered_subjects -= best_covered_subjects
        available_teachers.remove(best_teacher)

    return selected_teachers


if __name__ == '__main__':
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}

    teachers = [
        Teacher('Олександр', 'Іваненко', 45, 'o.ivanenko@example.com',
                {'Математика', 'Фізика'}),
        Teacher('Марія', 'Петренко', 38, 'm.petrenko@example.com',
                {'Хімія'}),
        Teacher('Сергій', 'Коваленко', 50, 's.kovalenko@example.com',
                {'Інформатика', 'Математика'}),
        Teacher('Наталія', 'Шевченко', 29, 'n.shevchenko@example.com',
                {'Біологія', 'Хімія'}),
        Teacher('Дмитро', 'Бондаренко', 35, 'd.bondarenko@example.com',
                {'Фізика', 'Інформатика'}),
        Teacher('Олена', 'Гриценко', 42, 'o.grytsenko@example.com',
                {'Біологія'})
    ]

    schedule = create_schedule(subjects, teachers)

    if schedule:
        print("Розклад занять:")
        print("=" * 70)
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(sorted(teacher.assigned_subjects))}\n")

        print("=" * 70)
        print(f"Всього викладачів у розкладі: {len(schedule)}")
        all_assigned = set()
        for teacher in schedule:
            all_assigned |= teacher.assigned_subjects
        print(f"Покриті предмети: {', '.join(sorted(all_assigned))}")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")