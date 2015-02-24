==============================
depgen
==============================

依存関係にある文節をとりだす Python モジュールです。

必要なもの
============

*   Python3
*   https://github.com/kenkov/cabocha


例
===

附属する次ようなテキストファイル test.txt

::

    今日はもう疲れたので寝たい。
    最高のサイコロステーキを食べたい。

を引数にして depgen.py を実行すると

.. code-block:: bash


    $ python depgen.py test.txt
    {'left': {'id': 1, 'pos': '副詞', 'subject': 'もう', 'surface': 'もう'},
     'right': {'id': 2, 'pos': '動詞', 'subject': '疲れる', 'surface': '疲れたので'}}
    {'left': {'id': 2, 'pos': '動詞', 'subject': '疲れる', 'surface': '疲れたので'},
     'right': {'id': 3, 'pos': '動詞', 'subject': '寝る', 'surface': '寝たい。'}}
    {'left': {'id': 0, 'pos': '名詞', 'subject': '最高', 'surface': '最高の'},
     'right': {'id': 1,
               'pos': '名詞',
               'subject': 'サイコロステーキ',
               'surface': 'サイコロステーキを'}}
    {'left': {'id': 1, 'pos': '名詞', 'subject': 'サイコロステーキ', 'surface': 'サイコロステーキを'},
     'right': {'id': 2, 'pos': '動詞', 'subject': '食べる', 'surface': '食べたい。'}}

と係り受け関係にある文節情報が得られます。

Python スクリプトの中から呼び出すには

.. code-block:: python

    >>> from depgen import DepGen
    >>> dg = DepGen()
    >>> text = "サイコロステーキを食べたいです。"
    >>> dg.analyze(text)
    [{'left': {'pos': '名詞',
       'subject': 'サイコロステーキ',
       'surface': 'サイコロステーキを',
       'id': 0},
      'right': {'pos': '動詞', 'subject': '食べる', 'surface': '食べたいです。', 'id': 1}}]

のようにします。
