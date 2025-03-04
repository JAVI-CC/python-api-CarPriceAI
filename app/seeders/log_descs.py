import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..db import engine
from ..models import LogDesc as ModelLogDesc
from ..schemas import LogDescCreateSeeder as SchemaLogDescCreateSeeder


def generate_seeder() -> None:
  with open("./app/seeders/data/log_descs.json", encoding="UTF-8") as json_file:

    for log_desc in json.load(json_file):

      log_desc = SchemaLogDescCreateSeeder(**log_desc)

      with Session(engine) as db:
        db_log_desc = ModelLogDesc(**log_desc.model_dump())
        db.add(db_log_desc)

        try:
          db.commit()
        except SQLAlchemyError:
          pass
          # 1062, Duplicate entry

    json_file.close()
