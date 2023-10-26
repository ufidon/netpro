#  Building and Parsing E-Mail 
FPNP3e ch12


A big picture
---
- [Electronic mail (email or e-mail)](https://en.wikipedia.org/wiki/Email) is a method of transmitting and receiving messages using electronic devices
- The lifespan of an email
  - A sender $S$ submit an email $e$ by the *Simple Mail Transport Protocol (SMTP:25)* to an email server $S_s$
    - SMTP Secure (SMTPS) uses port number 587
      - Port 465 is also used sometimes but outdated
  - $e$ is delivered from $S_s$ through a serials of intermediary email servers $S_{m_i}$ to the receiver $R$'s email server $S_r$
  - $R$ accesses $e$ from $S_r$ through the *Post Office Protocol v3 (POP3:110)* or the *Internet Message Access Protocol (IMAP:143)* using email clients such as
    - Mozilla Thunderbird, Microsoft Outlook
    - webmail services are prevalent today which let users
      - log on the email server with a web browser 
      - view their emails rendered as HTML 
      - the e-mails remain on the email server
    - the secured versions of POP3 and IMAP are *POP3S:995* and *IMAPS:993* respectively


💡 Explore
---
- [The lifespan of an email](https://en.wikipedia.org/wiki/Email)


🔭 Explore Email servers
---
- [DOVECOT: The Secure IMAP server](https://www.dovecot.org/)
  - [Install and configure Dovecot](https://ubuntu.com/server/docs/mail-dovecot)
  - [Postfix: a mail transfer agent (MTA) ](https://www.postfix.org/)
  - [Exim Internet Mailer](https://www.exim.org/)
- [Mailu: a simple yet full-featured mail server](https://mailu.io/)
- [DMS: docker-mailserver](https://docker-mailserver.github.io/docker-mailserver/latest/)
- [James: Java Apache Mail Enterprise Server](https://james.apache.org/)



🖊️ Practice
---
- Install local email systems *option 1*
  - [Dovecot](https://help.ubuntu.com/community/Dovecot)
  - [Postfix](https://ubuntu.com/server/docs/mail-postfix)
    - [How to use Sendmail](https://help.dreamhost.com/hc/en-us/articles/216687518-How-to-use-Sendmail)

```bash
# 1. install dovecot
sudo apt install dovecot-imapd dovecot-pop3d
# test installation
sudo systemctl status dovecot
ss -l lpt # lnpt
telnet localhost smtp
telnet localhost pop3
telnet localhost imap2
openssl s_client -connect localhost:993 # imaps
openssl s_client -connect localhost:995 # pop3s
openssl s_client -connect localhost:587 # smtps

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
- Install local email systems *option 2*
  - [Setting up James as an IMAP server](https://james.apache.org/howTo/imap-server.html)


E-Mail
---
- represented as plain ASCII text 
  - using character codes 1 through 127
  - other standards are supplemented to support Unicode characters and binary payloads
- the end-of-line marker is CRLF (carriage-return linefeed, \r\n, ASCII: 13,10 )
- consists of 
  - headers
    - each header consists of a case-insensitive name, a colon, and a value
      - can stretch to several lines indented with whitespace except the first line 
  - a blank line 
  - the body
- E-Mail Message Format is defined in standard [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322)


💡 Demo
---
- Go through the components of an email
  - especially the list of headers
- many of the headers were added by clients and servers along the email transmission
  - each client and server in route reserves the right to add additional headers


🔭 Explore
---
- Popular [email headers](https://en.wikipedia.org/wiki/Email#Message_header)


Building an E-Mail Message
---
- using the [email](https://docs.python.org/3/library/email.html) package
  - [examples](https://docs.python.org/3/library/email.examples.html)


Adding HTML and Multimedia 
Adding Content 
Parsing E-Mail Messages 
Walking MIME Parts 
Header Encodings 
Parsing Dates 

# References
- [Install mail servers](https://www.server-world.info/en/note?os=Ubuntu_22.04&p=mail&f=1)
- [The Mutt E-Mail Client](http://www.mutt.org/)