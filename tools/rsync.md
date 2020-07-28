-vra  
-a 是重要的，因为 rsync check up-to-date 的时候会用到日期信息，如果不加 -a 目标的修改时间都是拷贝的时候，没法增量拷贝。  
windows 配这个东西的自动化挺麻烦的，最方便的方法是把 ssh key 放到 cwRsync 自带的 .ssh 目录下（还得把 root 完全控制私钥的权限给取消了），然后修改它自带的 rsync.cmd 脚本。