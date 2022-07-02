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
import time
import cv2 as cv
import numpy
import matplotlib

print('> init')

# 引数 数チェック
print('> check count')
if len(sys.argv) <= 1:
    print('Require the args')
    print('')
    sys.exit(1);

# 引数の先頭(__FILE__)を削除
args = sys.argv
del args[0]

# ファイルリスト
print('> list')
for argv in args:
    print('   ',end='')
    print('- ',end='')
    print(argv)
print('')

# ファイル存在チェック
# 存在しない場合はリストから削除
print('> check exist true')
for argv in args:
    print('   ',end='')
    print('file .... ' + argv)
    print('   ',end='')
    print('exist ... ',end='')
    if not os.path.isfile(argv):
        args.remove(argv)
        print('no')
        print()
        continue
    print('yes')
    print()

# 引数 数チェック
print('> check count dump')
print(len(args))
print()

if len(args) < 1:
    print('No effective item in list')
    sys.exit(1);

# ファイルリスト
print('> list')
for argv in args:
    print('   ' + '- ' + argv)
print()

# 画像ファイルか判断
print('> check image quiet')
for argv in args:
    file = cv.imread(argv, -1)
    if file is None:
        args.remove(argv)

# ファイルリスト
print('> list')
for argv in args:
    print('   ',end='')
    print('- ',end='')
    print(argv)
print()

# 画像ファイルの幅＆高さ取得
print('> get size')
for argv in args:
    print('   ' + 'file .... ' + argv)
    img = cv.imread(argv, -1)
    try:
        # マルチバイトファイル名非対応
        img_h,img_w,img_c = img.shape[:3]
        print('   ' + 'height ... ' + str(img_h))
        print('   ' + 'width .... ' + str(img_w))
        print('   ' + 'channel .. ' + str(img_c))
    except AttributeError as e:
        img_h = img_w = img_c = 0
        args.remove(argv)
        continue
    print()

# 画像ファイルを横方向半分に分割
print('> set size half-width export')
for argv in args:
    print('   ' + 'file .... ' + argv)
    img = cv.imread(argv, -1)

    # マルチバイトファイル名非対応
    img_h,img_w,img_c = img.shape[:3]
    img1_h,img1_w = int(img_h / 2), int(img_w / 2)
    img2_h,img2_w = img_h - img1_h, img_w - img1_w

    print('   ' + 'height ... ' + str(img_h))
    print('   ' + 'width .... ' + str(img_w))

    argvExt = os.path.splitext(argv)
    argv1 = argvExt[0] + '_1' + argvExt[1]
    argv2 = argvExt[0] + '_2' + argvExt[1]

    print('-->' + 'file .... ' + argv1)
    print('-->' + 'height ... ' + str(img1_h))
    print('-->' + 'width .... ' + str(img1_w))

    print('-->' + 'file .... ' + argv2)
    print('-->' + 'height ... ' + str(img2_h))
    print('-->' + 'width .... ' + str(img2_w))

    img1 = img[0 : img_h, 0 : img1_w]
    cv.imwrite(argv1, img1)

    img2 = img[0 : img_h, (img1_w+1) : img_w]
    cv.imwrite(argv2, img2)

time.sleep(5)
