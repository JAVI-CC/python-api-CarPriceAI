# Order columns important!
COLUMN_VARIANTS = {
    'brand': ['marca', 'brand', 'marca de coche', 'marca vehículo', 'make', 'make car', 'make vehicle', 'fabricante', 'marque', 'marca automobile', 'make automobile'],
    'model': ['modelo', 'model', 'modèle', 'modèle vehicle', 'model car', 'model vehicle', 'modelo vehículo', 'modelo coche', 'modèle automobile'],
    'fuel': ['combustible', 'fuel', 'combustible vehicle', 'combustible coche', 'combustible automòbil', 'fuel type', 'type de carburant', 'tipus de combustible', 'carburant'],
    'year': ['año', 'year', 'any', 'année', 'ano', 'année modèle', 'data de fabricació', 'any vehicle', 'année de fabrication'],
    'mileage': ['kilometraje', 'mileage', 'kilometratge', 'kilometrage', 'kms', 'distancia', 'distancia recorrida', 'distancia total', 'kilometratge vehicle', 'millas', 'distance parcourue'],
    'horsepower': ['potencia', 'cavalls', 'horsepower', 'horse', 'horses' 'cv', 'cavalos', 'caballo', 'caballos', 'potència', 'cavalier', 'chiffre de puissance', 'puissance', 'vitesse moteur', 'horse power', 'potenza'],
    'doors': ['puertas', 'doors', 'portes', 'pòrtes', 'car doors', 'vehículo puertas', 'portes vehicule', 'doors car', 'nombre de portes', 'nombre de puertas'],
    'transmission': ['transmisión', 'transmissio', 'transmisio', 'transmision', 'transmission', 'caixa de canvis', 'caixa de canvis automàtic', 'gearbox', 'transmission automatique', 'transmissió', 'caixa de velocitats', 'caixa de canvis vehicle', 'gearbox vehicle'],
    'color': ['color', 'color vehicle', 'color automóvil', 'colore', 'color coche', 'color voiture', 'coulur', 'color pintura', 'color vehiculo', 'color carro', 'tinte', 'tonalitat'],
    'is_dealer': ['es_concesionario', 'is_dealer', 'concesionario', 'es_concessionari', 'vendedor', 'concessionnaire', 'concessionari', 'is_concessionari', 'distribuidor', 'distribuïdor'],
    'price': ['precio', 'price', 'preu', 'preu vehicle', 'precio total', 'coste', 'coste vehículo', 'preço', 'prix', 'cost', 'cost de l\'automòbil', 'precio coche', 'preu cotxe']
}


def structure_columns(df_columns: list):

  new_columns_dict = {}
  delete_columns = []

  for col_csv in df_columns:
    is_find_column = False

    for col, variants in COLUMN_VARIANTS.items():
      is_find_column = col_csv.strip().lower() in variants
      if is_find_column:
        new_columns_dict[col_csv] = col
        break

    if not is_find_column:
      delete_columns.append(col_csv)

  return new_columns_dict, delete_columns
