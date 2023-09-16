
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchableField,
    SearchFieldDataType,
    SimpleField
)
from core.config import settings
from core.log_config import logger
from lib.response import ResponseObj

class Indexer:
    def __init__(self):

        # Create the client for cognitive services
        self.credential = AzureKeyCredential(settings.azure_cognitive_search_api_key)
        self.client = SearchIndexClient(
            endpoint = settings.get_acs_endpoint(),
            credential = self.credential
        )

    def get_search_client(self, name = ""):

        if name == "":
            name = settings.azure_cognitive_search_index_name

        self.search_client = SearchClient(
            endpoint = settings.get_acs_endpoint(),
            index_name = name,
            credential = self.credential
        )

    def get_index(self, name):

        try:
            self.client.get_index(name)
            return True
        except Exception as e:
            logger.error(e)
            return False
            
    def create_index(self, name):

        # Only create the index if it does not already exist
        if self.get_index(name):
            raise FileExistsError("Index already exists!")

        # define the index
        index = SearchIndex(
            name = name,
            fields = [
                SimpleField(name = "id", type = SearchFieldDataType.String, key = True, filterable = True, sortable = True),
                SimpleField(name = "filename", type = SearchFieldDataType.String),
                SimpleField(name = "path", type = SearchFieldDataType.String),
                SearchableField(name = "title", type = SearchFieldDataType.String),
                SimpleField(name = "url", type = SearchFieldDataType.String),
                SearchableField(name = "content", type = SearchFieldDataType.String),
                SimpleField(name = "chunk_id", type = SearchFieldDataType.String),
                SimpleField(name = "last_updated", type = SearchFieldDataType.String)
            ]
        )

        # create the index
        result = self.client.create_index(index)

        return "Index created"
        
    # Index a document and return the results
    def index(self, index_name, document, content_encoding):

        # Create the searchclient to work with
        self.get_search_client(index_name)

        # Ensure that the document content is decoded
        document.resolve_content(content_encoding)

        doc = {
            "id": document.id,
            "filename": document.filename,
            "path": document.path,
            "title": document.title,
            "url": document.url, 
            "content": document.content,
            "last_updated": document.last_updated,
            "chunk_id": document.chunk_id
        }

        # get a client to be able to create an index
        result = self.search_client.upload_documents(
            documents = [
                doc
            ]
        )

        # check the result and determine if it was successful
        # return an object with this information
        return ResponseObj(
            error = not result[0].succeeded,
            status = result[0].succeeded,
            name = document.title,
            message = "Document indexed" if result[0].succeeded else result[0].error_message
        )

    # Ask a question
    def ask(self, question):

        self.get_search_client()

        response = self.search_client.search(query_type = "full", search_text = question.question, include_total_count = True)

        for result in response:
            return result
        
