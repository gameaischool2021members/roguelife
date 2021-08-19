#!/bin/bash
for i in {1..5}
do
    python run_log_bhp.py --run R01 Plots/bhp/R01_$i
    python run_log_bhp.py --run R02 Plots/bhp/R02_$i
    python run_log_bhp.py --run R03 Plots/bhp/R03_$i
    python run_log_bhp.py --run R04 Plots/bhp/R04_$i
done