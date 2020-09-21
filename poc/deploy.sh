set -ex

board_zorg=/media/carl/PYBFLASH
board_a=/media/carl/PYBFLASH1
board_b=/media/carl/PYBFLASH3
board_c=/media/carl/PYBFLASH2

cp -u main.py bundle.py ocan.py board.py $board_zorg
for board in $board_a $board_b $board_c; do
    cp -u main.py bundle.py ocan.py board.py edge.py driver.py $board
done

cp -u boards/zorg/* $board_zorg
cp -u systems/mapo.json systems/ls2oh/commission.json $board_zorg

cp -u boards/b3/* $board_a
cp -u boards/b3/* $board_b

cp -u boards/b2/* $board_c
