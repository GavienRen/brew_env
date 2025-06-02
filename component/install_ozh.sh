#!/bin/bash
set -e
# set -x

source ./utils/log.sh

declare -A repos=(
    ["ohmyzsh"]="https://mirrors.tuna.tsinghua.edu.cn/git/ohmyzsh.git"
    ["zsh-autosuggestions"]="https://gitee.com/mirrors/zsh-autosuggestions.git"
    ["zsh-syntax-highlighting"]="https://gitee.com/mirrors/zsh-syntax-highlighting.git"
    ["powerlevel10k"]="https://gitee.com/romkatv/powerlevel10k.git"
)

# 定义目标目录的路径
ohmyzsh_dir="$HOME/.oh-my-zsh"
zsh_custom_dir="$ohmyzsh_dir/custom"

cp gp.zsh ~/.gp.zsh

# 函数：克隆仓库（如果目录不存在）
clone_if_not_exists() {
    local repo_name=$1
    local repo_url=$2
    local target_dir=$3

    if [ ! -d "$target_dir" ]; then
        echo "Cloning $repo_name..."
        git clone --depth=1 "$repo_url" "$target_dir"
    else
        echo "$repo_name 已经存在，跳过克隆。"
    fi
}

rm ohmyzsh -rf
if [ ! -d "$ohmyzsh_dir" ]; then
    clone_if_not_exists "ohmyzsh" "${repos[ohmyzsh]}" "ohmyzsh"
    cd "ohmyzsh/tools"
    REMOTE=${repos[ohmyzsh]} sh install.sh
    rm -rf ohmyzsh
else
    log_warning "ohmyzsh 已经存在，跳过克隆。"
fi

clone_if_not_exists "zsh-autosuggestions" "${repos["zsh-autosuggestions"]}" "$zsh_custom_dir/plugins/zsh-autosuggestions"
clone_if_not_exists "zsh-syntax-highlighting" "${repos["zsh-syntax-highlighting"]}" "$zsh_custom_dir/plugins/zsh-syntax-highlighting"
clone_if_not_exists "powerlevel10k" "${repos[powerlevel10k]}" "$zsh_custom_dir/themes/powerlevel10k"

if ! grep -q "source ~/.gp.zsh" ~/.zshrc; then
    echo "source ~/.gp.zsh" >>~/.zshrc
fi
