'''create function that takes a single filename as argument and outputs
random number of sample lines in file'''

import numpy as np
import pandas as pd 

def sample_username(file_name):
	df = pd.read_csv(file_name)
	number = np.random.choice(np.arange(0, len(df)))
	indexes = np.random.choice(np.arange(0, len(df)), size=number, replace=False)
	print(df.iloc[indexes]) 

