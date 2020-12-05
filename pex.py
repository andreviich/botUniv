from pandas import read_csv, DataFrame, set_option
set_option('display.max_rows', 1000)
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
Для для того, чтобы узнать, ведет ли данный преподаватель у конкретной группы, введите "ведёт" ,  фамилию преподавателя в именительном падеже и название группы. Например: 'ведёт Милованов ПИ1-1'
""")
print("""
Для для того, чтобы узнать все оценки по конкретному предмету, введите "оценки по предмету" и название предмета. Например: 'оценки по предмету философия'
""")
print("""
Для для того, чтобы узнать все оценки у конкретного преподавателя, введите "оценки преподавателя" и фамилию преподавателя в именительном падеже. Например: 'оценки преподавателя Милованов'
""")
print("""
Для для того, чтобы узнать все оценки у конкретного преподавателя, введите "оценки преподавателя" и фамилию преподавателя в именительном падеже. Например: 'оценки преподавателя Милованов'
""")
def tryAgain(message):
	print(message)
def OutMessage(message):
	print(message)
while True:
	comm = input('Введите команду... ').upper()
	comm = comm.split()
	allSubjects = subjects['subject_name'].values.tolist()
	allTeachers = teachers['last_name'].values.tolist()
	allGroups = groups['name'].values.tolist()
	if len(comm) < 2 and 'КОМАНДЫ' not in comm:
		OutMessage('Команда была введена неверно, повторите попытку. Для вывода всех команд введите команду "команды"')
	if 'СТУДЕНТЫ' in comm:
		group = comm[1]
		def getAllStudents(group):
			try:	
				id_group = int(groups['id'].where(groups['name'] == group).dropna())
			except:
				tryAgain('Группа не найдена')
				return
			studentsOfThisGroup = students[['last_name', 'first_name']].where(students['group_id'] == id_group).dropna()
			OutMessage(f'Студенты группы {group}:')
			OutMessage(studentsOfThisGroup.to_string(index=False, header=['Фамилия', 'Имя']))
		getAllStudents(group)
	if 'ПРЕПОДАВАТЕЛИ' in comm:
		group = comm[1]
		OutMessage(f'Преподаватели группы {group}:')
		def getAllTeachers(group):
			try:
				id_group = int(groups['id'].where(groups['name'] == group).dropna())
			except:
				tryAgain('Группа не найдена')
				return
			firstStudentOfThisGroup = students[['id']].where(students['group_id'] == id_group).dropna().iloc[0]
			idFirstStudentOfThisGroup= round(float(firstStudentOfThisGroup.to_string(index=False, header=False)))
			idTeachersOfThisGroup = results['teacher_id'].where(results['student_id'] == idFirstStudentOfThisGroup).dropna().astype('int32').values.tolist()
			TeachersOfThisGroup = teachers[['last_name', 'first_name', 'middle_name']].where(teachers['id'].isin(idTeachersOfThisGroup)).dropna()
			TeachersOfThisGroup = TeachersOfThisGroup.to_string(index=False, header=False)
			OutMessage(TeachersOfThisGroup)
		getAllTeachers(group)
	if 'ГРУППЫ' in comm:
		teacher = comm[1].lower().capitalize()
		OutMessage(f'Вывод групп преподавателя {teacher}')
		def grps(teacher):
			try:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32')[0]
			except:
				tryAgain('Преподаватель не найден')
				return
			idsStudents = results['student_id'].where(results['teacher_id'] == idTeacher).dropna().astype('int32').values.tolist()
			idsGroup = students['group_id'].where(students['id'].isin(idsStudents)).dropna().astype('int32').values.tolist()

			idsGroup_undublicated = []
			for id in idsGroup:
				if id not in idsGroup_undublicated:
					idsGroup_undublicated.append(id)
			idsGroup_undublicated.sort()
			namesOfGroups = groups['name'].where(groups['id'].isin(idsGroup_undublicated)).dropna().to_string(index=False, header=False) 
			OutMessage(namesOfGroups)
		grps(teacher)
	if 'ОЦЕНКИ' in comm and len(comm)==3 and not 'ПРЕПОДАВАТЕЛЯ' in comm:
		first_name = comm[2]
		last_name = comm[1]
		first_name = first_name.lower().capitalize()
		last_name = last_name.lower().capitalize()
		def getAllPoints(first_name, last_name):
			try:	
				idStudent = students['id'].where((students['last_name'] == last_name) & (students['first_name'] == first_name)).dropna().astype('int32').values.tolist()[0]
			except: 
				tryAgain('Студент не найден')
				return
			resStudent = results[[ 'subject','att1', 'att2', 'exam', 'total']].where(results['student_id'] == idStudent).dropna().astype('int32')
			resStudent = subjects.merge(resStudent, left_on="id", right_on="subject")[['subject_name', 'att1', 'att2', 'exam', 'total']]
			outputResStudent = resStudent.to_string(index=False, header=['Предмет', 'Первая аттестация', 'Вторая аттестация', 'Экзамен', 'Тотал'])
			OutMessage(outputResStudent)
		getAllPoints(first_name, last_name)
	if 'СРЕДНИЙ' in comm and len(comm) == 3: 
		teacher = comm[2].lower().capitalize()
		def average(teacher):
			try:	
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32')[0]
			except:
				tryAgain('Преподаватель не найден')
				return
			allPoints = results['total'].where(results['teacher_id'] == idTeacher).dropna().astype('int32').values.tolist()
			average = sum(allPoints)/len(allPoints)
			OutMessage(average)
		average(teacher)
	if 'ВЕДЕТ' in comm and len(comm) ==3 or 'ВЕДЁТ' in comm and len(comm) ==3:
		group = comm[2]
		teacher = comm[1].lower().capitalize()
		def isGroupEducatedByTeacher(group, teacher):
			try:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32')[0]
			except:
				tryAgain('Преподаватель не найден')
				return
			try:
				OutMessage(group)
				id_group = groups['id'].where(groups['name'] == group).dropna().astype('int32').values.tolist()[0]
			except Exception as e:
				tryAgain('Данная группа не обнаружена в списке')
				return 
			try:
				idsStudents = results['student_id'].where(results['teacher_id'] == idTeacher).dropna().astype('int32').values.tolist()[0]
			except:
				tryAgain('У данного преподавателя студенты не найдены')
				return
			idsTeachers = results['teacher_id'].where(results['student_id'] == idsStudents).dropna().astype('int32').values.tolist()
			if idTeacher in idsTeachers:
				OutMessage(f'{teacher} ведёт у {group}')
			else:
				OutMessage(f'{teacher} не ведёт у {group}')
		isGroupEducatedByTeacher(group, teacher)
	if 'ОЦЕНКИ' in comm and len(comm)==3 and 'ПРЕПОДАВАТЕЛЯ' in comm:
		teacher = comm[2].lower().capitalize()
		def getAllPointsOfTeacher(teacher):
			try:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32')[0]
			except:
				tryAgain('Преподаватель не найден')
				return
			allpoints = results[['student_id', 'total']].where(results['teacher_id'] == idTeacher).dropna().astype('int32')
			OutMessage(allpoints)
		getAllPointsOfTeacher(teacher)
	if 'ОЦЕНКИ' in comm and 'ПО' in comm and 'ПРЕДМЕТУ' in comm:
		subject = comm[3:]
		subject = ' '.join(subject).lower().capitalize()
		def getAllPointsOfSubject(subject):
			try:
				idSubject = subjects['id'].where(subjects['subject_name'] == subject).dropna().astype('int32').values.tolist()[0]
			except:
				tryAgain('Предмет не найден')
				return
			allpoints = results[['student_id', 'total']].where(results['subject'] == idSubject).dropna().astype('int32')
		getAllPointsOfSubject(subject)
	if len(comm)==2:
		teacher = comm[0].lower().capitalize()
		group = comm[1]
		def getAllPointsOfTeacherAndGroup(teacher, group):
			if teacher in allTeachers and group in allGroups:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32').values.tolist()[0]
				id_group = groups['id'].where(groups['name'] == group).dropna().astype('int32').values.tolist()[0]
				allPoints = results[['subject','total', 'student_id']].where(results['teacher_id'] == idTeacher).dropna().astype('int32')
				for ind, val in allPoints.iterrows():
					sid = val['subject']
					for subject in allSubjects:
						index  = allSubjects.index(subject)+1
						if sid == index:
							allPoints['subject'] = allPoints['subject'].replace(sid, subject)
				subjects = allPoints['subject'].values.tolist()
				subjects = list(dict.fromkeys(subjects))
				for sub in subjects:
					print(f'Оценки по предмету {sub}:')
					five = 0.86
					four = 0.67
					three = 0.42
					fives = allPoints[['student_id','total']].where((allPoints['subject'] == sub) & (allPoints['total']/100 >= five)).dropna().astype('int32')
					fours = allPoints[['student_id','total']].where((allPoints['subject'] == sub) & (allPoints['total']/100 < five) & (allPoints['total']/100 >= four) ).dropna().astype('int32')
					threes = allPoints[['student_id','total']].where((allPoints['subject'] == sub)  & (allPoints['total']/100 < four) & (allPoints['total']/100 >= three)).dropna().astype('int32')
					twos = allPoints[['student_id','total']].where((allPoints['subject'] == sub) & (allPoints['total']/100 < three)).dropna().astype('int32')
					OutMessage('Оценка "5":')
					if fives.empty:
						OutMessage('Пусто')
					else:
						OutMessage(fives.to_string(index=False, header=['ID студента', 'Итог'],justify="left"))
					
					OutMessage('Оценка "4":')
					if fours.empty:
						OutMessage('Пусто')
					else:
						OutMessage(fours.to_string(index=False, header=['ID студента', 'Итог'],justify="left"))
					OutMessage('Оценка "3":')
					if threes.empty:
						OutMessage('Пусто')
					else:
						OutMessage(threes.to_string(index=False, header=['ID студента', 'Итог'],justify="left"))
					OutMessage('Оценка "2":')
					if twos.empty:
						OutMessage('Пусто')

					else:
						OutMessage(fives.to_string(index=False, header=['ID студента', 'Итог'],justify="left"))
						OutMessage(twos.values.tolist())
					
			elif group not in allGroups and teacher in allTeachers:
				tryAgain('Такой группы не существует')
				return
			elif teacher not in allTeachers and group in groups:
				tryAgain('Преподаватель не найден')
				return
			else:
				tryAgain('Команда была введена неверно, повторите попытку. Для вывода всех команд введите команду "команды"')
				return
		getAllPointsOfTeacherAndGroup(teacher, group)
		# print(subject)
		# def getAllPointsOfTeacher(teacher):
		# 	try:
		# 		idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32')[0]
		# 	except:
		# 		tryAgain('Преподаватель не найден')
		# 		return
		# 	allpoints = results[['student_id', 'total', 'teacher_id']].where(results['teacher_id'] == idTeacher).dropna().astype('int32')
		# 	print(allpoints)
		# getAllPointsOfTeacher(teacher)
	
