mkdir -v processed
for file in /u/cs401/tweets/*; do
  f=`basename $file`
  echo $f
  python twtt.py $file processed/$f.twt
done

