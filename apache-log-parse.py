#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime, date, time
from parse import compile

#Apacheのログのcombinedフォーマット
LOG_FORMAT = "{host} {longname} {user} [{dt:th}] \"{request}\" {status:d} {bytes} \"{referer}\" \"{agent}\""

#argparseでdate型として受け取るための関数
def datetype(date_str):
    try:
        return date.fromisoformat(date_str)
    #YYYY-MM-DDでなければ例外
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e) + " Enter in iso format. Example: 2017-04-01")

if __name__ == "__main__":
    #コマンドライン引数の設定
    #プログラムの説明を引数に入れてパーサを作成
    parser = argparse.ArgumentParser(description="Parse Apache logs.")
    #--betweenと--latestはどちらか一方しか受け取らない
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-b", "--between", nargs=2, type=datetype, help="Search within two specified periods. Example: -b 2017-04-01 2017-04-30 .")
    group.add_argument("-l", "--latest", type=datetype, help="Search from specified period to present. Example: -l 2017-04-01 .")
    #ファイルパスを受け取る(自動でオープンされる)
    parser.add_argument("file", nargs='+', type=argparse.FileType("r"), help="Enter the file path. Multiple allowed.")
    #パースを実行してargsに結果を代入
    args = parser.parse_args()

    #--betweenオプションが指定された場合
    if args.between is not None:
        #argsのdate型データをdatetime型データに変換して検索期間のスタートとエンドにそれぞれ代入
        start_dt = datetime.combine(args.between[0], time())
        end_dt = datetime.combine(args.between[1], time())
        #スタートとエンドが逆なら入れ替え
        if start_dt < end_dt:
            tmp = end_dt
            end_dt = start_dt
            start_dt = tmp
    #--latestオプションが指定された場合
    elif args.latest is not None:
        #スタートは指定された日付、エンドは現在
        start_dt = datetime.combine(args.latest, time())
        end_dt = datetime.now()
    #オプションが指定されなかったらスタートとエンドはNone
    else:
        start_dt = None
        end_dt = None

    hourly_count = [0] * 24 #時間毎の集計に使う長さ24の整数のリスト
    host_count = dict() #ホスト毎のアクセス数の集計に使う辞書
    parser = compile(LOG_FORMAT) #ログの一行を解析するためのパーサ

    #二重ループで各ファイルの各行毎に回す
    for f in args.file:
        for line in f:
            #パース実行
            result = parser.parse(line)
            #結果がNoneならログファイルのフォーマットに問題あり
            if result is None:
                raise ValueError("Invalid log file format.")
            #parseで作ったdatetime型にタイムゾーンの情報が含まれているので簡単のために消す
            current_dt = result["dt"].replace(tzinfo=None)
            #検索期間のスタートとエンドが指定されているか
            if start_dt is not None and end_dt is not None:
                #スタートより前かエンド以降ならこのループは無視
                if start_dt > current_dt or end_dt <= current_dt:
                    continue
            #時間帯のアクセス数を1カウント
            hourly_count[current_dt.hour] += 1
            #辞書にホスト名が無ければ追加し1カウント
            if not result["host"] in host_count:
                host_count[result["host"]] = 0
            host_count[result["host"]] += 1

    #結果の表示
    print("Number of accesses by hour.")
    for i,c in enumerate(hourly_count):
        print("{:02d}-{:02d}:{}".format(i, i+1, c))
    print("List of remote hosts order by access count.")
    #辞書からアクセス数順にソートされたリストを作成
    host_count_sorted = sorted(host_count.items(), key=lambda x:x[1], reverse=True)
    for h,c in host_count_sorted:
        print("{:15s}:{}".format(h, c))