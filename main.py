# MIT License
#
# Copyright (c) 2022 Yuu@n138
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import json
import hashlib
import time

ini_array0 = {}
ini_array0["ver"] = 1.2
ini_array0["debug"] = False
ini_array0["exportToDir"] = './'
ini_array0["consoleLog"] = True
ini_array0["consoleLogRule"] = '{TIME}-console.log'
ini_array1 = {}
ini_array1.update(ini_array0)

console_print = ''
console_print_temp = ''

# 設定ファイルが無いとき作成
ini_file = os.path.basename(sys.argv[0])
ini_file = os.path.splitext(os.path.basename(ini_file))[0] + '.json'
if not(os.path.isfile(ini_file)):
    console_print_temp = 'E: No such config.'
    print(console_print_temp, file=sys.stderr)

    try:
        with open(ini_file, encoding='UTF-8', mode='w') as fp:
            fp.write(json.dumps(ini_array0))

        console_print_temp = 'N: Creating... file=\'' + ini_file + '\''
        print(console_print_temp, file=sys.stderr)

    except Exception as e:
        console_print_temp = 'E: ' + str(type(e)) + ' ' + str(e)
        print(console_print_temp, file=sys.stderr)

    time.sleep(5)
    sys.exit(1)

# 設定読み込み
try:
    with open(ini_file, encoding='UTF-8', mode='r') as fp:
        ini_temp = fp.read()
        ini_array1.update(json.loads(ini_temp))

except json.decoder.JSONDecodeError as e:
    console_print_temp = 'E: ' + str(type(e)) + ' ' + str(e)
    print(console_print_temp, file=sys.stderr)

    time.sleep(5)
    sys.exit(1)

# バージョンチェック
if ini_array0["ver"] != ini_array1["ver"]:
    console_print_temp = 'E: Mismatch config version.'
    print(console_print_temp, file=sys.stderr)

    time.sleep(5)
    sys.exit(1)

# 変数値正規化
debug = ini_array1["debug"]
ini_array1["consoleLogRule"] = ini_array1["consoleLogRule"].replace('{TIME}', str(int(time.time())))

# ライン引数からファイルリスト生成
argv = sys.argv
argv.pop(0)
argc = len(sys.argv)
if not(argc > 0):
    # ファイルリストが無いとき
    print('E: Require any files', file=sys.stderr)

    time.sleep(5)
    sys.exit(1)

proc_file_count = 0
proc_file_count_done = 0
proc_file_count_fail = 0

for proc_file in sys.argv:
    proc_file_count += 1

    if not(os.path.isfile(proc_file)):
        proc_file_count_fail += 1
        console_print_temp = 'W: Unable to load file. skipping. \'' + proc_file + '\''
        console_print += console_print_temp + "\n"
        if debug:
            print(console_print_temp, file=sys.stderr)

        continue

    try:
        # https://github.com/n138-kz/Util_of_Genshin-Impact/blob/main/nameTomd5.py
        # hash計算
        # https://qiita.com/maboy/items/8ee4c408640700e52274
        h_algo = ini_array1["hash"]
        h = hashlib.new(h_algo)
        h_len = hashlib.new(h_algo).block_size * 0x800

        with open(proc_file,'rb') as fp:
            h_bin = fp.read(h_len)

            while h_bin:
                h.update(h_bin)
                h_bin = fp.read(h_len)

        hash_exportdata += h_algo + "\t" + proc_file + "\t" + h.hexdigest() + "\n"

        # neo name
        neo_file = ini_array1["exportListRule"].replace('{hash}', h.hexdigest()) + str(os.path.splitext(proc_file)[len(os.path.splitext(proc_file))-1]).lower()

        # exist check
        if os.path.isfile(neo_file):
            proc_file_count_fail += 1

            console_print_temp = 'W: Already exist neo file. skipping. old=\'' + proc_file + '\' neo=\'' + neo_file + '\''
            console_print += console_print_temp + "\n"
            if debug:
                print(console_print_temp, file=sys.stderr)

            continue

        # rename
        os.rename(proc_file, neo_file)

        console_print_temp = 'N: Renamed file. old=\'' + proc_file + '\' neo=\'' + neo_file + '\''
        console_print += console_print_temp + "\n"
        if debug:
            print(console_print_temp)

        if ini_array1["updateMtime"]:
            os.utime(neo_file, None)

        proc_file_count_done += 1
    except ValueError as e:
        console_print_temp = 'E: ' + str(type(e)) + ' ' + str(e)
        console_print += console_print_temp + "\n"
        print(console_print_temp, file=sys.stderr)

        proc_file_count_fail += 1
        continue
    except PermissionError as e:
        console_print_temp = 'E: ' + str(type(e)) + ' ' + str(e)
        console_print += console_print_temp + "\n"
        print(console_print_temp, file=sys.stderr)

        proc_file_count_fail += 1
        continue
    except:
        import traceback
        traceback.print_exc()
        time.sleep(30)
        sys.exit(1)


console_print_temp = 'N: Summary:\n   Total:   ' + str(proc_file_count) + '\n   Success: ' + str(proc_file_count_done) + '\n   Failure: ' + str(proc_file_count_fail)
console_print += console_print_temp + "\n"
if debug:
    print(console_print_temp)


if ini_array1["exportList"]:
    try:
        with open(ini_array1["exportToDir"] + ini_array1["exportListFile"], encoding='UTF-8', mode='w') as fp:
            fp.write(hash_exportdata)
    except:
        import traceback
        traceback.print_exc()
        time.sleep(5)
        sys.exit(1)

if ini_array1["consoleLog"]:
    try:
        with open(ini_array1["exportToDir"] + ini_array1["consoleLogRule"], encoding='UTF-8', mode='w') as fp:
            fp.write(console_print)
    except:
        import traceback
        traceback.print_exc()
        time.sleep(5)
        sys.exit(1)
