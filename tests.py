import pytest
from typing import Set

from final import Teacher, create_schedule

class TestCreateScheduleBasic:
    def test_simple_schedule_one_teacher(self):
        subjects = {'Математика', 'Фізика'}
        teachers = [
            Teacher('Іван', 'Петров', 35, 'ivan@example.com', {'Математика', 'Фізика'})
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule is not None
        assert len(schedule) == 1
        assert schedule[0].assigned_subjects == {'Математика', 'Фізика'}

    def test_simple_schedule_two_teachers(self):
        subjects = {'Математика', 'Фізика', 'Хімія'}
        teachers = [
            Teacher('Іван', 'Петров', 35, 'ivan@example.com', {'Математика', 'Фізика'}),
            Teacher('Марія', 'Сидоренко', 30, 'maria@example.com', {'Хімія'})
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule is not None
        assert len(schedule) == 2

        all_assigned = set()
        for teacher in schedule:
            all_assigned |= teacher.assigned_subjects
        assert all_assigned == subjects

    def test_empty_subjects(self):
        subjects = set()
        teachers = [
            Teacher('Іван', 'Петров', 35, 'ivan@example.com', {'Математика'})
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule == []

    def test_empty_teachers(self):
        subjects = {'Математика', 'Фізика'}
        teachers = []

        schedule = create_schedule(subjects, teachers)

        assert schedule is None


class TestCreateScheduleGreedyLogic:
    def test_greedy_choice_max_coverage(self):
        subjects = {'Математика', 'Фізика', 'Хімія'}
        teachers = [
            Teacher('Іван', 'Петров', 35, 'ivan@example.com', {'Математика'}),
            Teacher('Марія', 'Сидоренко', 30, 'maria@example.com', {'Математика', 'Фізика', 'Хімія'})
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule[0].first_name == 'Марія'
        assert len(schedule[0].assigned_subjects) == 3
        assert len(schedule) == 1

    def test_greedy_choice_younger_teacher(self):
        subjects = {'Математика', 'Фізика'}
        teachers = [
            Teacher('Іван', 'Петров', 45, 'ivan@example.com', {'Математика', 'Фізика'}),
            Teacher('Марія', 'Сидоренко', 30, 'maria@example.com', {'Математика', 'Фізика'}),
            Teacher('Петро', 'Коваль', 50, 'petro@example.com', {'Математика', 'Фізика'})
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule[0].first_name == 'Марія'
        assert schedule[0].age == 30
        assert len(schedule) == 1


class TestCreateScheduleRealScenario:
    """Тест реального сценарію з завдання"""

    @pytest.fixture
    def real_data(self):
        subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
        teachers = [
            Teacher('Олександр', 'Іваненко', 45, 'o.ivanenko@example.com', {'Математика', 'Фізика'}),
            Teacher('Марія', 'Петренко', 38, 'm.petrenko@example.com', {'Хімія'}),
            Teacher('Сергій', 'Коваленко', 50, 's.kovalenko@example.com', {'Інформатика', 'Математика'}),
            Teacher('Наталія', 'Шевченко', 29, 'n.shevchenko@example.com', {'Біологія', 'Хімія'}),
            Teacher('Дмитро', 'Бондаренко', 35, 'd.bondarenko@example.com', {'Фізика', 'Інформатика'}),
            Teacher('Олена', 'Гриценко', 42, 'o.grytsenko@example.com', {'Біологія'})
        ]
        return subjects, teachers

    def test_real_scenario_covers_all_subjects(self, real_data):
        subjects, teachers = real_data
        schedule = create_schedule(subjects, teachers)

        assert schedule is not None

        all_assigned = set()
        for teacher in schedule:
            all_assigned |= teacher.assigned_subjects

        assert all_assigned == subjects

    def test_real_scenario_minimal_teachers(self, real_data):
        subjects, teachers = real_data
        schedule = create_schedule(subjects, teachers)

        assert schedule is not None
        assert len(schedule) >= 3
        assert len(schedule) <= len(teachers)

    def test_real_scenario_assigned_subjects_valid(self, real_data):
        subjects, teachers = real_data
        schedule = create_schedule(subjects, teachers)

        for teacher in schedule:
            assert teacher.assigned_subjects.issubset(teacher.can_teach_subjects)
            assert len(teacher.assigned_subjects) > 0

    def test_real_scenario_no_duplicate_assignments(self, real_data):
        subjects, teachers = real_data
        schedule = create_schedule(subjects, teachers)

        assigned_count = {}
        for teacher in schedule:
            for subject in teacher.assigned_subjects:
                assigned_count[subject] = assigned_count.get(subject, 0) + 1

        for subject, count in assigned_count.items():
            assert count == 1


class TestCreateScheduleEdgeCases:
    def test_impossible_to_cover_all_subjects(self):
        subjects = {'Математика', 'Фізика', 'Хімія', 'Біологія'}
        teachers = [
            Teacher('Іван', 'Петров', 35, 'ivan@example.com', {'Математика', 'Фізика'})
            # Хімія та Біологія не покриті жодним викладачем
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule is None

    def test_teacher_with_no_subjects(self):
        subjects = {'Математика'}
        teachers = [
            Teacher('Іван', 'Петров', 35, 'ivan@example.com', set()),
            Teacher('Марія', 'Сидоренко', 30, 'maria@example.com', {'Математика'})
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule is not None
        assert len(schedule) == 1
        assert schedule[0].first_name == 'Марія'

    def test_all_teachers_same_age(self):
        subjects = {'Математика', 'Фізика'}
        teachers = [
            Teacher('Іван', 'Петров', 35, 'ivan@example.com', {'Математика'}),
            Teacher('Марія', 'Сидоренко', 35, 'maria@example.com', {'Фізика'})
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule is not None
        assert len(schedule) == 2


class TestCreateScheduleComplexScenarios:
    def test_multiple_optimal_solutions(self):
        subjects = {'Математика', 'Фізика', 'Хімія'}
        teachers = [
            Teacher('Іван', 'Петров', 40, 'ivan@example.com', {'Математика', 'Фізика'}),
            Teacher('Марія', 'Сидоренко', 35, 'maria@example.com', {'Математика', 'Фізика'}),
            Teacher('Олег', 'Коваль', 30, 'oleg@example.com', {'Хімія'})
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule[0].first_name == 'Марія'
        assert schedule[0].age == 35

    def test_large_number_of_subjects_and_teachers(self):
        subjects = {f'Предмет_{i}' for i in range(20)}
        teachers = [
            Teacher(f'Викладач_{i}', 'Прізвище', 30 + i, f'teacher{i}@example.com',
                    {f'Предмет_{j}' for j in range(i, min(i + 3, 20))})
            for i in range(20)
        ]

        schedule = create_schedule(subjects, teachers)

        assert schedule is not None

        all_assigned = set()
        for teacher in schedule:
            all_assigned |= teacher.assigned_subjects

        assert all_assigned == subjects

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])