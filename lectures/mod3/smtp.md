# SMTP
FPNP3e ch13


[Simple Mail Transfer Protocol (SMTP)](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol)
---
- an Internet standard communication protocol for electronic mail 
  - submission from MUA (mail user agent such as ThunderBird) to MSA (mail submission agent such as Postfix)
  - relay from one mail server to another
- TCP port numbers
  - 25 for plaintext
  - 587 or 465 (historically temporary) for encrypted communications per [RFC8314](https://datatracker.ietf.org/doc/html/rfc8314)


Writing and submitting emails using Command Line  
---
- command-line email programs:
  - mutt, pine, elm, mailx, mail
  - submit emails through background daemons such as 
    - [sendmail](https://en.wikipedia.org/wiki/Sendmail)
    - qmail, postfix, exim with their own implementation of sendmail
    - maintain an outgoing queue
  - read emails from a user file of mailbox with two popular formats:
    - [Maildir](https://en.wikipedia.org/wiki/Maildir)
      - each message is stored in a separate file with a unique name
      - A Maildir directory (often named Maildir) usually has three subdirectories named tmp, new, and cur
        - each mail folder is a file system directory
    - [mbox](https://en.wikipedia.org/wiki/Mbox)
      - All messages in an mbox mailbox are concatenated and stored as plain text in a single file
      - defined in [RFC4155](https://datatracker.ietf.org/doc/html/rfc4155)
- this is the first generation of email system
  - email client and server are on the same machine


🔭 Explore
---
- [The Mutt E-Mail Client](http://www.mutt.org/)


The Rise of email Clients
---
- In the second generation of email system, the client and server are deployed separately
  - the clients are installed on user's computer
    - popular clients: ThunderBird, Outlook
  - the services are installed on servers
- the clients download emails from servers through
  - Post Office Protocol (POP)
    - the read email is deleted from the server by default
    - the default mode is usually turned of to leave the email on the server
  - Internet Message Access Protocol (IMAP)
    - leaves emails on the server
    - emails can be arranged in folders on the server
- the clients submit emails to servers for queuing and delivery through
  - Simple Mail Transfer Protocol (SMTP)
- the user is authenticated by username and password to access these services


Steps in using email clients
---
1. Install the e-mail client like Thunderbird or Outlook
2. Configure the IMAP server hostname and port number for incoming emails
3. Configure the SMTP server hostname and port number for outgoing emails
4. Assign a username and password as authenticate to both services


The differences between SMTP submission and relay
---
- SMTP submission submit emails from clients to servers
  - most ISPs block outgoing TCP connections to port 25 from clients so that these they cannot be used as e-mail servers
  - redirected to port 587 for security
  - authenticated SMTP by user's username and password prevents spammers
- SMTP relay transfer emails between servers
  - changes SMTP envelope recipient repeatedly if needed on each hop
  - encourage email servers to add new headers to keep track of the message
    - these headers are called Received headers
      - valuable for debugging delivery problems
      - each server adds its Received header to the top of the message header
        - so the oldest Received header is listed last
    - spam emails are usually decorated with *fictitious* Received headers
  - a Delivered-to header is written by the destination server


🔭 Explore
---
- Investigate the headers of a real email


The Move to Webmail
---
- browser is used as the window for reading and writing emails on email server
- popular webmail service providers
  - Gmail, Outlook (formerly Hotmail)
  - email submission and retrieving are all through web API
    - obliviates SMTP for submission
    - obliviates IMAP/POP3 for retrieval
- client protocols are removed from the scenario
- pure server-to-server unauthenticated SMTP delivers email between large organizations


🔭 Explore
---
- [SquirrelMail: a standards-based webmail package written in PHP](https://squirrelmail.org/)



🔭 Explore
---
- Sending E-Mail in Python script
  - sends email to a SMTP listener
  - uses *sendmail*
- [How do I send mail from a Python script?](https://docs.python.org/3/faq/library.html#how-do-i-send-mail-from-a-python-script)


Headers and the Envelope Recipient
---
- email headers are separate from the “envelope sender” and “envelope recipient”
- email client edits email message’s headers before sending it
  - removing and adding headers
- An e-mail can pass across SMTP toward a destination address that is not mentioned anywhere in the e-mail headers or text itself
  - such as an email address subscribed [emailing list](https://en.wikipedia.org/wiki/Mailing_list)



🖊️ Practice 
---
- [interact with SMTP in commands](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol)
  - SMTP transport example
- [Sending E-mail with smtplib.sendmail()](./smtp/simple.py)
  ```bash
  # don't use any real smtp server to avoid getting your IP address blocked
  python3 simple.py localhost seed@localhost trump@localhost
  ```
- further reference [[PSL SMTP Library smtplib](https://docs.python.org/3/library/smtplib.html)](https://docs.python.org/3/library/smtplib.html)



Programming with smtplib: Error Handling and Conversation Debugging
---
- popular exceptions
  - socket.gaierror for errors looking up address information
  - socket.error for general network and communication problems
  - socket.herror for other addressing errors
  - smtplib.SMTPException or a subclass of it for SMTP conversation problems
- enable detailed debug messages
  ```python
  # enable tracking down any problems
  connection.set_debuglevel(1)
  ```

🖊️ Practice
---
- [A More Cautious SMTP Client](./smtp/debug.py) with 
  - basic error handling and debugging
  - smtp commands and responses
    - for a response, the code 250 matters, the message is auxiliary
    - further references
      - [RFC 2821: Simple Mail Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc2821)
  ```bash
  # don't use any real smtp server to avoid getting your IP address blocked
  python3 debug.py localhost seed@localhost biden@localhost
  ```
- pay attention to the envelope sender and receiver
  - which are separate from the To and From header


Getting Information from EHLO
---
- EHLO command is an “extended” successor to HELO
  - old clients speaking original SMTP greet server with HELO
  - recent clients speaking ESMTP (SMTP with extensions) greet server with EHLO
    - an ESMTP-aware server reply with extended information such as
      - the maximum message size
      - any supported optional SMTP features
    - an error is returned from servers without ESMTP
- further references 
  - [RFC 1869: SMTP Service Extensions](https://datatracker.ietf.org/doc/html/rfc1869)
  - [RFC 5336: SMTP Extension for Internationalized Email Addresses](https://datatracker.ietf.org/doc/html/rfc5336)


🖊️ Practice
---
- [Checking Message Size Restrictions](./smtp/ehlo.py)
  ```bash
  # don't use any real smtp server to avoid getting your IP address blocked
  python3 ehlo.py localhost seed@localhost biden@localhost
  ```


How to secure email and its transmission?
---
- two popular ways to protect emails
  - encrypt the email with receiver's public key
    - such as [Mailvelope](https://mailvelope.com/)
  - secure SMTP conversations with SSL/TLS
    - need SSL/TLS along the way from sender to receiver
    - many hops are out of user's control


🖊️ Practice
---
- [Dovecot SSL configuration](https://doc.dovecot.org/configuration_manual/dovecot_ssl_configuration/)



Steps of applying TLS in SMTP
---
1. Create an normal SMTP object
2. Send the EHLO command. If the remote server does not support EHLO, then it will not support TLS.
3. Check s.has_extn() to see if starttls is present. If not, then the remote server does not support TLS and the message can only be sent in plaintext.
4. Build an SSL context object to verify the server’s identity.
5. Call starttls() to initiate the encrypted channel.
6. Call ehlo() a second time; this time, it’s encrypted.
7. Finally, send the message.


🖊️ Practice
---
- [Using TLS Opportunistically](./smtp/tls.py)
  - use TLS if available but will fall back on unsecured transmission otherwise
  ```bash
  # don't use any real smtp server to avoid getting your IP address blocked
  python3 tls.py localhost seed@localhost biden@localhost
  ```


Authenticated SMTP
---
- authenticate user with username and password
  - smtplib provides a login() function that takes a username and a password
- TLS connection must be established first to avoid credential sniffing
- Most outgoing e-mail servers on the Internet do not support authentication



🖊️ Practice
---
- [Configure Dovecot Authentication](https://doc.dovecot.org/configuration_manual/authentication/)



🖊️ Practice
---
- [Authenticating over SMTP](./smtp/login.py)
  - warning: does not use TLS


SMTP Tips
---
- There is no way to guarantee that a message was delivered
- The *sendmail()* function raises an exception if any of the recipients failed
- SSL/TLS is insecure without certificate validation
- Python’s smtplib is not meant to be a general-purpose e-mail relay


# References
- [The Spamhaus Project tracks email spammers and spam-related activity](https://www.spamhaus.org/)