# ibmTrain.py
# 
# This file produces 11 classifiers using the NLClassifier IBM Service
# 
# TODO: You must fill out all of the functions in this file following 
# 		the specifications exactly. DO NOT modify the headers of any
#		functions. Doing so will cause your program to fail the autotester.
#
#		You may use whatever libraries you like (as long as they are available
#		on CDF). You may find json, request, or pycurl helpful.
#

###IMPORTS###################################
#TODO: add necessary imports
import csv
import requests

NLPSERVICE = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/"

###HELPER FUNCTIONS##########################

def convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name): 
	# Converts an existing training csv file. The output file should
	# contain only the 11,000 lines of your group's specific training set.
	#
	# Inputs:
	#	input_csv - a string containing the name of the original csv file
	#		ex. "my_file.csv"
	#
	#	output_csv - a string containing the name of the output csv file
	#		ex. "my_output_file.csv"
	#
	# Returns:
	#	None

  result_file = open(output_csv_name, 'w')
  zero_start = group_id * 5500
  zero_end = (group_id + 1) * 5500 - 1
  four_start = zero_start + 800000
  four_end = zero_end + 800000


  with open (input_csv_name, 'rb') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
      class_label = "\"" + line[0] + "\""
      tweet = "\"" + line[-1].strip().replace("\t", " ") + "\""
      if (i <= zero_end and i >= zero_start) or (i <= four_end and i >= four_start):
        s = unicode(tweet + "," + class_label + "\n", "utf-8")
        result_file.write(s)

def extract_subset_from_csv_file(input_csv_file, n_lines_to_extract, output_file_prefix='ibmTrain'):
	# Extracts n_lines_to_extract lines from a given csv file and writes them to 
	# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
	#
	# Inputs: 
	#	input_csv - a string containing the name of the original csv file from which
	#		a subset of lines will be extracted
	#		ex. "my_file.csv"
	#	
	#	n_lines_to_extract - the number of lines to extract from the csv_file, as an integer
	#		ex. 500
	#
	#	output_file_prefix - a prefix for the output csv file. If unspecified, output files 
	#		are named 'ibmTrain#.csv', where # is the input parameter n_lines_to_extract.
	#		The csv must be in the "watson" 2-column format.
	#		
	# Returns:
	#	None

  result_file = open(output_file_prefix + str(n_lines_to_extract) + ".csv", 'w')
  zero_start = 0
  zero_end = zero_start + n_lines_to_extract - 1
  four_start = zero_start + 5500
  four_end = four_start + n_lines_to_extract - 1

  with open(input_csv_file, 'rU') as file:
    for i, line in enumerate(file):
      if (i <= zero_end and i >= zero_start) or (i <= four_end and i >= four_start):
        result_file.write(line)
	
def create_classifier(username, password, n, input_file_prefix='ibmTrain'):
	# Creates a classifier using the NLClassifier service specified with username and password.
	# Training_data for the classifier provided using an existing csv file named
	# ibmTrain#.csv, where # is the input parameter n.
	#
	# Inputs:
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	n - identification number for the input_file, as an integer
	#		ex. 500
	#
	#	input_file_prefix - a prefix for the input csv file, as a string.
	#		If unspecified data will be collected from an existing csv file 
	#		named 'ibmTrain#.csv', where # is the input parameter n.
	#		The csv must be in the "watson" 2-column format.
	#
	# Returns:
	# 	A dictionary containing the response code of the classifier call, will all the fields 
	#	specified at
	#	http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/natural-language-classifier/api/v1/?curl#create_classifier
	#   
	#
	# Error Handling:
	#	This function should throw an exception if the create classifier call fails for any reason
	#	or if the input csv file does not exist or cannot be read.
	#
	
	#TODO: Fill in this function

  files = {
    'training_data': open(input_file_prefix + str(n) + '.csv', 'rb'),
    'training_metadata': (input_file_prefix + str(n) + '.csv', '{"language": "en", "name": "Classifier ' + str(n) + '"}'),
  }

  r = requests.post(NLPSERVICE, files=files, auth=(username, password))

  if r.status_code != 200:
    raise Exception("Classifier call failed for some reason.")

  return r.json()


def remove_double_quotes(line):
  return line.replace("\"", "")
	
if __name__ == "__main__":
	
  ### STEP 1: Convert csv file into two-field watson format
  input_csv_name = '/u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv'

  #DO NOT CHANGE THE NAME OF THIS FILE
  output_csv_name = 'training_11000_watson_style.csv'

  #convert_training_csv_to_watson_csv_format(input_csv_name, 63, output_csv_name)

  ### STEP 2: Save 11 subsets in the new format into ibmTrain#.csv files

  #TODO: extract all 11 subsets and write the 11 new ibmTrain#.csv files
  #
  # you should make use of the following function call:
  #
  # n_lines_to_extract = 500
  extract_subset_from_csv_file(output_csv_name, 500)
  extract_subset_from_csv_file(output_csv_name, 2500)
  extract_subset_from_csv_file(output_csv_name, 5000)

  ### STEP 3: Create the classifiers using Watson

  #TODO: Create all 11 classifiers using the csv files of the subsets produced in 
  # STEP 2
  # 
  #
  # you should make use of the following function call
  # n = 500
  username = "b153156f-444c-452f-bfaa-a3930a5877b9"
  password = "dnzjfVHcnvS6"
  # create_classifier(username, password, n, input_file_prefix='ibmTrain')
  create_classifier(username, password, 500)
  create_classifier(username, password, 2500)
  create_classifier(username, password, 5000)

