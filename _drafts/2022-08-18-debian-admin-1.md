---
layout: post
title: Be a lab server admin
comments: true
category:
- english
- linux
---

# Intro

t.b.c

# Troubleshooting 1 : network

```console
shiwei@pl:~$ last reboot
reboot   system boot  5.10.0-17-amd64  Thu Aug 18 17:57   still running
reboot   system boot  5.10.0-17-amd64  Thu Aug 18 17:04 - 17:55  (00:51)
reboot   system boot  5.10.0-17-amd64  Wed Aug 17 17:39 - 17:00  (23:20)
reboot   system boot  5.10.0-17-amd64  Wed Aug 17 17:14 - 17:34  (00:20)
reboot   system boot  5.10.0-17-amd64  Wed Aug 17 15:34 - 17:12  (01:37)
reboot   system boot  4.19.0-17-amd64  Tue Aug 16 14:38 - 15:28 (1+00:49)
reboot   system boot  4.19.0-17-amd64  Tue Aug 16 14:10 - 14:37  (00:27)
reboot   system boot  4.19.0-17-amd64  Tue Aug 16 13:51 - 14:07  (00:15)
reboot   system boot  4.19.0-17-amd64  Mon Aug 15 16:21 - 13:45  (21:23)
reboot   system boot  4.19.0-17-amd64  Mon Aug 15 15:33 - 16:20  (00:47)
reboot   system boot  4.19.0-17-amd64  Mon Aug 15 15:28 - 15:32  (00:03)
reboot   system boot  4.19.0-17-amd64  Mon Aug 15 14:50 - 15:21  (00:30)
reboot   system boot  4.19.0-17-amd64  Mon Aug 15 14:39 - 15:21  (00:41)
reboot   system boot  4.19.0-17-amd64  Mon Oct 25 12:04 - 14:00 (294+01:55)
reboot   system boot  4.19.0-17-amd64  Mon Oct 25 11:45 - 11:53  (00:08)
reboot   system boot  4.19.0-16-amd64  Thu May  6 23:51 - 11:53 (171+12:02)
reboot   system boot  4.19.0-16-amd64  Tue Apr 27 10:41 - 11:53 (181+01:12)
reboot   system boot  4.19.0-10-amd64  Thu Aug 27 12:39 - 11:53 (423+23:14)
reboot   system boot  4.19.0-10-amd64  Thu Aug 27 11:58 - 11:53 (423+23:55)
reboot   system boot  4.19.0-5-amd64   Mon Jul 15 13:35 - 11:53 (832+22:18)
```

I became the PL Lab server admin since May 2019. We had an old server that runs our website, chat service, git, and, of-course develop environment.

The server runs Debian. I updated it from debian 9 to debian 10 in summer 2019.

The last time to boot before this week is Oct 2021 (294 days ago) due to power outage. There was some boot or init error so I have to manually press enter several times before the login screen appears. But after that, it works fine.

```console
shiwei@pl:~$ sudo ls -al /var/log/apt/
total 396
drwxr-xr-x  2 root root   4096 Aug 18 17:46 .
drwxr-xr-x 29 root root  12288 Aug 19 00:00 ..
-rw-r--r--  1 root root  87264 Aug 18 17:46 eipp.log.xz
-rw-r--r--  1 root root   1148 Aug 18 17:46 history.log
-rw-r--r--  1 root root   1784 Dec  6  2020 history.log.10.gz
-rw-r--r--  1 root root   2036 Sep 29  2020 history.log.11.gz
-rw-r--r--  1 root root    527 Aug 27  2020 history.log.12.gz
-rw-r--r--  1 root root  33001 Aug 17 16:33 history.log.1.gz
-rw-r--r--  1 root root    145 Feb  5  2022 history.log.2.gz
-rw-r--r--  1 root root   3920 Feb  4  2022 history.log.3.gz
-rw-r--r--  1 root root    141 Jan 25  2022 history.log.4.gz
-rw-r--r--  1 root root   2211 Jun 21  2021 history.log.5.gz
-rw-r--r--  1 root root    446 Jun  5  2021 history.log.6.gz
-rw-r--r--  1 root root   1696 Mar 29  2021 history.log.7.gz
-rw-r--r--  1 root root    749 Feb  9  2021 history.log.8.gz
-rw-r--r--  1 root root   1502 Feb  8  2021 history.log.9.gz
-rw-r-----  1 root adm    8839 Aug 18 17:46 term.log
-rw-r-----  1 root adm    4533 Dec  6  2020 term.log.10.gz
-rw-r-----  1 root adm    5511 Sep 29  2020 term.log.11.gz
-rw-r-----  1 root adm    1538 Aug 27  2020 term.log.12.gz
-rw-r-----  1 root adm  112194 Aug 17 16:33 term.log.1.gz
-rw-r-----  1 root adm     305 Feb  5  2022 term.log.2.gz
-rw-r-----  1 root adm   12746 Feb  4  2022 term.log.3.gz
-rw-r-----  1 root adm     337 Jan 25  2022 term.log.4.gz
-rw-r-----  1 root adm    6086 Jun 21  2021 term.log.5.gz
-rw-r-----  1 root adm    1000 Jun  5  2021 term.log.6.gz
-rw-r-----  1 root adm    4517 Mar 29  2021 term.log.7.gz
-rw-r-----  1 root adm    2057 Feb  9  2021 term.log.8.gz
-rw-r-----  1 root adm    4178 Feb  8  2021 term.log.9.gz
```

I updates apt package on Feb 2022 for upgrading postgresql to 13. 

```console
$ sudo zless -r /var/log/apt/term.log.3.gz
```

I don't see interesting (conf) changes on network, ethernet, or exim4.

# init log error

```log
Aug 16 14:38:48 pl systemd-udevd[350]: ethtool: autonegotiation is unset or enabled, the speed and duplex are not writable.
Aug 16 14:38:48 pl systemd-udevd[343]: ethtool: autonegotiation is unset or enabled, the speed and duplex are not writable.
Aug 16 14:38:48 pl systemd-udevd[350]: eth0: Failed to rename network interface 2 from 'eth0' to 'eth1': File exists
Aug 16 14:38:48 pl systemd-udevd[343]: eth1: Failed to rename network interface 3 from 'eth1' to 'eth0': File exists
Aug 16 14:38:48 pl systemd-udevd[350]: eth0: Failed to process device, ignoring: File exists
Aug 16 14:38:48 pl systemd-udevd[343]: eth1: Failed to process device, ignoring: File exists
```

# dhclient

```
root@pl:/home/shiwei# journalctl -u systemd-udevd -b3
-- Journal begins at Tue 2022-08-16 14:38:47 EDT, ends at Fri 2022-08-19 00:48:32 EDT. --
Aug 17 17:14:18 pl systemd[1]: Starting Rule-based Manager for Device Events and Files...
Aug 17 17:14:19 pl systemd[1]: Started Rule-based Manager for Device Events and Files.
Aug 17 17:14:19 pl systemd-udevd[342]: Using default interface naming scheme 'v247'.
Aug 17 17:14:19 pl systemd-udevd[339]: Using default interface naming scheme 'v247'.
Aug 17 17:14:19 pl systemd-udevd[339]: ethtool: autonegotiation is unset or enabled, the speed and duplex are not writable.
Aug 17 17:14:19 pl systemd-udevd[342]: ethtool: autonegotiation is unset or enabled, the speed and duplex are not writable.
Aug 17 17:14:19 pl systemd-udevd[339]: eth1: Failed to rename network interface 3 from 'eth1' to 'eth0': File exists
Aug 17 17:14:19 pl systemd-udevd[342]: eth0: Failed to rename network interface 2 from 'eth0' to 'eth1': File exists
Aug 17 17:14:19 pl systemd-udevd[342]: eth0: Failed to process device, ignoring: File exists
Aug 17 17:14:19 pl systemd-udevd[339]: eth1: Failed to process device, ignoring: File exists
Aug 17 17:14:19 pl systemd-udevd[342]: ethtool: autonegotiation is unset or enabled, the speed and duplex are not writable.
Aug 17 17:16:21 pl systemd-udevd[1134]: Using default interface naming scheme 'v247'.
Aug 17 17:16:21 pl systemd-udevd[1134]: ethtool: autonegotiation is unset or enabled, the speed and duplex are not writable.
```

However,

```
shiwei@pl:~$ cat /etc/udev/udev.conf
# see udev.conf(5) for details
#
# udevd is also started in the initrd.  When this file is modified you might
# also want to rebuild the initrd, so that it will include the modified configuration.

#udev_log=info
#children_max=
#exec_delay=
#event_timeout=180
#timeout_signal=SIGKILL
#resolve_names=early
```

```
shiwei@pl:~$ ls -al /etc/udev/rules.d/
total 12
drwxr-xr-x 2 root root 4096 Sep  4  2013 .
drwxr-xr-x 4 root root 4096 Aug 17 14:26 ..
-rw-r--r-- 1 root root  715 Sep  4  2013 70-persistent-net.rules
```

```
shiwei@pl:~$ cat /etc/udev/rules.d/70-persistent-net.rules
# This file was automatically generated by the /lib/udev/write_net_rules
# program, run by the persistent-net-generator.rules rules file.
#
# You can modify it, as long as you keep each rule on a single
# line, and change only the value of the NAME= key.

# PCI device 0x8086:/sys/devices/pci0000:00/0000:00:1c.5/0000:04:00.0 (e1000e)
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="74:d0:2b:98:17:f1", ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="eth*", NAME="eth0"

# PCI device 0x8086:/sys/devices/pci0000:00/0000:00:1c.4/0000:03:00.0 (e1000e)
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="74:d0:2b:98:17:f0", ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="eth*", NAME="eth1"
```

