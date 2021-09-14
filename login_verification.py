"""
    @Author  : seeklife
    @Time    : 2021.2.1
    @Comment :
"""

from xml.dom.minidom import parse
import xml.dom.minidom as minidom


# 读取xml文件下的数据
def readXML(database, username, password):
    if database == 'data':
        # 搜索的表
        domTree = parse(u'data.xml')
        print("开始查找data")
    # 文档根元素
    rootNode = domTree.documentElement
    # 得到所有entry元素
    entries = rootNode.getElementsByTagName("entry")
    for entry in entries:
        if entry.hasAttribute("ID"):
            # if entry.getAttribute("ID") == u'C003':
            if entry.getElementsByTagName("username") is not None and entry.getElementsByTagName(
                    "password") is not None:
                if entry.getElementsByTagName("username")[0].firstChild.data == username and \
                        entry.getElementsByTagName("password")[0].firstChild.data == password:
                    return True
