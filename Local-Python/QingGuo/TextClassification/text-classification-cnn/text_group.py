#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
将文本整合到 train、test、val 三个文件中
"""

import os

def _read_file(filename):
    """读取一个文件并转换为一行"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', '').replace('\t', '').replace('\u3000', '')

def save_file(dirname):
    f_train = open('data/text/text.trian.txt', 'w', encoding='utf-8')
    # f_test = open('data/text/text.test.txt', 'w', encoding='utf-8')
    # f_val = open('data/text/text.val.txt', 'w', encoding='utf-8')
    for category in os.listdir(dirname):   # 分类目录
        cat_dir = os.path.join(dirname, category)
        if not os.path.isdir(cat_dir):
            continue
        files = os.listdir(cat_dir)
        count = 0
        for cur_file in files:
            filename = os.path.join(cat_dir, cur_file)
            content = _read_file(filename)
            # if count < 5000:
            f_train.write(category + '\t' + content + '\n')
            # elif count < 6000:
            #     f_test.write(category + '\t' + content + '\n')
            # elif count < 10000:
            #     f_val.write(category + '\t' + content + '\n')
            # else:
            #     break
            # count += 1

        print('Finished:', category)

    f_train.close()
    # f_test.close()
    # f_val.close()


if __name__ == '__main__':
    save_file('../Input/text')
    print(len(open('data/text/text.trian.txt', 'r', encoding='utf-8').readlines()))
    # print(len(open('data/text/text.test.txt', 'r', encoding='utf-8').readlines()))
    # print(len(open('data/text/text.val.txt', 'r', encoding='utf-8').readlines()))
