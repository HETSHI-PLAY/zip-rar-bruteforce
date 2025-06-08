# zip-rar-bruteforce
Brute Force for ZIP or RAR

this bruteforce can use wordlist or brute (a-z A-Z 0-9)

how to use 

#command if you want to use wordlist:
#python BruteForce.py -f target.zip -w wordlist.txt -t 4
#-f (name file you want to crack)
#-w (wordlist that contains password)
#-t (thread you want use, default 2)

#Command if you want to use brute-force:
#python BruteForce.py -f target.zip -b --min 1 --max 4 -t 4
#--b (Use brute-force mode (a-zA-Z0-9)
#--min (length password minimum)
#--max (length password maksimum)
