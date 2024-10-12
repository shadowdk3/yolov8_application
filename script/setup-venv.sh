#!/bin/bash

current_dir=$(pwd)
last_folder=$(basename "$current_dir")

if [ "$last_folder" == "script" ]; then
    cd ..
fi

echo "Create python3 venv"
python3 -m venv venv

echo "Activate the virtual environment"
source venv/bin/activate

sudo apt-get update
sudo apt-get install -y libopenblas-base libopenmpi-dev
sudo apt install -y libjpeg-dev zlib1g-dev
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran

echo "Install YOLO"
pip install -U pip
pip install ultralytics

echo "Install pytorch"
wget https://developer.download.nvidia.com/compute/redist/jp/v511/pytorch/torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl -O torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl
pip install torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl

echo "Install torchvision"
git clone --brach=v0.15.1 https://github.com/pytorch/vision torchvision
cd torchvision
python setup.py install --prefix=../venv/
cd ..

echo "Install onnxruntime-gpu"
wget https://nvidia.box.com/shared/static/zostg6agm00fb6t5uisw51qi6kpcuwzd.whl -O onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl
pip install onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl

echo "Install Tensorboard"
pip install -U testresources setuptools==65.5.0
pip install -U future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig packaging h5py==3.7.0
pip install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v512 tensorflow==2.12.0+nv23.06

rm torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl
rm -rf torchvision
rm onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl
