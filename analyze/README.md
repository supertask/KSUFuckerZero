学生ページ用クローラー
====
主に以下のURLを再帰的に辿っていき、クローリングして、データを収集します。

- http://www.cc.kyoto-su.ac.jp/~gX[学生証番号]/
- http://www.cse.kyoto-su.ac.jp/~gX[学生証番号]/

実際のところは、一度クローリングした後に、高頻度に出現するページを再度クロールすることによって、できる限り多くのデータを入手することに成功しています。詳しいダウンロード元は、`./analyze/dlconfig.py`に記入されています。

## クローラーの実行方法
以下のコマンドを実行すると、`./analyze/dlconfig.py`のダウンロードコンフィグ情報を元にクローリングが行われます。

	$ python main.py

ダウンロードされたデータは、`www.cse.kyoto-su.ac.jp/`と`www.cc.kyoto-su.ac.jp/`のフォルダ内にダウンロードされ、`analyze/DB/cse_student_DB.db`に情報が記録されます。尚、クローリングにかかる時間は、およそ3~4時間（最適化はしていない）です。ちなみに、他に優先してやることがあり、オプションなどは用意していないため、**`main.py`を使用する際はコードを読んで編集が必要ですm(_ _)m！**

## ツールキット（Tool.py）
Tool.pyは、以下のような役割があります。これは、オプションとして`main.py`にてダウンロードが終わった後に使うと、ストレージを節約したりするなどに役立ちます。

- 無駄なデータ（W3Cの検査結果など）を見つける
- 高頻度に出現するページ（課題ページなど）を見つける
- リンク先の多いスパムサイトを特定する（リンクが多すぎると検索に時間がかかるため）

## 解析データの保存先
`DB/`の中にそれぞれ解析したデータが保存されます。データベースの種類は以下の3つです。

- 推測した学生証番号 (`estimated_cse_student_DB.db`)
- 解析した学生情報 (`cse_student_DB.db`)
- 検索エンジンのためのキーワード辞書 (`keywords_DB.db`)

`cse_student_DB.db`と`keywords_DB.db`に関しては、[KSUFucker検索エンジン](https://github.com/supertask/KSUFucker)上で使われます。

## 動作環境
- メイン言語: Python
- フレームワーク: dlib, MeCab, sqlite3, skimage, numpy, scipy
- コマンド: wget

