# KSU Fucker
京都産業大学の学生データベース（工事中）です。[](WEBサイト[KSUFucker](http://ksufucker.heroku.com)にアクセスすると、データベース検索が可能です。)

## クローラー
学生データベースは、主に以下のURLを再帰的に辿っていき、クローリングして、データを収集することで作成されています。

- http://www.cc.kyoto-su.ac.jp/~gX[学生証番号]/
- http://www.cse.kyoto-su.ac.jp/~gX[学生証番号]/

実際のところは、一度クローリングした後に、高頻度に出現するページを再度クロールすることによって、できる限り多くのデータを入手することに成功しています。詳しいダウンロード元は、`./analyze/dlconfig.py`に記入されています。

### クローラーの実行方法
クローラーのプログラムは、`analyze/`ディレクトリの中に入っています。以下のコマンドを実行すると、`./analyze/dlconfig.py`のダウンロードコンフィグ情報を元にクローリングが行われます。

	$ cd analyze/
	$ python main.py

ダウンロードされたデータは、`www.cse.kyoto-su.ac.jp/`と`www.cc.kyoto-su.ac.jp/`のフォルダ内にダウンロードされ、`analyze/DB/cse_student_DB.db`に情報が記録されます。

## 動作環境
- サイト
	- メイン言語: PHP
	- WEBサーバー: Apache
- クローラー
	- メイン言語: Python
	- フレームワーク: dlib, MeCab, sqlite3, skimage, numpy, scipy



