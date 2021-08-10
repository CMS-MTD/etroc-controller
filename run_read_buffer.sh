#!/bin/bash

nEvents=${1:-100}
mode=${2:-tdc}
scrambled=${3:-True}


cd etl-kcu105-ipbus/
source init.sh
python read_buffer.py --nEvents $nEvents --mode $mode --scrambled $scrambled
