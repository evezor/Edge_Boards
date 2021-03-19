set -ex

# sudo mkfs.vfat -n PYBFLASH /dev/sdc1

board_zorg=/media/carl/PYBFLASH
board_a=/media/carl/PYBFLASH1
board_b=/media/carl/PYBFLASH3
board_c=/media/carl/PYBFLASH2

(
cd boards

(
cd busDrivers/zorg
cp -u  manifest.json $board_zorg
)

(
cd emu
cp -u main.py bundle.py ocan.py board.py zorg.py $board_zorg
for board in $board_a $board_b $board_c; do
    cp -u main.py bundle.py ocan.py board.py edge.py $board
done
)

(
cd edges
cp -u driver.py b3/* $board_a
cp -u driver.py b3/* $board_b

cp -u driver.py b2/* $board_c
)
)
cp -u systems/mapo.json systems/ls2oh/commission.json $board_zorg

