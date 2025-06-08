# ZIP & RAR BruteForce Tool

This is a simple brute-force tool for cracking password-protected `.zip` and `.rar` files using either:
- A wordlist
- Brute-force attack (customizable from a-z, A-Z, 0-9 with min/max length)

# Requirements

Install all required Python packages:

```bash
pip install pyzipper rarfile tqdm
```

if you want this script to support rar, add this:
```bash
sudo apt install unrar
```

how to use 

# command if you want to use wordlist:
```bash
python BruteForce.py -f target.zip -w wordlist.txt -t 4
```
- -f (name file you want to crack)
- -w (wordlist that contains password)
- -t (thread you want use, default 2)

# Command if you want to use brute-force:
```bash
python BruteForce.py -f target.zip -b --min 1 --max 4 -t 4
```
- --b (Use brute-force mode (a-zA-Z0-9)
- --min (length password minimum)
- --max (length password maksimum)
