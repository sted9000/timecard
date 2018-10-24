'''
*** Timecard App v3 ***
- Catalog my programming progress and projects
- Create so others can use it
'''

json_file = 'project_data.json'
backup_file = 'backup_data.json'
welcome_msg = 'Welcome to TimeCard'
number_letter_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g'}
letter_number_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}


import os.path
from termcolor import colored
import json
import numbers
import time
from sys import exit
import os


# find, open, and read file
with open(json_file, 'r') as file:

	try:
		py_data = json.load(file)

	except Exception as e:
		py_data = {"current_projects": [], "filed_projects": []}

# Overwrite currect back-up with most recent
with open('backup_file', 'w') as backup_file:
	json.dump(py_data, backup_file)

# Welcome message
os.system('cls' if os.name == 'nt' else 'clear')
print(colored('***' + welcome_msg + '***', 'green', attrs=['bold']))


# function dislay homescreen
def homeScreen(_py_data):

	# Display current projects
	if len(_py_data["current_projects"]) != 0:
		for counter, var in enumerate(_py_data["current_projects"]):
			print(number_letter_map[counter] + ' - to clock-in for: ' + colored(var["name"], 'blue', attrs=['bold']))
	else:
		print('None')

	# And other options
	print('n - for a new project')
	print('r - to review a project')
	print('q - to logout')

	# Gather user input
	home_input = input(colored('Enter letter: ', 'cyan'))

	# Call next function
	for i in range(len(_py_data["current_projects"])):
		if home_input == number_letter_map[i]:
			clockIn(_py_data, i)
			return

	if home_input == 'n':
		newProject(py_data)

	elif home_input == 'r':
		Report(_py_data)

	elif home_input == 'q':
		logOut(_py_data)

	else:
		print()
		homeScreen(_py_data)

# n - new project function
def newProject(_py_data):

	# user messagae: enter a <name> followed by a <description, spaces are allowed>
	new_name = input(colored('\nEnter new projects name: ', 'cyan'))
	new_decsr = input(colored('Enter a description for ' + new_name + ': ', 'cyan'))
	new_est = input(colored('Enter an estimated time (hrs) for ' + new_name + ': ', 'cyan'))
	print('\nIs this correct:\nName: ' + new_name + '\nDescription: ' + new_decsr + '\nEst Time: ' + new_est)
	if input(colored('(y/n): ', 'cyan')) == 'y':
		_py_data["current_projects"].append({
		"name":new_name,
		"descr":new_decsr,
		"est_time": new_est,
		"timecard": []

		})
		print('\nHow would you like to continue?')
		print('ci - clock-in for new project\nh - home\nor anything else - logout')
		new_project_exit = input(colored('Enter letter: ', 'cyan'))
		if new_project_exit == 'ci': clockIn(_py_data, len(_py_data["current_projects"]) - 1)
		elif new_project_exit == 'h':
			os.system('cls' if os.name == 'nt' else 'clear')
			homeScreen(_py_data)
		elif new_project_exit == 'q': logOut()
	else:
		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')
		homeScreen(_py_data)

# function clockin project (current id)
def clockIn(_py_data, _project_index):

	# clear screen
	os.system('cls' if os.name == 'nt' else 'clear')

	# clock in
	_py_data["current_projects"][_project_index]["timecard"].append([time.time()])

	# User message
	print('You have clocked-in for ' + _py_data["current_projects"][_project_index]["name"])

	# session variable
	session_in_progress = True

	while session_in_progress:
		exit_command = input(colored('Enter co to clock out: ', 'cyan'))
		if exit_command == 'co':

			project_timecard = _py_data["current_projects"][_project_index]["timecard"][len(_py_data["current_projects"][_project_index]["timecard"]) - 1]

			# clock out
			project_timecard.append(time.time())

			# clear screen
			os.system('cls' if os.name == 'nt' else 'clear')
			print('You have successfully clocked out of ' + _py_data["current_projects"][_project_index]["name"])

			# enter notes
			notes = input(colored('Notes from the session: ', 'cyan'))
			project_timecard.append(notes)

			# enter milestones
			milestones = input(colored('Milestones from the sesson: ', 'cyan'))
			project_timecard.append(milestones)

			# how long worked
			print('Your session was ' + str((project_timecard[1] - project_timecard[0]) / 60) + ' mins')

			# how to proceed
			clock_out_proceed = input(colored('\nci - clock-in again\nh - home\nor anything - logout: ', 'cyan'))
			if clock_out_proceed == 'ci': clockIn(_py_data, _project_index)
			elif clock_out_proceed == 'h': homeScreen(_py_data)
			else: logOut(_py_data)

			# exit loop
			return

def Report(_py_data):

	# clear terminal
	os.system('cls' if os.name == 'nt' else 'clear')

	# reports message
	print(colored("Reports:", attrs=['underline']))
	print("Here you can view and edit project details and file projects")


	# show all projects by name
	print("\nCurrent Projects:")
	displayed_projects = 0
	if len(_py_data["current_projects"]) != 0:
		for counter, current in enumerate(_py_data["current_projects"]):
			print(number_letter_map[counter] + ' - ' + current["name"])
			displayed_projects += 1
	else: print('None')

	print("\nFiled Projects:")
	if len(_py_data["filed_projects"]) != 0:
		for counter, filed in enumerate(_py_data["filed_projects"]):
			print(number_letter_map[counter + len(_py_data["current_projects"])] + ' - ' + filed["name"])
			displayed_projects += 1
	else: print('None')

	# user selection
	letter_of_project = input(colored('\nEnter letter: ', 'cyan'))

	# clear terminal
	os.system('cls' if os.name == 'nt' else 'clear')

	# show details
	try:

		if letter_number_map[letter_of_project] >= len(_py_data["current_projects"]):
			report_dictionary = "filed_projects"
			project_index = letter_number_map[letter_of_project] - len(_py_data["current_projects"])
			if letter_number_map[letter_of_project] > len(_py_data[report_dictionary]):
				homeScreen(_py_data)
				return

		else:
			report_dictionary = "current_projects"
			project_index = letter_number_map[letter_of_project]
			if letter_number_map[letter_of_project] > len(_py_data[report_dictionary]):
				homeScreen(_py_data)
				return
	except Exception:
		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')
		homeScreen(_py_data)

	# selected project
	selected_project = _py_data[report_dictionary][project_index]

	# Title (name)
	print(colored(selected_project["name"] + ":", attrs=["underline"]))

	# Description string
	print("Descripttion: " + selected_project["descr"])

	# Estimated time
	print("Estimated time: " + selected_project["est_time"])

	# Start date
	try:
		start_date = selected_project["timecard"][0][0]
		print('Start date: ' + time.asctime(time.localtime(start_date)))
	except Exception:
		print('Start date: TBD')

	# End date
	try:
		end_date = selected_project["timecard"][len(selected_project["timecard"]) - 1][1]
		print('End date: ' + time.asctime(time.localtime(end_date)))

		# Duration
		duration = end_date - start_date
		m, s = divmod(duration, 60)
		h, m = divmod(m, 60)
		d, h = divmod(h, 24)
		print("Duration: %d:%d:%02d (d:h:m)" % (d , h, m))

	except Exception:
		print('End date: TBD')

	# Time worked
	time_worked = 0
	for i in selected_project["timecard"]:
		time_worked += (i[1] - i[0])
	min, sec = divmod(time_worked, 60)
	hour, min = divmod(min, 60)
	print('Time worked: %d:%02d (h:m)' % (hour,min))

	# Sessions worked
	sessions_worked = len(selected_project["timecard"])
	print('Sessions worked: ' + str(sessions_worked))


	# User next action
	print('\nn - to view notes\nm - to view milestones\ne - to edit\nf - to file project\nh - to go home\nanything else - to log out')
	next_action = input(colored('Enter letter: ', 'cyan'))


	if next_action == 'n':
		viewNotes(_py_data, selected_project)

	elif next_action == 'm':
		viewMilestones(_py_data, selected_project)

	elif next_action == 'e':
		editProject(_py_data, selected_project)

	elif next_action == 'f':
		fileProject(_py_data, selected_project, project_index)

	elif next_action == 'h':
		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')
		homeScreen(_py_data)

	else:
		logOut(_py_data)

def editProject(_py_data, _selected_project):

	# clear terminal
	os.system('cls' if os.name == 'nt' else 'clear')

	# title
	print('How would you like to edit your project?')
	print('add - to manually add a shift')
	print('remove - to manually remove your last stift')
	print('delete - to manually delete the project')

	# user input
	user_edit = input(colored('Enter letter: ', 'cyan'))

	# add session maunally
	if user_edit == 'add':

		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')

		# How much time to add
		manual_time = int(input(colored('How much time (min)?: ', 'cyan'))) * 60

		# enter notes
		notes = input(colored('Notes from the session: ', 'cyan'))

		# enter milestones
		milestones = input(colored('Milestones from the sesson: ', 'cyan'))

		# append
		_selected_project["timecard"].append([time.time() - manual_time ,time.time(), notes, milestones])

		# user next action
		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')

		print('Thank you for your edit')
		print('Be sure to log out the save your changes\n')
		homeScreen(_py_data)

	# remove session manually
	elif user_edit == 'remove':

		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')

		# dbl check
		if input(colored('Are you sure you want to delete your last shift for ' + _selected_project["name"] + '? (y,n): ', 'cyan')) == 'y':
			# remove last shift
			del _selected_project["timecard"][-1]

			# user next action
			# clear terminal
			os.system('cls' if os.name == 'nt' else 'clear')

			print('Thank you for your edit')
			print('Be sure to log out the save your changes\n')
			homeScreen(_py_data)
		else:
			# clear terminal
			os.system('cls' if os.name == 'nt' else 'clear')
			homeScreen(_py_data)


	# delete project
	elif user_edit == 'delete':

		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')

		# dbl check
		if input(colored('Are you sure you want to delete the entire ' + _selected_project["name"] + ' project? (y,n): ', 'cyan')) == 'y':

			for i, proj in enumerate(_py_data["current_projects"]):
				if proj == _selected_project:
					del _py_data["current_projects"][i]

			for i, proj in enumerate(_py_data["filed_projects"]):
				if proj == _selected_project:
					del _py_data["filed_projects"][i]

			# user next action
			# clear terminal
			os.system('cls' if os.name == 'nt' else 'clear')

			print('Thank you for your edit')
			print('Be sure to log out the save your changes\n')
			homeScreen(_py_data)
		else:
			# clear terminal
			os.system('cls' if os.name == 'nt' else 'clear')
			homeScreen(_py_data)

	else:
		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')
		homeScreen(_py_data)


def fileProject(_py_data, _selected_project, _project_index):

	# user double check
	if input(colored(
	'\nAre you sure you want to file: ' + _selected_project["name"] + ' (y/n): ', 'cyan')) == 'y':

		# add to filed projects
		_py_data["filed_projects"].append(_selected_project)

		# remove project from current projects
		del _py_data["current_projects"][_project_index]

		# user next action

		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')
		print('Congrajulations your project has been filed\nPlease be sure to logout to save your changes\nWhere you you like to go now')
		print('h - to go home\nr - to view reports\nanything else - to logout')
		next_action = input(colored('Enter letter: ', 'cyan'))

		if next_action == 'h':
			# clear terminal
			os.system('cls' if os.name == 'nt' else 'clear')
			homeScreen(_py_data)


		elif next_action == 'r':
			Report(_py_data)

		else:
			logOut(_py_data)

	else:
		# clear tierminal
		os.system('cls' if os.name == 'nt' else 'clear')
		homeScreen(_py_data)

def viewNotes(_py_data, _selected_project):
	# clear terminal
	os.system('cls' if os.name == 'nt' else 'clear')

	# print header
	print(colored('Notes for ' + _selected_project["name"] + ':', attrs=['underline']))

	# loop through timecard
	for i in _selected_project["timecard"]:
		if i[2] != '':
			print('\n')
			print(colored(time.asctime(time.localtime(i[1])), 'white'))
			print(colored(i[2], 'yellow'))

	# next action
	print('\nh - to go home\nanything else - to log out')
	next_action = input(colored('Enter letter: ', 'cyan'))
	if next_action == 'h':
		os.system('cls' if os.name == 'nt' else 'clear')
		homeScreen(_py_data)
	else:
		logOut(_py_data)

def viewMilestones(_py_data, _selected_project):
	# clear terminal
	os.system('cls' if os.name == 'nt' else 'clear')

	# print header
	print(colored('Milestones for ' + _selected_project["name"] + ':', attrs=['underline']))

	# loop through timecard
	for i in _selected_project["timecard"]:
		if i[3] != '':
			print('\n')
			print(colored(time.asctime(time.localtime(i[1])), 'white'))
			print(colored(i[3], 'yellow'))

	# next action
	print('\nh - to go home\nanything else - to log out')
	next_action = input(colored('Enter letter: ', 'cyan'))
	if next_action == 'h':
		os.system('cls' if os.name == 'nt' else 'clear')
		homeScreen(_py_data)
	else:
		logOut(_py_data)

def logOut(_py_data):

	# update json file
	with open(json_file, 'w') as outfile:
		json.dump(_py_data, outfile)

	os.system('cls' if os.name == 'nt' else 'clear')

	print("Thanks for working. TimeCard logout successful")

# Call homescreen
homeScreen(py_data)
