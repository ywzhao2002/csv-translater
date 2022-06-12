import pandas as pd
import os
from google.cloud import translate_v2 as translate
from tqdm import tqdm

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./credential.json"
translate_client = translate.Client()

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

def translate(word):
    import six
    from google.cloud import translate_v2 as translate

    target_language = 'zh-CN'
    src_language = "en"
    if isinstance(word, six.binary_type):
        word = word.decode("utf-8")

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    result = translate_client.translate(word, target_language=target_language, source_language=src_language)
    return result["translatedText"]

if __name__ == "__main__":
    # https://cloudconvert.com/xlsx-to-csv
    src_file_path = "./power_words.csv"
    data = pd.read_csv(src_file_path)
    trg_file_path = "power_words_cn.csv"
    if os.path.exists(trg_file_path):
        os.remove(trg_file_path)
    translatedCSV = {"source": [], "target": []}
    for index, row in data.iterrows():
        translatedCSV["source"].append(str(row["source"]))
        translatedCSV["target"].append(str(translate(str(row["source"]))))
    print(translatedCSV)
    if os.path.exists(trg_file_path):
        os.remove(trg_file_path)
    with open(trg_file_path, 'w', encoding="utf-8") as f:
        f.write("%s,%s\n" % ("source", "target"))
        for source, target in tqdm(zip(translatedCSV["source"], translatedCSV["target"])):
            f.write("%s,%s\n" % (source, target))