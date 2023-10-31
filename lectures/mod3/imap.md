# IMAP
FPNP3e ch15


[Internet Message Access Protocol (IMAP)](https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol)
---
- an Internet standard protocol used by email clients to retrieve email messages from a mail server over a TCP/IP connection
- An IMAP server typically listens on port number 143
  - IMAP over SSL/TLS (IMAPS) is assigned the port number 993
- popular IMAP clients: ThunderBird, Outlook
- defined in [RFC 9051: Internet Message Access Protocol (IMAP) - Version 4rev2](https://datatracker.ietf.org/doc/html/rfc9051)


Advantages of IMAP over POP
---
- supports operations below on an IMAP server 
  - sorts mails into several folders (mailboxes)
    - folders can be shared with other users or marked read-only
  - flags messages as "read", "replied", "seen", "deleted", "archived", etc.
  - searches text strings from messages
  - maintains persistent unique message numbers for synchronization between local message store and remote server
    - A locally stored message can be uploaded directly to one of the remote folders
  - Some IMAP servers can present nonmail sources, like Usenet newsgroups, as though they were e-mail folders
  - An IMAP client can selectively download only one part of a message such as an attachment or the message header


IMAP in Python
---
- supports by synchronous Python libraries
  - [imaplib — IMAP4 protocol client](https://docs.python.org/3/library/imaplib.html)
  - [IMAPClient — an easy-to-use, Pythonic and complete IMAP client library](https://imapclient.readthedocs.io/)
  - Exceptions:
    - socket.error, socket.gaierror, IMAP4.error, IMAP4.abort, IMAP4.readonly
- for asynchronous support, refer to [Twisted mail](https://docs.twisted.org/)
- to implement a full-featured IMAP client, refer to
  - [Best Practices for Implementing an IMAP Client](https://www.imapwiki.org/ClientImplementation)


🖊️ Practice
---
- the PSL *imaplib* offers basic IMAP access
  - sends requests by wrapping IMAP commands
  - receives raw IMAP responses without further parsing
- [Connecting to IMAP and Listing Folders](./imap/open_imaplib.py)
  ```python
  python3 open_imaplib.py localhost seed
  ```

[IMAPClient]((https://imapclient.readthedocs.io/))
---
- implements several details of the IMAP protocol on [imaplib]((https://docs.python.org/3/library/imaplib.html))



Examining message folders  
---
- Like filesystem, messages are files organized in folders
- actions such as download, search, or modify are taken on the messages in the current or selected folder
- IMAP protocol is stateful so it remembers the pwd in one connection
  - reconnection starts freshly in the root folder


Message Numbers vs. UIDs
---
- A specific message within a folder can be identified by one of two different ways
  - a temporary message number assigned during each session
  - a unique identifier (UID) persists through sessions
    - used in synchronization between local and remote
    - if the folder is renamed or deleted from one client, the remote uid will conflict with local uid on other clients
    - check *UIDVALIDITY* in new session to assure uid consistence with previous session
  - use temporary message number only by setting *use_uid=False*
- message numbers can be specified in ranges such as
  - 2,4:6,20:* means message 2, 4 to 6, and 20 to the end
  - efficient for processing by commands that support multiple messages


Summary Information
---
- IMAP server provides some summary information about selected folder
  - the folder itself and its messages
- The summary returned by IMAPClient is a dictionary
- the keys that most IMAP servers will return when you run *select_folder()*
  - servers are only required to return FLAGS, EXISTS, and RECENT
    - most will also include UIDVALIDITY

| key | description |
| --- | --- |
| EXISTS | An integer giving the number of messages in the folder |
| FLAGS  | A list of the flags that can be set on messages in this folder  |
| RECENT  |  Specifies the server’s estimate of the number of messages that have appeared in the folder since the last time an IMAP client ran select_folder() on it  |
| UIDVALIDITY  | A string that can be used by clients to verify that the UID numbering has not changed  |
| PERMANENTFLAGS  | Specifies the list of custom flags that can be set on messages; this is usually empty  |
| UIDNEXT  | The server’s guess about the UID that will be assigned to the next incoming (or uploaded) message  |
| UNSEEN  | Specifies the message number of the first unseen message (the one without the \Seen flag) in the folder  |


🖊️ Practice
---
- [Displaying Folder Summary Information](./imap/folder_info.py)
  ```python
  python3 folder_info.py localhost seed Inbox
  ```


🖊️ Download an Entire Mailbox
---
- IMAPClient downloads mail using its *fetch() method* wrapping IMAP FETCH command
- all messages in a folder can be downloaded at once or individually
- [Downloading All Messages in a Folder](./imap/folder_summary.py)
  ```python
  python3 folder_summary.py localhost seed Inbox
  ```


Downloading Messages Individually
---
- IMAP supports operations download part of a message such as
  - email headers
  - particular headers
  - the outline of the MIME structure of a message
  - the text of particular sections of a message


🖊️ Practice
---
- [A Simple IMAP Client](./imap/simple_client.py)
  - *list_folders()* presents a list of e-mail folders and their flags
  - * fetch()* can be used to 
    - build message summaries
    - explore a MIME message’s parts with the BODYSTRUCTURE of the message
    - return a slice of a part such as 
      - BODY[]\<0.100\>, the first 100 bytes of the message body
  - Simple MIME parts are returned as a tuple consists of
    - MIME type and subtype
    - body parameters in a tuple of pairs of name and value
    - Content ID, description, encoding and size in bytes
    - the content length in lines for textual MIME types
  - Multipart returns a tuple with embedded tuples
    - Common multipart subtype includes: mixed, alternative, digest and parallel
- further reference [RFC 9051: Internet Message Access Protocol (IMAP) - Version 4rev2](https://datatracker.ietf.org/doc/html/rfc9051)


Message flags
---
- are attributes of messages, in the form of a backslash-prefixed word
  - \Seen: the message has been read
  - \Answered: the message has been replied
  - \Draft: the message is under composing
  - \Flagged: the message is singled out
  - \Recent: this flag is added by the server and removed automatically after the mailbox is selected
  ```python
  # query flags
  c.get_flags(2703) # c is an IMAPClient
  # remove and add flags
  c.remove_flags(2703, ['\\Seen'])
  c.add_flags(2703, ['\\Answered'])
  # set flags
  c.set_flags(2703, ['\\Seen', '\\Answered'])
  ```
- can be used to mark deletion on messages
  ```python
  # mark for deletion
  c.delete_messages([2703,2704])
  # commit the pending deletion
  c.expunge()
  ```


Searching
---
- search messages on the server by the *search(criteria)* method of an IMAPclient instance, the UIDs of the messages that match the criteria are returned
- e.g.
  ```python
  c.select_folder('INBOX')
  c.search('SINCE 31-Oct-2023 TEXT Halloween')
  # match all
  # 'SINCE 31-Oct-2023 TEXT Halloween' ≡ AND (SINCE 31-Oct-2023) (TEXT Halloween)
  # match at least one
  # OR (SINCE 31-Oct-2023) (TEXT Halloween)
  ```
- popular criteria
  - binary attributes
    - ALL: Every message in the mailbox
    - UID (id, ...): Messages with the given UIDs
    - LARGER n: Messages more than n octets in length
    - SMALLER m: Messages less than m octets in length
    - ANSWERED: Have the flag \Answered
    - DELETED: Have the flag \Deleted
    - DRAFT: Have the flag \Draft
    - FLAGGED: Have the flag \Flagged
    - KEYWORD flag: Have the given keyword flag set
    - NEW: Have the flag \Recent
    - OLD: Lack the flag \Recent
    - UNANSWERED: Lack the flag \Answered
    - UNDELETED: Lack the flag \Deleted
    - UNDRAFT: Lack the flag \Draft
    - UNFLAGGED: Lack the flag \Flagged
    - UNKEYWORD flag: Lack the given keyword flag
    - UNSEEN: Lack the flag \Seen
  - search for a given string in headers
    - BCC string
    - CC string
    - FROM string
    - HEADER name string
    - SUBJECT string
    - TO string
  - search for a given string in message
    - BODY string: The message body must contain the string.
    - TEXT string: The entire message, either body or header, must contain the string somewhere.
  - date related: the first three are *arrival dates*, the last three are *send dates*
    - BEFORE 01-Jan-1970
    - ON 01-Jan-1970
    - SINCE 01-Jan-1970
    - SENTBEFORE 01-Jan-1970
    - SENTON 01-Jan-1970
    - SENTSINCE 01-Jan-1970

```python
# using raw string to simplify escaping
c.search(r'TEXT "Quoth the raven, \"Nevermore.\""')
```


Manipulating Folders and Messages
---
```python
# Some IMAP servers or configurations may not permit these operations, 
# or they may have restrictions on naming
c.create_folder('Personal')
c.delete_folder('Work')

# two ways to create new e-mail messages
# 1. select then copy
c.select_folder('INBOX')
c.copy([2653L, 2654L], 'TODO')

# 2. add a message to a mailbox with IMAP
# pay attention to the line endings
# \n on Unix, \r\n on Windows, \r on older Macs

# splitlines() supports the three line endings above
'one\rtwo\nthree\r\nfour'.splitlines()

# join with the appropriate line endings
'\r\n'.join('one\rtwo\nthree\r\nfour'.splitlines())

# add the message to a mailbox (or folder)
c.append('INBOX', my_message) # flags and msg_time can be set as well
```

