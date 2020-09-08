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


def split_content_tag(raw_string: str):
    pattern = u'#' + (u'[_a-zA-Z0-9\u3130-\u318F\uAC00-\uD7A3'+''.join(emoji.UNICODE_EMOJI.keys())+']+').replace('#', '')
    tags = re.findall(pattern, raw_string)
    content = re.sub(pattern, '', raw_string)
    return tags, content


def get_data_from_hashtag(hashtag: str, data_path = './data'):
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    dir_name = '%s/%s_%s' %(data_path, current_datetime, hashtag)
    print(dir_name)
    os.makedirs(dir_name, exist_ok=True)
    url = 'https://www.instagram.com/explore/tags/%s/?__a=1' %hashtag
    response = requests.get(url)
    raw_json = response.json()
    json.dump(raw_json, open('%s/data.json' %dir_name, 'w'))
    nodes = raw_json['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    nodes.extend(raw_json['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'])
    ret = []
    for node in tqdm(nodes):
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
            date
        ])

        with open('%s/img_%s.jpg' %(dir_name, node['node']['id']), 'wb') as f:
            f.write(img)
    with open('%s/metadata.csv' %dir_name, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'original', 'content', 'hashtag', 'created_date'])
        writer.writerows(ret)


def run():
    config = ConfigParser()
    config.load_from_file('config/crawler.conf')

    hashtags = config['tags']
    data_path = config['data_path']

    print('크롤링 대상:', hashtags)

    for hashtag in hashtags:
        get_data_from_hashtag(hashtag, data_path)