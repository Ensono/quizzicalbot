from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector
import openai
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_type = os.getenv("OPENAI_API_TYPE")
openai_api_base = os.getenv("OPENAI_API_BASE")
openai_api_version = os.getenv("OPENAI_API_VERSION")

azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.getenv("AZURE_SEARCH_KEY")
azure_search_index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

# model = 'text-davinci-003' # Deprecated, MS will remove this soon.
model = 'ensono-alpha' # GPT 3.5 Instruct

# query = "What is the definition of Java and how is it used in programming? Make it rhyme."
# query = "What language is stacks cli written in? make it rhyme"
# query = "what is stacks cli written in?"
# query = "what is stacks cli?"
# query = "does stacks cli support linux?"
# query = "Is stacks cli written in Rust?"
# query = "What is love?"
query = "Is stacks cli written in PHP?"

# Azure Cognitive Search
def generate_embeddings(text):
	response = openai.Embedding.create(
		input=text,
		engine="text-embedding-ada-002",
	)
	embeddings = response['data'][0]['embedding']
	return embeddings

azure_key_credential = AzureKeyCredential(azure_search_key)
hybrid_search_client = SearchClient(azure_search_endpoint, azure_search_index_name, azure_key_credential)
vector = Vector(value=generate_embeddings(query), k=3, fields="content_vector")

results = hybrid_search_client.search(
	search_text=query,
	vectors=[vector],
	select=["content"],
	top=3,
)

joined_chunks = "\n".join([d["content"] for d in results])

prompt = f"""Answer the following query based on the context below. Be as brief as you can. Don't answer more than one question. If you don't know the answer, just say that you don't know. Don't try to make up an answer. Do not answer beyond this context.
query: {query}
context:"""

max_length = 4097 - len(prompt)
joined_chunks = joined_chunks[:max_length]
prompt = prompt + joined_chunks

# print(prompt)

# 'GPT35Instruct'
response = openai.Completion.create(
	deployment_id = model,
	prompt=prompt,
	temperature=0.3,
	max_tokens=500,
	stop=None,
)

# print("Resp:\n\n")
# print(response)

print(f"Question: {query}")
print([n for n in response.to_dict_recursive().items() if n[0] == "choices"][0][1][0]["text"])
