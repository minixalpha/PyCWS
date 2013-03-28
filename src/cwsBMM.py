#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: minix
# Date:   2013-03-20
# Email:  minix007@foxmail.com

# 使用BMM 进行中文分词

import codecs
import sys

# 由规则处理的一些特殊符号
numMath = [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9']
numMath_suffix = [u'.', u'%', u'亿', u'万', u'千', u'百', u'十', u'个']
numCn = [u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'〇', u'零']
numCn_suffix_date = [u'年', u'月', u'日']
numCn_suffix_unit = [u'亿', u'万', u'千', u'百', u'十', u'个']
special_char = [u'(', u')']
num_char = numMath + numCn
num_suffix = numMath_suffix + numCn_suffix_unit + numCn_suffix_date

def proc_num_math(line, start):
    """ 处理句子中出现的数学符号 """
    oldstart = start
    start = start + 1
    while line[start] in numMath or line[start] in numMath_suffix:
        start = start + 1
    return start - oldstart

def proc_num_cn(line, start):
    """ 处理句子中出现的中文数字 """
    oldstart = start
    while line[start] in numCn or line[start] in numCn_suffix_unit:
        start = start + 1
    return start - oldstart

def rules(line, start):
    """ 处理特殊规则 """
    if line[start] in numMath or line[start] in num_suffix:
        return proc_num_math(line, start)
    elif line[start] in numCn or line[start] in num_suffix:
        return proc_num_cn(line, start)
    else:
        return 1


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
    使用正向匹配的算法，从左到右扫描，遇到最长的词，
    就将它切下来，直到句子被分割完闭
    """
    # 对句子逆置，以便用正向匹配算法进行实际的逆向处理
    sentence = sentence[::-1]
    ruleChar = []
    ruleChar.extend(numCn)
    ruleChar.extend(numMath)
    result = []
    start = 0
    senlen = len(sentence)
    while start < senlen:
        curword = sentence[start]
        wdlen = 1
        wdlen_rule = 1
        # 首先查看是否可以匹配特殊规则
        if curword in num_char or curword in num_suffix:
            wdlen_rule = rules(sentence, start)
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
    option_maxlen = args[0]
    if len(args) < 5 or option_maxlen != '-maxlen':
        print 'Usage: python cwsBMM.py -maxlen word_maxlen dict_path test_path result_path'
        exit(-1)
    word_maxlen = int(args[1])
    dict_path = args[2]
    test_path = args[3]
    result_path = args[4]

    dicts = genDict(dict_path)
    fr = codecs.open(test_path,'r','utf-8')
    test = fr.read()
    result = divideWords(dicts,test,word_maxlen)
    fr.close()
    fw = codecs.open(result_path,'w','utf-8')
    for item in result:
        fw.write(item + ' ')
    fw.close()

if __name__ == "__main__":
    main()
