# -*- coding:utf-8 -*-
"""
author: Ziyu Chen
"""

import gensim
from aip import AipNlp
import matplotlib.pyplot as plt
import jieba
import jieba.posseg as pseg
import numpy as np
import PIL as image
from snownlp import SnowNLP
import re
from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread

"""
global variable
"""

APP_ID = '11411564'
API_KEY = 'FGlYLjAjKVH2BhuwtUGLDfMG'
SECRET_KEY = 'nI16gyLmIQoOGWs3gMA5gZD3zS3UyIyS'


class Poem:

    # 用于匹配的字段，读取的文件中的四个字段
    poem_title = '诗名'
    poet = '作者'
    poem_kind = '诗体'
    poem = '诗文'

    def return_poem_set(self):
        '''
        返回诗歌的集合，是一个list，list每个元素是dict，dict有四个键值，分别对应Poem类的四个静态成员
        Poem.poem_title\ Poem.poet\ Peom.poem_kind\ Poem.poem
        :return: 返回诗歌的集合
        '''
        return self.poem_set

    def __init__(self, filename):
        self.filename = filename
        self.stopwords = []
        self.poem_set = []

    def set_stopwords(self, filename):
        file_stopword = open(filename, 'r', encoding='utf-8')
        stopwords_data = file_stopword.readlines()
        for word in stopwords_data:
            self.stopwords.append(word.strip())
        # print(stopwords)

    def process(self):
        self.poem_set = []
        file = open(self.filename, 'r', encoding='utf-8')
        line = file.readline()
        p = dict()
        while line:
            # 繁体化简体
            if line == '\n':
                line = file.readline()
                continue
            traditional = line.strip()
            s = SnowNLP(traditional)
            simplified = s.han
            # 处理每一行，冒号前内容作为dict的键值，后面的内容作为dict的映射值
            key, content = re.split(r':', simplified)
            # print(key, content)
            if key != Poem.poem:
                p[key] = content
            else:
                result = jieba.cut(simplified, cut_all=False)
                p[key] = [r for r in result if r not in self.stopwords]
                self.poem_set.append(p.copy())
                # print(p)
                p.clear()
            line = file.readline()

    def generate_word_cloud(self, textfile, backgroud_pic, save_file, userpic_as_backgroud=False):
        '''
        :param textfile: 词云生成的依赖文本
        :param backgroud_pic: 词云生成的背景图片
        :param save_file: 生成的词云图的保存路径
        :param userpic_as_backgroud: 是否使用背景图片的色彩
        :return: 显示生成的图云并保存
        '''
        text = open(textfile, 'r', encoding='utf-8').read()
        pic = imread(backgroud_pic)
        wordcloud = WordCloud(mask=pic, font_path=r'C:\Windows\Fonts\FZYTK.TTF'
                              , background_color='white', margin=5, width=1600, height=900, max_words=500,
                              min_font_size=10, max_font_size=50, random_state=10).generate(text)
        image_colors = ImageColorGenerator(pic)
        if userpic_as_backgroud:
            plt.imshow(wordcloud.recolor(color_func=image_colors))
        else:
            plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()

        wordcloud.to_file(save_file)


if __name__ == '__main__':
    pass
    poem = Poem('poetry.txt')
    poem.set_stopwords('stopwords.txt')
    poem.process()
    poem_set = poem.return_poem_set()
    for one_poem in poem_set:
        print(one_poem)
    poem.generate_word_cloud('poetry1.txt', 'libai.jpg', 'result.jpg', userpic_as_backgroud=True)
