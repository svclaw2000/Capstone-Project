import os
from tqdm import tqdm
import pickle
import shutil

data = pickle.load(open('./data/sentence_gamjung.pkl', 'rb'))
data_dir = 'data'
train_dir = 'train_data'
if os.path.exists(train_dir):
	print('Directory already exists.')
	exit()

os.makedirs(train_dir)
for path in tqdm(data['image_path']):
	dir_path = train_dir + '/' + path.split('/')[0]
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	shutil.copy(data_dir + '/' + path, train_dir + '/' + path)
