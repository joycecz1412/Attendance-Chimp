'''create function that takes a single filename as argument and outputs
random number of sample lines in file'''

import numpy as np
import pandas as pd 

def sample_username(file_name):
	df = pd.read_csv(file_name)
	number = np.randomchoice(np.arange(0, len(df)))
	indexes = np.randomchoice(np.arange(0, len(df)), number)
	return df[indexes] 

