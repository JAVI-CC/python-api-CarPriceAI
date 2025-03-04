from langchain_community.embeddings.fastembed import FastEmbedEmbeddings


def get_embed_model():
  embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

  return embed_model
