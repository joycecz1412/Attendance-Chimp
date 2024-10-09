'''create function that takes a single filename as argument and outputs
random number of sample lines in file'''

def sample_username(file_name):
	with open('file.csv', mode='r') as file:
		for line in file:
        	line = line.strip()
        	values = line.split(',')
	return

