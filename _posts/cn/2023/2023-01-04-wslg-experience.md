---
layout: post
title: WSL使用心得（2023年）
comments: true
lang: cn
category:
- wsl
---

# 先说重点

Windows Subsystem for Linux (WSL)是Windows提供的Linux虚拟机。我用了四年多，踩过一些坑，总体体验良好。

我的日常工作主要使用OCaml语言相关工具，也在WSL里编译LLVM/Clang、z3等项目，运行Linux平台的工具比如texlive、博客（Ruby、Rust），管理实验室的server，出于好奇跑过pytorch和CUDA。WSL可以在十分钟之内编译Clang（优化后不到五分钟）。

WSL虚拟机磁盘镜像保存在Windows本地的某个vhdx文件里。WSL提供Windows本地文件和虚拟机实例内的文件实时互相访问：虚拟机内通过路径`/mnt/<driver>`访问Windows本地文件，Windows本地通过路径`\\wsl.localhost\Ubuntu`访问虚拟机内的文件。
我主要使用VSCode的Remote Development插件，通过ssh，在虚拟机内访问本地文件。（坑）目前的WSL架构下（WSL2)，跨OS的文件互相访问有IO瓶颈。我的日常项目没有太多IO操作所以影响不大。如果要编译大型项目，或者有操作会在当前目录安装大量文件，请将项目目录置于虚拟机本地路径。WSL的虚拟机的$PATH继承了Windows本地的环境变量，你也可以在虚拟机内运行Windows本地程序。

总之，WSL提供了一种“不在Windows原生环境下”进行开发的方法，是一个还不错的虚拟机。除了一些坑，当下缺点主要在于WSL基于一个微软定制的Linux kernel。kernel相关的工具或者需要额外的操作、或者尚未支持。

最近遇到的两个坑，

WSL默认给虚拟机分配一半的物理内存。可以通过修改`C:\Users\<id>\.wslconfig`来分配更多内存。详见： <https://learn.microsoft.com/en-us/windows/wsl/wsl-config#configuration-setting-for-wslconfig>

WSL内的git使用Windows内git-credential-manager来管理credential，需要修改~/.gitconfig。详见：<https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git#git-credential-manager-setup>


（上面的内容是这些年来的使用感悟，下面的内容是这两天现学的。）

# WSLg

最近偶然发现Windows 10 Build 19044实装了WSLg，内置了对Linux GUI apps的支持。此版本之前，通过配置Linux内的X Server，使用Windows程序（比如vcxsrv）来渲染。如果要使用WSLg，记得取消对`$DISPLAY`及相关环境变量的修改。

我试了OCaml的SDL绑定和PulseAudio绑定，表现良好。用VLC播放高清视频，流畅。播放无损音乐，略卡顿。暂不清楚原因。

![WSLg](/assets/img/2023/WSLg_e1.png)

现在，你的电脑里同时运行了你的虚拟机实例（图中user distro），WSLg实例（图中WSLg system distro），和Windows本地程序msrdc.exe。WSLg提供图画和声音的中转：接受你的user distro的音画请求，转发到Windows本地程序msrdc.exe。

![WSLg](/assets/img/2023/WSLg.png)


在你的虚拟机实例能发现相关设置：

```shell
$ ls /mnt/wslg
distro/  dumps/          PulseAudioRDPSink=    PulseServer=  stderr.log    weston.log
doc/     pulseaudio.log  PulseAudioRDPSource=  runtime-dir/  versions.txt  wlog.log
$ echo $DISPLAY
:0
$ echo $PULSE_SERVER
/mnt/wslg/PulseServer
```

在你的虚拟机里可以来快速检查图画和声音运行情况：

```shell
$ xclock

$ pactl play-sample
```

偶尔会遇到PulseAudio服务器链接中断：

```shell
$ pactl play-sample 
Connection failure: Connection refused
pa_context_connect() failed: Connection refused
```

解决方法是重启WSLg实例里的weston（参考<https://github.com/microsoft/wslg/issues/426#issuecomment-907635787>）。

```shell
# enter WSLg distro from Windows Terminal
PS wsl --system
# find the westop pid
$ ps x | grep weston
  131 ?        Sl     0:00 /usr/bin/weston --backend=rdp-backend.so --modules=wslgd-notify.so --xwayland --log=/mnt/wslg/weston.log --socket=wayland-0 --shell=rdprail-shell.so --logger-scopes=log,rdp-backend,rdprail-shell
# kill it to restart it
$ kill -9 131
```

Linux常见的声音服务有ALSA和PulseAudio。跳过PulseAudio而直接使用ALSA的程序，有方法提出可以通过`libasound2` (ALSA library)里的插件来获得支持，详见<https://github.com/microsoft/wslg/issues/864>。其他issues里有人提到这个方法可行。不过我测试mame不通过。再等等官方的更新吧。

另外，WSLg提供的是对GUI app的支持，目前并不提供对全desktop的支持（不能跑xfce）。这个问题里有讨论<https://askubuntu.com/questions/1385703/launch-xfce4-or-other-desktop-in-windows-11-wslg-ubuntu-distro>

