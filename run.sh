#!/bin/bash
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 'partition0_train.arff' -T 'partition0_test.arff' -o > 'smo0.txt'


#for cmd in `seq 0 9`; do
#  java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 'partition$cmd_train.arff' -T 'partition$cmd_test.arff' -o > 'smo$cmd.txt'
#done
