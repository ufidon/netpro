## Setup the lab environment

## Task 1: Install a Linux environment
You may follow any one of the 6 options below to install an `Ubuntu/Linux environment`.

---

### **1. Install a Dual Boot System on a Windows Machine**

**Objective:** Install Ubuntu alongside an existing Windows installation, enabling dual boot.

**Steps:**

1. **Backup Important Data:** Before proceeding, back up all important files from your Windows machine.

2. **Download Ubuntu ISO:**
   - Go to the [Ubuntu official website](https://ubuntu.com/download) and download the latest Ubuntu ISO.

3. **Create a Bootable USB:**
   - Use a tool like [Rufus](https://rufus.ie/) to create a bootable USB drive with the Ubuntu ISO.

4. **Prepare Windows for Dual Boot:**
   - **Shrink the Windows Partition:** In Windows, use the Disk Management tool to shrink the main partition and create unallocated space for Ubuntu (at least 20 GB).
   - **Disable Fast Startup:** Go to Control Panel > Power Options > Choose what the power buttons do > Change settings that are currently unavailable > Uncheck **Turn on fast startup**.

5. **Boot from USB:**
   - Insert the bootable USB drive, restart the machine, and boot from the USB by selecting it from the boot menu.

6. **Install Ubuntu:**
   - Choose **Install Ubuntu alongside Windows** during the installation process.
   - Allocate the unallocated space to Ubuntu.
   - Complete the installation and restart the machine. You will be presented with a GRUB menu to select between Ubuntu and Windows at boot.

**Verification:**
- Verify that both Windows and Ubuntu boot correctly.

---

### **2. Install a Dual Boot System on a Mac Machine**

**Objective:** Install Ubuntu alongside macOS, enabling dual boot using rEFInd or GRUB.

**Steps:**

1. **Backup Important Data:** Ensure all critical data on the Mac is backed up.

2. **Download Ubuntu ISO:**
   - Download the Ubuntu ISO from the [Ubuntu official website](https://ubuntu.com/download).

3. **Create a Bootable USB:**
   - Use the [Etcher](https://www.balena.io/etcher/) tool to create a bootable USB drive with the Ubuntu ISO.

4. **Prepare macOS for Dual Boot:**
   - **Partition the Drive:** Use Disk Utility to create a new partition for Ubuntu (at least 20 GB).
   - **Disable SIP (if necessary):** Some Macs may require you to disable System Integrity Protection (SIP) to install a non-Mac OS.

5. **Install rEFInd (Optional but Recommended):**
   - Install the [rEFInd boot manager](https://www.rodsbooks.com/refind/) to manage dual boot.

6. **Boot from USB:**
   - Insert the bootable USB drive, restart the machine, and hold the **Option** key to select the USB drive.

7. **Install Ubuntu:**
   - During installation, select **Install Ubuntu alongside macOS**.
   - Use the new partition you created for Ubuntu.
   - Complete the installation and reboot.

**Verification:**
- Ensure you can choose between macOS and Ubuntu during startup using rEFInd or GRUB.

---

### **3. Install a Virtual Machine of Ubuntu on Windows**

**Objective:** Install Ubuntu in a VirtualBox VM on a Windows machine.

**Steps:**

1. **Install VirtualBox:**
   - Download and install [VirtualBox](https://www.virtualbox.org/) on your Windows machine.

2. **Download Ubuntu ISO:**
   - Download the Ubuntu ISO from the [Ubuntu official website](https://ubuntu.com/download).

3. **Create a New Virtual Machine:**
   - Open VirtualBox and click **New**.
   - Name the VM (e.g., `Ubuntu`), set **Type** to Linux, and **Version** to Ubuntu (64-bit).
   - Allocate at least 2 GB of RAM and 20 GB of virtual hard disk space.

4. **Attach the Ubuntu ISO:**
   - In the VM settings, go to **Storage** > **Controller: IDE** > **Empty** > Click the disk icon > **Choose a disk file**.
   - Select the downloaded Ubuntu ISO.

5. **Install Ubuntu:**
   - Start the VM and proceed with the standard Ubuntu installation process.

**Verification:**
- Verify that Ubuntu boots correctly in the VM and that you can interact with the desktop environment.

---

### **4. Install Ubuntu in WSL (Windows Subsystem for Linux)**

**Objective:** Set up Ubuntu in Windows using WSL.

**Steps:**

1. **Enable WSL:**
   - Open PowerShell as Administrator and run:
     ```bash
     dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
     ```
   - Enable WSL 2:
     ```bash
     dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
     ```

2. **Install Ubuntu:**
   - Open the Microsoft Store, search for **Ubuntu**, and click **Get** to install the desired version (e.g., Ubuntu 20.04 LTS).

3. **Set Up Ubuntu:**
   - Launch Ubuntu from the Start menu, set up a new user, and complete the installation.

**Verification:**
- Verify that you can run Ubuntu commands in the WSL terminal.

---

### **5. Install a Virtual Machine of Ubuntu on Mac**

**Objective:** Install Ubuntu in a VirtualBox VM on a Mac machine.

**Steps:**

1. **Install VirtualBox:**
   - Download and install [VirtualBox](https://www.virtualbox.org/) on your Mac.

2. **Download Ubuntu ISO:**
   - Download the Ubuntu ISO from the [Ubuntu official website](https://ubuntu.com/download).

3. **Create a New Virtual Machine:**
   - Open VirtualBox and click **New**.
   - Name the VM (e.g., `Ubuntu`), set **Type** to Linux, and **Version** to Ubuntu (64-bit).
   - Allocate at least 2 GB of RAM and 20 GB of virtual hard disk space.

4. **Attach the Ubuntu ISO:**
   - In the VM settings, go to **Storage** > **Controller: IDE** > **Empty** > Click the disk icon > **Choose a disk file**.
   - Select the downloaded Ubuntu ISO.

5. **Install Ubuntu:**
   - Start the VM and proceed with the standard Ubuntu installation process.

**Verification:**
- Verify that Ubuntu boots correctly in the VM and that you can interact with the desktop environment.

---

### **6. Install Ubuntu on a Physical Machine**

**Objective:** Install Ubuntu as the sole operating system on a physical machine.

**Steps:**

1. **Backup Important Data:** Ensure all critical data on the physical machine is backed up, as the installation will erase all existing data.

2. **Download Ubuntu ISO:**
   - Download the Ubuntu ISO from the [Ubuntu official website](https://ubuntu.com/download).

3. **Create a Bootable USB:**
   - Use a tool like [Rufus](https://rufus.ie/) or [Etcher](https://www.balena.io/etcher/) to create a bootable USB drive with the Ubuntu ISO.

4. **Boot from USB:**
   - Insert the bootable USB drive into the physical machine, restart the machine, and boot from the USB.

5. **Install Ubuntu:**
   - Choose **Erase disk and install Ubuntu** during the installation process.
   - Complete the installation and reboot the machine.

**Verification:**
- Verify that Ubuntu boots correctly and that you can log into the desktop environment.

---

### **Conclusion**

Task 1 covers multiple approaches to installing a Linux environment on different systems and scenarios, providing comprehensive experience with Ubuntu installations. Whether through dual boot, virtual machines, WSL, or direct installation on physical hardware, these tasks will equip you with the necessary skills to work with Linux across various platforms.

---

## Task 2: Install Python development environment (PDE)

After installing Ubuntu, perform the following tasks to set up your Python development environment and verify it with a TCP server/client network program:

### **1: Install Python 3, pip3, IPython, and Jupyter Lab**

**Objective:** Set up a Python development environment on Ubuntu by installing Python 3, pip3, IPython, and Jupyter Lab.

**Steps:**

1. **Update Package List:**
   - Open a terminal and run:
     ```bash
     sudo apt update
     ```

2. **Install Python 3:**
   - Python 3 is typically pre-installed on Ubuntu, but to ensure you have the latest version:
     ```bash
     sudo apt install python3
     ```

3. **Install pip3:**
   - pip3 is the package manager for Python 3. Install it using:
     ```bash
     sudo apt install python3-pip
     ```

4. **Install IPython:**
   - IPython is an enhanced interactive Python shell:
     ```bash
     sudo apt install ipython3
     ```

5. **Install Jupyter Lab:**
   - Jupyter Lab is a web-based interactive development environment for Jupyter notebooks:
     ```bash
     pip3 install jupyterlab
     ```

6. **Verify the Installation:**
   - Check the installed versions:
     ```bash
     python3 --version
     pip3 --version
     ipython3 --version
     jupyter-lab --version
     ```
   - Launch Jupyter Lab:
     ```bash
     jupyter-lab
     ```
   - This will open Jupyter Lab in your web browser.

### **2: Verify the PDE with a TCP Server/Client Network Program with Python Socket Programming**

**Objective:** Develop a simple TCP server and client using Python's `socket` module to understand basic network programming concepts.

**Steps:**

1. **Create the TCP Server:**

   - Create a file named `tcp_server.py`:
     ```python
     import socket

     # Define the host and port
     HOST = '127.0.0.1'  # Localhost
     PORT = 65432        # Port to listen on

     # Create a socket object
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
         s.bind((HOST, PORT))
         s.listen()
         print(f"Server listening on {HOST}:{PORT}")
         conn, addr = s.accept()
         with conn:
             print('Connected by', addr)
             while True:
                 data = conn.recv(1024)
                 if not data:
                     break
                 conn.sendall(data)
     ```

2. **Create the TCP Client:**

   - Create a file named `tcp_client.py`:
     ```python
     import socket

     # Define the server address and port
     HOST = '127.0.0.1'  # The server's hostname or IP address
     PORT = 65432        # The port used by the server

     # Create a socket object
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
         s.connect((HOST, PORT))
         s.sendall(b'Hello, world')
         data = s.recv(1024)

     print('Received', repr(data))
     ```

3. **Run the Server:**

   - In a terminal, run the server script:
     ```bash
     python3 tcp_server.py
     ```
   - The server will start and wait for a connection.

4. **Run the Client:**

   - In another terminal, run the client script:
     ```bash
     python3 tcp_client.py
     ```
   - The client will send a message to the server and receive a response.

5. **Test the Program:**
   - Observe the output in both the server and client terminals. The server should display a connection message, and the client should display the received message.

### **Conclusion**

These tasks will help you set up a Python development environment on Ubuntu and give you hands-on experience with network programming using Python sockets. The TCP server/client program demonstrates how to establish communication between two systems over a network.


## **Task 3: Install Visual Studio Code on Ubuntu**

**Objective:** Install Visual Studio Code (VSCode) on Ubuntu to use as an IDE for developing Python networking programs.


### **Method 1: Install Visual Studio Code on Ubuntu Using a .deb File**


**Steps:**

1. **Download the VSCode `.deb` File:**
   - Open a web browser and go to the [Visual Studio Code official download page](https://code.visualstudio.com/Download).
   - Under the "Linux" section, click on **.deb** to download the latest VSCode `.deb` package.

2. **Install the VSCode `.deb` File:**
   - Open a terminal and navigate to the directory where the `.deb` file was downloaded. For example, if it was downloaded to the `Downloads` folder:
     ```bash
     cd ~/Downloads
     ```
   - Install the `.deb` package using `dpkg`:
     ```bash
     sudo apt install code_*.deb
     # or
     sudo dpkg -i code_*.deb
     ```
   - If there are any missing dependencies, you can fix them by running:
     ```bash
     sudo apt-get install -f
     ```

3. **Launch Visual Studio Code:**
   - Once installed, you can launch VSCode from the terminal or find it in your applications menu:
     ```bash
     code
     ```

4. **Install Python Extension for VSCode:**
   - Open VSCode, and in the **Extensions** view (Ctrl+Shift+X), search for "Python" and install the official Python extension provided by Microsoft.
   - This extension provides features like IntelliSense, linting, debugging, and Jupyter Notebook support.

**Verification:**
- Verify that VSCode launches successfully and that the Python extension is installed and configured.
- Open the simple Python socket program created in **Task 2**, run it in the terminal, and ensure that the integrated terminal in VSCode works properly.


### Optional method 2

**Steps:**

1. **Update Package List:**
   - Open a terminal and run:
     ```bash
     sudo apt update
     ```

2. **Install Required Dependencies:**
   - Install dependencies required by VSCode:
     ```bash
     sudo apt install software-properties-common apt-transport-https wget
     ```

3. **Add Microsoft GPG Key and VSCode Repository:**
   - Import the Microsoft GPG key:
     ```bash
     wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
     ```
   - Add the VSCode repository:
     ```bash
     sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
     ```

4. **Install Visual Studio Code:**
   - After adding the repository, install VSCode:
     ```bash
     sudo apt update
     sudo apt install code
     ```

### **Conclusion**

With VSCode installed and configured, you now have a powerful IDE to develop Python networking programs on your Ubuntu machine. This setup provides an enhanced development experience with features like debugging, IntelliSense, and integrated terminal access.


__References__
* [VirtualBox](https://www.virtualbox.org/)
* [SEED security labs](https://seedsecuritylabs.org/)
  * [How to setup SEED 2.0 lab environment?](https://youtu.be/ejydR40c_Gw)
  * [How to setup SEED 1.0 lab environment?](https://youtu.be/pc5QJPiFbNQ)
* [Hands on security](https://www.handsonsecurity.net/)
* [bootlin](https://bootlin.com)
* *For Mac computers*
  * [Developer preview VirtualBox for macOS / Arm64 (M1/M2) hosts](https://www.virtualbox.org/wiki/Download_Old_Builds_7_0)
  * [How to install Ubuntu on Mac using VirtualBox?](https://medium.com/tech-lounge/how-to-install-ubuntu-on-mac-using-virtualbox-3a26515aa869)
  * [How to Install Ubuntu Linux on Apple Silicon MacBooks](https://dev.to/andrewbaisden/how-to-install-ubuntu-linux-on-apple-silicon-macbooks-1nia)
  * [Using UTM: how To Install Parrot OS on Mac M1?](https://minkcoregame.medium.com/how-to-install-parrot-os-on-mac-m1-c1f20438631)
    * [Securely run operating systems on your Mac](https://mac.getutm.app/)