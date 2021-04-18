from .wordcut import *
def getDmWordTimes(df,key):
    word_dict={}
    wordList=list(df[key])
    wordList2=jieba_word(wordList)
    wordList2 = move_stopwords(wordList2, get_stopwords_list())
    for i in wordList2:
        word_dict[i]=word_dict.get(i,0)+1
    tmp1=pd.DataFrame(pd.Series(word_dict), columns=['times'])
    tmp1=tmp1.reset_index().rename(columns={'index':'id'}).sort_values('times',ascending=False).reset_index(drop=True)
    return tmp1

def getDmWordTimesNoWordCut(df,key):
    word_dict={}
    wordList=list(df[key])
    # wordList2=jieba_word(wordList)
    # wordList2 = move_stopwords(wordList2, get_stopwords_list())
    for i in wordList:
        word_dict[i]=word_dict.get(i,0)+1
    tmp1=pd.DataFrame(pd.Series(word_dict), columns=['times'])
    tmp1=tmp1.reset_index().rename(columns={'index':'id'}).sort_values('times',ascending=False).reset_index(drop=True)
    return tmp1
    