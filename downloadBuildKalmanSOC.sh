#This Script clones and builds kalman-soc Algo
#Resource:https://mesonbuild.com/Tutorial.html#the-humble-beginning

# Install Meson (Build Systems) and it's Dependencies 
sudo apt install meson ninja-build build-essential clang-format cmake

# Clone Git Repo to build including subprojects cpputests located in folder /dep/
git clone --recursive git@github.com:mulles/kalman-soc.git
cd kalman-soc
meson setup build
cd build
ninja

