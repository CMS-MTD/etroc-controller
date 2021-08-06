#!/bin/bash
cd etl-kcu105-ipbus/
source init.sh
python read_DebugRAM_2links.py
cd -
