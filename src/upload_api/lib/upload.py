
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError
from core.config import settings
from core.log_config import logger
from fastapi import UploadFile, Response, status
from lib.response import ResponseObj
from pathlib import Path
import os
import shutil
import mimetypes
import zipfile

class Upload():

    def __init__(self):

        # Add a new mimetype for asciidoc files
        mimetypes.add_type("text/asciidoc", ".adoc")

        # Define list of fille types that are acceptable
        self.filetypes = [
            "application/x-zip-compressed",
            "application/pdf",
            "application/msword",
            "text/plain",
            "text/markdown",
            "text/asciidoc"
        ]

        # Create a connection to the blob storage
        self.blob_service_client = BlobServiceClient.from_connection_string(settings.azure_storage_connection_string)

    def get_types(self):
        return ",".join(self.filetypes)

    def accept(self, file: UploadFile, response: Response, folder_name: str):

        self.folder_name = folder_name

        resp = ResponseObj()

        upload_path_split = os.path.split(settings.upload_dir)
        self.upload_path = os.path.join(*upload_path_split, file.filename)

        # check that the upload file exists
        if not os.path.exists(os.path.dirname(self.upload_path)):
            logger.info(f"Creating directory {os.path.dirname(self.upload_path)}")
            os.makedirs(os.path.dirname(self.upload_path))

        logger.info(f"Uploading file to {self.upload_path}")

        try:
            with open(self.upload_path, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object)
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            resp.set(True, str(e)) 
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return resp
        finally:
            file.file.close()

        resp.set(False, "File uploaded", file.filename, True)
        response.status_code = status.HTTP_201_CREATED

        return resp
    
    def process(self):
        """
        Process method determines if the file is a zip file and if so unpacks it. It determines if the
        file is a zip file by checking the mimetype
        It will then attempt to upload all the files into blob storage
        """

        files_to_upload = []

        # Determine the mimetype of the file, if it is a zip file call the method to unpack
        if mimetypes.guess_type(self.upload_path)[0] == "application/x-zip-compressed":
            files_to_upload = self.unpack()
        else:
            files_to_upload = [self.upload_path]

        logger.info(f"Would upload {len(files_to_upload)} files to blob storage")

        # aensure that the container exists
        try:
            container_client = self.blob_service_client.create_container(settings.azure_storage_container)
        except ResourceExistsError:
            logger.info(f"Container already exists: {settings.azure_storage_container}")


        # iterate around the files_to_upload and copy them to the storage account container
        for item in files_to_upload:

            # determine the name for the blob
            name = f"{self.folder_name}/{os.path.basename(item)}"

            # create a blob client for this file so it can be uploaded
            blob_client = self.blob_service_client.get_blob_client(
                container =settings.azure_storage_container,
                blob = name
            )

            logger.debug(f"Uploading to Azure Storage as blob: {name}")

            with open(file = item, mode="rb") as data:
                blob_client.upload_blob(data, overwrite=True)

    def get_content(self):
        """
        Get the content of the file as a string
        """

        # get the content from the file
        f = open(self.upload_path, "r")
        data = f.read()
        f.close()

        return data
    
    def unpack(self):
        """
        Unpack the uploaded file
        """

        files_to_upload = []

        logger.info(f"Unpacking zip file: {self.upload_path}")

        # Determine the directory into which the file will be unpacked
        unpack_dir = os.path.join(settings.upload_dir, os.path.splitext(os.path.basename(self.upload_path))[0])
        logger.debug(f"Unpacking into directory: {unpack_dir}")

        # Unpack the zip file
        with zipfile.ZipFile(self.upload_path, "r") as zip_ref:
            zip_ref.extractall(unpack_dir)

        # get all the files in the unpack dir and add each eligible one to the list
        logger.info("Finding eligible files to upload")
        for file in Path(unpack_dir).rglob("*"):
            
            # get the mimetype of the file
            mimetype = mimetypes.guess_type(file.absolute())[0]
            logger.debug(f"Mimetype: {file.name} - {mimetype}")

            if mimetype in self.filetypes:
                logger.debug(f"Adding file {file.absolute()} to upload list")
                files_to_upload.append(file.absolute())

        return files_to_upload