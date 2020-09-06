set -ex

# rm /media/carl/PYBFLASH*/*

cp main.py bits.py ocan.py board?.py /media/carl/PYBFLASH
cp main.py bits.py ocan.py board?.py /media/carl/PYBFLASH1
cp main.py bits.py ocan.py board?.py /media/carl/PYBFLASH2

cp boards/zorg/* /media/carl/PYBFLASH

cp boards/b2/* /media/carl/PYBFLASH1
cp boards/b3/* /media/carl/PYBFLASH2
cp boards/b3/* /media/carl/PYBFLASH3

