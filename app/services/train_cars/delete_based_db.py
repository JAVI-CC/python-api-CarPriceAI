import pandas as pd
from pandas import DataFrame
from ...db import engine
from ...enums.columns_car import ColumnsCar as EnumColumnsCar

def delete_duplicates_based_db(cars_df: DataFrame, is_merge: bool) -> DataFrame:
  from ...services import get_all_cars_df

  cars_sql_df = get_all_cars_df(engine)

  if not is_merge:
    cars_df = cars_df.loc[
      cars_df[EnumColumnsCar.ALL.value]
      .isin(cars_sql_df.to_dict(orient='list'))
      .all(axis=1) is False
    ]
  else:
    # I merge the 2 dataframes in case the algorithm I use
    # (for example RandomForest) does not allow training the data incrementally.
    cars_df = pd.concat([cars_df, cars_sql_df], ignore_index=True)
    cars_df.drop_duplicates(inplace=True)
    cars_df = cars_df.reset_index(drop=True)

  return cars_df


def delete_rows_alredy_exists_db(cars_df: DataFrame) -> DataFrame:
  from ...services import get_all_cars_df

  cars_sql_df = get_all_cars_df(engine)

  new_cars_df = cars_df.loc[cars_df.index.isin(cars_sql_df.index) == False]

  return new_cars_df
