import numpy as np
import pandas as pd
import requests
import json
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
from scipy.misc import imread

def get_comments(musicid,limit,offset):
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}?limit={}&offset={}'.format(musicid,limit,offset)
    payload = {
        'params': 'zWc+6qyuR6DN70+r75okwus9vXUKrVnOfZ8QzSetGWHB9wfWM72MRI0zh3h3bs+GvBv6urFLnHPFEnTploRBJ3n5qydRk3MvO9HVLJ65Z9L1/IPeTeqAJ7fkhkBipPZmgFaAKx7pW1yEogt3CgVawctZy8yeFDVMe2SFpilMzjxK4WBiJd5YdOmWHyBRmIC5',
        'encSecKey': '92343464f303d33a85dbab0c556a61837224d456938b5d952f6b7786538b6439bdd7063141fea1f12eded40722e14472c5e188a8e58f93e72aa52d3b93d1981ca9d2f41622124a3c7d9efe114c5e0b41334ce5a124b5e4ae44cc9eec4ec7a4fbb2693c308b08c90d33c40ad12dde1a1e6c93fdb4b43cc68af100fed6c7eb4988'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        'Referer': 'http://music.163.com/song?id={}'.format(musicid),
        'Host': 'music.163.com',
        'Origin': 'http://music.163.com'
    }
    response = requests.post(url=url, headers=headers, data=payload)
    data = json.loads(response.text)
    contents=[]
    for s in data['comments']:
        contents.append(s['content'])
    return contents


def drop_words(words,stopwords):
    words_clean=[]
    for word in words:
        if word in stopwords or word==' ' or word=='\n' or len(word)<2:
            continue
        else:
            words_clean.append(word)
    return words_clean


if __name__ == '__main__':
    print('输入歌曲id号(网易云音乐网页版的歌曲界面的URL最后就有歌曲id):',end='')
    number=int(input())
    words = ''
    for  j in range(30):
        contents = get_comments(number,100,100+j*100)
        for j in contents:
            words+=str(j)+' '
    cut_words = jieba.lcut(words)
    stopwords = pd.read_csv("stopwords.txt",
                            index_col=False, sep="\t", quoting=3,
                            names=['stopword'], encoding='utf-8')
    stopwords = stopwords.stopword.values.tolist()
    clean_words=drop_words(cut_words,stopwords)
    all_words = pd.DataFrame({'all_words': clean_words})
    words_count = all_words.groupby(by=['all_words'])['all_words'].agg({"count": np.size})
    words_count = words_count.reset_index().sort_values(by=["count"], ascending=False)

    mask=imread('girl.png')
    wordcloud = WordCloud(font_path="simhei.ttf", background_color="white",width=3600,height=1600)
    word_frequence = {x[0]: x[1] for x in words_count.head(300).values}
    wordcloud = wordcloud.fit_words(word_frequence)
    plt.imshow(wordcloud)
    plt.show()
    wordcloud.to_file('test.png')