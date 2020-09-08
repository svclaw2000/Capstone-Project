import requests
from utils.config_handler import ConfigParser
import csv
from jamotools import join_jamos
from datetime import datetime
import re
import emoji
import os
import json
from tqdm import tqdm
import parmap
import logging


def split_content_tag(raw_string: str):
    pattern = u'#' + (u'[_a-zA-Z0-9\u3130-\u318F\uAC00-\uD7A3'+''.join(emoji.UNICODE_EMOJI.keys())+']+').replace('#', '')
    tags = re.findall(pattern, raw_string)
    content = re.sub(pattern, '', raw_string)
    return tags, content


def get_data_from_hashtag(hashtag: str, data_path = './data'):
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    dir_name = '%s/%s_%s' %(data_path, current_datetime, hashtag)
    print(dir_name, 'start')
    os.makedirs(dir_name, exist_ok=True)
    url = 'https://www.instagram.com/explore/tags/%s/?__a=1' %hashtag
    response = requests.get(url)
    raw_json = response.json()
    json.dump(raw_json, open('%s/data.json' %dir_name, 'w'))
    nodes = {
        'popular': raw_json['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'],
        'recent': raw_json['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    }
    ret = []
    for k in nodes:
        for node in nodes[k]:
            img = requests.get(node['node']['display_url']).content
            original = join_jamos(node['node']['edge_media_to_caption']['edges'][0]['node']['text'] if node['node']['edge_media_to_caption']['edges'] else "")
            tags, content = split_content_tag(original)
            caption = node['node']['accessibility_caption']
            date = None
            if caption:
                date = re.findall('[A-Za-z]+ [0-9]{2}, [0-9]{4}', caption)
            if date:
                date = datetime.strptime(date[0], '%B %d, %Y').strftime('%Y-%m-%d')
            else:
                date = '9999-12-31'
            ret.append([
                node['node']['id'],
                original,
                content,
                tags,
                k,
                date
            ])

            with open('%s/img_%s.jpg' %(dir_name, node['node']['id']), 'wb') as f:
                f.write(img)
    with open('%s/metadata.csv' %dir_name, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'original', 'content', 'hashtag', 'category', 'created_date'])
        writer.writerows(ret)
    print(dir_name, 'finish')


def run(multiprocessing=False, processes=4):
    config = ConfigParser()
    config.load_from_file('config/crawler.conf')
    hashtags = config['tags']
    data_path = config['data_path']
    print('크롤링 대상:', hashtags)

    if multiprocessing:
        parmap.map(get_data_from_hashtag, hashtags, data_path,
                   pm_processes=processes)
    else:
        for hashtag in hashtags:
            get_data_from_hashtag(hashtag, data_path)