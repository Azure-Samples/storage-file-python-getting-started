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

import uuid
import io
import tempfile
import fileinput
import os
import config
import azure.common
from random_data import RandomData

from azure.storage.common import CloudStorageAccount
from azure.storage.file import FileService

#
# Azure File Service Sample - Demonstrate how to perform common tasks using the Microsoft Azure File Service.  
#  
# Documentation References:  
#  - What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/  
#  - Getting Started with Files - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-file-storage/  
#  - File Service Concepts - http://msdn.microsoft.com/en-us/library/dn166972.aspx  
#  - File Service REST API - http://msdn.microsoft.com/en-us/library/dn167006.aspx  
#  - Storage Emulator - http://azure.microsoft.com/en-us/documentation/articles/storage-use-emulator/
#  
class FileAdvancedSamples():

    def __init__(self):
        self.random_data = RandomData()
    
    # Runs all samples for Azure Storage File service.
    # Input Arguments:
    # account - CloudStorageAccount to use for running the samples
    def run_all_samples(self, account):
        print('Azure Storage File Advanced samples - Starting.')
        
        try:
            # Create a new file service that can be passed to all methods
            file_service = account.create_file_service()

            # List shares
            print('\n\n* List shares *\n')
            self.list_shares(file_service)
            
            # Set Cors
            print('\n\n* Set cors rules *\n')
            self.set_cors_rules(file_service)
            
            # Set Service Properties
            print('\n\n* Set service properties *\n')
            self.set_service_properties(file_service)

            # Share, directory and file properties and metadata
            print('\n\n* Metadata and properties *\n')
            self.metadata_and_properties(file_service)

        except Exception as e:
            print('Error occurred in the sample. Please make sure the account name and key are correct.', e) 

        finally:
            print('\nAzure Storage File Advanced samples - Completed.\n')
    
    # List file shares
    def list_shares(self, file_service):
        share_prefix = 'sharesample' + self.random_data.get_random_name(6)

        try:        
            print('1. Create multiple shares with prefix: ', share_prefix)
            for i in range(5):
                file_service.create_share(share_prefix + str(i))
            
            print('2. List shares')
            
            shares =  file_service.list_shares()
            
            for share in shares:
                print('  Share name:' + share.name)
        finally:
            print('3. Delete shares with prefix:' + share_prefix) 
            for i in range(5):
                if(file_service.exists(share_prefix + str(i))):
                    file_service.delete_share(share_prefix + str(i))

    # Set CORS
    def set_cors_rules(self, file_service):
        print('1. Get Cors Rules')
        original_cors_rules = file_service.get_file_service_properties().cors

        print('2. Overwrite Cors Rules')
        cors_rule = CorsRule(
            allowed_origins=['*'], 
            allowed_methods=['POST', 'GET'],
            allowed_headers=['*'],
            exposed_headers=['*'],
            max_age_in_seconds=3600)

        try:
            file_service.set_file_service_properties(cors=[cors_rule])
        finally:
            #reverting cors rules back to the original ones
            print('3. Revert Cors Rules back the original ones')
            file_service.set_file_service_properties(cors=original_cors_rules)
        
        print("CORS sample completed")
    
    # Manage properties of the File service, including logging and metrics settings, and the default service version.
    def set_service_properties(self, file_service):

        print('1. Get File service properties')
        props = file_service.get_file_service_properties()

        retention = RetentionPolicy(enabled=True, days=5)
        hour_metrics = Metrics(enabled=True, include_apis=True, retention_policy=retention)
        minute_metrics = Metrics(enabled=False)

        try:
            print('2. Ovewrite File service properties')
            file_service.set_file_service_properties(hour_metrics=hour_metrics, minute_metrics=minute_metrics)

        finally:
            print('3. Revert File service properties back to the original ones')
            file_service.set_file_service_properties(hour_metrics=props.hour_metrics, minute_metrics=props.minute_metrics)

        print('4. Set File service properties completed')
    
    # Manage metadata and properties of the share
    def metadata_and_properties(self, file_service):
        share_name = 'sharename' + self.random_data.get_random_name(6)

        try:
            # All directories and share must be created in a parent share.
            # Max capacity: 5TB per share
            print('1. Create sample share with name ' + share_name)
            quota = 1 # in GB
            metadata = { "foo": "bar", "baz": "foo" }
            file_service.create_share(share_name, metadata, quota)
            print('Sample share "'+ share_name +'" created.')

            print('2. Get share properties.')
            properties = file_service.get_share_properties(share_name)

            print('3. Get share metadata.')
            get_metadata = file_service.get_share_metadata(share_name)
            for k, v in get_metadata.items():
                print("\t" + k + ": " + v)

            dir_name = 'dirname' + self.random_data.get_random_name(6)

            print('4. Create sample directory with name ' + dir_name)
            metadata = { "abc": "def", "jkl": "mno" }
            file_service.create_directory(share_name, dir_name, metadata)
            print('Sample directory "'+ dir_name +'" created.')

            print('5. Get directory properties.')
            properties = file_service.get_directory_properties(share_name, dir_name)
            
            print('6. Get directory metadata.')
            get_metadata = file_service.get_directory_metadata(share_name, dir_name)
            for k, v in get_metadata.items():
                print("\t" + k + ": " + v)

            file_name = 'sample.txt'
            # Uploading text to share_name/dir_name/sample.txt in Azure Files account.
            # Max capacity: 1TB per file
            print('7. Upload sample file from text to directory.')
            metadata = { "prop1": "val1", "prop2": "val2" }   
            file_service.create_file_from_text(
                share_name,              # share        
                dir_name,          # directory path - root path if none
                file_name,               # destination file name
                'Hello World! - from text sample', # file text 
                metadata=metadata) # metadata
            print('Sample file "' + file_name + '" created and uploaded to: ' + share_name + '/' + dir_name)        

            print('8. Get file properties.')
            properties = file_service.get_file_properties(share_name, dir_name, file_name)

            print('9. Get file metadata.')
            get_metadata = file_service.get_file_metadata(share_name, dir_name, file_name)
            for k, v in get_metadata.items():
                print("\t" + k + ": " + v)

            # This is for demo purposes, all files will be deleted when share is deleted
            print('10. Delete file.')
            file_service.delete_file(share_name, dir_name, file_name)

            # This is for demo purposes, all directories will be deleted when share is deleted
            print('11. Delete directory.')
            file_service.delete_directory(share_name, dir_name)

        finally:
            print('12. Delete share.')
            file_service.delete_share(share_name)

        print("Metadata and properties sample completed")