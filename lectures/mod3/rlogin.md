#  Telnet and SSH
FPNP3e ch16


🔭 Explore
---
- [telnet: teletype network](https://en.wikipedia.org/wiki/Telnet)
- [SSH: Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell)
- command line automation in Python
  - [Fabric](https://www.fabfile.org/)
    - executes shell commands remotely over SSH 
    - yields useful Python objects in return
  - [Ansible](https://www.ansible.com/)
    - [doc](https://docs.ansible.com/ansible/latest/index.html)
  - [Salt](https://saltproject.io/)
  - [Pexpect](https://pexpect.readthedocs.io/)
    - a pure Python module for spawning child applications
    - controlling them; and responding to expected patterns in their output


Command-Line Expansion and Quoting
---
```bash
# special characters have special meaning to the shell
echo * # list all files and subfolders in the current folder

# using special characters literally needs escape
echo a star \*

# command substitution and arithmetic operations
# find the average number of words per line of afile
echo $(( $(wc -w < afile) / $(wc -l < afile) ))
```

Unix Command Arguments Can Include (Almost) Any Character
---
```python
# no shell, no special characters
import subprocess
cmdwargs = ['echo', 'Sometimes', '*', 'is just an asterisk']
subprocess.call(cmdwargs)

# explain the possible error below
subprocess.call(['echo python'])
# \0 is the null character used to mark the end of a string
subprocess.call(['echo', 'Sentences can end\0 abruptly.'])
```

```bash
# file name with blank space
echo Donald Trump.txt 
echo 'Donald Trump.txt' 
echo "Donald Trump.txt" 
echo Donald\ Trump.txt 
echo Donald*Trump.txt  # * matches zero or any number of any characters
echo Donald?Trump.txt  # ? matches a single character
```


🖊️ Practice
---
- [Shell Supporting Whitespace-Separated Arguments](./rlogin/shell.py)
  - no special characters besides whitespace


Quoting Characters for Protection
---
- the commands sent to a remote machine over remote-shell protocol are likely to be executed by a shell

```python
# invoke a shell to execute commands
import os
os.system('echo *')

# using pipes quote for simplicity
from pipes import quote
print(quote("filename"))
print(quote("file with spaces"))
print(quote("file 'single quoted' inside!"))
print(quote("danger!; rm -r *"))
```

```bash
# remote shell typically involves two levels of shell quoting
echo $HOST
ssh localhost echo $HOST
ssh localhost echo \$HOST
ssh localhost echo \\$HOST
ssh localhost echo \\\$HOST
ssh localhost echo \\\\$HOST

# Windows handle command line similar to Linux but with subtle difference
# they mainly handle the command line as a single string
# with different parsing for different commands
from subprocess import list2cmdline
args = ['rename', 'salary "Smith".xls', 'salary-smith.xls']

# list2cmdline() creates a single string using double quotes and backslashes when necessary
print(list2cmdline(args))
```


Things Are Different in a Terminal 
---
- A terminal consists of a keyboard for input and a screen for output
  - represented as device files /dev/ttySx (x is an integer)
    ```bash
    # check terminals. tty is abbreviated from TeleType
    ll /dev/ttyS*
    # isatty() is used to test whether a device is a terminal
    ```
- most terminals today are terminal emulators such as
  - xterm terminal, MATE terminal, Gnome terminal, PuTTy, etc.
  - terminal emulators attach user's shell to [pseudo-terminals (virtual terminals)](https://en.wikipedia.org/wiki/Pseudoterminal) represented by /dev/ttyx (x is an integer) for interaction
- a shell attached to a terminal presents a prompt
  - otherwise won't such as attaching to a pipe
    - buffers program's output until the output buffer is full or *flush()* is called
    ```bash
    cat | bash
    echo inside bash attached to a pipe, no prompt
    python3 # thinks the input as a file, 
    # only evaluates the program until the end of the file
    print('Python has no prompt either')
    import sys
    print('Is this a terminal?', sys.stdin.istty())
    # CTRL+D to end the input, python will then evaluate its input
    ```
  - terminal's behavior can be set with command *stty*
    - or PSL [termios — POSIX style tty control](https://docs.python.org/3/library/termios.html)
    ```bash
    # 1. disable canonical mode (read a whole line) to read per character
    stty -icanon

    # 2. to support binary stream, turn off pairs of keystrokes such as 
    # Ctrl+S for stop, Ctrl+Q for keep going, etc.
    stty -ixon -ixoff

    # 3. two modes cooked and raw which turn dozens of settings on and off together
    stty raw
    stty cooked

    man stty # for more info
    ```
- Some programs auto-adjust their output format depending on whether they are talking to a terminal
  ```bash
  # talk to a terminal
  ls
  # talk to a pipe
  ls | cat
  ```
- programs running behind telnet think they are talking to a terminal
  - while SSH can be configured to let the program on the remote end thinking its input from a terminal or a file/pipe
    ```bash
    ssh -t localhost # Force pseudo-terminal allocation
    ssh -T localhost # Disable pseudo-terminal allocation
    man ssh # for more info
    ``` 


---

[Telnet (teletype network)](https://en.wikipedia.org/wiki/Telnet)
---
- an ancient insecure protocol for remote shell access
- defined in a series of [rfcs](https://en.wikipedia.org/wiki/Telnet)
- runs atop tcp with default port number 23
  - establishes a channel 
  - then copy information in both directions across the channel
    - Everything you type is sent out across the channel
    - and Telnet prints to the screen everything it receives
- PSL [telnetlib — Telnet client](https://docs.python.org/3/library/telnetlib.html)
  - exceptions: socket.error, socket.gaierror, EOFError, select.error


🖊️ Practice
---
- [Install telnet service on Parrot Linux](https://manpages.ubuntu.com/manpages/lunar/en/man8/in.telnetd.8.html)
  ```bash
  sudo apt install telnetd
  ```
- [Logging Into a Remote Host Using Telnet](./rlogin/telnet_login.py)
  - interact in a receive-and-send pattern
  - [two methods](https://docs.python.org/3/library/telnetlib.html) for waiting for a string to arrive
    - *read_until()* returns all the characters from its start to the expected string
    - *expect()* reads until one from a list of a regular expressions matches
    - Both methods have an optional second argument *timeout*
- [How to Process Telnet Option Codes](./rlogin/telnet_codes.py)

---

[SSH: The Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell)
---
- used for secure remote shell, file transfer, and port forwarding
- descended from
  - rlogin: remote login
  - rsh: remote shell
  - rcp: remote file copy
- runs atop tcp with default port number 22
- supports multiplexing in one SSH socket by its own scheme
  - establishes multiple channels identified by channel IDs
  - amortizes the time for host key negotiation and authentication
- defined in a series of [rfcs](https://www.openssh.com/specs.html)
- The third-party Python library [Paramiko](https://www.paramiko.org/) implements both client and server functionality according to SSHv2 protocol
  - Exceptions: socket.error, socket.gaierror, paramiko.SSHException


The Channels supported by SSH
---
- interactive remote shell session
- individual execution of a single command
- file transfer session letting you browse the remote filesystem
- port forwarding session that intercepts TCP connections


SSH Host Keys
---
- random unsigned public-private key pairs without the burden of PKI
- two ways to [distribute keys](https://www.baeldung.com/linux/ssh-known_hosts-ignore-emporarily)
  - manual distribution: 
    - collect all host public keys 
    - save the collected keys in a ssh_know_hosts file 
    - copy ssh_know_hosts to the folder /etc/ssh/ on every system needed
  - first-time acceptance:
    - let SSH client memorize the remote host keys during the first connection
      - Fatal exception will be raised for subsequent connection with a different key
    - usually these keys are saved in file ~/.ssh/known_hosts


🖊️ Practice
---
- ssh from SEED to Parrot Linux
  - [install OpenSSH Server](https://ubuntu.com/server/docs/service-openssh)
    ```bash
    sudo apt install openssh-server openssh-client
    ```
- [linuxserver/openssh-server](https://hub.docker.com/r/linuxserver/openssh-server)
- connect to Parrot Linux with [*paramiko*]((https://www.paramiko.org/) implements)
  ```python
  import paramiko
  client = paramiko.SSHClient()
  client.connect('ParrotIP', username='parrot') # exception raised

  # 2. behave like normal ssh command
  client.load_system_host_keys()
  client.load_host_keys('/home/seed/.ssh/known_hosts')
  client.connect('ParrotIP', username='parrot')

  # 3. handle unknown hosts by subclassing MissingHostKeyPolicy
  class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
      return

  client.set_missing_host_key_policy(AllowAnythingPolicy())
  client.connect('ParrotIP', username='parrot') 
  ```


🔭 Explore
---
- [Paramiko SSH client & key policies](https://docs.paramiko.org/en/latest/api/client.html)
  - paramiko.RejectPolicy
    - Connecting to hosts with unknown keys simply raises an exception
  - paramiko.AutoAddPolicy
    - Host keys are automatically added to your user host key store when first encountered
    - but any change in the host key from then on will raise a fatal exception
  - paramiko.WarningPolicy
    - An unknown host causes a warning to be logged, but the
connection is allowed to proceed


SSH Authentication
---
- three ways to prove your identity to a remote server
  - $W_1$: provide a pair of username and password
  - $W_2$: public-key authentication provides a username and then let the client perform a public-key challenge-response
  - $W3$: resort to [Single sign-on (SSO)](https://en.wikipedia.org/wiki/Single_sign-on) such as [Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol))
  - no passwords needed for the last two ways


🖊️ Practice
---
- SSH authentication with parakimo
```python
# 1. w1
client.connect('ParrotIP', username='parrot', password='GoodPassword')

# 2. w2
# 2.1 setup the public key
# use ssh-keygen to generate a key pair
# copy ~/.ssh/id_rsa.pub to parrot@ParrotIP with ssh-copy-id
# ssh-copy-id -i ~/.ssh/id_rsa.pub parrot@ParrotIP
# or append the public key to your “authorized hosts” file on the remote end
# typically named as: /home/yourname/.ssh/authorized_keys
# normal access right requirements: chmod 0700 .ssh; chmod 0600 .ssh/*

# 2.2 connect to the remote server
client.connect('ParrotIP')
client.connect('ParrotIP', key_filename='path to your public key file')
```


🖊️ Practice
---
- [Running an Interactive Shell Under SSH](./rlogin/ssh_simple.py)
  - a connected SSH client set up a raw shell session running on the remote end inside a pseudoterminal
- [Running Individual SSH Commands](./rlogin/ssh_commands.py)
  - similar to subprocess but runs remotely
- in either case above, a new *SSH channel* is created behind the scenes to 
  - provide the filelike Python objects that let you talk to 
  - the remote command’s standard input, output, and error streams
- [SSH Channels Run in Parallel](./rlogin/ssh_threads.py)
  - with multithreading


[SSH File Transfer Protocol (SFTP)](https://en.wikipedia.org/wiki/SSH_File_Transfer_Protocol)
---
- supports complete operations on remote file systems
  - with commands *sftp, scp*
  - with [paramiko.SFTPClient](https://docs.paramiko.org/en/latest/api/sftp.html)
- even can mount the remote fs locally with [sshfs](https://en.wikipedia.org/wiki/SSHFS)
- there is no shell expansion on file names passed across SFTP
  - can be done manually with [fnmatch](https://docs.python.org/3/library/fnmatch.html)


🖊️ Practice
---
- [Listing a Directory and Fetching Files with SFTP](./rlogin/sftp_get.py)
  ```bash
  python3 sftp_get.py remoteMachine remoteAccount file1 file2 filen
  ```


Port forwarding and remote X11 sessions
---
- can be exploited by SSHClient's [transport object](https://docs.paramiko.org/en/latest/api/transport.html)
  ```python
  transport = client.get_transport()
  ```

🔭 Explore
---
- [paramiko demos on port forwarding](https://github.com/paramiko/paramiko/tree/main/demos)
- [SSH/OpenSSH/PortForwarding](https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding)