import sys
from scipy import stats

def main():
  acc_array = {'smo':[], 'bayes':[], 'tree':[]}
  output = open("output_all.txt", 'w')
  output.write("classifier\taccuracy\t\tprecision(0)\t\tprecision(4)\t\trecall(0)\t\trecall(4)\n")  
  for method in ['smo', 'bayes', 'tree']:
    output.write("\n")
    for i in range(10):
      f = open(method+str(i)+".txt", 'r')
      lst = f.readlines()
      f.close()
      
      c00 = float(lst[-3].strip().split()[0])
      c01 = float(lst[-3].strip().split()[1])
      c10 = float(lst[-2].strip().split()[0])
      c11 = float(lst[-2].strip().split()[1])
      accuracy = (c00 + c11) / 1100.000
      acc_array[method].append(accuracy)
      
      precision0 = c00 / (c00 + c01)
      precision4 = c11 / (c10 + c11)
      recall0 = c00 / (c00 + c10)
      recall4 = c11 / (c01 + c11)
      output.write (method+"\t"+str(accuracy)+"\t"+str(precision0)+"\t"+str(precision4)+"\t"+str(recall0)+"\t"+str(recall4)+"\n")
  #print(acc_array)
  s1 = stats.ttest_rel(acc_array['smo'], acc_array['bayes'])
  s2 = stats.ttest_rel(acc_array['smo'], acc_array['tree'])
  s3 = stats.ttest_rel(acc_array['tree'], acc_array['bayes'])
  print(s1)
  print(s2)
  print(s3)

if __name__ == "__main__":
  main()
