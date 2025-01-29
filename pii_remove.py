# !pip install spacy
# !python -m spacy download ja_core_news_sm

import re
import spacy


def replace_spaces_with_brackets(text: str) -> str:
    """
    テキスト中に含まれる半角スペースと全角スペースを検出し、
    それらをすべて"/"に置き換える。
    """
    return re.sub(r"[ \u3000]+", "/", text)

def analyze_and_replace(text: str, nlp) -> str:
    text = replace_spaces_with_brackets(text)
    doc1 = nlp(text)

    replaced_tokens1 = []
    for token in doc1:
        # TAGごとに置換を行う
        if "接頭辞" in token.tag_:
            replaced_tokens1.append("")
        elif "感動詞" in token.tag_:
            replaced_tokens1.append("")
        elif "連体詞" in token.tag_:
            replaced_tokens1.append("")
        else:
            # それ以外のTAGはそのまま残す
            replaced_tokens1.append(token.text)

    intermediate_text1 = "".join(replaced_tokens1)
    
    print("=== 接頭辞・感動詞・連体詞を除去、スペースを/に置換 ===")
    print(intermediate_text1)
    print("================================\n")

    doc2 = nlp(intermediate_text1)

    # --- 固有表現(NER)確認 ---
    print("=== 抽出された固有表現(NER) ===")
    for ent in doc2.ents:
        print(f"Entity: {ent.text}\tLabel: {ent.label_}")
    print("================================\n")

    chars = list(doc2.text)
    for ent in doc2.ents:
        if ent.label_ in ["PERSON", "GPE", "LOC", "ORG"]:
            for i in range(ent.start_char, ent.end_char):
                chars[i] = "[PERSON]"

    intermediate_text2 = "".join(chars)

    print("=== NERを[PERSON]に置換 ===")
    print(intermediate_text2)
    print("================================\n")

    doc3 = nlp(intermediate_text2)

    replaced_tokens3 = []
    for token in doc3:
        # TAGごとに置換を行う
        if "名詞-固有名詞" in token.tag_:
            replaced_tokens3.append("[PERSON]")
        elif "名詞-数詞" in token.tag_:
            replaced_tokens3.append("[0]")
        else:
            # それ以外のTAGはそのまま残す
            replaced_tokens3.append(token.text)

    # 日本語ではトークンの間にスペースを入れないことが多いのでそのまま結合
    # 必要に応じて " ".join(replaced_tokens) や改行など使い分けてください
    masked_text = "".join(replaced_tokens3)
    return masked_text

nlp = spacy.load("ja_core_news_sm")

print("=== 元の文章 ===")
print(txt)

replaced = analyze_and_replace(txt, nlp)

print("=== ルールを加えた最終的な置換後の文章 ===")
print(replaced)