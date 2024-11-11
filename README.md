# PuttyTools
由于mobaxterm 新增的数量有限制, xshell禁止使用,编写该工具
## 归档
发现更好的[WindTerm](https://github.com/kingToolbox/WindTerm)
## 使用方式
1. 需要先双击项目路径下Theme\PuttyTools.reg 把putty主题样式放入注册表
2. 打开PuttyTools.exe 进行新建文件夹或者ssh的配置信息文件



## 更新记录

### 2.1.3
修复bug
1. [bug 删除文件夹 #1](https://github.com/fdklgbh/putty_tools/issues/1)
2. [bug 删除文件 #2](https://github.com/fdklgbh/putty_tools/issues/2)
3. [bug 修改文件 #3](https://github.com/fdklgbh/putty_tools/issues/3)
4. [bug 多次弹窗错误弹窗 #4](https://github.com/fdklgbh/putty_tools/issues/4)
5. [bug 新建文件夹 #5](https://github.com/fdklgbh/putty_tools/issues/5)

### 2.1.2
修复python3.6升3.9出现的问题
#### 修复bug
1. 根目录下的连接文件,鼠标右键创建连接文件时出错

#### 优化
1. 捕获未处理异常,弹窗并保存错误信息到Log文件夹内,名称为error_xxx.log

### 2.1

程序标题增加版本号
#### 修复bug

1. 同级目录两个文件夹,再次创建会在中间插入
2. 修改文件后,右侧文件信息不会同步修改

#### 优化

1. 右侧文件信息选中后ctrl+c 不会复制,
2. 关闭文件信息文本框右键菜单,ctrl+c 直接复制

### 2.0

putty tools 新增输出日志信息到页面
去掉了1.0版本的黑框
日志存储于 %USERPROFILE%\.PuttyTools\Log




### 1.0
1. 开始使用
