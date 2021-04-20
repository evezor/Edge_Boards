set -ex

# args: board name, mount point

# Edge board setup
# Step 1: MicroPython
# Step 2: boot.py, edge.py, driver.py $board_name.py (and some others)

board=$1
dst=${2:-/media/$USER/PYBFLASH}

rm -f $dst/state.json

(
cd boards

(
cd emu
cp -u main.py bundle.py ocan.py board.py edge.py $dst
)

(
cd edges
cp -u driver.py $dst
cp -u $board/* $dst

)
)

echo "import machine; machine.soft_reset()"

