#! /usr/bin/env python
# coding:utf-8

from cabocha import CaboChaAnalyzer
import config


class DepGen:
    def __init__(self):
        self.analyzer = CaboChaAnalyzer()

    def check_chunk(self, chunk):
        """
        文節に使うチャンクかどうかをチェックする
        """
        stop_pos1s = config.stop_pos1s
        stop_words = config.stop_words

        return not any(
            token.pos1 in stop_pos1s or token.genkei in stop_words
            for token in chunk
        )

    def get_subject_token(self, chunk) -> ("token", "subject"):
        """
        文節の token と subject を返す

        接頭詞以外のはじめの単語が subject となる。

        ただし token.pos が名詞だった場合、subject は
        その token からはじまる連続した名詞を連結したものになる
        """
        subjects = []
        noun_flag = False
        for token in chunk:
            if token.pos in {"接頭詞"}:
                continue
            if token.pos in {"名詞"}:
                subjects.append(token)
                if not noun_flag:
                    ret_token = token
                    noun_flag = True
            elif token.pos not in {"名詞"} and noun_flag:
                break
            else:
                subjects.append(token)
                ret_token = token
                break
        if not subjects:
            subjects.append(chunk[0])
            ret_token = chunk[0]

        return (
            ret_token,
            "".join(_.surface for _ in subjects) if noun_flag else
            "".join(_.genkei for _ in subjects)
        )

    def clause_info(self, chunk, _id: int) -> dict:
        """
        文節情報の辞書を返す

        文節情報:
            * subject, 主辞
            * pos, 品詞
            * id, 文節ID
            * surface, 文節表記
            * normalized_surface, 文節標準形
                これはまだ実装していない
        """
        stoken, subject = self.get_subject_token(chunk)
        return {
            "id": _id,
            "subject": subject,
            "pos": stoken.pos,
            "surface": "".join(token.surface for token in chunk),
        }

    def clause_pairs(self, tree) -> [dict]:
        lst = []
        for _id, chunk in enumerate(tree):
            if chunk.has_next_link() and \
                    self.check_chunk(chunk) and \
                    self.check_chunk(chunk.next_link):
                left = self.clause_info(chunk, _id)
                right = self.clause_info(chunk.next_link, chunk.next_link_id)
                lst.append({
                    "left": left,
                    "right": right,
                })
        return lst

    def analyze(self, text) -> [dict]:
        tree = self.analyzer.parse(text)
        return self.clause_pairs(tree)


if __name__ == '__main__':
    import sys
    from pprint import pprint

    fd = open(sys.argv[1]) if len(sys.argv) >= 2 else sys.stdin
    dg = DepGen()

    for _id, text in enumerate(_.strip() for _ in fd):
        lst = dg.analyze(text)
        for dic in lst:
            pprint(dic)
