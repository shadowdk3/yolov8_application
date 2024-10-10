# YOLOv8 Jetson

- JetPack 5.1.2
- YOLOv8
- Pytorch
- Tensorflow

## Project 

- Brain Tumor Detection

## Run Script

```
cd /path/to/project
chmod +x srcipt/setup-venv.sh
./srcipt/setup-venv.sh
```

## Install YOLOv8

1. Source `venv`

```
source venv/bin/activate
```

2. Install ultralytics

`pip install ultralytics=8.2.103`

3. Install PyTorch

```
pip uninstall torch torchvision
sudo apt-get install -y libopenblas-base libopenmpi-dev
wget https://developer.download.nvidia.com/compute/redist/jp/v511/pytorch/torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl -O torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl
pip install torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl
```

4. Install Torchvision

```
sudo apt install -y libjpeg-dev zlib1g-dev
git clone https://github.com/pytorch/vision torchvision
cd torchvision
git checkout v0.15.1
python3 setup.py install --prefix=venv/
```

5. Install `onnxruntime-gpu`

```
wget https://nvidia.box.com/shared/static/zostg6agm00fb6t5uisw51qi6kpcuwzd.whl -O onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl
pip install onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl
```

##  Tensorboard

### Install

1. Install system packages required by TensorFlow

```
sudo apt-get update
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
```

2. Install the Python package dependencies

```
pip3 install -U testresources setuptools==65.5.0
pip3 install -U future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig packaging h5py==3.7.0
```

3. Install TensorFlow

```
pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v512 tensorflow==2.12.0+nv23.06
```

### Run Tensorboard

```
tensorboard --logdir path/to/runs --host=0.0.0.0
```

view at http://0.0.0.0:6006/

## DeepStream Configuration for YOLOv8

1. Install dependencies

```
sudo apt install libssl-dev libgstreamer1.0-0  gstreamer1.0-tools  gstreamer1.0-plugins-good  gstreamer1.0-plugins-bad  gstreamer1.0-plugins-ugly  gstreamer1.0-libav  libgstreamer-plugins-base1.0-dev  libgstrtspserver-1.0-0  libjansson4  libyaml-cpp-dev
pip install cmake
pip install onnxsim
```

2. Clone the following repository

```
git clone https://github.com/marcoslucianops/DeepStream-Yolo
cd DeepStream-Yolo
```

Download Ultralytics YOLOv8 detection model (.pt) of your choice from YOLOv8 releases. Here we use yolov8s.pt.

3. Convert model to ONNX

```
python3 utils/export_yoloV8.py -w yolov8s.pt
```

4. Set the CUDA version according to the JetPack version installed and compile

```
export CUDA_VER=11.4
make -C nvdsinfer_custom_impl_Yolo clean && make -C nvdsinfer_custom_impl_Yolo
```

5. Edit the `config_infer_primary_yoloV8.txt` file according to your model (for YOLOv8s with 80 classes)

```
[property]
...
onnx-file=yolov8s.onnx
...
num-detected-classes=80
...
```

6. Edit the `deepstream_app_config` file

```
...
[primary-gie]
...
config-file=config_infer_primary_yoloV8.txt
```

7. You can also change the video source in `deepstream_app_config` file. Here a default video file is loaded

```
...
[source0]
...
uri=file:///opt/nvidia/deepstream/deepstream/samples/streams/sample_1080p_h264.mp4
```

8. Run Inference

```
deepstream-app -c deepstream_app_config.txt
```

