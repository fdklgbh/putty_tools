# PuttyTools
由于mobaxterm 新增的数量有限制,编写该工具
## 使用方式
1. 需要先双击项目路径下Theme\PuttyTools.reg 把putty主题样式放入注册表
2. 打开PuttyTools.exe 进行新建文件夹或者ssh的配置信息文件

## 更新记录

### 2.0

putty tools 新增输出日志信息到页面
去掉了1.0版本的黑框
日志存储于 %USERPROFILE%\.PuttyTools\Log

##### 修复bug

1. 同级目录两个文件夹,再次创建会在中间插入
2. 修改文件后,右侧文件信息不会同步修改

##### 优化

1. 右侧文件信息选中后ctrl+c 不会复制,
2. 关闭文件信息文本框右键菜单,ctrl+c 直接复制

#### 2.1

程序标题增加版本号


### 1.0
1. 开始使用