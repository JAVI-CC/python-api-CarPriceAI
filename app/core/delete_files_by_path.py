
import shutil
from os import path as os_path, listdir, remove


def delete_files_by_path(path):
  for item in listdir(path):
    item_path = os_path.join(path, item)

    if item != '.gitkeep':
      try:
        if os_path.isfile(item_path):
          remove(item_path)
        elif os_path.isdir(item_path):
          shutil.rmtree(item_path)
      except (ValueError, TypeError):
        pass
