# kalman-soc

Okra's lightweight embedded state of charge algorithm.

## Test build instructions

1. Git clone this repository with `--recursive` option or run `git submodule update --init --recursive` after normal clone.

2. Setup build directory

    meson setup build

3. Build with ninja

    cd build
    ninja

4. Run tests

    ./run_tests
