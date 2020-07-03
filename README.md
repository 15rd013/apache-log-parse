# apache-log-parse

## 概要
apacheのデフォルトのログフォーマットのひとつであるcombined形式で書かれたログファイルから、各時間帯毎のアクセス件数とリモートホスト別のアクセス件数を集計して表示します。

## 必要条件
Python3.6以降が必要です。
Pythonのサードパーティ製モジュールであるparseが必要です。

## 使いかた
apache-log-parse.pyをダウンロードします。
コマンドラインから実行します。

例: `python3 apache-log-parse.py /var/log/httpd/access_log`

ファイルは複数入力できます。

例: `python3 apache-log-parse.py /var/log/httpd/access_log1 /var/log/httpd/access_log2`

-bオプションで２つの日付から期間を指定できます。

例: `python3 apache-log-parse.py -b 2010-01-01 2020-01-01 /var/log/httpd/access_log`

-lオプションでその日付から現在までの期間を指定できます。

例: `python3 apache-log-parse.py -l 2010-01-01 /var/log/httpd/access_log`

-hオプションでヘルプを見ることができます。

例: `python3 apache-log-parse.py -h`
