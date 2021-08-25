# kalman-soc

Fork of Okra's lightweight embedded state of charge algorithm based on extend kalman filter (EKF). 

## Usage (Linux) 

1. Install dependencies  
 
   `sudo apt install meson ninja-build build-essential clang-format cmake`
3. Git clone this repository with `--recursive` option:  

   `git clone --recursive git@github.com:mulles/kalman-soc.git`  
   
   or run `git submodule update --init --recursive` after normal clone.

2. Setup build directory  
    `cd kalman-soc`   
    `meson setup build`  

3. Build with ninja

    `cd build`  
    `ninja`  

4. Run unit tests

    `./run_tests`
    
5. Run backtest on dataset of current and voltage measurements you recored in the past

   `./backtest`  
   
   The dataset should be located in /data and consist of `raw_sensor_data.csv` and `node_data.csv` as input data and outputs calculated SOC to `processed_sensor_data.csv`
   
