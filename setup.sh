# install tinyFaas
git clone https://github.com/PaulsBecks/tinyFaaS --depth 1 --branch=master ~/tinyFaas
cd ~/tinyFaas
make clean
make

sleep 3

# setup python
cd ~/faascreen
pip3 install -r requirements.txt

# start programm
python3 main.py
