from langchain.vectorstores import AzureSearch
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import AzureOpenAI
from langchain.chains import RetrievalQAWithSourcesChain, StuffDocumentsChain, RetrievalQA, ConversationalRetrievalChain
from langchain.chat_models import AzureChatOpenAI
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_type = os.getenv("OPENAI_API_TYPE")
openai_api_base = os.getenv("OPENAI_API_BASE")
openai_api_version = os.getenv("OPENAI_API_VERSION")

azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.getenv("AZURE_SEARCH_KEY")
azure_search_index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

query = "What is java?"

# model = 'text-davinci-003' # Deprecated, MS will remove this soon.
model = 'ensono-alpha' # GPT 3.5 Instruct

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

# openai_model = AzureChatOpenAI(
# 	model_name=model,
# 	openai_api_key=openai_api_key,
# 	openai_api_type=openai_api_type,
# 	openai_api_base=openai_api_base,
# 	openai_api_version=openai_api_version,
# )

llm = AzureOpenAI(
	openai_api_key=openai_api_key,
	openai_api_type=openai_api_type,
	openai_api_base=openai_api_base,
	openai_api_version=openai_api_version,
	model_kwargs={
		"engine": model,
	},
)

# qa = ConversationalRetrievalChain(
# 	llm=llm,
# 	retriever=acs.as_retriever(),
# 	return_source_documents=True,
# 	verbose=False,
# )

# result = qa({"question": query, "chat_history": []})

# print("Answer is: ", result["answer"])

# chain = RetrievalQA.from_chain_type(
# 	llm = llm,
# 	retriever = acs.as_retriever(),
# 	chain_type = "stuff",
# )

# # Finally ask the question
# answer = chain.run(query)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=acs.as_retriever())
answer = qa.run(query)

print(answer)
