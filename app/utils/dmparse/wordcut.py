import app.lib.jieba as jieba
import pandas as pd
import string
import re
import os




def get_stopwords_list():
    abspath=os.getcwd()
    print(abspath)
    stopWordPath=os.path.join(abspath,'app\lib\stopwords-master\stopwords-master\hit_stopwords.txt')
    print(stopWordPath)
    stopwords = [line.strip() for line in open(stopWordPath,encoding='UTF-8').readlines()]
    return stopwords
def remove_digits(word):
    pun_num=string.punctuation+string.digits
    table= str.maketrans('','',pun_num)
    word=word.translate(table)
    return word
def move_stopwords(sentence_list, stopwords_list):
    # 去停用词
    out_list = []
    for word in sentence_list:
        if word not in stopwords_list:
            if word!=''and word!=' ':
                if word != '\t':
                    out_list.append(word)
    return out_list
def jieba_word(word_list):
    word_list2=[]
    remove_chars = '[·’!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~—◢—]+'
    # jieba.load_userdict("word.txt")
    pun_num=string.punctuation+string.digits
    table= str.maketrans('','',pun_num)
    ##去除字符与分词
    for i in word_list:
        i=i.translate(table)
        i=re.sub(u"[\u2E80-\u33FFh]", '',i)
        i = re.sub(remove_chars, "", i)
        word_list2.extend(jieba.lcut(i,cut_all=False))
    return word_list2




if __name__ == '__main__':

    path='F:\表情包\BV1Yk4y1m7Rf\BV1Yk4y1m7Rf_comment.csv'
   
    pd_1=pd.read_csv(path)

    word_dict = {}

    word_list=list(pd_1['message'])


    for i in word_list:
        word_dict[i]=word_dict.get(i,0)+1
    tmp1=pd.DataFrame(word_dict,index=['times']).T.sort_values('times',ascending=False)
    #tmp1.to_csv('tmp1.csv')
    print(tmp1)

    word_list2=jieba_word(word_list)

    word_list2 = move_stopwords(word_list2, get_stopwords_list())

    for i in word_list2:
        word_dict[i]=word_dict.get(i,0)+1

    tmp=pd.DataFrame(word_dict,index=['times']).T.sort_values('times',ascending=False)
    tmp.to_csv('tmp.csv')
    print(tmp)

    #print(word_list)