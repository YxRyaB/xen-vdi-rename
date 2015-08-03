#Renaming Xen virtual disk image.
The script finds all VDI and correlates them with the VM through the VBD, resulting in an array with the name of the virtual machine , the virtual disk name and position in the VBD.
Example: A virtual machine named CentOS6_Test and two virtual disks will look like this.
#Example:
 |   Name VM    |   Name VDI 0   |    Name VDI 1  |
 |:------------:|:--------------:|:--------------:|
 | CentOS6_Test | CentOS6_Test_0 | CentOS6_Test_1 |

#The parameters of the script
```
Usage: xen-storage-rename.py [option] arg1 ...

Options:

  -h, --help            show this help message and exit
  
  -s SERVER, --server=SERVER
                        IP address of the server you want to connect
                        
  -p PORT, --port=PORT  Server port to connect to
  
  -w PASSWORD, --password=PASSWORD
                        Password on the server
                        
  -u USERNAME, --user=USERNAME
                        Username on the server
                        
  -n NAMEVM, --by_name=NAMEVM
                        Change only in a particular VM VDI, example: -n
                        "CentOS 6 test"
                        
  -l LEVEL, --setlevel=LEVEL
                        Set the level of logging default is INFO. Possible
                        options is DEBUG, INFO
                        
```
#Logging
Logging done in the file xen_rename_VDI.log

There are two levels of logging (DEBUG and INFO)

