import warnings
from pandas import DataFrame
from ...enums.columns_car import ColumnsCar as EnumColumnsCar


# Disable all messages warnings
warnings.filterwarnings("ignore")


def null_data_handling(cars_df: DataFrame) -> DataFrame:
  cars_df = brands_null_data(cars_df)
  cars_df = models_null_data(cars_df)
  cars_df = fuels_null_data(cars_df)
  cars_df = years_null_data(cars_df)
  cars_df = mileage_null_data(cars_df)
  cars_df = horsepower_null_data(cars_df)
  cars_df = doors_null_data(cars_df)
  cars_df = transmission_null_data(cars_df)
  cars_df = color_null_data(cars_df)
  cars_df = is_dealer_null_data(cars_df)
  cars_df = price_null_data(cars_df)

  cars_df = cars_df.astype({'brand': str,
                            'model': str,
                            'fuel': str,
                            'year': int,
                            'mileage': int,
                            'horsepower': int,
                            'doors': int,
                            'transmission': str,
                            'color': str,
                            'is_dealer': bool,
                            'price': int})

  columns_str = EnumColumnsCar.STR.value

  for col in columns_str:
    cars_df[col] = cars_df[col].str.strip()
    cars_df[col] = cars_df[col].str.capitalize()

  return cars_df


def brands_null_data(cars_df: DataFrame) -> DataFrame:
  cars_df.dropna(subset=['brand'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df


def models_null_data(cars_df: DataFrame) -> DataFrame:
  cars_without_model = cars_df[cars_df['model'].isnull()]

  for idx, car in cars_without_model.iterrows():
    model_filter = cars_df[
        (cars_df['brand'] == car['brand']) &
        (cars_df['fuel'] == car['fuel']) &
        (cars_df['doors'] == car['doors']) &
        (cars_df['year'] == car['year']) &
        (cars_df['transmission'] == car['transmission'])
    ]

    model_most_frequents = model_filter['model'].mode()

    if not model_most_frequents.empty:
      cars_df.loc[idx, 'model'] = model_most_frequents[0]

  cars_df.dropna(subset=['model'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df


def fuels_null_data(cars_df: DataFrame) -> DataFrame:
  cars_without_fuel = cars_df[cars_df['fuel'].isnull()]

  for idx, car in cars_without_fuel.iterrows():
    fuel_filter = cars_df[
        (cars_df['brand'] == car['brand']) &
        (cars_df['model'] == car['model']) &
        (cars_df['doors'] == car['doors']) &
        (cars_df['year'] == car['year']) &
        (cars_df['transmission'] == car['transmission'])
    ]

    fuel_most_frequents = fuel_filter['fuel'].mode()

    if not fuel_most_frequents.empty:
      cars_df.loc[idx, 'fuel'] = fuel_most_frequents[0]

  cars_df.dropna(subset=['fuel'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df


def years_null_data(cars_df: DataFrame) -> DataFrame:
  cars_without_year = cars_df[cars_df['year'].isnull()]

  for idx, car in cars_without_year.iterrows():
    year_filter = cars_df[
        (cars_df['brand'] == car['brand']) &
        (cars_df['model'] == car['model']) &
        (cars_df['fuel'] == car['fuel']) &
        (cars_df['doors'] == car['doors']) &
        (cars_df['transmission'] == car['transmission'])
    ]

    year_most_frequents = year_filter['year'].mode()

    if not year_most_frequents.empty:
      cars_df.loc[idx, 'year'] = year_most_frequents[0]

  cars_df.dropna(subset=['year'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df


def mileage_null_data(cars_df: DataFrame) -> DataFrame:
  cars_df.dropna(subset=['mileage'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df


def horsepower_null_data(cars_df: DataFrame) -> DataFrame:
  cars_without_horsepower = cars_df[cars_df['horsepower'].isnull()]

  for idx, car in cars_without_horsepower.iterrows():
    horsepower_filter = cars_df[
        (cars_df['brand'] == car['brand']) &
        (cars_df['model'] == car['model']) &
        (cars_df['fuel'] == car['fuel']) &
        (cars_df['doors'] == car['doors']) &
        (cars_df['year'] == car['year']) &
        (cars_df['transmission'] == car['transmission'])
    ]

    horsepower_most_frequents = horsepower_filter['horsepower'].mode()

    if not horsepower_most_frequents.empty:
      cars_horsepower = horsepower_filter.mean(numeric_only=True)['horsepower']
      cars_df.loc[idx, 'horsepower'] = cars_horsepower

  cars_df.dropna(subset=['horsepower'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df


def doors_null_data(cars_df: DataFrame) -> DataFrame:
  cars_without_doors = cars_df[cars_df['doors'].isnull()]

  for idx, car in cars_without_doors.iterrows():
    doors_filter = cars_df[
        (cars_df['brand'] == car['brand']) &
        (cars_df['model'] == car['model']) &
        (cars_df['fuel'] == car['fuel']) &
        (cars_df['year'] == car['year']) &
        (cars_df['transmission'] == car['transmission'])
    ]

    doors_most_frequents = doors_filter['doors'].mode()

    if not doors_most_frequents.empty:
      cars_df.loc[idx, 'doors'] = doors_most_frequents[0]

  cars_df.dropna(subset=['doors'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df


def transmission_null_data(cars_df: DataFrame) -> DataFrame:
  cars_without_transmission = cars_df[cars_df['transmission'].isnull()]

  for idx, car in cars_without_transmission.iterrows():
    transmission_filter = cars_df[
        (cars_df['brand'] == car['brand']) &
        (cars_df['model'] == car['model']) &
        (cars_df['fuel'] == car['fuel']) &
        (cars_df['year'] == car['year']) &
        (cars_df['doors'] == car['doors'])
    ]

    transmission_most_frequents = transmission_filter['transmission'].mode()

    if not transmission_most_frequents.empty:
      cars_df.loc[idx, 'transmission'] = transmission_most_frequents[0]

  cars_df.dropna(subset=['transmission'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df


def color_null_data(cars_df: DataFrame) -> DataFrame:
  cars_without_color = cars_df[cars_df['color'].isnull()]

  for idx, car in cars_without_color.iterrows():
    color_filter = cars_df[
        (cars_df['brand'] == car['brand']) &
        (cars_df['model'] == car['model']) &
        (cars_df['fuel'] == car['fuel']) &
        (cars_df['year'] == car['year']) &
        (cars_df['transmission'] == car['transmission']) &
        (cars_df['doors'] == car['doors'])
    ]

    color_most_frequents = color_filter['color'].mode()

    if not color_most_frequents.empty:
      cars_df.loc[idx, 'color'] = color_most_frequents[0]

  cars_df.dropna(subset=['color'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df


def is_dealer_null_data(cars_df: DataFrame) -> DataFrame:
  is_dealer_most_frequents = cars_df['is_dealer'].mode()
  cars_df['is_dealer'].fillna(is_dealer_most_frequents[0], inplace=True)

  return cars_df


def price_null_data(cars_df: DataFrame) -> DataFrame:
  cars_df.dropna(subset=['price'], inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  return cars_df
