from csv import Sniffer
import chardet


def csv_find_encoding_and_delimiter(contents: str) -> str:

  charset = chardet.detect(contents)

  sniffer = Sniffer()

  delimiter = sniffer.sniff(
    contents.decode(charset['encoding'])
  ).delimiter

  return charset['encoding'], delimiter
