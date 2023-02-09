# RumexWeeds: A Grassland Dataset for Agricultural Robotics.
## Useful Links:
* [RumexWeeds Website](https://rgring.github.io/RumexWeeds/)
* Publication: [ToDo](https://github.com/RGring/RumexWeeds)
* Dataset: [ToDo](https://github.com/RGring/RumexWeeds)

## Abstract:
Computer vision can lead towards more sustainable agricultural production by enabling robotic precision agriculture. Vision-equipped robots are being deployed in the fields to handle crops and control weeds. However, publicly available agricultural datasets containing both image data as well as data from additional navigational robot sensors are scarce. Our real-world dataset RumexWeeds targets the detection of the grassland weeds: _Rumex obtusifolius L._ and _Rumex crispus L._. RumexWeeds includes whole image sequences instead of individual static images, which is rare for computer vision image datasets yet crucial for robotic applications. It allows for more robust object detection, incorporating temporal aspects and considering different viewpoints of the same object. Furthermore, RumexWeeds includes data from additional navigational robot sensors—GNSS, IMU and odometry—which can increase robustness, when additionally fed to detection models. In total the dataset includes 5,510 images with 15,519 manual bounding box annotations collected at 3 different farms and 4 different days in summer and autumn 2021. Additionally, RumexWeeds includes a subset of 340 ground truth pixels-wise annotations. The dataset is publicly available at [ToDo](https://github.com/RGring/RumexWeeds).


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
The Pytorch Datasets allows an easy entrypoint to work with the dataset.
To visualize some example images, please run.
```
python rumex_weeds/visualize_img_data.py --data_folder <path-to-your-extracted-RumexWeeds-folder> --num_images <number-of-images-to-display> --visualize_type <bbox/gt_mask/mask/all>
```


## Citation

If you find this work useful in your research, please cite:
```
@article{RumexWeeds2021,
  title={RumexWeeds: A Grassland Dataset for Agricultural Robotics.},
  author={Güldenring, Ronja and Evert van, Frits and Nalpantidis, Lazaros},
  booktitle={TBA},
  year={2021}
}
```