# -*- coding:utf-8 -*-
"""
author: Ziyu Chen
"""
from poem import Poem

if __name__ == '__main__':
    poem = Poem('poetry_simplified.txt')
    poem.set_stopwords('stopwords.txt')
    poem.process()
    poem_set = poem.return_poem_set()
    poem.generate_word_cloud('poetry_simplified.txt', 'jiubei.jpg', 'jiubei_cw.jpg', userpic_as_backgroud=False)
    poem.generate_wordcloud_for_poet('李白', 'libai.jpg', 'libai_cw.jpg')
    poem.generate_wordcloud_for_poet('杜甫', 'dufu.jpg', 'dufu_cw.jpg')
    poem.draw_top_produced_poet()
    poem.draw_top_poem_kind()
    # poem.word_statistics(15)