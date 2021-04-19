set -ex

dst=${1:-/media/$USER/PYBFLASH}

(
cd boards

(
cd busDrivers/zorg
cp -u  manifest.json commission.json $dst
)

(
cd emu
cp -u main.py bundle.py ocan.py board.py zorg.py $dst
)

)

cp systems/mapo.json $dst
