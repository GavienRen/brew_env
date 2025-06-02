# BrewEnv

> 🍺 Brew env - 一键酿造你的专属开发环境

# 快速开始
```bash
# 安装基础工具，支持本地及远程SSH操作环境配置
sudo apt install git openssh-server net-tools && ifconfig

# 配置开发环境(默认不更换软件源)
./brew_env.py env

# 配置开发环境并更换软件源
./brew_env.py env --change-source
```

# TODO
- ssh免密登录
  - ssh-copy-id -i ~/.ssh/id_rsa.pub xxx@xxx
- 配置网络环境
  - 远程唤醒（开机）
    - sudo vim /etc/network/if-up.d/wpasupplicant 增加/usr/sbin/ethtool -s enp14s0  wol g
    - sudo ethtool enp14s0
- pyenv（使用国内源）
  - curl https://pyenv.run | bash


