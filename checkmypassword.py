import requests
import hashlib
import sys

def get_api_data(char_pass):
    url = 'https://api.pwnedpasswords.com/range/' + char_pass
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error in fetching: {res.status_code}, Check the API')
    return res

def check_password_in_api_data(response,tail):
    result = (hash.split(':') for hash in response.text.splitlines()) # result is a generator object
    for hash,count in result:
        if hash==tail:
            return count
    return 0

def password_pwned(password):
    encrypted_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5char,tail = encrypted_password[:5], encrypted_password[5:]
    response = get_api_data(first5char)
    return check_password_in_api_data(response,tail)

def main(args):
    for password in args:
        count = password_pwned(password)
        if count:
            print(f'{password} had been appeared {count} times in previous databreaches. You should not use this password.')
        else :
            print(f'{password} is good to use.')
    return print('Done!')

if __name__=='__main__':
    main(sys.argv[1:])



