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
- runs atop tcp with default port number 22
- defined in a series of [rfcs](https://www.openssh.com/specs.html)
- Python library [Paramiko](https://www.paramiko.org/) implements both client and server functionality according to SSHv2 protocol
  - Exceptions: socket.error, socket.gaierror, paramiko.SSHException


- An Overview of SSH  
- SSH Host Keys  
- SSH Authentication  
- Shell Sessions and Individual Commands  
- SFTP: File Transfer Over SSH  
- Other Features  