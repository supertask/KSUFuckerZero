# KSU Fucker Zero
京都産業大学の学生データベースです．Webサイト[KSUFuckerZero](http://18.217.17.203/)にアクセスすると、データベース検索が可能です。ちなみに，元となったサイトは[KSUFucker](http://ksufucker.herokuapp.com/)です．ただ，バグが多々あります．
![KSU Fucker](./images/ksufucker_screen.png)

## KSU Fuckerとの違い
- herokuサーバ -> AWSサーバ
- 顔認識をするライブラリdlibを導入していません（開発期間が短くAWSへの移行に時間を割けなかったため）
- クローラーをWeb上から操作可能に（analyze/controller.php），一番大変でした．少しバグってます．
- CSEドメインはクローリングできますが，今回はCCドメインはconfigでオフにしています（アクセス制限があるので）

## クローラー
学生データベースは、主に以下のURLを再帰的に辿っていき、クローリングして、データを収集することで作成されています．

- http://www.cse.kyoto-su.ac.jp/~gX[学生証番号]/

実際のところは、一度クローリングした後に、高頻度に出現する相対パスを再度クロールすることによって、できる限り多くのデータを入手することに成功しています。詳しいダウンロード元は、`./analyze/dlconfig.py`に記入されています。

クローラーの詳しい情報は、[こちら](https://github.com/supertask/KSUFuckerZero/tree/master/analyze)のソースコードとREADMMEをご覧ください。


## 動作環境
- サイト
	- メイン言語: PHP
	- WEBサーバー: Apache
- クローラー
	- メイン言語: Python
	- フレームワーク:MeCab, MySQL
    - コマンド: wget
