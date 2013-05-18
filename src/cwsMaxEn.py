#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: minix
# Date:   2013-05-16
# Email:  minix007@foxmail.com

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
      else:
        tag_word = word[0] + '/B'
        mid_words = word[1:-1]
        for mid_word in mid_words:
          tag_word += (mid_word + '/M')
        tag_word += (word[-1] + '/E')

      tag_words_list.append(tag_word)

    tag_words = ''.join(tag_words_list)
    fw = codecs.open(tag_training_set_file, 'w', 'utf-8')
    fw.write(tag_words)
    fw.close()

    return (words,tag_words_list)

def get_event(tag_file_path, event_file_path):
    f = codecs.open(tag_file_path,'r','utf-8')
    contents = f.read()
    contents = contents.replace(u'\r', u'')
    contents = contents.replace(u'\n', u'')
    words_len = len(contents)/3

    event_list = []
    event_list.append(
          contents[2] + ' '
        + 'C-1=b' + ' ' + 'C0='+contents[0] + ' ' + 'C1='+contents[1*3] + ' '
        + 'C-1=b'+'C0='+contents[0] + ' ' + 'C0='+contents[0]+'C1='+contents[1*3] + ' '
        + 'C-1=b'+'C1='+contents[1*3] 
        + '\r')

    index = range(1,words_len-1)
    for i in index:
      event_list.append(
          contents[i*3+2] + ' '
          + 'C-1='+contents[(i-1)*3] + ' ' + 'C0='+contents[i*3] + ' ' + 'C1='+contents[(i+1)*3] + ' '
          + 'C-1='+contents[(i-1)*3]+'C0='+contents[i*3] + ' ' + 'C0='+contents[i*3]+'C1='+contents[(i+1)*3] + ' '
          + 'C-1='+contents[(i-1)*3]+'C1='+contents[(i+1)*3] 
        + '\r')

    event_list.append(
        contents[(words_len-1)*3+2]  + ' '
        + 'C-1='+contents[(words_len-2)*3] + ' ' + 'C0='+contents[(words_len-1)*3] + ' ' + 'C1='+'b' + ' '
        + 'C-1='+contents[(words_len-2)*3]+'C0='+contents[(words_len-1)*3] + ' ' + 'C0='+contents[(words_len-1)*3]+'C1='+'b' + ' '
        + 'C-1='+contents[(words_len-2)*3]+'C1='+'b'
        + '\r')
    events = ''.join(event_list)
    fw = codecs.open(event_file_path, 'w', 'utf-8')
    fw.write(events)
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
      feature_list.append(
            'C-1=b' + ' ' + 'C0='+line[0] + ' ' + 'C1='+line[1] + ' '
          + 'C-1=b'+'C0='+line[0] + ' ' + 'C0='+line[0]+'C1='+line[1] + ' '
          + 'C-1=b'+'C1='+line[1] 
          + '\r')

      index = range(1,words_len-1)
      for i in index:
        feature_list.append(
              'C-1='+line[(i-1)] + ' ' + 'C0='+line[i] + ' ' + 'C1='+line[(i+1)] + ' '
            + 'C-1='+line[(i-1)]+'C0='+line[i] + ' ' + 'C0='+line[i]+'C1='+line[(i+1)] + ' '
            + 'C-1='+line[(i-1)]+'C1='+line[(i+1)] 
          + '\r')

      feature_list.append(
            'C-1='+line[(words_len-2)] + ' ' + 'C0='+line[(words_len-1)] + ' ' + 'C1='+'b' + ' '
          + 'C-1='+line[(words_len-2)]+'C0='+line[(words_len-1)] + ' ' + 'C0='+line[(words_len-1)]+'C1='+'b' + ' '
          + 'C-1='+line[(words_len-2)]+'C1='+'b'
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
  for feature in feature_list:
    if (feature == 'split'):
      fw.write('\n\n\n')
      continue
    str_feature = []
    u_feature = feature.split(' ')
    for item in u_feature:
      str_feature.append(item.encode('utf-8'))
    label_prob_list = m.eval_all(str_feature)
    label = max_prob(label_prob_list)
    #print str_feature
    try:
      new_tag = str_feature[1].split('=')[1] + '/' + label
    except IndexError:
      print str_feature
    fw.write(new_tag.decode('utf-8'))
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

        print 'Usage: python cwsMaxEn.py training_file test_file result_file'
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
    times = [10,50,100,200,300,400,500,600]
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
      print 'get final result succeed' + result_file + str(time)

if __name__ == "__main__":
    main()

