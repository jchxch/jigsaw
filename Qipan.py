import math
import numpy as np
from Prediction import Prediction
import base64
import os
from PIL import Image


class Qipan:
    def __init__(self):
        self.n = 3
        self.N = self.n * self.n
        self.bk = 8  # ----------空格所对应的原图片的位置
        self.init = np.arange(1, self.N + 1).reshape(self.n, self.n)#二维矩阵最终的目标[[1,2,3],[4,5,6],[7,8,9]]
        # self.qipan = self.init.copy()
        # self.bk_x = self.n - 1
        # self.bk_y = self.n - 1
        self.qipan = np.array([[9, 5, 1], [8, 2, 4], [3, 6, 7]])  # ----需求解的二维矩阵
        self.bk_x = 1  # ---------------------#空白块在矩阵中的位置
        self.bk_y = 0  # ---------------------
        self.bk_x_p = -1#空白块之前的位置，当下一步是与之前位置相同则不选择此方向
        self.bk_y_p = -1
        self.step=0#共计步数
        self.pre = Prediction()#预测类
        self.started = False  # 标记是否开始
        self.X = [-1, 0, 1, 0]#i=0时X=-1，Y=0即空白块向上移动
        self.Y = [0, -1, 0, 1]
        self.stepout = []#存储步骤

    # def make_qipan(self):  # 生成随机棋盘
    #     # max_step = np.random.randint(40000, 80000)  # 随机生成移动棋子步数
    #     # step = 0
    #     # while step < max_step or self.qipan[self.n - 1][self.n - 1] != self.N:
    #     #     i = np.random.randint(4)
    #     #     x = self.bk_x + self.X[i]
    #     #     y = self.bk_y + self.Y[i]
    #     #     self.move(x, y)
    #     #     step += 1
    #
    #     self.bk_x_p = -1  # -----
    #     self.bk_y_p = -1
    #     self.step = 0  # 提示计步
    #     self.started = True  # 标记是否开始

    def move(self, x, y):  # 移动棋子
        if x < 0 or x >= self.n or y < 0 or y >= self.n:#如果x,y不可达则不操作棋盘
            return
        self.qipan[self.bk_x][self.bk_y] = self.qipan[x][y]
        self.qipan[x][y] = self.bk#空格处与x，y位置数字调换
        self.bk_x_p = self.bk_x#更新空白块上一步位置
        self.bk_y_p = self.bk_y
        self.bk_x = x#更新空白块当前位置
        self.bk_y = y

    def is_finish(self):  # 判断游戏是否结束
        for i in range(self.n):
            for j in range(self.n):
                if self.qipan[i][j] != self.init[i][j]:#与目标矩阵数据一一作比较
                    return False
        return True

    def show(self):  # 打印当前棋盘状态
        s = ""
        for i in range(self.n):
            for j in range(self.n):
                if self.qipan[i][j] == self.bk:##当遇到空白块的值则输出空格
                    s += "  "
                else:
                    s += str(self.qipan[i][j]) + " "
            s += "\n"
        print(s)

    def add_step(self, i):#在输出步骤中添加当前方向的步骤
        if i == 0:
            self.stepout.append('w')
        elif i == 1:
            self.stepout.append('a')
        elif i == 2:
            self.stepout.append('s')
        else:
            self.stepout.append('d')

    def tips(self):  # 提示一步
        i = self.pre.pre_next(self.qipan, self.bk_x, self.bk_y, self.bk_x_p, self.bk_y_p)#调用pre类中预测下一步的方法
        x = self.bk_x + self.X[i]#空白格目标位置x,y
        y = self.bk_y + self.Y[i]
        self.add_step(i)#在stepout中添加当前步骤
        self.move(x, y)#将空白格移向x,y
        self.step += 1
        self.show()#打印当前矩阵状态


# 图片处理
def cut_image(image):
    # 读取图片大小
    width, height = image.size
    item_width = int(width / 3)
    box_list = []
    # 两重循环，生成9张图片基于原图的位置
    for i in range(0, 3):
        for j in range(0, 3):
            box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
            box_list.append(box)

    image_list = [image.crop(box) for box in box_list]
    # 利用save_images保存切割好的图
    save_images(image_list)


def save_images(image_list):
    path = './problem'
    if not os.path.exists(path):
        os.mkdir('problem')
    index = 1
    for image in image_list:#将九张小图片保存
        image.save('./problem/' + str(index) + '.jpg')
        index += 1


img = Image.open('photo.jpg')  # 打开题目文件
cut_image(img)  # 切割题目文件为9个小片
TrainFiles = os.listdir('./picture')  # 检索已有的字母集
for file in TrainFiles:  # 所有字母
    count = 0#与每一个字母文件夹遍历比较，题目图片应该与原图片有8张小图片相同
    blank = []#记录匹配图片对应关系
    p1 = os.listdir('./picture/' + file)
    for problem1 in os.listdir("problem"):
        for p2 in p1:  # p1字母对比
            with open("./picture/" + file + "/" + p2, "rb") as f:  # 转为二进制格式
                base64_data1 = base64.b64encode(f.read())  # 使用base64进行加密
            with open("./problem/" + problem1, "rb") as f:  # 转为二进制格式
                base64_data2 = base64.b64encode(f.read())  # 使用base64进行加密
            if base64_data1 == base64_data2:
                count = count + 1
                img = Image.open("./problem/" + problem1)
                img.save("./answer/" + p2)
                blank.append([problem1[0], p2[0]])

    if count == 8:
        print(file)
        break
print(blank)
e = [1, 1, 1, 1, 1, 1, 1, 1, 1]#通过排除，找出空白块对应原编号
f = [1, 1, 1, 1, 1, 1, 1, 1, 1]

for i in range(0, 8):
    k = int(blank[i][0])

    e[k - 1] = 0
for i in range(0, 8):
    k = int(blank[i][1])
    f[k - 1] = 0
for i in range(0, 9):
    if e[i] != 0:
        blank1 = i + 1
        break
for i in range(0, 9):
    if f[i] != 0:
        blank2 = i + 1
        break
blank.append([str(blank1), str(blank2)])  # 添加空格
print(blank)
img = Image.open("./problem/" + str(blank1) + ".jpg")
img.save("./answer/" + str(blank2) + '.jpg')
reshape_answer = []#整理出求解矩阵
for i in range(0, 3):
    line = []
    for j in range(0, 3):
        for item in blank:
            if item[0] == str(i * 3 + j + 1):
                line.append(int(item[1]))
                break
    reshape_answer.append(line)
print(reshape_answer)  # 处理后的图片序号数组


def turnToarray(qipan, bk):#将二维矩阵专一维数组，求逆序对时需要
    t = []
    for i in range(3):
        for j in range(3):
            if qipan[i][j] != bk:
                t.append(qipan[i][j])
    return t


def judgment(temp):#判断矩阵是否可解
    position = -1
    signal = 0#当signal为以为数组中存在的逆序数对的个数，为偶数时，矩阵可解，奇数时不可解，
    for i in range(len(temp)):
        for j in range(i + 1, len(temp)):
            if temp[i] > temp[j]:
                signal += 1
            if signal == 1:
                position = i
    if signal % 2 != 0:
        print('no way')
        return signal, position


def swap(qipan, p):#更换期盼矩阵中第p位与第p+1位的图片
    print('swap[%d , %d]' % (qipan[p // 3][p % 3], qipan[(p + 1) // 3][(p + 1) % 3]))
    t_1 = qipan[p // 3][p % 3]
    qipan[p // 3][p % 3] = qipan[(p + 1) // 3][(p + 1) % 3]
    qipan[(p + 1) // 3][(p + 1) % 3] = t_1

path='quary/q_tab_8.npz'
qi = Qipan()
qi.pre.load_tab(path)
qi.qipan = np.array(reshape_answer)  # ----
qi.bk_x = math.floor((blank1 - 1) / 3)  # ---------------------
qi.bk_y = (blank2 - 1) % 3  # ---------------------
while not qi.is_finish():
    t = turnToarray(qi.qipan, qi.bk)
    if judgment(t):
        signal, position = judgment(t)
        swap(qi.qipan, position)
    qi.tips()
print(qi.stepout)
