__author__ = 'xlvector'

from Tkinter import *
import random
import math
from operator import itemgetter


def RDT(points,wx,hy, max_depth):
    splits = []
    for k in range(0,max_depth):
        axis = random.randint(0,1)
        sv = random.random()
        splits.append([axis, sv])
    root = [0, 0, -1, -1, 0, points]
    tree = [root]
    Q = [root]
    k = 0
    while len(Q) > 0:
        [depth, index, left, right, predict, ps] = Q.pop()
        if len(ps) == 0 and predict != 0:
            print index
        if depth >= max_depth or len(ps) < 10:
            continue
        [axis,sv] = splits[depth]
        pleft = dict()
        pright = dict()
        p1 = 0
        p2 = 0
        for p, c in ps.items():
            f = [float(int(p/1000))/(wx*1.0), float(int(p%1000))/(hy*1.0)]
            if f[axis] < sv:
                pleft[p] = c
                p1 += c
            else:
                pright[p] = c
                p2 += c
        tree[index][5] = dict()

        p1 = p1 / (len(pleft) * 1.0 + 10.0)
        tree[index][2] = len(tree)
        leftNode = [depth+1, len(tree), -1, -1, p1, pleft]
        tree.append(leftNode)
        Q.append(leftNode)
            

        p2 = p2 / (len(pright) * 1.0 + 10.0)
        tree[index][3] = len(tree)
        rightNode = [depth+1, len(tree), -1, -1, p2, pright]
        tree.append(rightNode)
        Q.append(rightNode)
    return [tree, splits]

master = Tk()

W = 600
H = 500

w = Canvas(master, width=W, height=H, bg="white")
w.pack(fill=BOTH)

points = dict()
train = dict()
cpoints = set()
random.seed(198571)
def getHash(x, y):
    return x * 1000 + y


for k in range(1500):
    x = int(random.uniform(0, W))
    y = int(random.uniform(0, H))
    d = math.sqrt((x - W / 2) * (x - W / 2) + (y - H / 2) * (y - H / 2))

    if d > 80 and d < 130:
        points[getHash(x,y)] = 1
        if k < 300:
            train[getHash(x,y)] = 1

    if d > 150 and d < 190:
        points[getHash(x,y)] = -1
        if k < 300:
            train[getHash(x,y)] = -1

random.seed(198571)
pb = dict()
nn = dict()
for tree in range(0,64):
    [tree, splits] = RDT(train,W,H,50)
    for i in range(0,W):
        for j in range(0,H):
            if (i + j) % 5 > 0:
                continue
            f = [i / (W*1.0),j / (H*1.0)]
            k = 0
            pk = 0
            while True:
                [depth, index, left, right, predict, ps] = tree[k]
                if left < 0 and right < 0:
                    pk = predict
                    break
                [axis, sv] = splits[depth]
                if f[axis] < sv:
                    if left < 0:
                        pk = predict
                        break
                    else:
                        k = left
                else:
                    if right < 0:
                        pk = predict
                        break
                    else:
                        k = right
            h = getHash(i, j)
            if h not in nn:
                nn[h] = 0
                pb[h] = 0
            nn[h] += 1
            pb[h] += pk

for key, value in pb.items():
    x = int(key/1000)
    y = key % 1000
    if value < 0:
        w.create_line(x,y, x+1,y+1, fill="orange")
    if value > 0:
        w.create_line(x,y, x+1,y+1, fill="green")

for p,c in points.items():
    px = int(p / 1000)
    py = p % 1000
    if c < 0:
        if p in train:
            w.create_oval(px - 3,py-3, px+3,py+3, fill="pink", outline="pink")
        else:
            w.create_oval(px - 2,py-2, px+2,py+2, fill="red",outline="red")
    else:
        if p in train:
            w.create_oval(px - 3,py-3, px+3,py+3, fill="yellow", outline="yellow")
        else:
            w.create_oval(px - 2,py-2, px+2,py+2, fill="blue",outline="blue")
        
mainloop()