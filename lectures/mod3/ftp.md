#  FTP
FPNP3e ch17


Overview of [File Transfer Protocol (FTP)](https://en.wikipedia.org/wiki/File_Transfer_Protocol) 
---
- runs atop two tcp connections
  - port 21 for control
    - carries commands, acknowledgments, or error codes
  - port 20 for data
    - carries file data, blocks of information such as directory
    - two working modes
      - active mode in the early days
      - passive mode as default today
listings
- used for file download, upload, synchronization and full fs access
- insecure due to plaintext transfer of username, password and file
- alternatives to ftp
  - http for file download and upload
  - *rsync, rdist* for file synchronization
  - sftp for full fs access



Using FTP in Python [ftplib — FTP protocol client](https://docs.python.org/3/library/ftplib.html)
---
- handles the details of establishing connections 
- provides convenient ways to automate common commands
- [urllib2](https://docs.python.org/2/library/urllib2.html) can be used for simple ftp file download
- exceptions: socket.error, IOError, ftplib.all_errors


🖊️ Practice
---
- [Install vsftpd on Parrot Linux](https://ubuntu.com/server/docs/service-ftp)
  ```bash
  sudo apt install vsftpd
  ```
- [Making a Simple FTP Connection](./ftp/connect.py)
  - try [Ram's list of FTP sites](http://robotics.stanford.edu/people/ramkumar/ftp.html)



ASCII and Binary modes
---
- in binary mode
  - files are treated as a monolithic block of binary data
- in ASCII mode
  - one line is delivered a time from the file
  - without line endings


🖊️ Practice
---
- [Downloading an ASCII File](./ftp/asciidl.py)
- [Downloading a Binary File](./ftp/binarydl.py)
- [Binary Download with Status Updates](./ftp/advbinarydl.py)
- [Binary Upload](./ftp/binaryul.py)
  ```bash
  python3 binaryul.py localhost seed binaryul.py /tmp
  ```
- two ways to discover information about server files and directories
  - nlst() method returns a list of bare names only of entries in a given directory
    - similar to *ls*
    - [Getting a Bare Directory Listing](./ftp/nlst.py)
  - dir() method returns a directory listing in a system-defined format
    - similar to *ls -la* or *ls -l*
    - [Getting a Fancy Directory Listing](./ftp/dir.py)
- [Trying to Recurse into Directories](./ftp/recursedl.py)


Creating and deleting files and directories
---
- *delete(filename)* deletes a file from the server
- *mkd(dirname)* creates a new directory
- *rmd(dirname)* deletes an empty directory
- *rename(oldname, newname)* works as Unix command *mv*


Secure FTP using TLS
---
- configure [vsftpd using TLS](https://www.rosehosting.com/blog/install-vsftpd-with-ssl-tls-on-ubuntu-20-04/)
- use [FTP_TLS class](https://docs.python.org/3/library/ftplib.html) to protect the command channel in TLS
- FTP_TLS.prot_p() is called to protect the data channel
- FTP_TLS.prot_c() turns the protected data channel to plain