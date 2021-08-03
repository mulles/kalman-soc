#This Script builds kalman-soc Algo
#Resource:https://mesonbuild.com/Tutorial.html#the-humble-beginning

# Install Meson (Build Systems) and it's Dependencies 
sudo apt install meson ninja-build build-essential clang-format

# Clone Git Repo to build including subprojects cpputests located folder /dep/
git clone --recursive git@github.com:okrasolar/kalman-soc.git

cd kalman-soc/dep/cpputest/

# Get missing meson.build file for cpputest subproject
wget https://raw.githubusercontent.com/hofab/meson-cpputest/master/subprojects/cpputest/meson.build
cd ..
cd ..

# Adjust main meson.build to work with the above cpputest meson.build file
sed -i ''s/'cpputest_dep'/'lcpp_dep'/g''  meson.build

meson setup builddir
cd builddir
ninja


