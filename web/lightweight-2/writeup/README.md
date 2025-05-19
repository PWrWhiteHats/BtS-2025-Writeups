# lightweight-2

### Enumeration

We are greeted by a simple login page. Trying different special characters reveals that it acts in a different way for these characters: `*`, `(`, `)`.

Parentheses cause a 500 error, and `*` lets us bypass the login - it's what we would expect from LDAP, and definitely not SQL. "Lightweight" could be a hint - LDAP stands for Lightweight Directory Access Protocol.

So by putting `username=*&password=*` we can bypass the auth.

Unlike the last time (`lightweight` chal), we see the user's description and a mention of all sensitive data being removed from LDAP:

```html
User Description: Junior Mid-Senior DevOps Penetration Tester Engineer <!-- SPRT-1337 Removed all sensitive data from LDAP. -->
```

Based on this hint, trying to leak fields from LDAP might not be the right direction. If we leak `description` again, we just get "Junior Mid-Senior DevOps Penetration Tester Engineer".

One thing to notice is that the username field is always reflected on the page after a successful login. We should try some common SSTI payloads.

### SSTI

To test for SSTI we need a username which:
1) Bypasses the auth
2) Contains a test string like `{{7*7}}`

It can be achieved with a negation:

```
username=*)(!(description={{7*7}}*)&password=*
```

We can see that on the page the expression got executed: `49`.

By following the common SSTI tree:

![SSTI decision tree](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2F1116388331-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-Mks5MA8MikNk7jIq3z3%252Fsync%252F6fca302ed2a973de6733000eceadd51725c53972.png%3Fgeneration%3D1633028919960201%26alt%3Dmedia&width=768&dpr=1&quality=100&sign=bf4e206a&sv=2)

(source: [hacktricks.boitatech.com.br](https://hacktricks.boitatech.com.br/pentesting-web/ssti-server-side-template-injection))

..we can determine that it's probably Jinja2.

Let's leak the config:

```
username=*)(!(description={{config}}*)&password=*
```

Among other things, we see (html-entity-encoded):

```
'SECRET_KEY': 'BtSCTF{ld4p_1nj3ction_plus_sst1_3quals_fl4g}'
```
