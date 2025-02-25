# 项目介绍

一个使用Python进行图形化配置H3C交换机以及路由器的项目
# 使用方法
## H3C交换机开启SSH以及NETCONF over SSH

```
system-view
public-key local create rsa
local-user admin class manage
password simple YourPassword  # 实际建议使用加密密码（如：password cipher）
service-type ssh netconf       # 允许SSH和NETCONF服务
authorization-attribute user-role network-admin  # 赋予最高权限
quit
ssh server enable              # 全局启用SSH
ssh server version 2           # 强制使用SSH v2（更安全）
ssh user admin service-type all authentication-type password  # 绑定用户和认证方式
user-interface vty 0 15
 protocol inbound ssh          # 仅允许SSH登录
 authentication-mode scheme    # 使用AAA认证（需本地用户）
 user-role network-admin       # 用户权限
quit
netconf ssh server enable      # 启用NETCONF over SSH
save
```
## 测试SSH连接性

```
ssh admin@交换机IP
``` 
