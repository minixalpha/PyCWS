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
=============================================================================
 0.    cwsFMM
Description:

    Using Foward Maximum Match(FMM) algorithm to do Chinese Word Segamentation

=== TOTAL TRUE WORDS RECALL:    0.924

=== TOTAL TEST WORDS PRECISION: 0.897

=== F MEASURE:  0.910

Usage:

    python cwsFMM.py training_file test_file result_file
    
    perl score training_file gold_file result_file > score_file

Notice:
   All the data and the tool score come from:http://sighan.cs.uchicago.edu/bakeoff2005/
   
   
----------------------------------------------------------------------------------


 1.    cwsBMM
Description:

    Using Backward Maximum Match(BMM) algorithm to do Chinese Word Segamentation

=== TOTAL TRUE WORDS RECALL:    0.920

=== TOTAL TEST WORDS PRECISION: 0.895

=== F MEASURE:  0.907

Usage:

    python cwsBMM.py training_file test_file result_file
    
    perl score training_file gold_file result_file > score_file

Notice:
   All the data and the tool score come from:http://sighan.cs.uchicago.edu/bakeoff2005/
