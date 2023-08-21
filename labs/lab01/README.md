## Setup the lab environment

__Description__

Setup the lab environment and get familiar with the **SEED VM 2.0**. You need a USB 3.0+ thumb drive or USB 3.0+ SSD with at least 256GB or install on your own laptop with free space of at least 256GB.

* *Rule of thumb to choose software: always choose the latest and STABLE version*
* Download and install [VirtualBox](https://www.virtualbox.org/)
* Download the [SEED VM](https://seedsecuritylabs.org/) form its official website
* Choose an installation approach and follow the corresponding [SEED manuals](https://seedsecuritylabs.org/labsetup.html) to install a SEED environment.
* Here we choose [Installing SEED VM](https://github.com/seed-labs/seed-labs/blob/master/manuals/vm/seedvm-manual.md) on a local computer.
* Browse and play with the integrated software
* Practice the basic Linux commands on the [Linux command memento](https://bootlin.com/doc/legacy/command-line/)
* *If SEED VMs can NOT adjust to full screen automatically, it can be changed manually inside the VM. System Settings -> Display -> Resolution (change it what you want.)*
* Update SEED VM
    ```bash
    sudo apt update
    sudo apt upgrade
    ```
* Download and install [Visual Studio Code](https://code.visualstudio.com/download)
* Run vs code, install Python extension

	
__Report__

Write a report about:

* (20%)the process you setup the SEED VM (VM summary is sufficient)
* (50%)the process you test the NAT network
* (30%)the process you setup and test vs code and the Python extension

__Demo video__
* [How to setup SEED 2.0 lab environment?](https://youtu.be/ejydR40c_Gw)
* [How to setup SEED 1.0 lab environment?](https://youtu.be/pc5QJPiFbNQ)


__Extra credits: Install Parrot Security Linux__
* (2%) Go to its official website [Parrot Security Linux](https://www.parrotsec.org/download/), download its 64-bit Virtual machine in VirtualBox format - virtualbox (amd64).
* (2%) Import this VM into VirtualBox. For further information, refer to [its official document](https://www.parrotsec.org/docs/).
```bash
default username: parrot
default password: parrot
```
* (2%) Put SEED VM and Parrot Security Linux in the same NAT network, create a NAT network in VirtualBox if you don't have one
* (4%)Make sure SEED VM and Parrot Security Linux can ping each other

__References__
* [VirtualBox](https://www.virtualbox.org/)
* [SEED security labs](https://seedsecuritylabs.org/)
* [Hands on security](https://www.handsonsecurity.net/)
* [bootlin](https://bootlin.com)