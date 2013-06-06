#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: 赵晓凯
# Date:   2013-06-05
# Email:  minix007@foxmail.com

import codecs
import sys

def genDict(path):
    """ 获取词典 """
    f = codecs.open(path,'r','utf-8')
    contents = f.read()
    contents = contents.replace(u'\r', u'')
    contents = contents.replace(u'\n', u'')
    # 将文件内容按空格分开
    mydict = contents.split(u' ')
    # 去除词典List中的重复
    newdict = list(set(mydict))
    newdict.remove(u'')

    # 建立词典
    # key为词首字，value为以此字开始的词构成的List
    truedict = {}
    for item in newdict:
        if len(item)>0 and item[0] in truedict:
            value = truedict[item[0]]
            value.append(item)
            truedict[item[0]] = value
        else:
            truedict[item[0]] = [item]
    return truedict

def print_unicode_list(uni_list):
    for item in uni_list:
        print item,

def divideWords(mydict, sentence):
    """ 
    根据词典对句子进行分词,
    使用正向匹配的算法，从左到右扫描，遇到最长的词，
    就将它切下来，直到句子被分割完闭
    """
    result = []
    start = 0
    senlen = len(sentence)
    while start < senlen:
        curword = sentence[start]
        maxlen = 1
        # 寻找以当前字开头的最长词
        if curword in mydict:
            words = mydict[curword]
            for item in words:
                itemlen = len(item)
                if sentence[start:start+itemlen] == item and itemlen > maxlen and itemlen <= 5:
                    maxlen = itemlen
        result.append(sentence[start:start+maxlen])
        start = start + maxlen
    return result

def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print 'Usage: python ' + sys.argv[0] + ' dict_path test_path result_path'
        exit(-1)
    dict_path = args[0]
    test_path = args[1]
    result_path = args[2]

    dicts = genDict(dict_path)
    fr = codecs.open(test_path,'r','utf-8')
    test = fr.read()
    result = divideWords(dicts,test)
    fr.close()
    fw = codecs.open(result_path,'w','utf-8')
    for item in result:
        fw.write(item + ' ')
    fw.close()

if __name__ == "__main__":
    main()
