import albumentations as A
import argparse
import albumentations.pytorch as AP
import cv2
import matplotlib.pyplot as plt
import numpy as np
from rumex_weeds.data import RumexWeedsDataset
from rumex_weeds.data import RumexWeedsBBox
from rumex_weeds.data import RumexWeedsMask
import glob
import os

colors = [(255, 215, 0),
        (255, 69, 0)]

def draw_ellipses(img, ellipses):
    for i in range(ellipses.shape[0]):
        t_i = ellipses[i, :]
        if not np.all((t_i == 0)):
            cv2.ellipse(img, (int(t_i[0]), int(t_i[1])), (int(t_i[2]), int(t_i[3])), 0, 0, 360, [*colors[int(t_i[4])], 0], 1)
            cv2.circle(img, (int(t_i[0]), int(t_i[1])), 2, colors[int(t_i[4])], 7)
    return img


def draw_bboxes(img, bboxes):
    for i in range(bboxes.shape[0]):
        t_i = bboxes[i, :]
        if not np.all((t_i == 0)):
            cv2.rectangle(img, (int(t_i[0]), int(t_i[1])), (int(t_i[0] + t_i[2]), int(t_i[1] + t_i[3])), colors[int(t_i[4])], 5)
    return img

def tensor_to_rgb(img):
    img = img.permute(1, 2, 0)
    img = img.numpy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def draw_annotations(img):
    transform = A.Compose([
        AP.ToTensorV2(),
    ], bbox_params=A.BboxParams(format='coco', label_fields=['labels']))


def main(data_folder, sequence_folder, output_folder):
    transform = A.Compose([
        AP.ToTensorV2(),
    ], bbox_params=A.BboxParams(format='coco', label_fields=['labels']))

    img_files = glob.glob(f"{sequence_folder}/imgs/*.png")
    img_files = [img_file.replace(f"{data_folder}/", "") for img_file in img_files]
    img_files = sorted(img_files)
    dataset = RumexWeedsDataset(
        data_dir=data_folder,
        image_list=img_files,
        classes_to_consider=["rumex_obtusifolius", "rumex_crispus"],
        preproc=transform,
        annotation_files=["../annotations.xml"],
    )


    seq = []
    for i in range(len(dataset)):
        img, bboxes, ellipses, masks, img_info = dataset[i]
        img = tensor_to_rgb(img)
        img = draw_bboxes(img, bboxes)
        img = draw_ellipses(img, ellipses)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # cv2.imwrite(f"{output_folder}/{i:04d}.jpg", )
        seq.append(img)

    # Writing images as video
    out = cv2.VideoWriter(f"{output_folder}/movie2.avi",cv2.VideoWriter_fourcc(*'DIVX'), 5, img.shape[:2][::-1])
 
    for img in seq:
        out.write(img)
    out.release() 

        
if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("--data_folder", type=str)
    argparse.add_argument("--seq_folder", type=str)
    argparse.add_argument("--output_folder", type=str)
    args = argparse.parse_args()
    args.data_folder = "/home/rog/data/glrmi_imgs/RumexWeeds"
    args.seq_folder = "/home/rog/data/glrmi_imgs/RumexWeeds/20210807_lundholm/seq23"
    args.output_folder = "/home/rog/sample_videos/20210807_lundholm/seq23"
    os.makedirs(args.output_folder, exist_ok=True)
    main(data_folder=args.data_folder, sequence_folder=args.seq_folder, output_folder=args.output_folder)
