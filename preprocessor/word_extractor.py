import pandas as pd
from konlpy.tag import Komoran
from textrank import KeywordSummarizer
import emoji
import re
import numpy as np
from utils.config_handler import ConfigParser
from tqdm import tqdm

pattern = (u'[\u3130-\u318F'+''.join(emoji.UNICODE_EMOJI.keys())+']+').replace('#', '')

class Extractor:
    def __init__(self):
        self.komoran = Komoran()
        self.config = ConfigParser()
        self.config.load_from_file('config/preprocessor.conf')
        # self.keyword_extractor = KeywordSummarizer(
        #     tokenize=self.tokenize_noun,
        #     window=1,
        #     verbose=False
        # )

    def tokenize(self, sent):
        try:
            words = self.komoran.pos(sent, join=True)
            pos = self.config['pos']
            ret = []
            for p in pos:
                ret.extend([w for w in words if p in w])
            return ret
        except:
            return []

    def extract_words(self, sents):
        return [self.tokenize(re.sub(pattern, '', s)) if s is not np.nan else [] for s in tqdm(sents)]