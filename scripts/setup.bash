cd /tmp/
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
export PATH=/root/.local/bin:$PATH
source ~/PROFILE_SCRIPT
pip --version
