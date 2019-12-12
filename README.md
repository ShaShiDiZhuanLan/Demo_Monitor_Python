# 1、Python语言的应用 之 Demo_Monitor_Python
简单监控的CPU利用率、CPU平均负载、硬盘使用率、内存使用率 和 各个端口的开启状况 <BR/>
适用系统：Linux （注意：不适合Windows） <BR/> 
<BR/>
# 2、更新信息
开发者：沙振宇（沙师弟专栏） <BR/>
创建时间：2019-7-9 <BR/>
最后一次更新时间：2019-12-12<BR/>
CSDN博客地址：https://shazhenyu.blog.csdn.net/article/details/98615482<BR/>
<BR/>
# 3、使用前准备
python版本要求：python3.0 以上<BR/>
安装 python 的 psutil 包 和 requests 包 <BR/>
pip install psutil<BR/>
pip install requests<BR/>
<BR/>
# 4、启动方式
nohup python3 monitor.py > monitor.log 2>&1 &<BR/>
注：需要定期清理 monitor.log 文件<BR/>
<BR/>
# 5、运行效果
![image](https://github.com/ShaShiDiZhuanLan/Demo_Monitor_Python/blob/master/%E7%9B%91%E6%8E%A7.png)