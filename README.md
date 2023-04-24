# 3D-HumanPose-RepL

This is a reproducibility study for: [DLow: Diversifying Latent FLows](https://arxiv.org/pdf/2003.08386.pdf)

## Setup

1. Install conda for your OS from https://conda.io/docs/user-guide/install/

2. Create an new environment via conda

- For Linux (CUDA 11.6 and Tensorflow 2.12.x)
    ```bash
    conda env create -f env_linux_tensorflow.yaml
    ```

3. Download the dataset from http://vision.imar.ro/ or use the preprocessed versions below:

- For 3D annotations download the preprocessed version from ([data_3d_h36m.npz](https://drive.google.com/file/d/1VrPFnUWxb56SXrkucy-HIxjcc6t80uxi/view?usp=share_link)) or follow the data preprocessing steps ([DATASETS.md](https://github.com/facebookresearch/VideoPose3D/blob/master/DATASETS.md)) inside the [VideoPose3D](https://github.com/facebookresearch/VideoPose3D) repo. Place the prepocessed data ``data_3d_h36m.npz`` under the ``data`` folder.

- For 2D annotations (~350MB) and images (~26GB) use the links below

    ```bash
    wget http://visiondata.cis.upenn.edu/volumetric/h36m/h36m_annot.tar
    wget http://visiondata.cis.upenn.edu/volumetric/h36m/S1.tar
    wget http://visiondata.cis.upenn.edu/volumetric/h36m/S5.tar
    wget http://visiondata.cis.upenn.edu/volumetric/h36m/S6.tar
    wget http://visiondata.cis.upenn.edu/volumetric/h36m/S7.tar
    wget http://visiondata.cis.upenn.edu/volumetric/h36m/S8.tar
    wget http://visiondata.cis.upenn.edu/volumetric/h36m/S9.tar
    wget http://visiondata.cis.upenn.edu/volumetric/h36m/S11.tar
    ```

## Train the models

# Simple Autoencoder

```python
python src/train.py --model AE
```

# Variational Autoencoder
```python
python src/train.py --model VAE
```

## Evaluate a pre-trained model

# Reconstruction

```python
python src/eval.py --model AE --action reconstruct
```

# Sampling (Using a normal distribution by default)
```python
python src/eval.py --model AE --action sample
```

