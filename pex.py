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
print("""
Для получения списка группы у определенного преподавателя введите команду 'группы' и фамилию преподавателя в именительном падеже. Например: 'группы Милованов'
""")
print("""
Для получения оценок конкретного студента введите команду 'оценки', фамилию и имя студента в именительном падеже. Например: 'оценки Бирюков Максим'
""")
print("""
Для получения среднего балла всех студентов у конкретного преподавателя введите команду 'средний балл' и фамилию преподавателя в именительном падеже. Например: 'средний балл Милованов'
""")

print("""
Для для того, чтобы узнать, ведет ли данный преподаватель у конкретной группы, введите название группы и фамилию преподавателя в именительном падеже. Например: 'ПИ1-1 Милованов'
""")

while True:
    comm = input('Введите команду... ').upper()
    comm = comm.split()
    if len(comm) < 2 and 'КОМАНДЫ' not in comm:
    	print('Команда была введена неверно, повторите попытку. Для вывода всех команд введите команду "команды"')
    if 'СТУДЕНТЫ' in comm:
        group = comm[1]
        id_group = int(groups['id'].where(groups['name'] == group).dropna())
        studentsOfThisGroup = students[['last_name', 'first_name']].where(students['group_id'] == id_group).dropna()
        print(f'Студенты группы {group}:')
        print(studentsOfThisGroup.to_string(index=False, header=['Фамилия', 'Имя']))
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
    if 'ГРУППЫ' in comm:
    	teacher = comm[1].lower().capitalize()
    	print(f'Вывод групп преподавателя {teacher}')
    	idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32')[0]
    	idsStudents = results['student_id'].where(results['teacher_id'] == idTeacher).dropna().astype('int32').values.tolist()
    	idsGroup = students['group_id'].where(students['id'].isin(idsStudents)).dropna().astype('int32').values.tolist()

    	idsGroup_undublicated = []
    	for id in idsGroup:
    		if id not in idsGroup_undublicated:
    			idsGroup_undublicated.append(id)
    	idsGroup_undublicated.sort()
    	namesOfGroups = groups['name'].where(groups['id'].isin(idsGroup_undublicated)).dropna().to_string(index=False, header=False) 
    	print(namesOfGroups)
    if 'ОЦЕНКИ' in comm:
    	first_name = comm[2]
    	last_name = comm[1]
    	first_name = first_name.lower().capitalize()
    	last_name = last_name.lower().capitalize()
    	idStudent = students['id'].where((students['last_name'] == last_name) & (students['first_name'] == first_name)).dropna().astype('int32').values.tolist()[0]
    	print(idStudent)
    	resStudent = results[[ 'subject','att1', 'att2', 'exam', 'total']].where(results['student_id'] == idStudent).dropna().astype('int32')
    	resStudent = subjects.merge(resStudent, left_on="id", right_on="subject")[['subject_name', 'att1', 'att2', 'exam', 'total']]
    	outputResStudent = resStudent.to_string(index=False, header=['Предмет', 'Первая аттестация', 'Вторая аттестация', 'Экзамен', 'Тотал'])
    	print(outputResStudent)
    if 'СРЕДНИЙ' in comm:
    	teacher = comm[2].lower().capitalize()
    	idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32')[0]
    	allPoints = results['total'].where(results['teacher_id'] == idTeacher).dropna().astype('int32').values.tolist()
    	average = sum(allPoints)/len(allPoints)
    	print(average)
    
