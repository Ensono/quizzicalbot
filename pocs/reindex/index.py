# from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from langchain.vectorstores import AzureSearch
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import AzureBlobStorageContainerLoader
import io
import os

account_url = os.getenv("BLOB_STORAGE_ACCOUNT_URL")
connect_str = os.getenv("BLOB_STORAGE_CONNECTION_STRING")
container = os.getenv("BLOB_STORAGE_CONTAINER")
prefix = os.getenv("BLOB_STORAGE_PREFIX")

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_type = os.getenv("OPENAI_API_TYPE")
openai_api_base = os.getenv("OPENAI_API_BASE")
openai_api_version = os.getenv("OPENAI_API_VERSION")

azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.getenv("AZURE_SEARCH_KEY")
azure_search_index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

try:
	embeddings = OpenAIEmbeddings(
		model="text-embedding-ada-002",
		chunk_size=16,
		openai_api_key=openai_api_key,
		openai_api_type=openai_api_type,
		openai_api_base=openai_api_base,
		openai_api_version=openai_api_version,
	)

	acs = AzureSearch(
		azure_search_endpoint=azure_search_endpoint,
		azure_search_key=azure_search_key,
		index_name=azure_search_index_name,
		embedding_function=embeddings.embed_query,
	)

	# text_splitter = TokenTextSplitter(
	# 	chunk_size=1000,
	# 	chunk_overlap=200,
	# )

	text_splitter = RecursiveCharacterTextSplitter(
		chunk_size = 1000,
		chunk_overlap  = 200,
	)

	loader = AzureBlobStorageContainerLoader(
		conn_str=connect_str,
		container=container,
		prefix=prefix,
	)
	documents = loader.load()

	# for document in documents:
	# 	print(f"{document.page_content}")

	text_splitter.split_documents(documents)

	acs.add_documents(documents=documents)


	# blob_list = container_client.list_blobs()
	# for blob in blob_list:
	# 	blob_client = container_client.get_blob_client(blob)
	# 	stream = io.BytesIO()
	# 	num_bytes = blob_client.download_blob().readinto(stream)
	# 	acs.add_documents()
	# 	print(f"Number of bytes: {num_bytes}")
	# 	print("\t" + blob.name)

except Exception as ex:
	print('Exception:')
	print(ex)
