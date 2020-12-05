from pandas import read_csv, DataFrame, set_option
set_option('display.max_rows', 350)
print('Загружаю группы... ')
groups = read_csv('groups.csv', sep=";")
print('Загружаю результаты... ')
results = read_csv('results.csv', sep=";")
print('Загружаю студентов... ')
students = read_csv('students.csv', sep=";")
print('Загружаю предметы... ')
subjects = read_csv('subjects.csv', sep=";")
print('Загружаю преподавателей... ')
teachers = read_csv('teachers.csv', sep=";")
print('Готово! Данные загружены!')

print("""
Для получения студентов по наименованию группы введите команду 'студенты' и название группы в верхнем или нижнем регистре. Например: 'студенты ПИ1-1'
""")
print("""
Для получения преподавателей по наименованию группы введите команду 'преподаватели' и название группы в верхнем или нижнем регистре. Например: 'преподаватели ПИ1-1'
""")
while True:
    comm = input('Введите команду... ').upper()
    comm = comm.split()
    if 'СТУДЕНТЫ' in comm:
        group = comm[1]
        id_group = int(groups['id'].where(groups['name'] == group).dropna())
        studentsOfThisGroup = students[['last_name', 'first_name', 'id']].where(students['group_id'] == id_group).dropna()
        print(f'Студенты группы {group}:')
        print(studentsOfThisGroup.to_string(index=False, header=['Фамилия', 'Имя', 'ID']))
    if 'ПРЕПОДАВАТЕЛИ' in comm:
        group = comm[1]
        print(f'Преподаватели группы {group}:')
        id_group = int(groups['id'].where(groups['name'] == group).dropna())
        firstStudentOfThisGroup = students[['id']].where(students['group_id'] == id_group).dropna().iloc[0]
        idFirstStudentOfThisGroup= round(float(firstStudentOfThisGroup.to_string(index=False, header=False)))
        idTeachersOfThisGroup = results['teacher_id'].where(results['student_id'] == idFirstStudentOfThisGroup).dropna().astype('int32').values.tolist()
        TeachersOfThisGroup = teachers[['last_name', 'first_name', 'middle_name']].where(teachers['id'].isin(idTeachersOfThisGroup)).dropna()
        TeachersOfThisGroup = TeachersOfThisGroup.to_string(index=False, header=False)
        print(TeachersOfThisGroup)
