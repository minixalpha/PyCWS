#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: minix
# Date:   2013-05-18
# Email:  minix007@foxmail.com

# 功能：
#     0. 自动为多个文件评分
#     1. 提取多个评分结果
#     2. 打印所有评分结果

# 使用：
#   例如分词结果文件为：pku_test.result.10,pku_test.result.50,pku_test.result.xxx
#   这样文件名的模板为pku_test.result
#   python autoScore pku_test.result 即可将所有此类文件评分，输出评分结果

import sys
import os

def score_files(file_name_temp):
  filename_list = os.popen('ls ' + file_name_temp + '.*').readlines()
  score_path = '/home/zhaoxk/Project/PyCWS/score/score'
  for filename in filename_list:
    filename = filename.rstrip()
    fileid = filename.split('.')[-1]
    name = filename.split('.')[0]
    cmd = 'perl ' + score_path + ' pku_training.utf8 pku_test_gold.utf8 ' + filename  + ' > ' + name +'.score.' + fileid
    print cmd
    os.system(cmd)

def extract_score_result(file_name_temp):
  filename_list = os.popen('ls ' + file_name_temp + '.*').readlines()
  fileid_list = []
  for filename in filename_list:
    filename = filename.rstrip()
    fileid = filename.split('.')[-1]
    fileid_list.append(int(fileid))
  fileid_list.sort()
  
  result_list = []
  for fileid in fileid_list:
    filename = file_name_temp + '.' + str(fileid)
    cmd = 'tail -16 ' + filename 
    result = os.popen(cmd).readlines()
    cur_result_list = []
    for item in result[:-1]:
      tmp = item.rstrip().split('\t')
      if len(tmp) > 1:
        cur_result_list.append(tmp[1])
          
    result_list.append(cur_result_list)

  return (fileid_list, result_list)

def main():
  args = sys.argv[1:]

  if len(args)<1:
    print 'Usage: python autoScore.py file_to_score'
    exit(-1)

  file_to_score = args[0]
  score_files(file_to_score)
  (id_list, re_list) = extract_score_result(file_to_score.split('.')[0] + '.score')
  id_len = len(id_list)
  i = 0
  print 'id'
  label_list = [
      'TRUE WORDS RECALL', 'TEST WORDS PRECISION',
      'TOTAL INSERTIONS', 'TOTAL DELETIONS',
      'TOTAL SUBSTITUTIONS', 'TOTAL NCHANGE',
      'TOTAL TRUE WORD COUNT', 'TOTAL TEST WORD COUNT',
      'TOTAL TRUE WORDS RECALL', 'TOTAL TEST WORDS PRECISION',
      'F MEASURE',
      'OOV Rate', 'OOV Recall Rate',
      'IV Recall Rate'
      ]
  print label_list
  while i< id_len:
    print id_list[i]
    print re_list[i]
    i += 1

if __name__ == "__main__":
  main()
