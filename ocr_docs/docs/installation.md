# Installation

## A) Server requirements for GPU version (Recommended):

### Hardware:
1. CPU cores(4 plus)
2. RAM (8 GB plus)
3. SSD storage: 100 GB
4. GPU card(atleast 4GB memory)

### Software:
1. Ubuntu 18 / Ubuntu 20
2. CUDA 10.2 / CUDA 11.6 with cuda compiler 
3. Python3

### Sample result after running `nvidia-smi` command:

![nvidia-smi command](assets/installation/sample-nvidia-command-result.png)


### Sample result after running `nvcc --version` command:

![nvidia-smi command](assets/installation/sample-cuda-compiler-version-command-result.png.png)


## Installation:

### 1. Docker:

Command to build:

```sudo docker build . -t ocr_english_optimized:latest```

Run : 

```sudo docker run -p 5000:5000 --gpus all --init -it  ocr_english_optimized```


### 2. Docker compose:

You can use it for **development purpose** also, as per written config code, models volume will be mounted and no need to rebuild docker compose after changing code. You can modify code and execute modified python file.

Command to build:

```sudo docker compose build .```

Run : 

```sudo docker compose run -p 5000:5000 ocr_docker_compose  bash```


## B) CPU only Inference (GPU will be much faster than this):

Considering development system scenario, as always GPU not available, so to test and modify solution in CPU only system you can build CPU version of docker.

Command to build:

```sudo docker build -f "Dockerfile-CPU" . -t ocr_english_optimized_cpu:latest```

Run : 

```sudo docker run -p 5000:5000 --init -it  ocr_english_optimized_cpu```

