# Fig pre block. Keep at the top of this file.
[[ -f "$HOME/.fig/shell/zshrc.pre.zsh" ]] && builtin source "$HOME/.fig/shell/zshrc.pre.zsh"
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export PATH="$HOME/.bin:$PATH"
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
ENABLE_CORRECTION="true"
COMPLETION_WAITING_DOTS="false"
DISABLE_UNTRACKED_FILES_DIRTY="true"

# Set Locale
export LANG=en_US
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# History settings
HISTSIZE=5000
SAVEHIST=5000
setopt BANG_HIST                 # Treat the '!' character specially during expansion.
setopt EXTENDED_HISTORY          # Write the history file in the ":start:elapsed;command" format.
setopt INC_APPEND_HISTORY        # Write to the history file immediately, not when the shell exits.
setopt SHARE_HISTORY             # Share history between all sessions.
setopt HIST_EXPIRE_DUPS_FIRST    # Expire duplicate entries first when trimming history.
setopt HIST_IGNORE_DUPS          # Don't record an entry that was just recorded again.
setopt HIST_IGNORE_ALL_DUPS      # Delete old recorded entry if new entry is a duplicate.
setopt HIST_FIND_NO_DUPS         # Do not display a line previously found.
setopt HIST_IGNORE_SPACE         # Don't record an entry starting with a space.
setopt HIST_SAVE_NO_DUPS         # Don't write duplicate entries in the history file.
setopt HIST_REDUCE_BLANKS        # Remove superfluous blanks before recording entry.
setopt HIST_VERIFY               # Don't execute immediately upon history expansion.
setopt HIST_BEEP                 # Beep when accessing nonexistent history.

plugins=(
  ag
  aliases
  autoupdate
  colored-man-pages
  common-aliases
  dircycle
  kubectl
  git
  git-auto-fetch
  git zsh-autosuggestions
  zsh-autosuggestions
  zsh-syntax-highlighting
)
source $ZSH/oh-my-zsh.sh
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# Load zsh-completions
if type brew &>/dev/null; then
  fpath=( $(brew --prefix)/share/zsh-completions $fpath )

  autoload -Uz compinit
  compinit
fi
autoload -U +X bashcompinit && bashcompinit

test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

# aliases
export EDITOR="nvim"
alias vim="nvim"
alias sudoedit="nvim"
alias sed=gsed
alias grep=ggrep
alias ssv=/usr/local/bin/ssv.sh
alias bootcamp_bastion=/usr/local/bin/ssv-bastion.sh
alias devops_bastion=/usr/local/bin/devops_bastion_us-east-1.sh
fpath=($fpath ~/.zsh/completion)

export PATH="/usr/local/opt/mysql-client/bin:$PATH"

# Minikube kubectl alias
alias kubectl="minikube kubectl --"

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

eval $(thefuck --alias)
source ~/.fig/shell/pre_integration
source ~/.fig/shell/post_integration

# Fig post block. Keep at the bottom of this file.
[[ -f "$HOME/.fig/shell/zshrc.post.zsh" ]] && builtin source "$HOME/.fig/shell/zshrc.post.zsh"

# Source post-integration scripts
source /Users/yaacov/.fig/shell/zprofile.post.zsh
source /Users/yaacov/.fig/shell/zshrc.post.zsh
