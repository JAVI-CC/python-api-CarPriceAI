import sys
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ...enums.columns_car import ColumnsCar as EnumColumnsCar
from textblob import TextBlob

# nlp = spacy.load('es_core_news_md')
nlp = spacy.load('en_core_web_md')
# spell = SpellChecker(language='en')


def structure_columns_v2(df_columns: list[str]):

  df_new_columns = []
  for col_corrected in df_columns:
    col_text = col_corrected.strip().lower()
    blob = TextBlob(col_text)
    text_corrected = blob.correct()

    df_new_columns.append(str(text_corrected))

  print(df_new_columns)


  name_col_original_vectors = [nlp(name_col).vector for name_col in EnumColumnsCar.ALL.value]
  name_col_csv_vectors = [nlp(col).vector for col in df_new_columns]

  similarity_col_res = []
  for idx, col in enumerate(name_col_csv_vectors):
    similarity = calculate_similarity(col, name_col_original_vectors)
    index_max_similarity = np.argmax(cosine_similarity([col], name_col_original_vectors))
    col_similarity = EnumColumnsCar.ALL.value[index_max_similarity]
    similarity_col_res.append({'col_csv': df_columns[idx],
                               'col_similarity': col_similarity,
                               'similarity_res': similarity})

  ###
  for similarity in similarity_col_res:
    print(f"col_csv {similarity['col_csv']},\n"
          f"col_similarity: {similarity['col_similarity']}\n",
          f"similarity_res: {similarity['similarity_res']}\n\n")
  ###

  sys.exit("Se detuvo la ejecución del script.")

  return similarity_col_res


def calculate_similarity(name_col, name_col_vectors):
  similarity = cosine_similarity([name_col], name_col_vectors)
  max_similarity = similarity.max() * 100
  return round(max_similarity, 2)
