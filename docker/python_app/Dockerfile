FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt upgrade -y && apt install -y curl
RUN apt install -y git make build-essential
RUN apt install -y sudo bash
RUN apt install -y libev-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl


ARG py_ver=3.7.2
ARG pyenv_version=1.2.9

ARG user=web-user
ARG home=/home/$user

ARG app_name=python_app
ARG app_dir=/$app_name

ARG pyenv_dir=$home/.pyenv
ARG pyenv_bin=$pyenv_dir/bin/pyenv
ARG py_bin=$pyenv_dir/versions/$app_name/bin/python3
ARG env_py_bin=$pyenv_dir/versions/$app_name/bin/python
ARG env_pip_bin=$pyenv_dir/versions/$app_name/bin/pip

ARG shell_fn=.shell_pyenv
ARG shell_env_fp=$home/$shell_fn

RUN useradd -m -s /bin/bash $user

RUN echo 'Europe/Kiev' > /etc/timezone
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN dpkg-reconfigure -f noninteractive tzdata

USER $user
WORKDIR $home
RUN git clone https://github.com/pyenv/pyenv.git $pyenv_dir
RUN git clone https://github.com/pyenv/pyenv-virtualenv.git $pyenv_dir/plugins/pyenv-virtualenv
WORKDIR $pyenv_dir
RUN git checkout tags/v$pyenv_version
WORKDIR $home
COPY --chown=web-user:web-user $shell_fn $home
RUN echo ". $shell_env_fp" >> $home/.bashrc

RUN $pyenv_bin install $py_ver
RUN $pyenv_bin virtualenv $py_ver $app_name

user root
RUN mkdir $app_dir
RUN chown $user:$user -R $app_dir

USER $user
WORKDIR $app_dir
COPY requirements.txt $app_dir
RUN $env_pip_bin install -U pip
RUN $env_pip_bin install -r requirements.txt

ENV VENV_NAME=$app_name
ENV PYTHON_VERSION=$py_ver

# add entrypoint script
USER root
COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
USER $user

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
