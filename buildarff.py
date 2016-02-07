import sys
import re

from twtt import load_helper

# Feature list, easy to add new features
features = [
  "first_person_pronouns",
  "second_person_pronouns",
  "third_person_pronouns",
  "coordinating_conjunctions",
  "past_tense_verbs",
  "future_tense_verbs",
  "commas",
  "colons_and_semi_colons",
  "dashes",
  "parentheses",
  "ellipses",
  "common_nouns",
  "proper_nouns",
  "adverbs",
  "wh_words",
  "modern_slang_acroynms",
  "words_all_in_upper_case",
  "average_length_of_sentences",
  "average_length_of_tokens",
  "number_of_sentences",
]

def main(argv):
  max_tweets = sys.maxint

  # load word lists
  fp = load_helper("/u/cs401/Wordlists/First-person")
  sp = load_helper("/u/cs401/Wordlists/Second-person")
  tp = load_helper("/u/cs401/Wordlists/Third-person")
  sl = load_helper("/u/cs401/Wordlists/Slang")
  words = {
    "fp": fp,
    "sp": sp,
    "tp": tp,
    "sl": sl,
  }

  result_file = open(argv[1], 'w')

  if len(argv) > 2:
    max_tweets = int(argv[2])
  print max_tweets

  # Write file header
  result_file.write("@relation %s\n\n" % argv[-1].split(".")[0])
  for feature in features:
    result_file.write("@attribute %s numeric\n" % feature)

  class_names = []
  class_mapping = {}

  '''
  for i, arg in enumerate(argv):
    # First argument starts with a hyphen
    # indicates the maximum number of
    # tweets will be used
    if arg.startswith("-") and i == 0:
      max_tweets = int(arg[1:])
    elif i < len(argv) - 1:
      # Variable n classes arguments
      classes = arg.split(":")
      class_list = classes[-1].split("+")
      if len(classes) == 2:
        class_name = classes[0]
      else:
        class_name = "".join(map(remove_suffix, class_list))
      class_names.append(class_name)
      class_mapping[class_name] = class_list'''


  result_file.write("@attribute class numeric\n\n")
  result_file.write("@data\n")

  write_data(result_file, 4, ["train.twt"], words, max_tweets)

  '''
  for (class_name, files) in class_mapping.items():
    write_data(result_file, class_name, files, words, max_tweets)'''

def write_data(result_file, class_name, files, words, max_tweets):
  tweet = []
  for f in files:
    with open(f, 'rU') as file:
      tweet_count = 0
      for sentence in file:
        print sentence.strip()
        if sentence.strip() in  ["<A=0>", "<A=4>"]:
          result_file.write(write_data_line("Frank", tweet, words) + "\n")
          tweet = []
          tweet_count += 1
          if tweet_count >= max_tweets:
            break
        else:
          tokens = sentence.strip().split()
          tweet.append(map(split_token, tokens))


def write_data_line(class_name, tweet, words):
  feature_counts = []

  feature_counts.append(count_pronoun(tweet, words["fp"], ["PRP", "PRP$"]))
  feature_counts.append(count_pronoun(tweet, words["sp"], ["PRP", "PRP$"]))
  feature_counts.append(count_pronoun(tweet, words["tp"], ["PRP", "PRP$"]))
  feature_counts.append(count_helper(tweet, 1, ["CC"]))
  feature_counts.append(count_helper(tweet, 1, ["VBD"]))
  feature_counts.append(count_future(tweet))
  feature_counts.append(count_helper(tweet, 1, [","]))
  feature_counts.append(count_helper(tweet, 0, [";", ":"]))
  feature_counts.append(count_dashes(tweet))
  feature_counts.append(count_helper(tweet, 1, ["(", ")"]))
  feature_counts.append(count_helper(tweet, 0, ["..."]))
  feature_counts.append(count_helper(tweet, 1, ["NN", "NNS"]))
  feature_counts.append(count_helper(tweet, 1, ["NNP", "NNPS"]))
  feature_counts.append(count_helper(tweet, 1, ["RB", "RBR", "RBS"]))
  feature_counts.append(count_helper(tweet, 1, ["WDT", "WP", "WP$", "WRB"]))
  feature_counts.append(count_helper(tweet, 0, words["sl"]))
  feature_counts.append(count_upper(tweet))
  feature_counts.append(count_avg_sen_len(tweet))
  feature_counts.append(count_avg_token_len(tweet))
  feature_counts.append(len(tweet))

  return ",".join(map(stringify, feature_counts)) + "," + class_name

def count_pronoun(tweet, words, tags):
  count = 0
  for sentence in tweet:
    for word in sentence:
      if word[0] in words and word[1] in tags:
        count += 1
  return count

def count_helper(tweet, index, tags):
  count = 0
  for sentence in tweet:
    print sentence
    for word in sentence:
      print word
      print index
      if word[index] in tags:
        count += 1
  return count

def count_future(tweet):
  count = count_helper(tweet, 0, ["'ll", "will", "gonna"])

  for sentence in tweet:
    if len(sentence) >= 3:
      for i in range(len(sentence) - 2):
        if sentence[i][0] == "going" and \
            sentence[i + 1][0] == "to" and sentence[i + 2][1] == "VB":
          count += 1

  return count

def count_dashes(tweet):
  count = 0

  for sentence in tweet:
    for word in sentence:
      for char in word[0]:
        if char == "-":
          count += 1

  return count

def count_upper(tweet):
  count = 0

  for sentence in tweet:
    for word in sentence:
      if word[0].isupper() and len(word[0]) > 1:
        count += 1

  return count

def count_avg_sen_len(tweet):
  total_len = 0

  if len(tweet) > 0:
    for sentence in tweet:
      total_len += len(sentence)
  try:
    return total_len / len(tweet)
  except Exception:
    return 0

def count_avg_token_len(tweet):
  total_len = 0
  total_tokens = 0

  for sentence in tweet:
    for word in sentence:
      total_len += len(word[0])
      total_tokens += 1

  try:
    return total_len / total_tokens
  except Exception:
    return 0

def split_token(token):
  return token.split("/")

def stringify(integer):
  return str(integer)

def remove_suffix(file_name):
  '''
  Remove .twt file extension
  '''
  return file_name[:-4]
if __name__ == '__main__':
  main(sys.argv[1:])
