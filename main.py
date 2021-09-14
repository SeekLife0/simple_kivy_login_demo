"""
    @Author  : seeklife
    @Time    : 2021.2.1
    @Comment :
"""
import kivy
kivy.require('1.9.1')
import re
import login_verification
from kivy.app import App
from kivy.uix.gridlayout import GridLayout  # 需要指定列，然后按照顺序从左到右
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.event import EventDispatcher
from kivy.uix.boxlayout import BoxLayout    # 默认从左到右进行排列
from kivy.graphics import Color, Rectangle  # 给布局添加背景
from kivy.core.text import LabelBase        # 统一中文字体

LabelBase.register(name='Font_Hanzi', fn_regular='./font/msyh.ttc')  # 导入字体文件


class MyInput(TextInput):
    pat = '[A-Za-z0-9]+'  # 网上搜索的正则表达式直接复制可能有些问题自己输入一遍解决

    def __init__(self, **kwargs):
        super(MyInput, self).__init__(**kwargs)

    # 输入过滤，这里只能输入数字,每次输入一个字符都会调用该方法,s就是输入的那个字符
    def insert_text(self, s, from_undo=False):
        print(s)
        pat = self.pat
        # 使用正则进行匹配如果不是数字或字母返回none
        m = re.search(self.pat, s)
        print(m)
        # 如果输入的内容不是数字或字母那group必定为none
        if m is None:
            s = ''  # 写入空字符
            print('把字符替换成了空白')
        return super(MyInput, self).insert_text(s, from_undo=from_undo)


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        # 修改boxlayout的背景颜色-------------------------------------------开始
        with self.canvas.before:
            Color(0, 0, 0, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # 修改背景颜色结束--------------------------------------------------结束

        self.lq = Label(text='用户名', font_name='Font_Hanzi', font_size='40sp')
        self.add_widget(self.lq)
        self.username = MyInput(multiline=False, font_size='40sp')  # text  font_name 也可以指定初始文本
        self.add_widget(self.username)

        self.lm = Label(text='密码', font_name='Font_Hanzi', font_size='40sp')
        self.add_widget(self.lm)
        self.password = MyInput(multiline=False, font_size='40sp')  # password=true输入的字符会变成星号
        self.add_widget(self.password)

        self.button = Button(text='点击登录', font_name='Font_Hanzi')
        # 创建好一个按钮然后就可以给这个按钮添加对应的事件处理函数了,和tkinter类似
        self.button.bind(on_press=self.myPress)
        self.add_widget(self.button)

        # 移除控件
        # layout.remove)widget(button)
        # 清除所有子控件
        # layout.clear_widget()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def myPress(self, obj):
        flag = False
        # 获取内容然后去除前后空格
        # 首先判断输入的内容是否为空
        if (self.username.text is not None or self.username.text.strip() != '') and (
                self.password.text is not None or self.password.text.strip() != ''):
            # 对qj进行查找
            flag = login_verification.readXML('data', self.username.text, self.password.text)
            if flag is True:
                self.lq.text = '用户名:' + '存在该用户'
            else:
                self.lq.text = '用户名:' + '不存在该用户'

    # #用来接收处理收到的input内容
    # def qjInputText(self,instance,value):
    #     print('qjContent:',instance,'内容为',value)
    #
    # # 用来接收处理收到的input内容
    # def mtInputText(self, instance, value):
    #     print('mtContent:' ,instance,'内容为',value)


class test(App):
    def build(self):
        return MyBoxLayout(padding=20, orientation='vertical', spacing=30)  # 默认情况是水平排列


if __name__ == '__main__':
    test().run()
