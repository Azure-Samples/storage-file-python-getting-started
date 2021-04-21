#-------------------------------------------------------------------------
# Microsoft Developer & Platform Evangelism
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, 
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
#----------------------------------------------------------------------------------
# The example companies, organizations, products, domain names,
# e-mail addresses, logos, people, places, and events depicted
# herein are fictitious. No association with any real company,
# organization, product, domain name, email address, logo, person,
# places, or events is intended or should be inferred.
#--------------------------------------------------------------------------

#This sample can be run using either the Azure Storage Emulator (Windows) or by updating the config.py file with your Storage account name and key.

# To run the sample using the Storage Emulator:
# 1. Download and install the Azure Storage Emulator https://azure.microsoft.com/en-us/downloads/ 
# 2. Start the emulator (once only) by pressing the Start button or the Windows key and searching for it by typing "Azure Storage Emulator". Select it from the list of applications to start it.
# 3. Run the project. 

# To run the sample using the Storage Service
# 1. Create a Storage Account through the Azure Portal and provide your STORAGE_CONNECTION_STRING in the config.py file. See https://azure.microsoft.com/en-us/documentation/articles/storage-create-storage-account/ for more information.
# 2. Set breakpoints and run the project. 
#---------------------------------------------------------------------------
import config
from file_basic_samples import FileBasicSamples
from file_advanced_samples import FileAdvancedSamples

print('Azure File Storage samples for Python')

storage_connection_string = config.STORAGE_CONNECTION_STRING

#Basic File samples
print ('---------------------------------------------------------------')
print('Azure Storage File samples')
file_basic_samples = FileBasicSamples()
file_basic_samples.run_all_samples(storage_connection_string)

#Advanced File samples
print ('---------------------------------------------------------------')
print('Azure Storage Advanced Fileable samples')
file_advanced_samples = FileAdvancedSamples()
file_advanced_samples.run_all_samples(storage_connection_string)