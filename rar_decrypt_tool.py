import sys
import re
import subprocess

def __main__():
	rar_filename = ''
	text_filename = ''
	number_of_lines = 1

	help = """
Usage:
	python rar_decrypt_tool.py \\
		path_to_rar_file path_to_text \\
		<number_of_lines_per_try>
	"""

	cleaning_regex = re.compile(r'[\W_]+')

	if(len(sys.argv) > 1):
			rar_filename = sys.argv[1]
	else:
		print help
		sys.exit()

	if(len(sys.argv) > 2):
		text_filename = sys.argv[2]
	else:
		print "No text file specified"
		sys.exit()

	if(len(sys.argv) > 3):
		number_of_lines = int(sys.argv[3])
	
	text_file = open(text_filename, 'r')

	text_lines = text_file.readlines()

	line_array = []

	current_line = 1

	for line in text_lines:

		line = line.lower()
		line = cleaning_regex.sub(r'', line)

		if(len(line) == 0):
			continue

		line_array.append(line)

		if(current_line == number_of_lines):
			try_unrar(rar_filename, line_array)
			line_array = []
			current_line = 1

		else:
			current_line += 1


def try_unrar(rar_filename, line_array):

	lines = ''

	for line in line_array:
		lines += line

	print "Trying: ", lines

	command = ["unrar", "e", rar_filename, ("-p%s" % lines), "-y"]

	success = subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	if(success == 0):
		print "Found the password! It is: ", lines
		sys.exit()


__main__()
