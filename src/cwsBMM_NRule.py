#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: 赵晓凯
# Date:   2013-06-05
# Email:  minix007@foxmail.com

# 使用BMM 进行中文分词

import codecs
import sys


def genDict(path):
    """ 获取词典 """
    f = codecs.open(path,'r','utf-8')
    contents = f.read()
    contents = contents.replace(u'\r', u'')
    contents = contents.replace(u'\n', u'')
    # 将内容逆置，以便进行逆向匹配
    contents = contents[::-1]
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

def divideWords(mydict, sentence, maxlen):
    """ 
    根据词典对句子进行分词,
    使用逆向匹配的算法，从右到左扫描，遇到最长的词，
    就将它切下来，直到句子被分割完闭
    """
    # 对句子逆置，以便用正向匹配算法进行实际的逆向处理
    sentence = sentence[::-1]
    result = []
    start = 0
    senlen = len(sentence)
    while start < senlen:
        curword = sentence[start]
        wdlen = 1
        wdlen_rule = 1

        # 寻找以当前字开头的最长词
        if curword in mydict:
            wdlen = maxlen
            words = mydict[curword]
            while wdlen > 1:
                end = min(start+wdlen, senlen)
                if sentence[start:end] in words:
                    break
                else:
                    wdlen = wdlen - 1
        # 将新词使用[::-1]逆置，变为正常词序
        wdlen = max(wdlen_rule, wdlen)
        end = min(start+wdlen, senlen)
        result.append(sentence[start:end][::-1])
        start = start + wdlen
    return result[::-1]

def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print 'Usage: python' + sys.argv[0] + ' dict_path test_path result_path'
        exit(-1)
    dict_path = args[0]
    test_path = args[1]
    result_path = args[2]

    dicts = genDict(dict_path)
    fr = codecs.open(test_path,'r','utf-8')
    test = fr.read()
    result = divideWords(dicts,test,5)
    fr.close()
    fw = codecs.open(result_path,'w','utf-8')
    for item in result:
        fw.write(item + ' ')
    fw.close()

if __name__ == "__main__":
    main()
