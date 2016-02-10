import sys

def main(argv):
  num = 550
  for i in range(10):
    train = open("partition"+str(i)+'_train.arff', 'w')
    test = open("partition"+str(i)+"_test.arff", 'w')
    
    with open(argv) as myfile:
      linenum=0
      for line in myfile:
        if linenum < 25:
          train.write(line)
          test.write(line)
        elif (linenum >= 25+(num*i) and linenum < 25+num*(i+1)) or (linenum >= 5525+(num*i) and linenum < 5525+num*(i+1)):
          test.write(line)
        else:
          train.write(line)
        linenum += 1


if __name__ == "__main__":
  main('all.arff')
