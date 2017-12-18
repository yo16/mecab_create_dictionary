# MakeMecabUserDictionary

このプログラムは、MeCabのユーザ辞書ファイル(dicファイル)を作成して
適切なフォルダへ格納するものです。
ユーザ辞書ファイルの元となるファイルは、ExcelファイルとTextファイルで、
事前に用事する必要があります。

## 対応する書式
1. Excelファイル
  1.1. `単語 | ヨミガナ`の形式
  1.2 `単語`だけの形式
2. テキストファイル(UTF-8)
  2.1. `単語,ヨミガナ`のCSV形式
  2.2. `単語`だけの形式

## 処理概要
1. すべての入力されたファイルから、単語とヨミガナを抽出して、リストへ追加する
2. リストをCSVファイルへ出力する
  - CSVファイルの文字コードは、`shift_jis(cp932)`で作成する
3. CSVファイルからMeCabのユーザ辞書ファイルを作成する
  - 内部的にMeCabのプログラムを使用する
4. 辞書ファイルをMeCabフォルダへ格納し、設定ファイルへユーザ辞書を使うよう記述する
  - 格納場所:`(MeCabインストールフォルダ)\dic\userdic`   
  - 記述するファイル:`(MeCabインストールフォルダ)\etc\mecabrc`

