#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: 赵晓凯
# Date:   2013-06-05
# Email:  minix007@foxmail.com

# 基于最大熵模型及字标注的分词工具，13特征版本

import codecs
import sys
from maxent import MaxentModel

def tag_training_set(training_file, tag_training_set_file):
    f = codecs.open(training_file,'r','utf-8')
    contents = f.read()
    contents = contents.replace(u'\r', u'')
    contents = contents.replace(u'\n', u'')
    # 将文件内容按空格分开
    words = contents.split(' ')
    print len(words)
    
    tag_words_list = []
    i = 0
    for word in words:
      i += 1
      if (i % 100 == 0): tag_words_list.append(u'\r')
      if(len(word) == 0):
        continue
      if(len(word) == 1):
        tag_word = word + '/S'
      elif(len(word) == 2):
        tag_word = word[0] + '/B' + word[1] + '/E'
      elif(len(word) == 3):
        tag_word = word[0] + '/B' + word[1] + '/C' + word[2] + '/E'
      elif(len(word) == 4):
        tag_word = word[0] + '/B' + word[1] + '/C' + word[2] + '/D' + word[3] + '/E'
      else:
        tag_word = word[0] + '/B' + word[1] + '/C' + word[2] + '/D'
        mid_words = word[3:-1]
        for mid_word in mid_words:
          tag_word += (mid_word + '/M')
        tag_word += (word[-1] + '/E')

      tag_words_list.append(tag_word)

    tag_words = ''.join(tag_words_list)
    fw = codecs.open(tag_training_set_file, 'w', 'utf-8')
    fw.write(tag_words)
    fw.close()

    return (words,tag_words_list)

def get_near_char(contents, i, times):
    words_len = len(contents) / times;
    if (i<0 or i >words_len-1): return '_'
    else: return contents[i*times]

def get_near_tag(contents, i, times):
    words_len = len(contents) / times;
    if (i<0 or i >words_len-1): return '_'
    else: return contents[i*times+2]

def isPu(char):
    punctuation = [u'，', u'。', u'？', u'！', u'；', u'－', u'、', u'—', u'（',u'）',u'《', u'》',u'：',
        u'“',u'”',u'’',u'‘']
    if char in punctuation:
      return '1'
    else:
      return '0'

def get_class(char):
    zh_num = [u'零',u'○',u'一', u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千',u'万']
    ar_num = [u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'.',
              u'０',u'１',u'２',u'３',u'４',u'５',u'６',u'７',u'８',u'９']
    date = [u'日', u'年', u'月']
    letter = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    if char in zh_num or char in ar_num: 
      return '1'
    elif char in date: 
      return '2'
    elif char in letter:
      return '3'
    else:
      return '4'


def get_event(tag_file_path, event_file_path):
    f = codecs.open(tag_file_path,'r','utf-8')
    contents = f.read()
    contents = contents.replace(u'\r', u'')
    contents = contents.replace(u'\n', u'')
    words_len = len(contents)/3
    event_list = []

    index = range(0,words_len)
    for i in index:
      pre_char = get_near_char(contents,i-1,3)
      pre_pre_char = get_near_char(contents,i-2,3)
      cur_char = get_near_char(contents,i,3)
      next_char = get_near_char(contents,i+1,3)
      next_next_char = get_near_char(contents,i+2,3)
      event_list.append(
          contents[i*3+2] + ' '
          + 'C-2='+pre_pre_char + ' ' + 'C-1='+pre_char + ' ' 
          + ' ' + 'C0='+cur_char + ' ' 
          + 'C1='+next_char + ' ' + 'C2='+next_next_char + ' '
          + 'C-2='+pre_pre_char+'C-1='+pre_char + ' '
          + 'C-1='+pre_char+'C0='+cur_char + ' ' 
          + 'C0='+cur_char+'C1='+next_char + ' '
          + 'C1='+next_char+'C2='+next_next_char + ' '
          + 'C-1='+pre_char+'C1='+next_char + ' '
          + 'Pu='+isPu(cur_char) + ' '
          + 'TC-2='+get_class(pre_pre_char)+'TC-1='+get_class(pre_char)
          + 'TC0='+get_class(cur_char)+'TC1='+get_class(next_char)
          + 'TC2='+get_class(next_next_char) + ' '
          + 'T-1='+get_near_tag(contents,i-1,3) + ' '
          + 'T-2='+get_near_tag(contents,i-2,3)
          + '\r')

   
    #events = ''.join(event_list)
    fw = codecs.open(event_file_path, 'w', 'utf-8')
    for event in event_list:
      fw.write(event)
    fw.close()

    return event_list

def get_feature(test_file_path, feature_file_path):
    f = codecs.open(test_file_path,'r','utf-8')
    contents = f.read()
    contents_list = contents.split('\r\n')
    contents_list.remove('')
    contents_list.remove('')

    fw = codecs.open(feature_file_path, 'w', 'utf-8')
    for line in contents_list:
      words_len = len(line)
      feature_list = []

      index = range(0,words_len)
      for i in index:
        pre_char = get_near_char(line,i-1,1)
        pre_pre_char = get_near_char(line,i-2,1)
        cur_char = get_near_char(line,i,1)
        next_char = get_near_char(line,i+1,1)
        next_next_char = get_near_char(line,i+2,1)
        feature_list.append(
              'C-2='+pre_pre_char + ' ' + 'C-1='+pre_char + ' ' 
            + 'C0='+cur_char + ' ' 
            + 'C1='+next_char + ' ' + 'C2='+next_next_char + ' '
            + 'C-2='+pre_pre_char+'C-1='+pre_char + ' '
            + 'C-1='+pre_char+'C0='+cur_char + ' ' 
            + 'C0='+cur_char+'C1='+next_char + ' '
            + 'C1='+next_char+'C2='+next_next_char + ' '
            + 'C-1='+pre_char+'C1='+next_char + ' '
            + 'Pu='+isPu(cur_char) + ' '
            + 'TC-2='+get_class(pre_pre_char)+'TC-1='+get_class(pre_char)
            + 'TC0='+get_class(cur_char)+'TC1='+get_class(next_char)
            + 'TC2='+get_class(next_next_char) + ' '
            + '\r')

      for item in feature_list:
        fw.write(item)
      fw.write('split\r\n')

    fw.close()

    return feature_list

def split_by_blank(line):
  line_list = []
  line_len = len(line)
  i = 0
  while i < line_len:
    line_list.append(line[i])
    i += 2

  return line_list

def training(feature_file_path, trained_model_file, times):
  m = MaxentModel()
  fr = codecs.open(feature_file_path, 'r', 'utf-8')
  all_list = []
  m.begin_add_event()
  for line in fr:
    line = line.rstrip()
    line_list = line.split(' ')
    str_list = []
    for item in line_list:
      str_list.append(item.encode('utf-8'))
    all_list.append(str_list)
    m.add_event(str_list[1:], str_list[0], 1)
  m.end_add_event()
  print 'begin training'
  m.train(times, "lbfgs")
  print 'end training'
  m.save(trained_model_file)
  return all_list

def max_prob(label_prob_list):
  max_prob = 0
  max_prob_label = ''
  for label_prob in label_prob_list:
    if label_prob[1] > max_prob:
      max_prob = label_prob[1]
      max_prob_label = label_prob[0]

  return max_prob_label

def tag_test(test_feature_file, trained_model_file,  tag_test_set_file):
  fr = codecs.open(test_feature_file, 'r', 'utf-8')
  fw = codecs.open(tag_test_set_file, 'w', 'utf-8')
  m = MaxentModel()
  m.load(trained_model_file)
  contents = fr.read()
  feature_list = contents.split('\r')
  feature_list.remove('\n')
  #return feature_list
  pre_tag = '_'
  pre_pre_tag = '_'
  for feature in feature_list:
    if (feature == 'split'):
      fw.write('\n\n\n')
      continue
    str_feature = []
    u_feature = feature.split(' ')
    for item in u_feature:
      str_feature.append(item.encode('utf-8'))
    str_feature.append('T-1=' + pre_tag)
    str_feature.append('T-2=' + pre_pre_tag)
    label_prob_list = m.eval_all(str_feature)
    label = max_prob(label_prob_list)
    #print str_feature
    try:
      new_tag = str_feature[2].split('=')[1] + '/' + label
    except IndexError:
      print str_feature
    fw.write(new_tag.decode('utf-8'))
    pre_pre_tag = pre_tag 
    pre_tag = label
  return feature_list

def tag_to_words(tag_training_set_file, result_file):
    fr = codecs.open(tag_training_set_file, 'r', 'utf-8')
    fw = codecs.open(result_file, 'w', 'utf-8')

    contents = fr.read()
    words_len = len(contents)/3
    result = []
    i = 0
    while (i<words_len):
      cur_word_label = contents[i*3+2]
      cur_word = contents[i*3]
      if (cur_word_label == 'S'):
        result.append(cur_word + ' ')
      elif(cur_word_label == 'B'):
        result.append(cur_word)
      elif(cur_word_label == 'C'):
        result.append(cur_word)
      elif(cur_word_label == 'D'):
        result.append(cur_word)
      elif(cur_word_label == 'M'):
        result.append(cur_word)
      elif(cur_word_label == 'E'):
        result.append(cur_word + ' ')
      else:
        result.append(cur_word)
      i += 1

    fw.write(''.join(result))


def main():
    args = sys.argv[1:]
    if len(args) < 3:

        print 'Usage: python ' + sys.argv[0] + ' training_file test_file result_file'
        exit(-1)
    training_file = args[0]
    test_file = args[1]
    result_file = args[2]

    # 标注训练集
    tag_training_set_file = training_file + ".tag"
    tag_training_set(training_file, tag_training_set_file)
    print 'tag training set succeed'

    # 获取训练集特征
    feature_file_path = training_file + ".feature"
    get_event(tag_training_set_file, feature_file_path)
    print 'get training set features succeed'

    # 测试集生成特征
    test_feature_file = test_file + ".feature"
    get_feature(test_file, test_feature_file)
    print 'get test set features succeed'

    # 训练模型
    times = [1000]
    for time in times:
      trained_model_file = training_file + '.' + str(time) + ".model"
      training(feature_file_path, trained_model_file,time)
      print 'training model succeed:' + str(time)

      # 标注测试集
      tag_test_set_file = test_file + ".tag"
      tag_test(test_feature_file, trained_model_file,  tag_test_set_file)
      print 'tag test set succeed'
  
      # 获取最终结果
      tag_to_words(tag_test_set_file, result_file+'.'+str(time))
      print 'get final result succeed ' + result_file + '.'+str(time)

if __name__ == "__main__":
    main()

