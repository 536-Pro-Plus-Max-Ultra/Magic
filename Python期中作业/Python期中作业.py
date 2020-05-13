import pygame, sys
from enum import Enum, unique
from math import sqrt
from random import randint
from math import pi
'''
导入各种库的说明：
1. pygame库：
    
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
    def __init__(self, x, y, radius, sx, sy, color=Color.RED):           #初始化方法   
                                                                         # color初始值为Color类中的RED颜色
        self.x = x                                                       # 球的初始x坐标，鼠标点击时获取
        self.y = y                                                       # 球的初始y坐标，鼠标点击时获取
        self.radius = radius                                             # 球的初始半径，随机半径
        self.sx = sx                                                     # 球在x方向上的位移
        self.sy = sy                                                     # 球在y方向上的位移
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

def main():                                                              
    balls = []                                                           # 定义用来装所有球的容器
    pygame.init()                                                        # 初始化导入的pygame中的模块
    screen = pygame.display.set_mode((1000, 800))                        # 初始化用于显示的窗口并设置窗口尺寸
    pygame.display.set_caption('大球吃小球游戏——Python期中作业')          # 设置当前窗口的标题
    pygame.mixer.music.load('D:/python/Welcome to Wonderland.mp3')       # 导入背景音乐
    pygame.mixer.music.play()                                            # 播放背景音乐
    running = True
    #color = Color.random_color()
    #ball = Ball(10,100,20,3,3,color)                                                          # 开启一个事件循环处理发生的事件
    while running:   
                                                         # 从消息队列中获取事件并对事件进行处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos                                          # 获得点击鼠标的位置，赋值给初始位置的x,y
                print(event.pos)
                radius = randint(10, 60)                                  # 半径在[10,60)中随机生成
                sx, sy = randint(-5, 5), randint(-8, 8)                   # 球的速度
                color = Color.random_color()                              # 获得球的随机颜色
                ball = Ball(x, y, radius, sx, sy, color)                  # 在点击鼠标的位置创建一个球(大小、速度和颜色随机)
                balls.append(ball)
                '''
                for ball in balls:
                    if sqrt((event.pos[0]-ball.x)**2 + (event.pos[1]-ball.y)**2) <= ball.radius:
                       balls.append(ball) 
                    else:
                       pass                                               # 将球添加到列表容器中
                '''
        screen.fill((255, 255, 255))
        for ball in balls:                                                # 取出容器中的球，如果没被吃掉就绘制，被吃掉了就移除
            if ball.alive:
                ball.draw(screen)
            else:
                balls.remove(ball)
        pygame.display.flip()                                             # 每隔60毫秒就改变球的位置再刷新窗口
        pygame.time.delay(60)
        for ball in balls:
            ball.move(screen)
            for other in balls:                                           # 检查球有没有吃到其他的球
                ball.eat(other)

if __name__ == '__main__':
    main()
