class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    # Метод выставления оценки лектору студентом
    def rate_lecture(self, lecturer, course, grade):
        # Проверяем, что лектор - это объект класса Lecturer,
        # курс есть у студента в изучении и этот же курс ведет лектор
        if (isinstance(lecturer, Lecturer) and
                course in self.courses_in_progress and
                course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    # Метод для расчета средней оценки
    def average_grade(self):
        # Собираем все оценки из всех списков в словаре в один плоский список
        total_grades = sum(self.grades.values(), [])
        if not total_grades:
            return 0
        return sum(total_grades) / len(total_grades)

    def __str__(self):
        # Получаем среднюю оценку
        avg_grade = self.average_grade()
        # Склеиваем списки курсов через запятую
        in_progress = ', '.join(self.courses_in_progress) if self.courses_in_progress else 'Нет'
        finished = ', '.join(self.finished_courses) if self.finished_courses else 'Нет'

        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_grade:.1f}\n"
                f"Курсы в процессе изучения: {in_progress}\n"
                f"Завершенные курсы: {finished}")

    # Магические методы для сравнения студентов
    def __lt__(self, other):
        if not isinstance(other, Student):
            return "Нельзя сравнить!"
        return self.average_grade() < other.average_grade()

    def __le__(self, other):
        if not isinstance(other, Student):
            return "Нельзя сравнить!"
        return self.average_grade() <= other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return "Нельзя сравнить!"
        return self.average_grade() == other.average_grade()

class Mentor: # Родительский класс
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer (Mentor): # Класс лекторов

    def __init__(self, name, surname):
        super().__init__(name, surname)
        # Добавляем специфичный атрибут только для лекторов
        self.grades = {}

    # Метод для расчета средней оценки
    def average_grade(self):
        total_grades = sum(self.grades.values(), [])
        if not total_grades:
            return 0
        return sum(total_grades) / len(total_grades)

    def __str__(self):
        avg_grade = self.average_grade()
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {avg_grade:.1f}")

    # Магические методы для сравнения лекторов
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return "Нельзя сравнить!"
        return self.average_grade() < other.average_grade()

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return "Нельзя сравнить!"
        return self.average_grade() <= other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return "Нельзя сравнить!"
        return self.average_grade() == other.average_grade()

class Reviewer (Mentor): # Класс проверяющих
    def rate_hw(self, student, course, grade):
        # Проверяем, что студент - это объект класса Student,
        # курс прикреплен к проверяющему и курс изучается студентом
        if (isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}")

 # Cредняя оценка за ДЗ по всем студентам в рамках конкретного курса
def student_average_grade (students_list, course_name):
    total_grades = []
    for student in students_list:
        # Проверяем, есть ли у студента оценки по этому курсу
        if course_name in student.grades:
            total_grades.extend(student.grades[course_name])
    if not total_grades:
        return 0
    return sum(total_grades) / len(total_grades)

# Cредняя оценка за лекции по всем лекторам в рамках конкретного курса
def lecturer_average_grade(lecturers_list, course_name):
    total_grades = []
    for lecturer in lecturers_list:
        # Проверяем, есть ли у лектора оценки по этому курсу
        if course_name in lecturer.grades:
            total_grades.extend(lecturer.grades[course_name])
    if not total_grades:
        return 0
    return sum(total_grades) / len(total_grades)

# Проверка 4 задания
# 1. Создаем двух студентов
student_1 = Student('Ruoy', 'Eman', 'М')
student_1.courses_in_progress += ['Python', 'Git']

student_2 = Student('Anna', 'Smith', 'Ж')
student_2.courses_in_progress += ['Python']

# 2. Создаем двух лекторов
lecturer_1 = Lecturer('John', 'Doe')
lecturer_1.courses_attached += ['Python', 'Git']

lecturer_2 = Lecturer('Jane', 'Doe')
lecturer_2.courses_attached += ['Python']

# 3. Создаем двух проверяющих (Reviewer)
reviewer_1 = Reviewer('Some', 'Buddy')
reviewer_1.courses_attached += ['Python']

reviewer_2 = Reviewer('Ostap', 'Bender')
reviewer_2.courses_attached += ['Git']

# 4. Выставляем оценки студентам за ДЗ (это делают проверяющие)
reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 9)

reviewer_1.rate_hw(student_2, 'Python', 8)
reviewer_1.rate_hw(student_2, 'Python', 7)

reviewer_2.rate_hw(student_1, 'Git', 10)

# 5. Выставляем оценки лекторам за лекции (это делают студенты)
student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_1, 'Git', 9)

student_2.rate_lecture(lecturer_1, 'Python', 8)
student_2.rate_lecture(lecturer_2, 'Python', 10)

#Работа функций
# Списки студентов и лекторов
students_list = [student_1, student_2]
lecturers_list = [lecturer_1, lecturer_2]

print("Подсчет средних оценок по курсам")

# Считаем для студентов по курсу Python
avg_stud_python = student_average_grade (students_list, 'Python')
print(f"Средняя оценка студентов по курсу Python: {avg_stud_python:.1f}")

# Считаем для лекторов по курсу Python
avg_lect_python = lecturer_average_grade (lecturers_list, 'Python')
print(f"Средняя оценка лекторов по курсу Python: {avg_lect_python:.1f}")

# Считаем для лекторов по курсу Git
avg_lect_git = lecturer_average_grade (lecturers_list, 'Git')
print(f"Средняя оценка лекторов по курсу Git: {avg_lect_git:.1f}")

# Проверяем сравнение
print(f"Студент 1 лучше Студента 2? {student_1 > student_2}")
print(f"Лектор 1 лучше Лектора 2? {lecturer_1 > lecturer_2}")

# # Проверка 3 задания
# # 1. Студенты
# student1 = Student('Ruoy', 'Eman', 'М')
# student1.courses_in_progress += ['Python', 'Git']
# student1.finished_courses += ['Введение в программирование']
#
# student2 = Student('Anna', 'Smith', 'Ж')
# student2.courses_in_progress += ['Python']
#
# # 2. Лекторы и проверяющие
# lecturer1 = Lecturer('John', 'Doe')
# lecturer1.courses_attached += ['Python', 'Git']
#
# lecturer2 = Lecturer('Jane', 'Doe')
# lecturer2.courses_attached += ['Python']
#
# reviewer = Reviewer('Some', 'Buddy')
# reviewer.courses_attached += ['Python', 'Git']
#
# # 3. Выставляем оценки
# reviewer.rate_hw(student1, 'Python', 10)
# reviewer.rate_hw(student1, 'Git', 8)
# reviewer.rate_hw(student2, 'Python', 7)
#
# student1.rate_lecture(lecturer1, 'Python', 9)
# student2.rate_lecture(lecturer1, 'Python', 10)
# student1.rate_lecture(lecturer2, 'Python', 6)
#
# # 4. Проверяем __str__ (красивый вывод)
# print(reviewer)
# print("-" * 20)
# print(lecturer1)
# print("-" * 20)
# print(student1)
# print("-" * 20)
#
# # 5. Проверяем сравнение
# print(f"Студент 1 лучше Студента 2? {student1 > student2}")
# print(f"Лектор 1 лучше Лектора 2? {lecturer1 > lecturer2}")


# lecturer = Lecturer('Иван', 'Иванов')
# reviewer = Reviewer('Пётр', 'Петров')
# # print(isinstance(lecturer, Mentor)) # True
# # print(isinstance(reviewer, Mentor)) # True
# # print(lecturer.courses_attached)    # []
# # print(reviewer.courses_attached)    # []
# student = Student('Алёхина', 'Ольга', 'Ж')
#
# student.courses_in_progress += ['Python', 'Java']
# lecturer.courses_attached += ['Python', 'C++']
# reviewer.courses_attached += ['Python', 'C++']

# print(student.rate_lecture(lecturer, 'Python', 7))  # None
# print(student.rate_lecture(lecturer, 'Java', 8))  # Ошибка
# print(student.rate_lecture(lecturer, 'С++', 8))  # Ошибка
# print(student.rate_lecture(reviewer, 'Python', 6))  # Ошибка
#
# print(lecturer.grades)  # {'Python': [7]}


     # def rate_hw(self, student, course, grade):
     #     if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
     #         if course in student.grades:
     #             student.grades[course] += [grade]
     #         else:
     #             student.grades[course] = [grade]
     #     else:
     #         return 'Ошибка'


# best_student = Student('Ruoy', 'Eman', 'your_gender')
# best_student.courses_in_progress += ['Python']
#
# cool_mentor = Reviewer('Some', 'Buddy')
# cool_mentor.courses_attached += ['Python']
#
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
#
# print(best_student.grades)