import argparse
import os
import sys
import time
import itertools
import pyzipper
import rarfile
from tqdm import tqdm
from multiprocessing import Pool, Manager

#command if you want to use wordlist:
#python BruteForce.py -f target.zip -w wordlist.txt -t 4
#-f (name file you want to crack)
#-w (wordlist that contains password)
#-t (thread you want use, default 2)
#
#Command if you want to use brute-force:
#python BruteForce.py -f target.zip -b --min 1 --max 4 -t 4
#--b (Use brute-force mode (a-zA-Z0-9)
#--min (length password minimum)
#--max (length password maksimum)

def try_password_zip(args):
    zip_file, password, stop_flag = args
    if stop_flag.value:
        return None
    try:
        with pyzipper.AESZipFile(zip_file) as zf:
            zf.extractall(pwd=password.encode('utf-8'))
        stop_flag.value = True
        return password
    except:
        return None

def try_password_rar(args):
    rar_file, password, stop_flag = args
    if stop_flag.value:
        return None
    try:
        with rarfile.RarFile(rar_file) as rf:
            rf.extractall(pwd=password)
        stop_flag.value = True
        return password
    except:
        return None

def generate_combinations(min_len, max_len):
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for length in range(min_len, max_len + 1):
        for combo in itertools.product(charset, repeat=length):
            yield ''.join(combo)

def brute_force_generator(file_path, password_iter, max_workers, is_zip=True):
    start_time = time.time()
    task = try_password_zip if is_zip else try_password_rar
    manager = Manager()
    stop_flag = manager.Value('b', False)

    found_password = None
    total = 0
    with Pool(max_workers) as pool:
        with tqdm(desc="Brute Force Progress", unit="pass", ncols=80) as pbar:
            args_gen = ((file_path, pwd, stop_flag) for pwd in password_iter)
            for result in pool.imap_unordered(task, args_gen, chunksize=100):
                pbar.update(1)
                total += 1
                if result:
                    found_password = result
                    pool.terminate()
                    pool.join()
                    break

    elapsed = time.time() - start_time
    if found_password:
        print("\n" + "=" * 50)
        print(f"{'ZIP' if is_zip else 'RAR'}: Password found : {found_password}")
        print(f"Attempts        : {total}")
        print(f"Execution time  : {elapsed:.2f} seconds")
        print("=" * 50)
    else:
        print(f"\n[✗] {'ZIP' if is_zip else 'RAR'}: Password not found.")
    return found_password is not None

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Brute Force ZIP/RAR (Memory Efficient + Multithreaded)")
        parser.add_argument("-f", "--file", required=True, help="Target archive file (.zip/.rar)")
        parser.add_argument("-t", "--threads", type=int, default=2, help="Number of worker threads (default: 2)")

        mode = parser.add_mutually_exclusive_group(required=True)
        mode.add_argument("-w", "--wordlist", help="Wordlist file")
        mode.add_argument("-b", "--brute", action="store_true", help="Use brute-force mode (a-zA-Z0-9)")

        parser.add_argument("--min", type=int, help="Minimum password length (for brute-force)")
        parser.add_argument("--max", type=int, help="Maximum password length (for brute-force)")

        args = parser.parse_args()

        if not os.path.isfile(args.file):
            print(f"[!] File not found: {args.file}")
            sys.exit(1)

        is_zip = args.file.lower().endswith(".zip")
        is_rar = args.file.lower().endswith(".rar")
        if not (is_zip or is_rar):
            print("[!] Unsupported file format. Use .zip or .rar")
            sys.exit(1)

        max_workers = max(1, args.threads)

        if args.wordlist:
            if not os.path.isfile(args.wordlist):
                print(f"[!] Wordlist not found: {args.wordlist}")
                sys.exit(1)
            with open(args.wordlist, "r", encoding="utf-8", errors="ignore") as f:
                passwords = (line.strip() for line in f if line.strip())
            brute_force_generator(args.file, passwords, max_workers, is_zip=is_zip)

        elif args.brute:
            if args.min is None or args.max is None:
                print("[!] For brute-force mode, please use --min and --max")
                sys.exit(1)
            if args.min > args.max or args.min < 1:
                print("[!] Invalid brute-force length range")
                sys.exit(1)
            print(f"[*] Brute-forcing with password lengths from {args.min} to {args.max}")
            pw_gen = generate_combinations(args.min, args.max)
            brute_force_generator(args.file, pw_gen, max_workers, is_zip=is_zip)

    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user.")
        sys.exit(0)
