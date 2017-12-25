# coding: utf-8

# MakeMecabUserDictionary
# 2017 (c) yo16

import sys
import os
import shutil
import readWordDefXxx
import codecs
from myLogger import debug, info
import subprocess
import re


def main(args):
    # <<to do>>下記は 引数で受け取ることを検討する
    # 最終的に作成する辞書ファイル名
    dicFileName = 'userDictionary.dic'
    # MeCabのパス
    mecabDirPath = 'C:\\Program Files (x86)\\MeCab'

    # 単語とヨミガナのリスト
    words = []
    yomis = []


    # 引数からファイルが格納されているフォルダを得て
    # その中に入っているファイルパスを得る
    files = []
    for param in args:
        if os.path.exists(param) and os.path.isdir(param):
            dirfiles = os.listdir(param+'/')
            for oneFile in dirfiles:
                files.append(param+'/'+oneFile)
                #debug(param+'/'+oneFile)
    if len(files)==0:
        return 1

    # ファイルを読んで、単語リストへ追加する
    #  - 拡張子ごとにリストへ格納する処理選ぶ
    for filePath in files:
        ext = filePath.rsplit('.',1)[1]
        if ext=='xls' or ext=='xlsx':
            readWordDefXxx.readWordDefExcel( filePath, words, yomis )
        elif ext=='txt':
            readWordDefXxx.readWordDefText( filePath, words, yomis )
        #debug(len(words))

    # 単語リストから辞書登録用のCSVファイルを作成する
    csvFilePath = os.getcwd() + '\\' + 'tmpCsv.csv'
    list2Csv(words, yomis, csvFilePath)

    # CSVファイルから、辞書ファイルを作成する
    dicFilePath = os.getcwd() + '\\' + dicFileName
    csv2UserDic(csvFilePath, mecabDirPath, dicFilePath)

    # 辞書ファイルをMeCabフォルダへ格納し、
    # 設定ファイルを書き換える
    setEnableUserDic(mecabDirPath, dicFilePath)

    return 0


# 単語リストから辞書登録用のCSVファイルを作成する
def list2Csv( wl, yl, csvFilePath ):
    f = codecs.open(csvFilePath, mode='w', encoding='cp932')
    for (w,y) in zip(wl, yl):
        if len(y)==0:
            y='シンヨウゴ'
        outstr = u'{0},1285,1285,10,名詞,新用語,*,*,*,*,{0},{1},{1}\n'.format(w,y)
        f.write(outstr)
    f.close()

    return 0


# CSVファイルから、辞書ファイルを作成する
def csv2UserDic( csvFilePath, mecabDirPath, dicFilePath ):
    # MeCab辞書フォルダのパス
    mecabDicDirPath = mecabDirPath + '\\dic\\ipadic'
    
    # MeCab辞書を作るモジュールのパス
    mecabLdm = mecabDirPath + '\\bin\\mecab-dict-index.exe'
    
    
    info("Create MeCab dictionary file. -start-")
    # 辞書ファイルを作成
    #debug('LDM:'+mecabLdm)
    #debug('dic:'+dicFilePath)
    #debug('csv:'+csvFilePath)
    subprocess.call([mecabLdm, '-d', mecabDicDirPath, '-u', dicFilePath, '-t', 'utf-8', csvFilePath])
    info("Create MeCab dictionary file. -end-")
    
    return 0


# 辞書ファイルをMeCabフォルダへ格納し、
# 設定ファイルを書き換える
def setEnableUserDic( mecabDirPath, dicFilePath ):
    # 辞書ファイル名
    dicFileName = dicFilePath[dicFilePath.rfind('\\')+1:]
    
    # 辞書ファイルをコピー
    newDicFilePath = mecabDirPath + '\\dic\\userdic\\' + dicFileName
    shutil.copyfile( dicFilePath, newDicFilePath )
    
    
    # 設定ファイル内のuserdicで設定されている項目を抜き出す
    valUserDic = ''
    rcFilePath = mecabDirPath+'\\etc\\mecabrc'
    f = open(rcFilePath, 'r')
    for line in f:
        m = re.match(r"^userdic *= *(.*)$", line)
        if m:
            valUserDic = m.group(1)
    f.close()
    #debug( 'userDic:'+valUserDic )
    
    # 新しいmecabrcの作成
    if len(valUserDic)==0:
        # userdicの行がない場合
        # 追記
        f = open( rcFilePath, 'a')
        f.write('\nuserdic = "' + mecabDirPath + '\\dic\\userdic\\' + dicFileName + '\n')
        f.close()
        
    else:
        # 今回のファイルが登録済みか未登録かを判断し、未登録の場合は追加
        registedDictionary = False
        configDicFiles = valUserDic.split(',')
        for configFile in configDicFiles:
            # スペースとついでに"も除去
            configFile = configFile.strip(' \t"')
            #debug('config:'+configFile)
            if configFile == newDicFilePath :
                registedDictionary = True
        
        if not registedDictionary:
            # debug('newDicFile:'+newDicFilePath)
            valUserDic += ', "' + newDicFilePath + '"'
            # debug('valUserDic:'+valUserDic)
            
            # 元ファイルを見ながら、新しいファイルを作成
            workFile = os.getcwd() + '\\mecabrc_work'
            fin = open( rcFilePath, 'r' )
            fout = open( workFile, 'w')
            for line_in in fin:
                m = re.match(r"^userdic *= *(.*)([\r\n]{0,2})$", line_in)
                if m:
                    line_out = 'userdic = ' + valUserDic
                else:
                    line_out = line_in
                fout.write(line_out)
            fin.close()
            fout.close()
            
            # 元ファイルをリネームして、新しいファイルをコピー
            rcFilePathBack = rcFilePath + '_back'
            shutil.move(rcFilePath, rcFilePathBack)
            shutil.copy(workFile, mecabDirPath + '\\etc\\mecabrc')
            # 元ファイルを削除
            os.remove(rcFilePathBack)
    
    return 0



if __name__ == '__main__':
    sys.exit( main(sys.argv[1:]) )
