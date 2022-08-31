import os 
from base64 import b64encode


def main():
    key = os.environ.get('SERVICE_ACCOUNT_KEY')
    with open('path.json', 'w') as f:
        f.write(b64encode(key.decode()))
    print(os.path.realpath('path.json'))

if __name__ == '__main__':
    main()