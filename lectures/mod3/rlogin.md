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



Terminals Do Buffering  
---


---

- Telnet 
- SSH: The Secure Shell 
  - An Overview of SSH  
  - SSH Host Keys  
  - SSH Authentication  
  - Shell Sessions and Individual Commands  
  - SFTP: File Transfer Over SSH  
  - Other Features  