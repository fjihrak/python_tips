import re

class TextMasker:
    def __init__(self, nlp):
        """
        コンストラクタ
        :param nlp: spaCyやMeCabなどの言語処理パイプライン
        """
        self.nlp = nlp

    def replace_spaces_with_brackets(self, text: str) -> str:
        """
        文字列中のスペースや全角スペースをスラッシュ('/')に置換する
        """
        return re.sub(r"[ \u3000]+", "/", text)

    def analyze_and_replace(self, text: str, name=True, number=True, interjection=True):
        """
        テキストを解析し、一部の語句をマスクする。
        - 固有表現(NER)で認識されたトークン(PERSON, GPE, LOC, ORG)を[ラベル]表記に変換
        - 品詞情報(tag_)に応じてマスクや置換を行う
        :param text: 入力テキスト
        :return: (masked_text, replaced_tokens, replace_dic) のタプル
            - masked_text: マスクを施した連結文字列
            - replaced_tokens: マスク後のトークンのリスト
            - replace_dic: 元のトークンとマスク情報を持つ辞書
        """

        replace_dic = {}
        replaced_tokens = []

        # spaCy等で解析
        doc = self.nlp(text)

        # # --- 固有表現(NER)確認 (デバッグ用) ---
        # print("=== 抽出された固有表現(NER) ===")
        # for ent in doc.ents:
        #     print(f"Entity: {ent.text}\tLabel: {ent.label_}")
        # print("================================\n")

        # 1. 品詞情報に応じたマスク/置換
        for i, token in enumerate(doc):
            if name:
              if "名詞-固有名詞" in token.tag_:
                replace_dic[i] = {'token': token.text, 'replace': '[PERSON]'}
            if number:
              if "名詞-数詞" in token.tag_:
                replace_dic[i] = {'token': token.text, 'replace': '[0]'}
            if interjection:
              if "感動詞" in token.tag_:
                replace_dic[i] = {'token': token.text, 'replace': ''}
              elif "連体詞" in token.tag_:
                replace_dic[i] = {'token': token.text, 'replace': ''}

        # 2. 固有表現 (PERSON, GPE, LOC, ORG) をマスク
        for i, token in enumerate(doc):
          if name:
            if token.ent_type_ in ["PERSON", "GPE", "LOC", "ORG"]:
                print(token.text)  # デバッグ出力
                replace_dic[i] = {
                    'token': token.text,
                    'replace': f'[{token.ent_type_}]'
                }

        # 3. トークンごとに置換辞書を反映して文字列を組み立てる
        for i, token in enumerate(doc):
            if i in replace_dic:
                replaced_tokens.append(replace_dic[i]['replace'])
            else:
                replaced_tokens.append(token.text)

        # 4. 最終的なマスク文字列と、元のトークンやマスク情報を返す
        for i in range(len(replaced_tokens)):
          if i>0:
            if replaced_tokens[i] == replaced_tokens[i-1]:
              replaced_tokens[i] = ''

        masked_text = "".join(replaced_tokens)
        return masked_text, replaced_tokens, replace_dic

    def reverse(self, masked_list, replace_dic):
        """
        analyze_and_replace でマスクした結果を、元のトークンへ復元する
        :param masked_list: マスク後のトークンリスト (またはDocオブジェクトに相当)
        :param replace_dic: マスク情報 (元トークンとマスク後の対応表)
        :return: decoded: 復元された文字列のリスト
        """
        decoded = []
        for i, token in enumerate(masked_list):
            if i in replace_dic:
                decoded.append(replace_dic[i]['token'])
            else:
                decoded.append(token)

        # 必要に応じて文字列を連結して返す等、用途によって変える
        return decoded


# ===== 使い方サンプル =====
if __name__ == "__main__":
    # 例: spaCyの日本語モデルをロードして使う場合
    import spacy
    nlp = spacy.load("ja_core_news_sm")  # 日本語モデルがある場合

    # # デモ用に英語モデルやダミーを使う
    # nlp = spacy.load("en_core_web_sm")

    # TextMaskerを初期化
    masker = TextMasker(nlp=nlp)

    # テキスト例
    example_text = txt

    # マスク処理
    masked_text, replaced_tokens, replace_dic = masker.analyze_and_replace(example_text)
    print("\n--- マスク後の文字列 ---")
    print(masked_text)
    print("\n--- 置換辞書 ---")
    print(replace_dic)

    # 復元処理
    reversed_tokens = masker.reverse(replaced_tokens, replace_dic)
    reversed_text = "".join(reversed_tokens)
    print("\n--- 復元後の文字列 ---")
    print(reversed_text)
