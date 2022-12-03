cd ~/sd-service/stable-diffusion-bentoml/fp32
export PATH="$HOME/.pyenv/bin:$PATH"
export BENTOML_CONFIG="configuration.yaml"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
pyenv local sdsd
bentoml serve service:svc --production