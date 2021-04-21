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

import os
from random_data import RandomData

from azure.storage.fileshare import ShareServiceClient
from azure.storage.fileshare import CorsRule, RetentionPolicy, Metrics

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
    def run_all_samples(self, connection_string):
        print('Azure Storage File Advanced samples - Starting.')
        
        try:
            # Create an instance of ShareServiceClient
            service = ShareServiceClient.from_connection_string(conn_str=connection_string)

            # List shares
            print('\n\n* List shares *\n')
            self.list_shares(service)

            # Set Cors
            print('\n\n* Set cors rules *\n')
            self.set_cors_rules(service)

            # Set Service Properties
            print('\n\n* Set service properties *\n')
            self.set_service_properties(service)

            # Share, directory and file properties and metadata
            print('\n\n* Metadata and properties *\n')
            self.metadata_and_properties(service)

        except Exception as e:
            print('Error occurred in the sample.', e) 

        finally:
            print('\nAzure Storage File Advanced samples - Completed.\n')
    
    # List file shares
    def list_shares(self, service):
        share_prefix = 'sharesample' + self.random_data.get_random_name(6)

        try:        
            print('1. Create multiple shares with prefix: ', share_prefix)
            for i in range(5):
                service.create_share(share_name=share_prefix + str(i))
            
            print('2. List shares')
            shares = service.list_shares()
            for share in shares:
                print('  Share name:' + share.name)

        except Exception as e:
            print(e) 

        finally:
            print('3. Delete shares with prefix:' + share_prefix) 
            for i in range(5):
                service.delete_share(share_prefix + str(i))
    

    # Set CORS
    def set_cors_rules(self, service):
        print('1. Get Cors Rules')
        original_cors_rules = service.get_service_properties()['cors']

        print('2. Overwrite Cors Rules')
        cors_rule = CorsRule(
            allowed_origins=['*'], 
            allowed_methods=['POST', 'GET'],
            allowed_headers=['*'],
            exposed_headers=['*'],
            max_age_in_seconds=3600)

        try:
            service.set_service_properties(cors=[cors_rule])
        except Exception as e:
            print(e)
        finally:
            #reverting cors rules back to the original ones
            print('3. Revert Cors Rules back the original ones')
            service.set_service_properties(cors=original_cors_rules)
        
        print("CORS sample completed")
    

    # Manage properties of the File service, including logging and metrics settings, and the default service version.
    def set_service_properties(self, service):

        print('1. Get File service properties')
        props = service.get_service_properties()

        retention = RetentionPolicy(enabled=True, days=5)
        hour_metrics = Metrics(enabled=True, include_apis=True, retention_policy=retention)
        minute_metrics = Metrics(enabled=False)

        try:
            print('2. Ovewrite File service properties')
            service.set_service_properties(hour_metrics=hour_metrics, minute_metrics=minute_metrics)

        finally:
            print('3. Revert File service properties back to the original ones')
            service.set_service_properties(hour_metrics=props['hour_metrics'], minute_metrics=props['minute_metrics'])

        print('4. Set File service properties completed')
    

    # Manage metadata and properties of the share
    def metadata_and_properties(self, service):
        share_name = 'sharename' + self.random_data.get_random_name(6)

        try:
            # All directories and share must be created in a parent share.
            # Max capacity: 5TB per share
            print('1. Create sample share with name ' + share_name)
            quota = 1 # in GB
            metadata = { "foo": "bar", "baz": "foo" }
            share_client = service.create_share(share_name=share_name)
            print('Sample share "'+ share_name +'" created.')

            print('2. Get share properties.')
            properties = share_client.get_share_properties()

            print('3. Get share metadata.')
            get_metadata = properties['metadata']
            for k, v in get_metadata.items():
                print("\t" + k + ": " + v)

            dir_name = 'dirname' + self.random_data.get_random_name(6)

            print('4. Create sample directory with name ' + dir_name)
            metadata = { "abc": "def", "jkl": "mno" }
            directory_client = share_client.create_directory(dir_name, metadata=metadata)
            print('Sample directory "'+ dir_name +'" created.')

            print('5. Get directory properties.')
            properties = directory_client.get_directory_properties()
            
            print('6. Get directory metadata.')
            get_metadata = properties['metadata']
            for k, v in get_metadata.items():
                print("\t" + k + ": " + v)

            file_name = 'sample.txt'
            # Uploading text to share_name/dir_name/sample.txt in Azure Files account.
            # Max capacity: 1TB per file
            print('7. Upload sample file from text to directory.')
            metadata = { "prop1": "val1", "prop2": "val2" }
            file_client = directory_client.get_file_client(file_name)
            file_client.upload_file('Hello World! - from text sample', metadata=metadata)
            print('Sample file "' + file_name + '" created and uploaded to: ' + share_name + '/' + dir_name)        

            print('8. Get file properties.')
            properties = file_client.get_file_properties()

            print('9. Get file metadata.')
            get_metadata = properties['metadata']
            for k, v in get_metadata.items():
                print("\t" + k + ": " + v)

            # This is for demo purposes, all files will be deleted when share is deleted
            print('10. Delete file.')
            file_client.delete_file()

            # This is for demo purposes, all directories will be deleted when share is deleted
            print('11. Delete directory.')
            directory_client.delete_directory()

        finally:
            print('12. Delete share.')
            share_client.delete_share(share_name)

        print("Metadata and properties sample completed")