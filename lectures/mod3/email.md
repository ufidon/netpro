#  Building and Parsing E-Mail 
FPNP3e ch12


A big picture
---

IMAP-143
IMAPS-993
POP3-110
POP3S-995

🔭 Explore Email servers
---
- [Mailu: a simple yet full-featured mail server](https://mailu.io/)
- [DMS: docker-mailserver](https://docker-mailserver.github.io/docker-mailserver/latest/)
- [James: Java Apache Mail Enterprise Server](https://james.apache.org/)
- [DOVECOT: The Secure IMAP server](https://www.dovecot.org/)
  - [Install and configure Dovecot](https://ubuntu.com/server/docs/mail-dovecot)
  - [Postfix: a mail transfer agent (MTA) ](https://www.postfix.org/)
  - [Exim Internet Mailer](https://www.exim.org/)


🖊️ Practice
---
- Install local email systems
  - [Dovecot](https://help.ubuntu.com/community/Dovecot)
  - [Postfix](https://ubuntu.com/server/docs/mail-postfix)
    - [How to use Sendmail](https://help.dreamhost.com/hc/en-us/articles/216687518-How-to-use-Sendmail)

```bash
# 1. install dovecot
sudo apt install dovecot-imapd dovecot-pop3d
# test installation
sudo systemctl status dovecot
ss -l lpt # lnpt
telnet pop3
telnet imap2
openssl s_client -connect localhost:993 # imaps
openssl s_client -connect localhost:995 # pop3s

# 2. install Postfix
sudo apt install postfix # choose local only

# 3. sendmail
# create a new user
sudo adduser emailuser1

# send an email to the new user
sendmail emailuser1@localhost
Subject: Test email
Hello? How are you?
CTRL+D
```


E-Mail Message Format 
Building an E-Mail Message 
Adding HTML and Multimedia 
Adding Content 
Parsing E-Mail Messages 
Walking MIME Parts 
Header Encodings 
Parsing Dates 

# References
- [Install mail servers](https://www.server-world.info/en/note?os=Ubuntu_22.04&p=mail&f=1)
- [The Mutt E-Mail Client](http://www.mutt.org/)