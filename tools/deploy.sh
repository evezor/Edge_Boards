set -ex

# sudo mkfs.vfat -n PYBFLASH /dev/sdc1

board_zorg=/media/carl/PYBFLASH
board_a=/media/carl/PYBFLASH1
board_b=/media/carl/PYBFLASH3
board_c=/media/carl/PYBFLASH2

cd boards

cp -u emuCode/*.py  $board_zorg
cp -u busDrivers/zorg/commission.json  $board_zorg
cp -u busDrivers/zorg/manifest.json  $board_zorg
cp -u busDrivers/zorg/mapo.json  $board_zorg

for board in $board_a $board_b $board_c; do
    cp -u emuCode/*.py edges/driver.py $board
done

cp -u edges/b3/* $board_a
cp -u edges/b3/* $board_b

cp -u edges/b2/* $board_c
