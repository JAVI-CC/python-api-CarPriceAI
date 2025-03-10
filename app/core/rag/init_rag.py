from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_chroma.vectorstores import Chroma
from ...enums.storage_path import StoragePath as EnumStoragePath
from ...core import create_vectorstore, getenv
from ...schemas import CarAnswer as SchemaCarAnswer
from .embed_model import get_embed_model


def init_chat():
  llm = ChatOllama(base_url=getenv('BASE_URL_OLLAMA'), model="llama3", temperature=0.7)
  embed_model = get_embed_model()

  vector_store = Chroma(embedding_function=embed_model,
                        persist_directory=EnumStoragePath.CHROMA_DB.value,
                        collection_name="cars")

  total_rows = len(vector_store.get()['ids'])

  if not total_rows:
    vector_store = create_vectorstore()

  retriever = vector_store.as_retriever(search_kwargs={'k': 5})

  prompt_template = """
  You are an expert car assistant. Answer the following query using the information retrieved:
  - Provide concise answers and responses that are not too long.
  - Answer in the same language as the question is written.

  If the question is in English, respond in English.
  If the question is in Spanish, respond in Spanish.
  If the question is in Catalan, respond in Catalan.

  When mentioning car prices, convert the price from USD to EUR. Use the current exchange rate (1 USD = 0.85 EUR). Display the price in euros (€)

  Here is the conversation history: {context}
  
  Question: {question}

  """

  prompt = PromptTemplate(input_variables=["question", "context"], template=prompt_template)

  qa_chain = RetrievalQA.from_chain_type(
      llm=llm,
      chain_type="stuff",
      retriever=retriever,
      return_source_documents=True,
      chain_type_kwargs={"prompt": prompt}
    )

  return qa_chain


def get_chat_answer(question: str, chat_history=None) -> SchemaCarAnswer:
  qa_chain = init_chat()

  if chat_history is None:
    chat_history = []

  context = ""
  for msg in chat_history:
    context += f"\nUser: {msg['question']}\nAI: {msg['answer']}"

  response = qa_chain.invoke({"query": question, "context": context})
  answer = response['result']

  chat_history.append({
    'question': question,
    'answer': response['result'],
  })

  return {'answer': answer, 'chat_history': chat_history}
