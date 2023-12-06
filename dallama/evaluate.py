import os
from collections import Counter
from typing import List

import nltk
import pandas as pd
import phunspell
from langdetect import LangDetectException, detect

# def detect_language(df):
#     df =


def read_csv():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    csv_path = os.path.join(parent_dir, "data", "overview.csv")
    df = pd.read_csv(csv_path)

    return df


def overwrite_csv(df):
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    csv_path = os.path.join(parent_dir, "data", "overview.csv")

    df.to_csv(csv_path)


def detect_language_distribution(lines: List[str]):
    counts = []
    for line in lines:
        try:
            counts.append(detect(line))
        except LangDetectException:
            continue

    # TODO: return a distribution
    res = Counter(counts)

    return dict(res)


def split_text(text: str) -> List[str]:
    lines = text.split("\n")
    return lines


def get_results_columns():
    df = read_csv()

    res = []

    for i in df.columns:
        if str(i).startswith("res_"):
            res.append(i)

    return res


def get_misspellings(text: str):
    pspell = phunspell.Phunspell("da_DK")
    misspelled = pspell.lookup_list(text.split(" "))
    return misspelled


def lookup_words(words: List[str]):
    pspell = phunspell.Phunspell("da_DK")
    return pspell.lookup_list(words)


# This is way of evaluationg the text is probably a little imprecisise,
# Tokenization is better


# def evaluate():
#     df = read_csv()
#     res_columns = get_results_columns()
#     for res_column in res_columns:
#         eval_col_name = res_column.replace("res_", "eval_")
#         misspellings = []
#         for text in df[res_column]:
#             # print(text)
#             misspellings.append(
#                 get_misspellings(
#                     text.replace("\n", " ")
#                     .replace(".", "")
#                     .replace("\t", "")
#                     .replace(",", "")
#                     .replace(")", "")
#                     .replace("(", "")
#                     .replace("?", "")
#                     .replace("*", "")
#                 )
#             )
#         df[eval_col_name] = misspellings

#     df.to_csv("foo.csv")


def evaluate():
    nltk.download("punkt")
    df = read_csv()
    res_columns = get_results_columns()
    for res_column in res_columns:
        eval_col_name = res_column.replace("res_", "eval_")
        misspellings = []

        for text in df[res_column]:
            tokens = nltk.word_tokenize(text)
            foo = [token for token in tokens if token.isalpha()]
            foo = lookup_words(foo)
            misspellings.append(foo)

        df[eval_col_name] = misspellings

    overwrite_csv(df)
    # df.to_csv("overview_evaluated.csv")
