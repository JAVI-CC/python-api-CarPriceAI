from fuzzywuzzy import process

# TODO: Training columns ML

COLUMNS = ['marca',
           'modelo',
           'combustible',
           'año',
           'kilometraje',
           'caballos',
           'puertas',
           'transmision',
           'color',
           'es_concesionario',
           'precio'
           ]

COLUMNS_TRADUCTION = {
    'marca': 'brand',
    'modelo': 'model',
    'combustible': 'fuel',
    'año': 'year',
    'kilometraje': 'mileage',
    'caballos': 'horsepower',
    'puertas': 'doors',
    'transmision': 'transmission',
    'color': 'color',
    'es_concesionario': 'is_dealer',
    'precio': 'price'
}

PERCENTAGE_MATCH = 75


def structure_columns(df_columns: list):

  new_columns_dict = {}
  delete_columns = []

  for col in df_columns:
    best_match = process.extractOne(col, COLUMNS)

    if best_match[1] >= PERCENTAGE_MATCH:
      new_columns_dict[col] = COLUMNS_TRADUCTION[best_match[0]]
    else:
      delete_columns.append(col)

  return new_columns_dict, delete_columns
