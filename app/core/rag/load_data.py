import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain.schema import Document
from langchain_chroma.vectorstores import Chroma
from progress.bar import Bar
from ...enums.columns_car import ColumnsCar as EnumColumnsCar
from ...enums.storage_path import StoragePath as EnumStoragePath
from .embed_model import get_embed_model


def convert_df_to_documents(date=None):
  from ...db.session import engine

  where_date = ""
  if date:
    where_date = f"WHERE date = '{str(date)}'"

  columns_compare_str = ', '.join(EnumColumnsCar.ALL_AND_ID.value)
  cars_df = pd.read_sql((f"SELECT {columns_compare_str} FROM cars {where_date}"), engine)

  loader = DataFrameLoader(cars_df, page_content_column="id")

  documents = []
  with Bar('Convert row DataFrame to Document', max=len(cars_df)) as progress_bar:
    for row in loader.lazy_load():
      documents.append(
        Document(page_content=row.page_content, metadata=row.metadata)
          )
      progress_bar.next()

  return documents


def create_vectorstore(date=None):

  docs = convert_df_to_documents(date)

  embed_model = get_embed_model()

  vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embed_model,
    persist_directory=EnumStoragePath.CHROMA_DB.value,
    collection_name="cars"
  )

  return vector_store
