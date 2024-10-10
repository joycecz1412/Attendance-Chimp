'''create function that takes a single filename as argument and outputs
random number of sample lines in file'''
import random
import argparse

def samplit(filename):
	file = open(filename, 'r') 
	for line in file:
		if random.random() <= 0.01:
			print(line, end = '')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('filename', type=str, help='name of the file')
	args = parser.parse_args()
	samplit(args.filename)


