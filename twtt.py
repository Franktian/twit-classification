import sys
import re

import NLPlib

TAG_RE = re.compile(r'<[^>]+>')

class Parser:
  pass

def parse_line(line, abbrev, pn_abbrev, names, tagger):
  # All html tags and attributes are removed
  line = TAG_RE.sub('', line)
  # HTML character codes are replaced with an ASCII equivalent
  line = line.replace('&amp;gt;', '>') \
             .replace('&amp;lt;', '<') \
             .replace('&amp;', '&') \
             .replace('&quot;', '"')

  # Tokenize the tweet line
  tokens = line.strip().split()

  # All URLs are removed
  tokens = filter(not_url, tokens)

  # The first character in Twitter user names
  # (@) and hash tags (#) are removed
  tokens = map(process_hash, tokens)

  # Place sentence boundary
  tokens = sentence_division(tokens, abbrev, pn_abbrev, names)

  # Tokenize punctuation and clitics
  tokens = punctuation_tokenize(tokens, abbrev, pn_abbrev)

  # Tag the token
  tags = tagger.tag(tokens)
  tagged_tokens = []

  for token, tag in zip(tokens, tags):
    tagged_tokens.append("/".join([token, tag]))

  # Format the updated tokens to sentence
  return " ".join(tagged_tokens).split("**/NN")


def not_url(token):
  return not token.startswith(("http", "Http", "www", "ofa.bo", "OFA.BO")) and \
         not token.endswith((".com", ".net", ".org", ".ca", ".edu"))

def process_hash(token):
  if token.startswith(("#", "@")):
    return token[1:]
  return token

def sentence_division(tokens, abbrev, pn_abbrev, names):
  '''
  Implement heuristic sentence boundary
  detection algorithm.

  Takes a list of tokens, returns a list of sentences
  '''
  sentence = []

  for i, token in enumerate(tokens):
    # Place putative sentence boundaries after
    # all occurrences of .?!;:"

    # TODO: double check multiple punctuations
    #if token.endswith(("...", "!!!")):
      #continue
    if token.endswith((";", ":", "\"")):
      tokens.insert(i + 1, "**")
    elif token.endswith(".") and not token.lower() in abbrev \
                             and not token.lower() in pn_abbrev:
      tokens.insert(i + 1, "**")
    elif token.endswith(("!", "?")) and i + 1 < len(tokens):
      if not (tokens[i + 1][0].islower() or tokens[i + 1].lower() in names):
        tokens.insert(i + 1, "**")
  return tokens

def punctuation_tokenize(tokens, abbrev, pn_abbrev):
  new_tokens = []
  # TODO: implement clitics
  for i, token in enumerate(tokens):
    if token.startswith(("'", "(", "$")):
      new_tokens.append(token[0])
      new_tokens.append(token[1:])
    elif token.endswith((":", ";", ",", "'", ")", "?", "!")):
      new_tokens.append(token[:-1])
      new_tokens.append(token[-1])
    elif token.endswith(".") and not (token.lower() in abbrev or token.lower() in pn_abbrev):
      new_tokens.append(token[:-1])
      new_tokens.append(token[-1])
    else:
      new_tokens.append(token)
  return new_tokens

def load_helper(file_name):
  with open(file_name, 'rU') as file:
    return [line.strip().lower() for line in file]

def main(argv):
  '''
  Main method, responsible for parsing system args
  '''
  raw_file = argv[0]
  result_file = argv[1]
  result_output = open(result_file, 'w')

  # Load resources
  abbrev = load_helper("abbrev.english")
  pn_abbrev = load_helper("pn_abbrev.english")
  male_names = load_helper("maleFirstNames.txt")
  female_names = load_helper("femaleFirstNames.txt")
  last_names = load_helper("lastNames.txt")
  names = male_names + female_names + last_names

  # Load tagger
  tagger = NLPlib.NLPlib()

  with open (raw_file, 'rU') as file:
    for line in file:
      lines = parse_line(line, abbrev, pn_abbrev, names, tagger)
      for l in lines:
        result_output.write(l + "\n")
      result_output.write("|\n")

if __name__ == '__main__':
  main(sys.argv[1:])
