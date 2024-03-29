# RumexWeeds: A Grassland Dataset for Agricultural Robotics.
## Useful Links:
* [RumexWeeds Website](https://dtu-pas.github.io/RumexWeeds/)
* [Publication](https://onlinelibrary.wiley.com/doi/10.1002/rob.22196)
* [Dataset](https://data.dtu.dk/articles/dataset/Data_for_RumexWeeds_A_Grassland_Dataset_for_Agricultural_Robotics_/17040518)

## Abstract:
Computer vision can lead towards more sustainable agricultural production by enabling robotic precision agriculture. Vision-equipped robots are being deployed in the fields to handle crops and control weeds. However, publicly available agricultural datasets containing both image data as well as data from additional navigational robot sensors are scarce. Our real-world dataset RumexWeeds targets the detection of the grassland weeds: _Rumex obtusifolius L._ and _Rumex crispus L._. RumexWeeds includes whole image sequences instead of individual static images, which is rare for computer vision image datasets yet crucial for robotic applications. It allows for more robust object detection, incorporating temporal aspects and considering different viewpoints of the same object. Furthermore, RumexWeeds includes data from additional navigational robot sensors—GNSS, IMU and odometry—which can increase robustness, when additionally fed to detection models. In total the dataset includes 5,510 images with 15,519 manual bounding box annotations collected at 3 different farms and 4 different days in summer and autumn 2021. Additionally, RumexWeeds includes a subset of 340 ground truth pixels-wise annotations. The dataset is publicly available [here](https://data.dtu.dk/articles/dataset/Data_for_RumexWeeds_A_Grassland_Dataset_for_Agricultural_Robotics_/17040518).


## Example Images
<p float="left">
  <img src="imgs/ds_sample1.png" width="500" />
</p>
<p float="left">
  <img src="imgs/ds_sample2.png" width="500" /> 
</p>
<p float="left">
  <img src="imgs/ds_sample3.png" width="500" /> 
</p>

Sample Sequences can be found here: 
* [20210806_hegnstrup - Sequence 17](https://www.youtube.com/embed/3WoM9ILuoJ8)
* [20210806_stengard - Sequence 8](https://www.youtube.com/embed/X7Oi9enc7xc)
* [20210807_lundholm - Sequence 23](https://www.youtube.com/embed/7OSrtETfVYw)

## Getting started: Pytorch Dataset Class
Download data
```
wget https://data.dtu.dk/ndownloader/files/39268307
```
Install dependencies
```
pip install -r requirements.txt
```
The Pytorch Datasets allows an easy entrypoint to work with the dataset.
To visualize some example images, please run.
```
python rumex_weeds/visualize_img_data.py --data_folder <path-to-your-extracted-RumexWeeds-folder> --num_images <number-of-images-to-display> --visualize_type <bbox/gt_mask/mask/all>
```


## Citation

If you find this work useful in your research, please cite:
```
@article{https://doi.org/10.1002/rob.22196,
author = {Güldenring, Ronja and van Evert, Frits K. and Nalpantidis, Lazaros},
title = {RumexWeeds: A grassland dataset for agricultural robotics},
journal = {Journal of Field Robotics},
keywords = {agricultural robotics, grassland weed, object detection, precision farming, robotics dataset, Rumex crispus, Rumex obtusifolius},
doi = {https://doi.org/10.1002/rob.22196},
url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/rob.22196},
eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1002/rob.22196}
}
```