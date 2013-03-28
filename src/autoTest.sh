python cwsBMM.py -maxlen 6 pku_training.utf8 pku_test.utf8 pku_bmm_result.utf8
cp pku_bmm_result.utf8 ../score/
cd ../score/
perl score pku_training.utf8 pku_test_gold.utf8 pku_bmm_result.utf8 > pku_bmm_score.utf8
tail pku_bmm_score.utf8
cd ../src/
