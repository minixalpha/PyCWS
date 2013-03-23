Requirements:
  * Ubuntu 12.04
  * Python 2.7.3
  * Perl 5

File Description:
    src/cwsFMM.py -- source code of tool cwFMM
    src/pku_training.utf8 -- training data
    src/pku_test.utf8 -- test data
    socre/score -- tools to socre the result
    socre/pku_test_gold.utf8 -- gold data

Tool:
    cwsFMM
Description:
    Using Foward Maximum Match(FMM) algorithm to do Chinese Word Segamentation
Usage:
    python cwsFMM.py training_file test_file result_file
    perl score training_file gold_file result_file > score_file

