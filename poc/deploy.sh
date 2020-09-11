set -ex

# rm /media/carl/PYBFLASH*/*

cp main.py bundle.py ocan.py board.py /media/carl/PYBFLASH
cp main.py bundle.py ocan.py board.py edge.py /media/carl/PYBFLASH1
cp main.py bundle.py ocan.py board.py edge.py /media/carl/PYBFLASH2
cp main.py bundle.py ocan.py board.py edge.py /media/carl/PYBFLASH3

cp boards/zorg/* /media/carl/PYBFLASH
cp systems/ls2oh/mapo.json systems/ls2oh/commission.json \
    /media/carl/PYBFLASH

cp boards/b2/* /media/carl/PYBFLASH1

cp boards/b3/* /media/carl/PYBFLASH2
cp boards/b3/* /media/carl/PYBFLASH3

