# read log file
cat tmp.log | grep "inserted" | sed -n "s/.*symbol=\(.*\);.*/\1/p" 