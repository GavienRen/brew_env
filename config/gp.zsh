# zsh config
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(git
        z
        zsh-syntax-highlighting
        zsh-autosuggestions
)
source $ZSH/oh-my-zsh.sh
# zsh config end

setopt no_share_history
alias his="history"
alias gs='git status'
alias gl='git log --graph --pretty='\''%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%ar) %C(bold blue)<%an>%Creset'\'' --all'
alias f='find . -name '

export REPO_URL='https://mirrors.tuna.tsinghua.edu.cn/git/git-repo'
export PATH=/home/$HOME/bin:$PATH

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
# p10k configure

# pyenv config
export PYTHON_BUILD_MIRROR_URL=https://registry.npmmirror.com/-/binary/python/
export PYTHON_BUILD_MIRROR_URL_SKIP_CHECKSUM=1
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"