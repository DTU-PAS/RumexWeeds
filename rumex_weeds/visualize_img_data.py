import albumentations as A
import argparse
import albumentations.pytorch as AP
import cv2
import matplotlib.pyplot as plt
import numpy as np
from rumex_weeds.data import RumexWeedsDataset
from rumex_weeds.data import RumexWeedsBBox
from rumex_weeds.data import RumexWeedsMask

colors = [(255, 215, 0),
        (255, 69, 0)]

def draw_bboxes(img, bboxes):
    for i in range(bboxes.shape[0]):
            t_i = bboxes[i, :]
            if not np.all((t_i == 0)):
                cv2.rectangle(img, (int(t_i[0]), int(t_i[1])), (int(t_i[0] + t_i[2]), int(t_i[1] + t_i[3])), colors[int(t_i[4])], 2)
    return img

def tensor_to_rgb(img):
    img = img.permute(1, 2, 0)
    img = img.numpy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def visualize_boxes(data_folder, img_list, num_images):
    transform = A.Compose([
        AP.ToTensorV2(),
    ], bbox_params=A.BboxParams(format='coco', label_fields=['labels']))

    dataset = RumexWeedsBBox(
        data_dir=data_folder,
        image_list=img_list,
        classes_to_consider=["rumex_obtusifolius", "rumex_crispus"],
        preproc=transform,
    )

    for i in range(num_images):
        i = np.random.randint(0, len(dataset))
        try:
            img, bboxes, img_info = dataset[i]
        except:
            continue
        img = tensor_to_rgb(img)
        img = draw_bboxes(img, bboxes)

        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        ax.imshow(img)
        plt.show()

def visualize_masks(data_folder, img_list, num_images, gt_masks=True):
    transform = A.Compose([
        AP.ToTensorV2(),
    ])

    annotation_files = ["../annotations.xml"]
    if not gt_masks:
        annotation_files.append("../annotations_seg.xml")

    dataset = RumexWeedsMask(
        data_dir=data_folder,
        image_list=img_list,
        classes_to_consider=["rumex_obtusifolius", "rumex_crispus"],
        preproc=transform,
        annotation_files=annotation_files,
    )

    count = 0
    while count < num_images:
        i = np.random.randint(0, len(dataset))

        # ToDo: Remove if resolved.
        try:
            img, masks, img_info = dataset[i]
        except Exception as e:
            print(e)
            continue
        if sum(sum(sum(masks))) == 0:
            continue
        img = tensor_to_rgb(img)

        mask_img = np.zeros_like(img)
        mask_img[masks[:, :, 0] == 1] = colors[0]
        mask_img[masks[:, :, 1] == 1] = colors[1]
        overlay = cv2.addWeighted(img, 0.5, mask_img, 0.5, 0)

        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        ax.imshow(overlay)
        plt.show()
        count += 1

def visualize_all(data_folder, img_list, num_images, gt_masks=True):
    transform = A.Compose([
        AP.ToTensorV2(),
    ], bbox_params=A.BboxParams(format='coco', label_fields=['labels']))

    annotation_files = ["../annotations.xml"]
    if not gt_masks:
        annotation_files.append("../annotations_seg.xml")

    dataset = RumexWeedsDataset(
        data_dir=data_folder,
        image_list=img_list,
        classes_to_consider=["rumex_obtusifolius", "rumex_crispus"],
        preproc=transform,
        annotation_files=annotation_files,
    )

    count = 0
    while count < num_images:
        i = np.random.randint(0, len(dataset))
        try:
            img, bboxes, masks, img_info = dataset[i]
        except Exception as e:
            print(e)
            continue

        img = tensor_to_rgb(img)
        img = draw_bboxes(img, bboxes)

        mask_img = np.zeros_like(img)
        mask_img[masks[:, :, 0] == 1] = colors[0]
        mask_img[masks[:, :, 1] == 1] = colors[1]
        overlay = cv2.addWeighted(img, 0.5, mask_img, 0.5, 0)

        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        ax.imshow(overlay)
        plt.show()
        count += 1


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("--data_folder", type=str)
    argparse.add_argument("--num_images", type=int, default=1)
    argparse.add_argument("--visualize_type", type=str, default="all")
    args = argparse.parse_args()

    # Load the training data
    splits = ["random_train.txt"]
    img_list = []
    for s in splits:
        with open(f"{args.data_folder}/dataset_splits/{s}", "r+") as f:
            img_list = [line.replace('\n', '') for line in f.readlines()]
    
    if args.visualize_type == "bbox":
        visualize_boxes(args.data_folder, img_list, args.num_images)
    elif args.visualize_type == "gt_mask":
        visualize_masks(args.data_folder, img_list, args.num_images, gt_masks=True)
    elif args.visualize_type == "mask":
        visualize_masks(args.data_folder, img_list, args.num_images, gt_masks=False)
    elif args.visualize_type == "all":
        visualize_all(args.data_folder, img_list, args.num_images, gt_masks=False)




# ToDo:
# Make sure bboxes do not exceed image boundaries