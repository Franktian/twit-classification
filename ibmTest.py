# ibmTest.py
# 
# This file tests all 11 classifiers using the NLClassifier IBM Service
# previously created using ibmTrain.py
# 
# TODO: You must fill out all of the functions in this file following 
# 		the specifications exactly. DO NOT modify the headers of any
#		functions. Doing so will cause your program to fail the autotester.
#
#		You may use whatever libraries you like (as long as they are available
#		on CDF). You may find json, request, or pycurl helpful.
#		You may also find it helpful to reuse some of your functions from ibmTrain.py.
#

import requests
import csv
import json

NLPSERVICE = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/"

def get_classifier_ids(username,password):
	# Retrieves a list of classifier ids from a NLClassifier service 
	# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#		
	# Returns:
	#	a list of classifier ids as strings
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason
	#

  r = requests.get(NLPSERVICE, auth=(username, password))

  if r.status_code != 200:
    raise Exception("Classifier call failed for some reason.")

  return map(lambda x: x["classifier_id"], r.json()["classifiers"])


def assert_all_classifiers_are_available(username, password, classifier_id_list):
	# Asserts all classifiers in the classifier_id_list are 'Available' 
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id_list - a list of classifier ids as strings
	#		
	# Returns:
	#	None
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason AND 
	#	It should throw an error if any classifier is NOT 'Available'
	#

  for classifier in classifier_id_list:
    r = requests.get(NLPSERVICE + classifier, auth=(username, password))

    if r.json()["status"] != "Available" or r.status_code != 200:
      raise Exception("Classifier call failed or classifier is not ready yet!")


def classify_single_text(username,password,classifier_id,text):
	# Classifies a given text using a single classifier from an NLClassifier 
	# service
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id - a classifier id, as a string
	#		
	#	text - a string of text to be classified, not UTF-8 encoded
	#		ex. "Oh, look a tweet!"
	#
	# Returns:
	#	A "classification". Aka: 
	#	a dictionary containing the top_class and the confidences of all the possible classes 
	#	Format example:
	#		{'top_class': 'class_name',
	#		 'classes': [
	#					  {'class_name': 'myclass', 'confidence': 0.999} ,
	#					  {'class_name': 'myclass2', 'confidence': 0.001}
	#					]
	#		}
	#
	# Error Handling:
	#	This function should throw an exception if the classify call fails for any reason 
	#

  payload = {
    "text": text
  }

  r = requests.get(NLPSERVICE + classifier_id + "/classify", auth=(username, password), params=payload)

  if r.status_code != 200:
    raise Exception("Classify call failed!")

  return {
    "top_class": r.json()["top_class"],
    "classes": r.json()["classes"],
  }


def classify_all_texts(username,password,input_csv_name):
  # Classifies all texts in an input csv file using all classifiers for a given NLClassifier
  # service.
  #
  # Inputs:
  #       username - username for the NLClassifier to be used, as a string
  #
  #       password - password for the NLClassifier to be used, as a string
  #      
  #       input_csv_name - full path and name of an input csv file in the 
  #              6 column format of the input test/training files
  #
  # Returns:
  #       A dictionary of lists of "classifications".
  #       Each dictionary key is the name of a classifier.
  #       Each dictionary value is a list of "classifications" where a
  #       "classification" is in the same format as returned by
  #       classify_single_text.
  #       Each element in the main dictionary is:
  #       A list of dictionaries, one for each text, in order of lines in the
  #       input file. Each element is a dictionary containing the top_class
  #       and the confidences of all the possible classes (ie the same
  #       format as returned by classify_single_text)
  #       Format example:
  #              {classifiername:
  #                      [
  #                              {'top_class': 'class_name',
  #                              'classes': [
  #                                        {'class_name': 'myclass', 'confidence': 0.999} ,
  #                                         {'class_name': 'myclass2', 'confidence': 0.001}
  #                                          ]
  #                              },
  #                              {'top_class': 'class_name',
  #                              ...
  #                              }
  #                      ]
  #              , classifiername2:
  #                      [
  #                      
  #                      ]
  #              
  #              }
  #
  # Error Handling:
  #       This function should throw an exception if the classify call fails for any reason
  #       or if the input csv file is of an improper format.
  #

  classifier_ids = get_classifier_ids(username, password)
  results = {}
  tweets = []

  # Read in the tweets
  with open(input_csv_name, 'rb') as f:
    reader = csv.reader(f)
    for line in reader:
      tweets.append(line[-1])

  # Get classifier names
  classifier_names = []
  for classifier_id in classifier_ids:
    r = requests.get(NLPSERVICE + classifier_id, auth=(username, password))

    if r.status_code != 200:
      raise Exception("Classify call failed")

    classifier = r.json()
    results[classifier["name"]] = []
    classifier_names.append(classifier["name"])


  # Classify the data
  for classifier_id, classifier_name in zip(classifier_ids, classifier_names):
    for tweet in tweets:
      results[classifier_name].append(classify_single_text(username, password, classifier_id, tweet))

  return results


def compute_accuracy_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the accuracy of this
	# classifier according to the input csv file
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The accuracy of the classifier, as a fraction between [0.0-1.0] (ie percentage/100). \
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#

  correct_classification = 0

  with open(input_csv_file_name, 'rb') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
      if line[0] == classifier_dict[i]["top_class"]:
        correct_classification +=1

  return correct_classification / float(len(classifier_dict))


def compute_average_confidence_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the average 
	# confidence of this classifier wrt the selected class, according to the input
	# csv file. 
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The average confidence of the classifier, as a number between [0.0-1.0]
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#

  correct_confidence = 0
  correct_count = 0
  incorrect_confidence = 0
  incorrect_count = 0

  with open(input_csv_file_name, 'rb') as f:
    reader = csv.reader(f)

    for i, line in enumerate(reader):
      if line[0] == classifier_dict[i]["top_class"]:
        correct_confidence += classifier_dict[i]["classes"][0]["confidence"]
        correct_count += 1
      else:
        incorrect_confidence += classifier_dict[i]["classes"][0]["confidence"]
        incorrect_count += 1

  return (correct_confidence / correct_count, incorrect_confidence / incorrect_count)


if __name__ == "__main__":

  input_test_data = '/u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv'

  username = "b153156f-444c-452f-bfaa-a3930a5877b9"
  password = "dnzjfVHcnvS6"

  #STEP 1: Ensure all 11 classifiers are ready for testing
  #classifier_ids = get_classifier_ids(username, password)
  #assert_all_classifiers_are_available(username, password, classifier_ids)
	
	#STEP 2: Test the test data on all classifiers
  classifiers = classify_all_texts(username, password, input_test_data)

  #STEP 3: Compute the accuracy for each classifier
  print compute_accuracy_of_single_classifier(classifiers["Classifier 500"], input_test_data)
  print compute_accuracy_of_single_classifier(classifiers["Classifier 2500"], input_test_data)
  print compute_accuracy_of_single_classifier(classifiers["Classifier 5000"], input_test_data)

  #STEP 4: Compute the confidence of each class for each classifier
  print compute_average_confidence_of_single_classifier(classifiers["Classifier 500"], input_test_data)
  print compute_average_confidence_of_single_classifier(classifiers["Classifier 2500"], input_test_data)
  print compute_average_confidence_of_single_classifier(classifiers["Classifier 5000"], input_test_data)

