#!/usr/bin/env python3

"""
----------------------------------------------------------------------------------------------
This python script automates the process of following:

a. Copying a folder (along with its contents) from source to destination
b. Search for matching text in a file and replace it with new text
    i. In this example, we are replacing text of current website address with new website address in the apache conf files

Pre-Requisites:
-----------------
This script needs Python environment 3.5 or above

Assumptions:
-----------------
1. Script expects two input parameters to be passed.
    a. Name of current (source) folder using the --cf switch
    b. Name of new (destination) folder using the --nf switch
----------------------------------------------------------------------------------------------
"""

from pathlib import Path
import argparse, os, shutil, sys

# Declaring variables
current_folder = ""
new_folder = ""

# Base path of the folders/directories
web_dir = '/var/www/'

# Base path of apache conf files
conf_files_dir = '/etc/apache/sites/'

print(f'\nBeginning the script execution...\n')

# -----------------------------------------------------------------------------------------
# Block to read the command line arguments - Begin
# if len(sys.argv) < 3:
#    print(f'\nERROR: This script requires 2 arguments as inputs.You have specified less than 2. Aborting the operation..!\n')
#    sys.exit()

try:
    # Parsing the command line arguments
    arg_parser = argparse.ArgumentParser(allow_abbrev=False)
    arg_parser.add_argument('--cf', action='store', required=True)
    arg_parser.add_argument('--nf', action='store', required=True)
    args = arg_parser.parse_args()

    current_folder = args.cf
    new_folder = args.nf

    # Printing the command line arguments received
    print(f'\n-------------------------------------------------------------------------------')
    print(f'Reading the input variables received as command line arguments...\n')
    print(f'Current folder name is:', current_folder)
    print(f'New folder name is:', new_folder)
    print(f'-------------------------------------------------------------------------------\n')

except:
    print(f'\n-------------------------------------------------------------------------------')
    print(f'ERROR - Some error occured while parsing the command line arguments.')
    print(f'Either the required number of arguments are missing or invalid arguments passed.')
    print(f'Aborting the operation..!\n')
    print(f'-------------------------------------------------------------------------------\n')
    sys.exit()

# Block to read the command line arguments - End
# -----------------------------------------------------------------------------------------



# -----------------------------------------------------------------------------------------
# Block to recursively copy source folder to destination - Begin
print(f'\n-------------------------------------------------------------------------------')
print(f'Copying the contents of current folder to new folder...\n')
try:
# Check if current folder exists or not
    source_dir = os.path.join(web_dir, current_folder)
    dest_dir = os.path.join(web_dir, new_folder)
    if os.path.exists(source_dir):
        print(f'\nCurrent folder [{source_dir}] exists.')
        # Copy the contents of current folder to new folder
        shutil.copytree(source_dir, dest_dir)
        print(f'Copied the folder and its contents [{source_dir}] to [{dest_dir}]')
        print(f'-------------------------------------------------------------------------------\n')
    else:
        print(f'\nERROR: Directory [{current_folder}] does not exist. Please check if you have specified the correct name.')
        print(f'Aborting the execution here...\n')
        sys.exit()
except OSError as err:
    print(f'\nERROR: Error occured while copying the current folder to new folder. Please check.')
    print(f'ERROR: Aborting the execution..!')
    print(f'ERROR: % s\n' % err)
# Block to recursively copy source folder to destination - End
# -----------------------------------------------------------------------------------------



# -----------------------------------------------------------------------------------------
# Block to copy and update the apache (port 80) conf file - Begin
# Variables for file name
port80_conf_file_current = current_folder + ".conf"
port80_conf_file_new = new_folder + ".conf"

# Building full system path for the files
port80_conf_file_current_path = os.path.join(conf_files_dir, port80_conf_file_current)
port80_conf_file_new_path = os.path.join(conf_files_dir, port80_conf_file_new)

try:
# Check if file exists or not
    print(f'\n-------------------------------------------------------------------------------')
    print(f'Checking if port 80 conf file of current website [{port80_conf_file_current}] exists...\n')
    path = Path(port80_conf_file_current_path)

    if path.is_file():
        print(f'File [{port80_conf_file_current_path}] exist.\nCreating a copy of this file for the new website [{new_folder}]')
        shutil.copyfile(port80_conf_file_current_path, port80_conf_file_new_path)

        print(f'\nReading contents of the file [{port80_conf_file_new_path}]\n')

        try:
            # Reading the input file
            file_in = open(f'{port80_conf_file_new_path}', 'r+')

            #read content of file to string
            data = file_in.read()

            # Counting the number of text occurences
            text_count = data.count(current_folder)

            if text_count < 1:
                print(f'No occurences of [{current_folder}] found in the file [{port80_conf_file_new_path}]...')
                print(f'Nothing to do here. Exiting the file read operation.')
                print(f'-------------------------------------------------------------------------------\n')
            elif text_count > 0 :
                print(f'Total of [{text_count}] occurences of current website address [{current_folder}] found in the file [{port80_conf_file_new}]')
                print(f'Proceeding to update the current domain with new domain name...\n')
        except:
            sys.exit('Some error occured while reading the file [{port80_conf_file_new_path}]. Please check...!')

        
        try:
            # Reading file
            with open(f'{port80_conf_file_new_path}', 'r') as file:
                filedata = file.read()
            
            # Replace the target string
            filedata = filedata.replace(current_folder, new_folder)

            # Write the file out again
            with open(f'{port80_conf_file_new_path}', 'w') as file:
                file.write(filedata)
            
            print(f'\nNew domain name replaced successfully in the file [{port80_conf_file_new_path}].\nCheck the file to confirm...')
            print(f'-------------------------------------------------------------------------------\n')
        except:
            sys.exit('Some error occured while updating the file with new domain name. Aborting the execution..!')
    
    else:
        print(f'The file [{port80_conf_file_new_path}] does not exist. Aborting the operation...!\n')


except OSError as err:
    print(f'\nERROR: Error occured while updating the port 80 conf file with new domain name.')
    print(f'ERROR: Aborting the execution..!')
    print(f'ERROR: % s\n' % err)

# Block to copy and update the apache port 80 file - End
# -----------------------------------------------------------------------------------------



# -----------------------------------------------------------------------------------------
# Block to copy and update the apache (ssl port 443) conf file - Begin
# Variables for file name
ssl_conf_file_current = current_folder + "-le-ssl.conf"
ssl_conf_file_new = new_folder + "-le-ssl.conf"

# Building full system path for the files
ssl_conf_file_current_path = os.path.join(conf_files_dir, ssl_conf_file_current)
ssl_conf_file_new_path = os.path.join(conf_files_dir, ssl_conf_file_new)

try:
# Check if file exists or not
    print(f'\n-------------------------------------------------------------------------------')
    print(f'Checking if ssl conf file of current domain [{ssl_conf_file_current}] exists...\n')
    path = Path(ssl_conf_file_current_path)

    if path.is_file():
        print(f'File [{ssl_conf_file_current_path}] exist.\nCreating a copy of this file for the new domain [{new_folder}]')
        shutil.copyfile(ssl_conf_file_current_path, ssl_conf_file_new_path)

        print(f'\nReading contents of the file [{ssl_conf_file_new_path}]\n')

        try:
            # Reading the input file
            file_in = open(f'{ssl_conf_file_new_path}', 'r+')

            #read content of file to string
            data = file_in.read()

            # Counting the number of text occurences
            text_count = data.count(current_folder)

            if text_count < 1:
                print(f'No occurences of the domain name [{current_folder}] found in the file [{ssl_conf_file_new_path}]...')
                print(f'Nothing to do here. Exiting the file read operation.')
                print(f'-------------------------------------------------------------------------------\n')
            elif text_count > 0 :
                print(f'Total of [{text_count}] occurences of current domain name [{current_folder}] found in the file [{ssl_conf_file_new}]')
                print(f'Proceeding to update the current domain with new domain name...\n')
        except:
            sys.exit('Some error occured while reading the file [{ssl_conf_file_new_path}]. Please check...!')

        
        try:
            # Reading file
            with open(f'{ssl_conf_file_new_path}', 'r') as file:
                filedata = file.read()
            
            # Replace the target string
            filedata = filedata.replace(current_folder, new_folder)

            # Write the file out again
            with open(f'{ssl_conf_file_new_path}', 'w') as file:
                file.write(filedata)
            
            print(f'\nNew domain name replaced successfully in the file [{ssl_conf_file_new_path}].\nCheck the file to confirm...')
            print(f'-------------------------------------------------------------------------------\n')
        except:
            sys.exit('Some error occured while updating the file with new domain name. Aborting the execution..!')
    
    else:
        print(f'The file [{ssl_conf_file_new_path}] does not exist. Aborting the operation...!\n')


except OSError as err:
    print(f'\nERROR: Error occured while updating the ssl conf file with new domain name.')
    print(f'ERROR: Aborting the execution..!')
    print(f'ERROR: % s\n' % err)

# Block to copy and update the apache (ssl port 443) conf file - End
# -----------------------------------------------------------------------------------------

print(f'\nScript has finished its execution... Bye...\n')
