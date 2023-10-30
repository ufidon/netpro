# POP
FPNP3e ch14


[Post Office Protocol (POP)](https://en.wikipedia.org/wiki/Post_Office_Protocol)
---
- a protocol for retrieving e-mail from a mail server by email clients such as
  - Thunderbird or Outlook
  - POP3, the most common implementation, is used interchangeable with POP
  - defined in [RFC 1393: Post Office Protocol - Version 3](https://datatracker.ietf.org/doc/html/rfc1939)
- main benefit: simplicity
  -  access a remote mailbox on a POP server
  -  gather summary information about a mailbox
  -  download any new email that has appeared 
  -  have the choice of deleting the e-mail after the download
  -  support by PSL [poplib — POP3 protocol client](https://docs.python.org/3/library/poplib.html)
- for further features, IMAP should be used instead of POP
  - support multiple mailboxes on the server
  - provide reliable, persistent message identification
  - perform email synchronization between local and remote


POP Server Compatibility
---
- Standards do not exist for some POP behaviors
  - basic operations will generally work fine 
  - certain behaviors do vary from server to server
- the details are up to the authors of server software
  - some servers will mark all of your messages as read whenever you connect to the server
     - whether you download any of them or not
  - some mark a message as read only when it is downloaded
  - some never mark any messages as read at all


🖊️ Practice
---
- [Interact with a POP server through commands](https://en.wikipedia.org/wiki/Post_Office_Protocol)
  - Session example


Connecting and Authenticating
---
- two most common authentication methods among several
  - basic username-password authentication
  - [APOP](https://datatracker.ietf.org/doc/html/rfc1460) command
    - provides origin authentication and replay protection
    - sends password in ciphertext over the network by a challenge–response scheme
    - used on an ancient POP server that does not support SSL
    - but, emails are in plaintext
- steps
  1. Create a POP3_SSL or just a plain POP3 object with the remote hostname and port 
  2. Call user() and pass_() to send the username and password
  3. the exception poplib.error_proto indicates the login has failed
- POP3_SSL must be chosen over POP3 if possible
  - further reference: [RFC2595: Using TLS with IMAP, POP3 and ACAP](https://datatracker.ietf.org/doc/html/rfc2595)


🖊️ Practice
---
- [A Very Simple POP Session](./pop/popconn.py)
  ```python
  python3 popconn.py localhost seed
  ```
  - some POP servers will nonetheless alter mailbox flags simply because you connected
    - don't run against live mailboxes
- [Attempting APOP and Falling Back](./pop/apopconn.py)
- a successful login can cause some older POP servers locking the mailbox
  - always call *quit()* to end a POP session to avoid lockup




Obtaining Mailbox Information
---
- the two examples above return the number of messages in the mailbox and their total size
  - using *stat()* to issue the POP command STAT
- using *list()* to issue the POP command LIST returns more detailed information about each message
  - there may be gaps between message numbers
  - the number assigned to a particular message may be different on each connection


🖊️ Practice
---
- [Using the POP list() Command](./pop/mailbox.py)
  ```python
  python3 mailbox.py localhost seed
  ```
- using *poplib* to issue atomic commands returns a tuple as the results


Downloading and Deleting Messages
---
- with [three relevant methods]((https://docs.python.org/3/library/poplib.html)) identifying messages using the integer identifiers returned from *list()*
  - *retr(num)* 
    - downloads a single message and returns a tuple containing a result code and the message itself
    - causes most POP servers to set the “seen” flag for the message to “true,”
      - barring you from ever seeing it from POP again
  - *top(num, body_lines)* 
    - returns its result in the same format as retr() without marking the message as “seen.”
    - returns only the headers and the number of lines of the body you ask for in *body_lines*
    - useful for previewing messages
  - *dele(num)*
    - marks the message for deletion from the POP server
      - deleted when when the POP session quits


🖊️ Practice
---
- [A Simple POP E-mail Reader](./pop/download-and-delete.py)
  ```python
  python3 download-and-delete.py localhost seed
  ```


# References
- [Gmail: Use IMAP or POP mail programs](https://support.google.com/a/topic/4456189)
- [Gmail SMTP Settings: Easy Step-by-Step Setup Guide](https://www.gmass.co/blog/gmail-smtp/) 
- [Send email from a printer, scanner, or app](https://support.google.com/a/answer/176600) 