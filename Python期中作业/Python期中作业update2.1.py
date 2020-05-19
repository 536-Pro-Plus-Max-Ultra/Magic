import pygame, sys
from enum import Enum, unique
from math import sqrt, pi
from random import randint
import pygame.font
import time
'''
导入各种库的说明：
1. pygame库：实现游戏的主体结构；
2. enum库  ：实现随机颜色；
3. random库：实现随机半径、速度；
4. math库  ：计算半径、距离；
5. time库  ：实现游戏结束不立刻退出游戏.
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
                self.color = Color.random_color()
    

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
    playSurface = pygame.display.set_mode((800, 600))                    # 画布
    score = 0                                                            # 记录分数
    ballnumber = 0
    eatballnumber = 0 
    balls = []                                                           # 定义用来装所有球的容器
    pygame.init()                                                        # 初始化导入的pygame中的模块
    screen = pygame.display.set_mode((1200, 600))                        # 初始化用于显示的窗口并设置窗口尺寸
    pygame.display.set_caption('大球吃小球游戏——Python期中作业')       # 设置当前窗口的标题
    game_font = pygame.font.SysFont('SimHei', 17, True)                  # 设置字体
    pygame.mixer.music.load('Welcome to Wonderland.mp3')                 # 导入背景音乐
    pygame.mixer.music.play(20)                                          # 播放背景音乐
    
    start_ck = pygame.Surface(playSurface.get_size())                    # 充当开始界面的画布
    start_ck2 = pygame.Surface(playSurface.get_size())                   # 充当第一关的画布界面暂时占位（可以理解为游戏开始了)
    start_ck = start_ck.convert()
    start_ck2 = start_ck2.convert()
    start_ck.fill((255,255,255))                                         # 白色
    start_ck2.fill((255,255,255))                                        # 白色
    clock = pygame.time.Clock()
    i1 = pygame.image.load("s1.png")                                     # 加载各个素材图片 并且赋予变量名
    i1.convert()
    i11 = pygame.image.load("s2.png")
    i11.convert()

    i2 = pygame.image.load("n2.png")
    i2.convert()
    i21 = pygame.image.load("n1.png")
    i21.convert()

    i3 = pygame.image.load('m2.png')
    i3.convert()
    i31 = pygame.image.load('m1.png')
    i31.convert()
    i32 = pygame.image.load('ss.png')
    i32.convert()

    n1=True                                                              # 开始界面的第一重循环
    while n1:
        clock.tick(30)
        buttons = pygame.mouse.get_pressed()                             # 检测鼠标点击
        x1, y1 = pygame.mouse.get_pos()                                  # 鼠标点击坐标的获取
        if x1 >= 227 and x1 <= 555 and y1 >= 261 and y1 <=327:           # 实现按钮颜色的变化以及向游戏界面的跳转
            start_ck.blit(i11, (200, 240))
            if buttons[0]:                                               # 检测点击关闭一重循环进入下一重游戏循环
                n1 = False
        elif x1 >= 227 and x1 <= 555 and y1 >= 381 and y1 <=447:         # 实现按钮颜色转变和退出        
            start_ck.blit(i21, (200, 360))
            if buttons[0]:
                 pygame.quit()
                 exit()

        elif x1 >= 227 and x1 <= 555 and y1 >= 513 and y1 <=579:        # 实现按钮颜色转变以及制作人信息
            start_ck.blit(i31, (200, 480))
            if buttons[0]:
                start_ck.blit(i32,(200,480))
        else:                                                           # 没有点击和鼠标触及的情况下常态下播放的图片
            start_ck.blit(i1, (200, 240))
            start_ck.blit(i2, (200, 360))
            start_ck.blit(i3, (200, 480))


        playSurface.blit(start_ck,(0,0))                                #刷新                               
        pygame.display.update()

        for event in pygame.event.get():                                # 事件检测
            if event.type == pygame.QUIT:
                print('游戏退出...')
                pygame.quit()
                exit()
    playSurface.blit(start_ck2,(0,0))                                    # 上一重循环结束后播放游戏界面的画布占位
    pygame.display.update()                                              # 刷新
    running = True                                                       # 开启游戏界面循环处理发生的事件
    while running:
        clock.tick(30)
        playSurface.blit(start_ck2, (0, 0))
                                                                         # 从消息队列中获取事件并对事件进行处理     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos                                          # 获得点击鼠标的位置，赋值给初始位置的x,y
                radius = randint(20, 50)                                  # 半径在[20,50)中随机生成
                sx, sy = randint(-7, 7), randint(-7, 7)                   # 球的速度，球的速度可能为0
                def isZero(sx,sy):                                        # 判断速度，为0则重新生成再重新判断，直至不为0
                    if sx == 0 and sy == 0 :
                        sx, sy = randint(-7, 7), randint(-7, 7)
                        return isZero(sx,sy)
                    else:
                        pass
                isZero(sx,sy)
                color = Color.random_color()                              # 获得球的随机颜色
                ball = Ball(x, y, radius, sx, sy, color)                  # 在点击鼠标的位置创建一个球(大小、速度和颜色随机)
                if len(balls) >= 7:                                       # 球数超过设定则不能放球
                    print('球的个数太多了，慢一点放吖！')
                    pass                                                  # 超过则不允许放球，忽略操作
                else:
                    balls.append(ball)                                    # 将球添加到列表容器中

        screen.fill((255, 255, 255))                                      # 背景填充为白色

        for ball in balls:                                                # 取出容器中的球，如果没被吃掉就绘制，被吃掉了就移除
            if ball.radius >= 110:                                        # 如果球的半径大于等于120，则“灭活”该球，使得alive = False
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
            print('你胜利了!\n','*'*75,'\n游戏将在3秒后退出')
            gameOver(playSurface,score)


if __name__ == '__main__':
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

