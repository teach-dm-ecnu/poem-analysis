# -*- coding:utf-8 -*-
"""
author: Ziyu Chen
"""

import matplotlib.pyplot as plt
import jieba
from snownlp import SnowNLP
import re
from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread
import os
from pylab import mpl

# 全局画图设置
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


class Poem:
    '''
    用于匹配的字段，读取的文件中的四个字段
    '''
    poem_title = '诗名'
    poet = '作者'
    poem_kind = '诗体'
    poem = '诗文'

    def return_poem_set(self):
        '''
        返回诗歌的集合，是一个list，list每个元素是dict，dict有四个键值，分别对应Poem类的四个静态成员
        Poem.poem_title\ Poem.poet\ Peom.poem_kind\ Poem.poem 对应数据类型
        str            \ str      \ str           \ list，元素是str
        :return: 返回诗歌的集合
        '''
        return self.poem_set

    def __init__(self, filename):
        '''
        初始化成员变量
        :param filename: 读取的文件名
        '''
        self.filename = filename
        self.stopwords = []
        self.poem_set = []

    def set_stopwords(self, filename):
        '''
        设置停用词
        :param filename: 停用词文件名
        :return: 设置成员变量stopwords
        '''
        file_stopword = open(filename, 'r', encoding='utf-8')
        stopwords_data = file_stopword.readlines()
        for word in stopwords_data:
            self.stopwords.append(word.strip())
        self.stopwords.extend(['\n', ' ', Poem.poet, Poem.poem_kind, Poem.poem_title, Poem.poem])
        #print(self.stopwords)
        file_stopword.close()

    def process(self):
        '''
        处理读入的数据，转换成成员变量poem_set
        :return:
        '''
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
            filter = re.compile('\(.*\)')
            simplified = filter.sub('', simplified)
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
        file.close()

    def generate_word_cloud(self, textfile, backgroud_pic, save_file, userpic_as_backgroud=True):
        '''
        :param textfile: 词云生成的依赖文本
        :param backgroud_pic: 词云生成的背景图片
        :param save_file: 生成的词云图的保存路径
        :param userpic_as_backgroud: 是否使用背景图片的色彩
        :return: 显示生成的图云并保存
        '''
        text = open(textfile, 'r', encoding='utf-8').read()
        pic = imread(backgroud_pic)
        word_frequency = dict()
        word_list = jieba.cut(text)
        for word in word_list:
            if word not in self.stopwords:
                word_frequency[word] = word_frequency.get(word, 0) + 1
        '''调整画词云的参数，让图中的词更多更密集'''
        # print('word_frequency', word_frequency)
        # wordcloud = WordCloud(mask=pic, font_path=r'C:\Windows\Fonts\FZYTK.TTF'
        #                       , background_color='white', margin=2, width=1600, height=900, max_words=700,
        #                       min_font_size=3, max_font_size=40,
        #                       random_state=42).generate_from_frequencies(word_frequency)
        wordcloud = WordCloud(mask=pic, font_path=r'C:\Windows\Fonts\FZYTK.TTF'
                              , background_color='white', margin=2, width=1600, height=900, max_words=650,
                              min_font_size=4, max_font_size=30,
                              random_state=42).generate_from_frequencies(word_frequency)
        image_colors = ImageColorGenerator(pic)
        if userpic_as_backgroud:
            plt.imshow(wordcloud.recolor(color_func=image_colors))
        else:
            plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
        wordcloud.to_file(save_file)

    def poet_statistics(self):
        '''
        诗人作诗量的统计
        :return: 返回统计结果，为一个dict，键值为诗人名，映射值为作诗数量
        '''
        poet_poems = dict()
        for p in self.poem_set:
            poet_poems[p[Poem.poet]] = poet_poems.get(p[Poem.poet], 0) + 1
        return poet_poems

    def poet_kind_statistics(self):
        '''
        统计每种诗体的数量
        :return: 返回统计结果，为一个dict，键值为诗体，映射值为对应诗的数量
        '''
        poet_kind_poems = dict()
        for p in self.poem_set:
            poet_kind_poems[p[Poem.poem_kind]] = poet_kind_poems.get(p[Poem.poem_kind], 0) + 1
        return poet_kind_poems

    def generate_wordcloud_for_poet(self, poet, backgroud_pic, save_file):
        '''
        为一诗人做出词云
        :param poet: 诗人名字
        :param backgroud_pic: 词云背景图片
        :param save_file: 词云存储路径
        :return:
        '''
        poems_by_poet = ''
        for p in self.poem_set:
            if p[Poem.poet] == poet:
                poems_by_poet += (" ".join([word for word in p[Poem.poem]]))
                poems_by_poet += " "
        temp = open('temp.txt', 'w', encoding='utf-8')
        temp.write(poems_by_poet)
        temp.close()
        self.generate_word_cloud('temp.txt', backgroud_pic, save_file, userpic_as_backgroud=False)
        os.remove('temp.txt')

    def draw_pie(self, labels, quants, save_file, title, top=10):
        '''
        根据标签和对应数量作出饼状图
        :param labels: 一个list，代表标签
        :param quants: 一个list，代表标签所对应的数量
        :param save_file: 存储路径
        :param title: 图上的标题
        :param top: 饼图中成分的数量
        :return:
        '''
        plt.figure(1, figsize=(6, 6))
        expl = [0.1]
        expl.extend([0]*(top-1))
        colors = ["blue", "red", "coral", "green", "yellow", "orange"]  # 设置颜色（循环显示）
        # 设置百分号的格式
        plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=True)
        plt.title(title, bbox={'facecolor': '0.8', 'pad': 5})
        # plt.show()
        plt.savefig(save_file)
        plt.close()

    def top_10_poet_poem(self):
        '''
        选出前10名创作量最多的诗人
        :return: 返回对应的诗人及其产量
        '''
        poet_poem = dict()
        for p in self.poem_set:
            poet_poem[p[Poem.poet]] = poet_poem.get(p[Poem.poet], 0) + 1
        sorted_poet_poem = sorted(poet_poem.items(), key=lambda d: d[1], reverse=True)
        labels = [v[0] for v in sorted_poet_poem[:10]]
        quants = [v[1] for v in sorted_poet_poem[:10]]
        # print(labels, quants)
        return labels, quants

    def draw_top_produced_poet(self):
        '''
        为创作量前10的诗人统计结果做出饼状图
        :return:
        '''
        labels, quants = self.top_10_poet_poem()
        self.draw_pie(labels, quants, 'top_10_produced_poets.jpg', '创作量前十的诗人')

    def top_poem_kind(self, top=5):
        '''
        选出前top数量的诗体
        :param top: 前top名
        :return:
        '''
        poem_kind = dict()
        for p in self.poem_set:
            poem_kind[p[Poem.poem_kind]] = poem_kind.get(p[Poem.poem_kind], 0) + 1
        sorted_poem_kind = sorted(poem_kind.items(), key=lambda d: d[1], reverse=True)
        labels = [v[0] for v in sorted_poem_kind[:top]]
        quants = [v[1] for v in sorted_poem_kind[:top]]
        return labels, quants

    def draw_top_poem_kind(self):
        '''
        为前top名数量的诗体的统计结果做出饼图
        :return:
        '''
        labels, quants = self.top_poem_kind(top=5)
        self.draw_pie(labels, quants, 'top_5_poem_kind.jpg', '各种诗体占的比重', top=5)

    def word_statistics(self, top=15):
        word = dict()
        for p in self.poem_set:
            each_poem_list = p[Poem.poem]
            for item in each_poem_list:
                word[item] = word.get(item, 0) + 1
        word_sorted = sorted(word.items(), key=lambda d: d[1], reverse=True)
        word_num_list = word_sorted[0:top]
        plt.bar(range(len(word_num_list)), word_num_list)
        plt.show()
        plt.savefig('word_sta.jpg')




