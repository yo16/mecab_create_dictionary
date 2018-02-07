# coding: utf-8

# readWordDefXxx
# 2017 (c) yo16

import sys
import xlrd
import codecs
from myLogger import debug


# 単語が定義されたExcelファイルから
# 単語とヨミガナを取得して、リストへ追加する
def readWordDefExcel( filePath, wl, yl ):
	debug('ExcelFile:'+filePath)
	book = xlrd.open_workbook(filePath)
	for sindex in range( book.nsheets ):
		sht = book.sheet_by_index(sindex)
		for row in range(sht.nrows):
			# wlにまだ登録されていなかったら登録する
			if sht.cell(row, 0) not in wl:
				wl.append( sht.cell(row,0).value )
				if sht.ncols > 1:
					yl.append( sht.cell(row,1).value )
				else:
					yl.append( '' )

	return 0

# 単語が定義されたテキストファイルから
# 単語とヨミガナを取得して、リストへ追加する
#  - codecはutf-8固定
def readWordDefText( filePath, wl, yl ):
	debug('TextFile:'+filePath)
	f = codecs.open(filePath, 'r', encoding='utf-8')
	for line in f:
		line = line.replace('[\r\n]', '')
		ary = line.split(',')
		# wlにまだ登録されていなかったら登録する
		if ary[0] not in wl:
			wl.append( ary[0] )
			if len(ary) > 1:
				yl.append( ary[1] )
			else:
				yl.append( '' )
	f.close()

	return 0
