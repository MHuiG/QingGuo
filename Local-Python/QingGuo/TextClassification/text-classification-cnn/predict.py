# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr

from cnn_model import TCNNConfig, TextCNN
from data.cnews_loader import read_category, read_vocab

try:
    bool(type(unicode))
except NameError:
    unicode = str

base_dir = 'data/text'
vocab_dir = os.path.join(base_dir, 'text.vocab.txt')

save_dir = 'checkpoints/textcnn'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class CnnModel:
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]


if __name__ == '__main__':
    cnn_model = CnnModel()
    test_demo = [
        #'人','鸟','猫','狗','马','羊','牛','大象','熊','斑马','长颈鹿',
        #'飞机','自行车','汽车','摩托车','公共汽车','火车','卡车','船','红绿灯','停车标志','停车计时器','消防栓',
        #'牙刷','叉','刀','勺子','瓶子','酒杯','杯子','碗','时钟','花瓶','剪刀','泰迪熊','书','手提箱','盆栽植物','领带','雨伞','背包','手提包',
        #'长凳','沙发','餐桌','厕所','水池','椅子','床',
        #'棒球棒','棒球手套','滑板','冲浪板','滑雪板','运动球','网球拍','风筝','滑雪板','飞盘',
        #'香蕉','苹果','橘子','西兰花','胡萝卜','披萨','甜甜圈','蛋糕','三明治','热狗',
        #'键盘','电视','笔记本电脑','鼠标','遥控器','手机','烤面包机','吹风机','冰箱','烤箱','微波炉',
    ]
    for i in test_demo:
        print(cnn_model.predict(i))
