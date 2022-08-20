---
layout: post
title: Debian network booting
comments: true
category:
- english
- linux
---

# Debian init basics

Debian uses [systemd](https://wiki.debian.org/systemd) as the default init system after Debian 8 ("jessie"). It initialize the system services including the network.

Tradionally, the network is specified in `/etc/network/interfaces` and is maniputed by `/sbin/ifup`. During the system init, `/etc/init.d/networking` invokes `ifup` and loads `interfaces` for you before systemd. This set of tools can also be called `ifupdown`.

With systemd, the scripts in `/etc/init.d` is not directly used. systemd tasks are organized as **units**. `networking.service` is the unit that adapts the traditional `ifup` and `interfaces`. That's the reason editting `interfaces` is still effective.

```console
$ systemctl status networking
● networking.service - Raise network interfaces
     Loaded: loaded (/lib/systemd/system/networking.service; enabled; vendor preset: enabled)
     Active: active (exited) since Mon 2022-08-15 17:17:06 EDT; 4 days ago
       Docs: man:interfaces(5)
    Process: 281 ExecStart=/sbin/ifup -a --read-environment (code=exited, status=0/SUCCESS)
   Main PID: 281 (code=exited, status=0/SUCCESS)
        CPU: 251ms

Aug 15 17:17:06 raspberrypi systemd[1]: Starting Raise network interfaces...
Aug 15 17:17:06 raspberrypi systemd[1]: Finished Raise network interfaces.
```

# Debian network alternatives

Besides `ifupdown`, there are network management alternatives including: (the description is from [Debian Reference][debian-ref])

- ifupdown: legacy `ifupdown` package and its configuration file `/etc/network/interfaces`
- NetworkManager (NM): the modern network configuration for desktop
- systemd-network (networkd): the modern network configuration without GUI

`netplan` is developped and used by Ubuntu.

Accroding to the reference, it's suggested `networking.service` (a.k.a `interface` only config `lo`) while leaving the rest interfaces e.g. eth to NM or networkd.

# DHCP and DNS

t.b.c

[debian-ref]: https://www.debian.org/doc/manuals/debian-reference/ch05.en.html#_the_modern_network_configuration_for_desktop

