import pygame, sys
from enum import Enum, unique
from math import sqrt, pi
from random import randint
import pygame.font
import tkinter as tk
import time
'''
导入各种库的说明：
1. pygame库 ：实现游戏的主体结构；
2. enum库   ：实现随机颜色；
3. random库 ：实现随机半径、速度；
4. math库   ：计算半径、距离；
5. tkinter库：实现开局按钮；
6. time库   ：实现游戏结束不立刻退出游戏
'''
@unique                                                                  # 借助 @unique 装饰器,这样当枚举类中出现相同值的成员时，
                                                                         # 程序会报 ValueError 错误
class Color(Enum):                                                       # 定义颜色,这些形如（255，0，0）是该颜色在RGB色域中对应的值
   
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (242, 242, 242)

    @staticmethod                                                        # 声明静态方法，可以不接受任何参数
    def random_color():                                                  # 获得随机颜色。r、g、b 分别为颜色对应的三个值
                                                                         # 均在[0,255)内取值，这样就可以获得随机颜色了
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)

class App():                                                             # 定义开局按钮
    def __init__(self,root):
        frame = tk.Frame(root)
        frame.pack()
        self.start = tk.Button(frame,text = "开始",fg = "black",command = self.start_1)
        self.start.pack(side = tk.LEFT)
    def start_1(self):
        main()
        while(True):
            print("如果要退出程序,按Y/N")
            in_content = input("请输入：")
            if in_content == "Y":
                print("执行成功！")
                exit(0)
            elif in_content == "N":
                print("你已退出了该程序！")
                exit(0)
            else:
                print('继续')


class Ball(object):                                                      # 定义球，绘制球的大小、球的颜色，移动方法、吃掉其他球的规则
    def __init__(self, x, y, radius, sx, sy, color=Color.RED):           # 初始化方法   
                                                                         # color初始值为Color类中的RED颜色
        self.x = x                                                       # 球的初始x坐标，鼠标点击时获取
        self.y = y                                                       # 球的初始y坐标，鼠标点击时获取
        self.radius = radius                                             # 球的初始半径，随机半径
        self.sx = sx                                                     # 球在x方向上的位移(速度)
        self.sy = sy                                                     # 球在y方向上的位移(速度)
        self.color = color                                               # 球的初始颜色
        self.alive = True                                                # 球是否“存活”（是否被吃掉了）

    def move(self, screen):                                              # 定义球的移动，接收屏幕大小参数
        self.x += self.sx                                                # 新的x值为原值+变化值
        self.y += self.sy                                                # 新的y值为原值+变化值
        if self.x - self.radius <= 0 or self.x + self.radius >= screen.get_width():
            self.sx = -self.sx                                           # 如果移动距离小于半径，或者移动距离＋半径大于了屏幕的宽度，
                                                                         # 即球超出屏幕时，反向移动
        if self.y - self.radius <= 0 or self.y + self.radius >= screen.get_height():
            self.sy = -self.sy                                           # 如果移动距离小于半径，或者移动距离＋半径大于了屏幕的长度，
                                                                         # 即球超出屏幕时，反向移动     

    def eat(self, other):                                                # 定义吃掉其他球的规则
        if self.alive and other.alive and self != other:                 # 如果当前球还活着，其他球还活着，并且实例化对象不等于other时：
            dx, dy = self.x - other.x, self.y - other.y                  # dx, dy = 当前球的x值-其他球的x值， 当前球的y值-其他球的y值
            distance = sqrt(dx ** 2 + dy ** 2)                           #（球心）距离(distance) = (dx)的平方 + (dy)的平方 的和 开根号（和数学上一致）
                                                                         # 即：判断两球球心的距离，如果小于两球半径之和或且当前球半径大于其他球时，“吃掉”其他的球
            if distance < self.radius + other.radius and self.radius > other.radius:
                other.alive = False                                      # 其他球的存活（alive）= False，即其他球被吃掉
                self.radius = self.radius + int(other.radius * 0.146)    # 定义合并后新球的半径
    

    def draw(self, screen):                                              # 在窗口上绘制球，利用pygame库绘制
                                                                         # 屏幕参数、球的颜色、球的初始位置、球的半径
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)

def gameOver(playSurface,score):                                         # 显示GAME OVER并定义字体以及大小
    greyColour = pygame.Color(150, 150, 150)
    gameOverFont = pygame.font.SysFont('arial', 72)
    gameOverSurf = gameOverFont.render('Game Over', True, greyColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 125)
    playSurface.blit(gameOverSurf, gameOverRect)                        # 显示分数并定义字体和大小
    scoreFont = pygame.font.SysFont('arial', 72)
    scoreSurf = scoreFont.render('SCORE: ' + str(score), True, greyColour)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (320, 225)
    playSurface.blit(scoreSurf, scoreRect)
    pygame.display.flip()                                               # 刷新显示界面
    time.sleep(3)                                                       # 暂停3S后退出游戏
    pygame.quit()
    sys.exit()

def main():
    playSurface = pygame.display.set_mode((640, 480))
    score = 0                                                            # 记录分数
    ballnumber = 0
    eatballnumber = 0 
    balls = []                                                           # 定义用来装所有球的容器
    pygame.init()                                                        # 初始化导入的pygame中的模块
    screen = pygame.display.set_mode((1200, 600))                        # 初始化用于显示的窗口并设置窗口尺寸
    pygame.display.set_caption('大球吃小球游戏——Python期中作业')       # 设置当前窗口的标题
    game_font = pygame.font.SysFont('SimHei', 17, True)                  # 设置字体
    pygame.mixer.music.load('D:\Python\Welcome to Wonderland.mp3')       # 导入背景音乐
    pygame.mixer.music.play(20)                                          # 播放背景音乐

    running = True                                                       # 开启一个事件循环处理发生的事件
    while running:   
                                                                         # 从消息队列中获取事件并对事件进行处理     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos                                          # 获得点击鼠标的位置，赋值给初始位置的x,y
                radius = randint(20, 50)                                  # 半径在[20,50)中随机生成
                sx, sy = randint(-5, 5), randint(-6, 6)                   # 球的速度，球的速度可能为0
                def isZero(sx,sy):                                        # 判断速度，为0则重新生成再重新判断，直至不为0  
                    if sx == 0 and sy == 0 :
                        sx, sy = randint(-5, 5), randint(-6, 6)
                        return isZero(sx,sy)
                    else:
                        pass
                color = Color.random_color()                              # 获得球的随机颜色
                ball = Ball(x, y, radius, sx, sy, color)                  # 在点击鼠标的位置创建一个球(大小、速度和颜色随机)
                if len(balls) >= 6:                                       # 球数超过设定则不能放球
                    print('球的个数太多了，慢一点放吖！')
                    pass                                                  # 超过则不允许放球，忽略操作
                else:
                    balls.append(ball)                                    # 将球添加到列表容器中

        screen.fill((255, 255, 255))                                      # 背景填充为白色

        for ball in balls:                                                # 取出容器中的球，如果没被吃掉就绘制，被吃掉了就移除
            if ball.radius >= 120:                                        # 如果球的半径大于等于120，则“灭活”该球，使得alive = False
                ballnumber += 1
                print('你已经消灭 %d 个球啦！'% ballnumber)               # 记录由于半径过大被消灭的球
                ball.alive = False                                        # 防止球面积过大，占满屏幕
            if ball.alive:
                ball.draw(screen)
            else:
                eatballnumber += 1
                print('你已经吃掉 %d 个球啦！'% eatballnumber)            # 记录被吃掉球的个数
                balls.remove(ball)
                score += ball.radius*10                                   # 在屏幕上显示得分、“战况”、游戏说明
        screen.blit(game_font.render(u'吃掉了 {0} 个球 , 消灭了 {1} 个球！'.format(eatballnumber, ballnumber), True, [255, 0, 0]), [900,20])
        screen.blit(game_font.render(u'当前得分：%d 达到15000就赢了！' % score, True, [255, 0, 0]), [20, 20])
        screen.blit(game_font.render(u'鼠标点击任意位置放球，球合并即得分' , True, [89, 0, 0]), [890, 580])
        pygame.display.flip()                                             # 每隔30毫秒就改变球的位置再刷新窗口
        pygame.time.delay(30)
        for ball in balls:
            ball.move(screen)
            for other in balls:                                           # 检查球有没有吃到其他的球
                ball.eat(other)
        if score>=15000:
            print('*'*75)
            print('你胜利了!\n','*'*75,'\n游戏将在3秒后退出，点击开始按钮可以继续！')
            gameOver(playSurface,score)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
