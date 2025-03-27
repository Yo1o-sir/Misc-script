# 记录如何对Linux制作符号表

> 以下操作可以保证是是在win11系统下的wsl2中进行的，其中wsl2是Debian系统

## 先记录vol2和vol3的安装

毕竟python2已经不再维护了，所以我这里准备主环境安装python3,vol3,开虚拟环境安装vol2以及python2

### vol3配置

```
sudo apt install python3 python3-pip -y
sudo apt install git -y
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
接下来可以使用python3 vol.py -h来判断是否安装成功
如果我们发现最后有几个Windows的插件配置失败的话，我们可以以下命令来安装对应的库
sudo apt install libyara-dev -y
sudo pip3 install yara-python pycryptodome pefile
然后就差不多我们拿到了纯血版的vol3
然后我这里图方便，设置了个软链接，方法放到这里
sudo ln -s /home/yolo/Desktop/tool/volatility3/vol.py /usr/local/bin/vol3
这样的话，我们就可以在全局使用vol3了
```

### vol2配置

接下来讲解安装vol2

```
sudo apt update
sudo apt install python2 python2-dev virtualenv -y
对了，这里有个小点，我的是Debian的wsl2子系统，它自身的镜像源里面没有python2的，这里建议在/etc/apt/sources.list中再加两条源
deb http://deb.debian.org/debian buster main
deb http://deb.debian.org/debian-security buster/updates main
然后安装好了python2，以及虚拟工具，接下来就是开启虚拟环境配置vol2了
virtualenv -p /usr/bin/python2 ~/Desktop/tool/vol2env
然后激活
source ~/Desktop/tool/vol2env/bin/activate
进来后下载vol2的源码
git clone https://github.com/volatilityfoundation/vol atility.git volatility2
vol2还需要一些库
pip install distorm3 pycrypto yara-python
最后用完vol2后，我们可以使用deactivate退出虚拟环境
```

## 给vol3制作符号表

这里得啃啃论文https://volatility3.readthedocs.io/en/latest/symbol-tables.html

然后开始了，我们需要找到镜像文件的banner信息

这是方法一

```
❯ vol3 -f 1.mem banners.Banners
Volatility 3 Framework 2.25.0
Progress:  100.00               PDB scanning finished
Offset  Banner

0x213a001a0     Linux version 5.4.0-205-generic (buildd@lcy02-amd64-055) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.2)) #225-Ubuntu SMP Fri Jan 10 22:23:35 UTC 2025 (Ubuntu 5.4.0-205.225-generic 5.4.284)
0x2155a0e54     Linux version 5.4.0-205-generic (buildd@lcy02-amd64-055) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.2)) #225-Ubuntu SMP Fri Jan 10 22:23:35 UTC 2025 (Ubuntu 5.4.0-205.225-generic 5.4.284)
0x23fec9390     Linux version 5.4.0-205-generic (buildd@lcy02-amd64-055) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.2)) #225-Ubuntu SMP Fri Jan 10 22:23:35 UTC 2025 (Ubuntu 5.4.0-205.225-generic 5.4.284)

```

方法二很直接，就算是vol2也很适用的工具，就是有点费时间

```
❯ strings 1.mem | grep -i "version"
%s version %s (buildd@lcy02-amd64-055) (gcc)
6J!tVERSION
PROFILE_VERSIONq
, VERSIONCRC
EC_CMD_PROTO_VERSION
VERSION
"version: %u, com
, {0x0000, "EC_CMD_PROTO_VERSION"}"
5.4.0-205-generic (buildd@lcy02-amd64-055) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.2)) #225-Ubuntu SMP Fri Jan 10 22:23:35 UTC 2025
Unsupported properties proto version
%s version %s (buildd@lcy02-amd64-055) (gcc)
6J!tVERSION
```

通过上述方法，得到我们需要的banner信息

```
Linux version 5.4.0-205-generic (buildd@lcy02-amd64-055) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.2)) #225-Ubuntu SMP Fri Jan 10 22:23:35 UTC 2025 (Ubuntu 5.4.0-205.225-generic 5.4.284)
```

emm，目标内核是Ubuntu 5.4.0-205-generic 是Ubuntu 20.04的内核版本

现在让我梳理下需要哪些文件，5.4.0-205-generic版本对应的调试符号包应该是linux-image-5.4.0-205-generic-dbgsym

正好，Ubuntu提供了足够全的包仓库，这是链接https://archive.ubuntu.com/ubuntu/pool/main/l/linux/

http://ddebs.ubuntu.com/pool/main/l/linux/

得多找找，好在找到了

![image-20250326220003033](https://yo1o.top/images/image-20250326220003033.png)

接下来运行命令解压ddeb文件，在这个目录下得到我们需要的vmlinux文件

```
❯ dpkg -x linux-image-unsigned-5.4.0-205-generic-dbgsym_5.4.0-205.225_amd64.ddeb ./extracted
❯ ls extracted/usr/lib/debug/boot/
vmlinux-5.4.0-205-generic
```

接下来我们需要用dwarf2json生成我们需要的符号表文件，首先是安装部分，这个工具需要go环境，使用`sudo apt install golang`进行安装

```
❯ go install github.com/volatilityfoundation/dwarf2json@latest
go: downloading github.com/volatilityfoundation/dwarf2json v0.9.0
go: downloading github.com/spf13/pflag v1.0.5
❯ $HOME/go/bin/dwarf2json --version
dwarf2json 0.9.0
output schema 6.2.0
❯ export PATH=$PATH:$HOME/go/bin
❯ dwarf2json --version
dwarf2json 0.9.0
output schema 6.2.0
```

通过上述操作，让我们完美安装好了工具

运行命令得到符号表

```
dwarf2json linux --elf ./extracted/usr/lib/debug/boot/vmlinux-5.4.0-205-generic > ubuntu-5.4.0-205-generic.json
```

这里需要我们把符号表保存到符号表文件夹下面

```
❯ cp ubuntu-5.4.0-205-generic.json ~/Desktop/tool/volatility3/volatility3/framework/symbols/linux
```

然后用linux.bash测试下，果然成功了

```
❯ vol3 -f 1.mem linux.bash
Volatility 3 Framework 2.25.0
Progress:  100.00               Stacking attempts finished
PID     Process CommandTime     Command

1583    bash    2025-02-14 11:24:45.000000 UTC  ls
1583    bash    2025-02-14 11:25:44.000000 UTC  insmod ./lime-5.4.0-205-generic.ko "path=/home/st4rr/1.mem format=lime"

```

哦，对了，这里用的1.mem来自于nctf2024的那道mc取证题目，一会儿我会在彩蛋中放置用vol2和vol3分别处理的wp，以及附件的网盘链接

## 给vol2制作profile文件

依旧需要我们拿到banner信息才行，但是使用vol2的linux.banner会失败，所以这里就依旧鼓励使用vol3的banner.Banner或strings手撕

```
sudo apt install dwarfdump
sudo apt install zip
```

这两条命令可以帮助我们提取DWARF调试信息，打包Profile文件

这里我们需要两个文件，vmlinux(带调试符号的内核镜像)，system.map(内核的静态符号表)，其中vmlinux的制作方法其实已经给出了，就是vol3中的那样，所以这里就不会赘叙

------

首先进入虚拟环境

❯ source ~/Desktop/tool/vol2env/bin/activate

然后进入有Makefile的路径中，在我这里则是~/Desktop/tool/volatility2/tools/linux

接下来将banner信息写入Makefile中

❯ sed -i 's/$(shell uname -r)/5.4.0-205-generic/g' Makefile

然后按照banner信息，在当前路径下拉取对应的Linux镜像

❯ docker run -it --rm -v $PWD:/volatility ubuntu:20.04 /bin/bash

然后拉取进来了，做一些工具配置（里面可以看到需要安装那几个文件，我在Ubuntu的官方库中一直找不到，最后只能采用这个方法了

```
root@a22870752bc3:/# apt update && apt install -y linux-image-5.4.0-205-generic linux-headers-5.4.0-205-generic build-essential dwarfdump make zip
```

接下来重新进入到Makefile的路径下，直接使用make

然后就大功告成了，对应的文件也会被生成

然后把我们需要的两个文件打包一下就行了，然后退出

```
root@a22870752bc3:/volatility# ls
Makefile  Makefile.enterprise  kcore  module.c  module.dwarf
root@a22870752bc3:/volatility# ls /boot
System.map-5.4.0-205-generic  grub        initrd.img-5.4.0-205-generic  vmlinuz                    vmlinuz.old
config-5.4.0-205-generic      initrd.img  initrd.img.old                vmlinuz-5.4.0-205-generic
root@a22870752bc3:/volatility# zip Ubuntu2004.zip module.dwarf /boot/System.map-5.4.0-205-generic
  adding: module.dwarf (deflated 91%)
  adding: boot/System.map-5.4.0-205-generic (deflated 79%)
root@a22870752bc3:/volatility# exit
exit
❯ ls
kcore  Makefile  Makefile.enterprise  module.c  module.dwarf  Ubuntu2004.zip
```

退出来了，我们再把zip移动到vol2储存profile的地方

```
❯ cp Ubuntu2004.zip ~/Desktop/tool/volatility2/volatility/plugins/overlays/linux/
```

使用info检查profile是否成功被选择

```
❯ python2 vol.py --info | grep Profile
Volatility Foundation Volatility Framework 2.6.1
Profiles
LinuxUbuntu2004x64    - A Profile for Linux Ubuntu2004 x64
VistaSP0x64           - A Profile for Windows Vista SP0 x64
VistaSP0x86           - A Profile for Windows Vista SP0 x86
```

我这里是成功了的

```
❯ python2 vol.py -f ~/Desktop/timu/1.mem --profile=LinuxUbuntu2004x64 linux_banner
Volatility Foundation Volatility Framework 2.6.1
Linux version 5.4.0-205-generic (buildd@lcy02-amd64-055) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.2)) #225-Ubuntu SMP Fri Jan 10 22:23:35 UTC 2025 (Ubuntu 5.4.0-205.225-generic 5.4.284)
❯ python2 vol.py -f ~/Desktop/timu/1.mem --profile=LinuxUbuntu2004x64 linux_pslist
Volatility Foundation Volatility Framework 2.6.1
Offset             Name                 Pid             PPid            Uid             Gid    DTB                Start Time
------------------ -------------------- --------------- --------------- --------------- ------ ------------------ ----------
0xffff9d4474443b80 systemd              1               0               0               0      0x0000000232238000 2025-02-14 06:16:04 UTC+0000
0xffff9d4474441dc0 kthreadd             2               0               0               0      ------------------ 2025-02-14 06:16:04 UTC+0000
```



## 小彩蛋

这里把上面使用的内存转储文件保存到网盘中欢迎自取（镜像文件来自于NCTF2024——谁动了我的mc

```
通过网盘分享的文件：passwords.txt等2个文件
链接: https://pan.baidu.com/s/1AtGZfy1iGdog2todU_KDnw?pwd=85x2 提取码: 85x2 
--来自百度网盘超级会员v6的分享
```

当初没有做出题目的原因中，制作不出符号表是原因之一，另一个原因就是我对vol3相关的Linux插件没有掌握

我顺便研究了所有的插件，并将它们汇总到新的文章中，这是[传送门](https://github.com/Yo1o-sir/Misc-script/blob/main/vol/Vol_plugins_summarize.md)

下面我会放使用vol2,vol3两个版本对提取文件的过程

### Vol3

首先呢，这里有三个语句可以尝试尝试

<img src="https://yo1o.top/images/image-20250327193522425.png" alt="image-20250327193522425" style="zoom:50%;" />

```
vol3 -f 1.mem linux.pagecache.Files >pagecache.txt
```

使用第一个语句，我们可以找到这个镜像文件的所有目录下的文件信息，包括它的InodeNum,InodeAddr，就比如这里，我之所以锁定mcsmanager是因为之前解题时曾手撕取证，知道所谓的平台实际上就是mcsmanager

![image-20250327193738382](https://yo1o.top/images/image-20250327193738382.png)

然后我们可以记录它的SuperblockAddr，然后使用第二条语句单独提取出来

```
❯ vol3 -f 1.mem linux.pagecache.InodePages --inode 0x9d43832b5688 --dump
Volatility 3 Framework 2.25.0
Progress:  100.00               Stacking attempts finished
PageVAddr       PagePAddr       MappingAddr     Index   DumpSafe        Flags

❯ ls
 1.mem                                                                                    linux-modules-5.4.0-205-generic_5.4.0-205.225_amd64.deb
 extracted                                                                                linux_profile
 inode_0x9d43832b5688.dmp                                                                 module.dwarf
```

然后发现提取的文件没有问题，用bandzip打开可以确定和我要查的配置信息有关

接下来再说说第三个命令，其实这里也比较建议第三条命令，因为vol3在恢复数据的时候，有一些数据无法恢复出来，这也就导致了使用第二条命令提取的时候偶尔会失败，还有，第二条命令只能一条一条提取，而这个mcsmanager的相关文件又太多，所以才会用到第三个命令，一次性将所有可以恢复的数据恢复出来保存成tarball，就是需要费一点点时间

`vol3 -f 1.mem linux.pagecache.RecoverFs`

最后自动在当前目录下保存了recovered_fs.tar.gz

使用WinRAR打开即可

很轻松就发现只有三个路径下有数据

![image-20250327194910674](https://yo1o.top/images/image-20250327194910674.png)

然后这个WinRAR还有个查找功能，直接查找mcsmanager即可

![image-20250327194947286](https://yo1o.top/images/image-20250327194947286.png)

我这里偷了个懒，直接把mcsmanager这整个文件夹解压提取出来了，后续的操作后面补，这里再把vol2提取的流程补充一下

### Vol2

这里磕了好一会儿，一直得到的报错是没有权限去创建文件夹，好在在root模式下再进入虚拟环境后，就有权限创建文件了，这里偷了个懒，只用linux_recover_filesystem恢复了，借鉴网上其他的wp，他们先用linux_find_file -L列出全部文件，然后用linux_find_file -i offset -o xxx.dat一个一个文件进行导出操作

至于我的话，就用了这个

```
(vol2env) root@Yolo:/home/yolo/Desktop/tool/volatility2# python2 vol.py -f /home/yolo/Desktop/timu/1.mem --profile=LinuxUbuntu2004x64 linux_recover_filesystem --dump-dir=/home/yolo/Desktop/tool/volatility2/vol2fullresolve/
Volatility Foundation Volatility Framework 2.6.1

```

由于恢复时间实在是漫长，我这里看到mcsmanager恢复出来后，就选择中止恢复了

![image-20250327220652738](https://yo1o.top/images/image-20250327220652738.png)

------

接下来就是对题目剩下部分的数据分析处理了，先说题目信息，我要找到面板的密码，放火者的id，放火点的坐标

然后呢，我就以vol2恢复的这个结果进行操作（用vol3恢复的结果和这个一模一样的，这是我用WinRAR提取的结果，二者一样的）

![image-20250327221545637](https://yo1o.top/images/image-20250327221545637.png)

对mcsmanager的配置有所了解的话，很轻松的在这个路径下找到用户信息![image-20250327221736731](https://yo1o.top/images/image-20250327221736731.png)

用bcrypt进行加密保存的密码我们可以写脚本遍历爆破得到明文密码(有件事没说，题目给的附件中除了镜像，还有个密码本)

```python
import bcrypt

def crack_bcrypt(hash_to_crack, password_file):
    with open(password_file, 'r', encoding='utf-8') as f:
        for line in f:
            password = line.strip().encode()
            if bcrypt.checkpw(password, hash_to_crack.encode()):
                print(f"[+] 找到密码: {password.decode()}")
                return
    print("[-] 未找到匹配的密码")

if __name__ == "__main__":
   
    target_hash = "$2a$10$jtOn5mgMKwhjevsKPe/ps.CIRJ1NoP/uAFWNZos7OF8vzKKGJrIxm"
    
  
    password_file = "passwords.txt"
    
    crack_bcrypt(target_hash, password_file)

```

得到的密码是这个`I0am0alone`

当初手撕取证的时候，我可以知道，这个镜像隔一段时间会用FTB进行存档一次，共计10个压缩包（这里没啥技术含量的其实，就是用strings导出mem中的所有明文信息，就能分析到的

这里举个例子

![image-20250327222456891](https://yo1o.top/images/image-20250327222456891.png)

根据里面的信息，可以直接锁定归档的文件

![image-20250327222606581](https://yo1o.top/images/image-20250327222606581.png)

emm，有几个文件恢复的不够好，解压失败，这里随便解压了最后一次归档

分析了下stats下的json文件，可以找出使用过的工具

![image-20250327224259104](https://yo1o.top/images/image-20250327224259104.png)

这里有个关键信息，就是说这里用了lava_bucket1次，而这个就是熔岩桶，与题目要求的点火者有很大的关系

多翻翻其他json文件，可以判断，这里只有6个玩家玩过

![image-20250327223531575](https://yo1o.top/images/image-20250327223531575.png)

然后结合上面的uuid信息，已经能锁定玩火者就是Nathan了

找到了可疑点了

![image-20250327225723784](https://yo1o.top/images/image-20250327225723784.png)

然后将那个解压出来的world搬到我电脑上的mc配置文件的saves下面，再打开就行，这里用了F3打开调试信息

![image-20250327231552549](https://yo1o.top/images/image-20250327231552549.png)

显然坐标是-405_63_132

然后得到了最终flag`nctf{I0am0alone_Nathan_-405_63_132}`

