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

from random_data import RandomData
import tempfile
import os

from azure.storage.fileshare import ShareServiceClient


class FileBasicSamples():

    def __init__(self):
        self.random_data = RandomData()

    # Runs all samples for Azure Storage File service.
    def run_all_samples(self, connection_string):
        print('Azure Storage File Basis samples - Starting.')
        
        #declare variables
        filename = 'filesample' + self.random_data.get_random_name(6)
        sharename = 'sharesample' + self.random_data.get_random_name(6)
        
        try:
            # Create an instance of ShareServiceClient
            service = ShareServiceClient.from_connection_string(conn_str=connection_string)

            print('\n\n* Basic file operations *\n')
            self.basic_file_operations(sharename, filename, service)

        except Exception as e:
            print('error:' + e) 

        finally:
            # Delete all Azure Files created in this sample
            self.file_delete_samples(sharename, filename, service)

        print('\nAzure Storage File Basic samples - Completed.\n')
    
    def basic_file_operations(self, sharename, filename, service):
        # Creating an SMB file share in your Azure Files account.
        print('\nAttempting to create a sample file from text for upload demonstration.')   
        # All directories and share must be created in a parent share.
        # Max capacity: 5TB per share

        print('Creating sample share.')
        share_client = service.create_share(share_name=sharename)
        print('Sample share "'+ sharename +'" created.')


        # Creating an optional file directory in your Azure Files account.
        print('Creating a sample directory.')    
        # Get the directory client
        directory_client = share_client.create_directory("mydirectory")
        print('Sample directory "mydirectory" created.')


        # Uploading text to sharename/mydirectory/my_text_file in Azure Files account.
        # Max capacity: 1TB per file
        print('Uploading a sample file from text.')   
        # create_file_client
        file_client = directory_client.get_file_client(filename)
        # Upload a file
        file_client.upload_file('Hello World! - from text sample')
        print('Sample file "' + filename + '" created and uploaded to: ' + sharename + '/mydirectory')
  

        # Demonstrate how to copy a file
        print('\nCopying file ' + filename)
        # Create another file client which will copy the file from url
        destination_file_client = share_client.get_file_client('file1copy')

        # Copy the sample source file from the url to the destination file
        copy_resp = destination_file_client.start_copy_from_url(source_url=file_client.url)
        if copy_resp['copy_status'] ==  'pending':
            # Demonstrate how to abort a copy operation (just for demo, probably will never get here)
            print('Abort copy operation')
            destination_file.abort_copy()
        else:
            print('Copy was a ' + copy_resp['copy_status'])
        

        # Demonstrate how to create a share and upload a file from a local temporary file path
        print('\nAttempting to upload a sample file from path for upload demonstration.')  
        # Creating a temporary file to upload to Azure Files
        print('Creating a temporary file from text.') 
        with tempfile.NamedTemporaryFile(delete=False) as my_temp_file:
            my_temp_file.file.write(b"Hello world!")
        print('Sample temporary file created.') 

        # Uploading my_temp_file to sharename folder in Azure Files
        # Max capacity: 1TB per file
        print('Uploading a sample file from local path.')
        # Create file_client
        file_client = share_client.get_file_client(filename)

        # Upload a file
        with open(my_temp_file.name, "rb") as source_file:
            file_client.upload_file(source_file)

        print('Sample file "' + filename + '" uploaded from path to share: ' + sharename)

        # Close the temp file
        my_temp_file.close()

        # Get the list of valid ranges and write to the specified range
        print('\nGet list of valid ranges of the file.') 
        file_ranges = file_client.get_ranges()

        data = b'abcdefghijkl'
        print('Put a range of data to the file.')
        
        file_client.upload_range(data=data, offset=file_ranges[0]['start'], length=len(data))


        # Demonstrate how to download a file from Azure Files
        # The following example download the file that was previously uploaded to Azure Files
        print('\nAttempting to download a sample file from Azure files for demonstration.')

        destination_file = tempfile.tempdir + '\mypathfile.txt'

        with open(destination_file, "wb") as file_handle:
            data = file_client.download_file()
            data.readinto(file_handle)

        print('Sample file downloaded to: ' + destination_file)


        # Demonstrate how to list files and directories contains under Azure File share
        print('\nAttempting to list files and directories directory under share "' + sharename + '":')

        # Create a generator to list directories and files under share
        # This is not a recursive listing operation
        generator = share_client.list_directories_and_files()

        # Prints the directories and files under the share
        for file_or_dir in generator:
            print(file_or_dir['name'])
        
        # remove temp file
        os.remove(my_temp_file.name)

        print('Files and directories under share "' + sharename + '" listed.')
        print('\nCompleted successfully - Azure basic Files operations.')


    # Demonstrate how to delete azure files created for this demonstration
    # Warning: Deleting a share or directory will also delete all files and directories that are contained in it.
    def file_delete_samples(self, sharename, filename, service):
        print('\nDeleting all samples created for this demonstration.')

        try:
            # Deleting file: 'sharename/mydirectory/filename'
            # This is for demo purposes only, it's unnecessary, as we're deleting the share later
            print('Deleting a sample file.')

            share_client = service.get_share_client(sharename)
            directory_client = share_client.get_directory_client('mydirectory')
            
            directory_client.delete_file(file_name=filename)
            print('Sample file "' + filename + '" deleted from: ' + sharename + '/mydirectory' )

            # Deleting directory: 'sharename/mydirectory'
            print('Deleting sample directory and all files and directories under it.')
            share_client.delete_directory('mydirectory')
            print('Sample directory "/mydirectory" deleted from: ' + sharename)

            # Deleting share: 'sharename'
            print('Deleting sample share ' + sharename + ' and all files and directories under it.')
            share_client.delete_share(sharename)
            print('Sample share "' + sharename + '" deleted.')

            print('\nCompleted successfully - Azure Files samples deleted.')

        except Exception as e:
            print('********ErrorDelete***********')
            print(e)