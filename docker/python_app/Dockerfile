FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt upgrade -y && apt install -y curl
RUN apt install -y git make build-essential
RUN apt install -y sudo bash
RUN apt install -y libev-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
RUN apt install -y wget nano vim tmux htop

ENV PYTHON_VERSION=3.7.2
ENV PYENV_VERSION=1.2.9

ENV USER=web-user
ENV HOME=/home/$USER

ENV APP_NAME=python_app
ENV APP_DIR=/$APP_NAME

ENV PYENV_DIR=$HOME/.pyenv
ENV PYENV_BIN_ROOT=$PYENV_DIR/bin
ENV PYENV_BIN=$PYENV_BIN_ROOT/pyenv
ENV ENV_BIN_ROOT=$PYENV_DIR/versions/$APP_NAME/bin
ENV ENV_PYTHON_BIN=$ENV_BIN_ROOT/python
ENV ENV_PIP_BIN=$ENV_BIN_ROOT/pip

ENV SHELL_FN=.shell_pyenv
ENV SHELL_ENV_FP=$HOME/$SHELL_FN

RUN useradd -m -s /bin/bash $USER

RUN echo 'Europe/Kiev' > /etc/timezone
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN dpkg-reconfigure -f noninteractive tzdata

USER $USER
WORKDIR $HOME
RUN git clone https://github.com/pyenv/pyenv.git $PYENV_DIR
RUN git clone https://github.com/pyenv/pyenv-virtualenv.git $PYENV_DIR/plugins/pyenv-virtualenv
WORKDIR $PYENV_DIR
RUN git checkout tags/v$PYENV_VERSION
WORKDIR $HOME
COPY $SHELL_FN $HOME
USER root
RUN chown $USER:$USER $HOME/$SHELL_FN
USER $USER
RUN echo ". $SHELL_ENV_FP" >> $HOME/.bashrc

RUN $PYENV_BIN install $PYTHON_VERSION
RUN $PYENV_BIN virtualenv $PYTHON_VERSION $APP_NAME

user root
RUN mkdir $APP_DIR
RUN chown $USER:$USER -R $APP_DIR

USER $USER
WORKDIR $APP_DIR
COPY requirements.txt $APP_DIR
RUN $ENV_PIP_BIN install -U pip
RUN $ENV_PIP_BIN install -r requirements.txt

# ohmyzsh
ENV ZSH_CONF_FN=.zshrc
ENV ZSH_CONF_FP=$HOME/$ZSH_CONF_FN
USER root
RUN apt install -y zsh
RUN chsh $USER -s /bin/zsh

ENV TERM xterm
USER $USER
WORKDIR $HOME
# run the installation script
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
RUN echo ". $SHELL_ENV_FP" >> $ZSH_CONF_FP
RUN sed -i -e 's/plugins=(git)/plugins=(git python django docker nmap pip postgres rsync sudo tmux systemd)/g' $ZSH_CONF_FP
RUN sed -i -e 's/ZSH_THEME="robbyrussell"/ZSH_THEME="ys"/g' $ZSH_CONF_FP
RUN echo "export LANG=en_US.UTF-8" >> $ZSH_CONF_FP
RUN echo "workon $APP_NAME" >> $ZSH_CONF_FP
WORKDIR $APP_DIR


# add entrypoint script
USER root
COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
RUN apt -y install postgresql-client iputils-ping telnet
USER $USER

ENTRYPOINT ["/bin/zsh", "/entrypoint.sh"]
