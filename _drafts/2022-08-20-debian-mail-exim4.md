---
layout: post
title: Debian Mail
comments: true
category:
- english
- linux
---

`sudo zless /var/log/exim4/mainlog.5.gz`

```
2022-08-15 13:36:26 Start queue run: pid=19248
2022-08-15 13:36:26 End queue run: pid=19248
2022-08-15 13:40:02 1oNe4I-00052i-01 <= www-data@pl.cs.jhu.edu U=www-data P=local S=1130
2022-08-15 13:40:02 1oNe4I-00052i-01 => zpalmer <root@pl.cs.jhu.edu> R=local_user T=maildir_home
2022-08-15 13:40:02 1oNe4I-00052i-01 Completed
2022-08-15 13:50:01 1oNeDx-00054s-Hc <= www-data@pl.cs.jhu.edu U=www-data P=local S=1130
2022-08-15 13:50:01 1oNeDx-00054s-Hc => zpalmer <root@pl.cs.jhu.edu> R=local_user T=maildir_home
2022-08-15 13:50:01 1oNeDx-00054s-Hc Completed
2022-08-15 14:00:02 1oNeNe-0005DD-60 <= www-data@pl.cs.jhu.edu U=www-data P=local S=1130
2022-08-15 14:00:02 1oNeNe-0005DD-60 => zpalmer <root@pl.cs.jhu.edu> R=local_user T=maildir_home
2022-08-15 14:00:02 1oNeNe-0005DD-60 Completed
2022-08-15 14:42:22 1oNf2b-0000Dd-FO <= root@pl.cs.jhu.edu U=root P=local S=427
2022-08-15 14:42:22 1oNf2b-0000E9-FP <= root@pl.cs.jhu.edu U=root P=local S=488
2022-08-15 14:42:22 1oNf2b-0000Dw-FO <= root@pl.cs.jhu.edu U=root P=local S=488
2022-08-15 14:42:22 1oNf2b-0000Dt-FO <= root@pl.cs.jhu.edu U=root P=local S=427
2022-08-15 14:42:22 1oNf2b-0000E6-FQ <= root@pl.cs.jhu.edu U=root P=local S=427
2022-08-15 14:42:22 1oNf2b-0000Dg-FO <= root@pl.cs.jhu.edu U=root P=local S=488
2022-08-15 14:42:23 1oNf2b-0000E6-FQ H=smtp.cs.jhu.edu [128.220.13.50] Network is unreachable
2022-08-15 14:42:23 1oNf2b-0000Dg-FO H=smtp.cs.jhu.edu [128.220.13.50] Network is unreachable
2022-08-15 14:42:23 1oNf2b-0000E9-FP H=smtp.cs.jhu.edu [128.220.13.50] Network is unreachable
2022-08-15 14:42:23 1oNf2b-0000Dw-FO H=smtp.cs.jhu.edu [128.220.13.50] Network is unreachable
2022-08-15 14:42:23 1oNf2b-0000Dt-FO H=smtp.cs.jhu.edu [128.220.13.50] Network is unreachable
2022-08-15 14:42:23 1oNf2b-0000Dd-FO H=smtp.cs.jhu.edu [128.220.13.50] Network is unreachable
2022-08-15 14:42:24 1oNf2b-0000E6-FQ == root@pl.cs.jhu.edu R=smarthost T=remote_smtp_smarthost defer (101): Network is unreachable
2022-08-15 14:42:24 1oNf2b-0000Dg-FO == root@pl.cs.jhu.edu R=smarthost T=remote_smtp_smarthost defer (101): Network is unreachable
2022-08-15 14:42:24 1oNf2b-0000Dt-FO == root@pl.cs.jhu.edu R=smarthost T=remote_smtp_smarthost defer (101): Network is unreachable
2022-08-15 14:42:24 1oNf2b-0000Dw-FO == root@pl.cs.jhu.edu R=smarthost T=remote_smtp_smarthost defer (101): Network is unreachable
2022-08-15 14:42:25 1oNf2b-0000E9-FP == root@pl.cs.jhu.edu R=smarthost T=remote_smtp_smarthost defer (101): Network is unreachable
2022-08-15 14:42:25 1oNf2b-0000Dd-FO == root@pl.cs.jhu.edu R=smarthost T=remote_smtp_smarthost defer (101): Network is unreachable
2022-08-15 14:42:30 exim 4.92 daemon started: pid=1332, -q30m, listening for SMTP on [127.0.0.1]:25 [::1]:25
```

