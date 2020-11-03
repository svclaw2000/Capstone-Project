import pandas as pd
from utils.config_handler import ConfigParser
import os
from tqdm import tqdm
from preprocessor.word_extractor import Extractor
import pickle
import re

def load_data(root_dir: str, tags: list, start_date: str = None, end_date: str = None):
    dirs = os.listdir(root_dir)
    dirs = [d for d in dirs if os.path.isdir('%s/%s' %(root_dir, d))]
    metas = []
    n_total = 0
    n_error = 0

    for d in tqdm(dirs):
        try:
            if not start_date <= d.split('_')[0] <= end_date:
                continue

            meta = pd.read_csv('%s/%s/metadata.csv' %(root_dir, d))
            n_total += len(meta)

            tag = d.split('_')[-1]
            has_category = False
            for category in tags:
                if tag in tags[category]:
                    meta['category1'] = category
                    meta['category2'] = tag
                    has_category = True
                    break

            if not has_category:
                n_error += len(meta)
                continue

            meta['image_path'] = '%s/img_' %d + meta['id'].astype(str) + '.jpg'

            metas.append(meta)
        except:
            continue

    data = pd.concat(metas)
    data = data.drop_duplicates(['id'])
    print('Total: %d, Duplicated: %d, Error: %d, Left: %d' %(n_total, n_total-len(data), n_error, len(data)))

    return data

def filter_korean(s):
    try:
        return re.sub('[^\uAC00-\uD7AF]+', '', s)
    except:
        return ''

def run():
    config = ConfigParser()
    config.load_from_file('config/crawler.conf')
    config.load_from_file('config/preprocessor.conf')
    pos = config['pos']

    data = load_data(config['data_path'], config['tags'], config['start_date'], config['end_date'])
    data['clean_text'] = [filter_korean(s) for s in data['content']]
    extractor = Extractor()
    tokens = extractor.extract_words(data['content'])
    for p in pos:
        data[p[1:]] = [[t for t in token if p in t] for token in tokens]
    data.to_csv('%s.csv' %config['output_path'], index=False)
    pickle.dump(data, open('%s.pkl' %config['output_path'], 'wb'))
