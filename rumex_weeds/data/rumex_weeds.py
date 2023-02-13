#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
from torch.utils.data import Dataset

from annotation_converter.AnnotationConverter import AnnotationConverter


class RumexWeedsDataset(Dataset):

    """
    RumexWeeds Dataset

    Args:
        data_dir (string): filepath to RumexWeeds folder.
        image_list (list(string)): list of img ids to consider
        preproc (callable, optional): transformation to perform on the
            input image
        classes_to_consider (list(string), optional): list of classes to consider. If "rumex" is set, all classes are considered.
    """

    def __init__(
        self,
        data_dir,
        image_list,
        preproc=None,
        classes_to_consider=["rumex"],
        annotation_files=["../annotations.xml"]
    ):
        super().__init__()
        self.data_dir = data_dir
        self.image_list = image_list
        self._classes = classes_to_consider
        self.preproc = preproc
        self.annotation_files = annotation_files
        self.annotations = self._load_annotations(self.image_list)


    def __len__(self):
        return len(self.annotations)

    def _get_img_ids(self):
        ids = []
        for img_path in self.image_list:
            ids.append(os.path.basename(img_path))
        return ids

    def _load_annotations(self, image_list):
        return [self._load_anno_from_ids(_ids) for _ids in image_list]

    def _load_anno_from_ids(self, id_):
        bboxes = np.zeros((0, 5))
        polygons = []
        img_info = {}

        for ann_file in self.annotation_files:    
            annotation_file = f"{os.path.dirname(f'{self.data_dir}/{id_}')}/{ann_file}"
            img_annotations = AnnotationConverter.read_cvat_by_id(annotation_file, os.path.basename(id_))
            img_info["img_height"] = img_annotations.get_img_height()
            img_info["img_width"] = img_annotations.get_img_width()
            img_info["file_name"] = id_
            # Getting the bounding boxes
            all_bboxes = img_annotations.get_bounding_boxes()
            for i, bb in enumerate(all_bboxes):

                if self._classes[0] == "rumex":
                    obj_id = 0
                else:
                    label = bb.get_label()
                    if label in self._classes:
                        obj_id = self._classes.index(label)
                    else:
                        continue
                x, y, w, h = bb.get_x(), bb.get_y(), bb.get_width(), bb.get_height()
                bboxes = np.append(bboxes, [[x, y, w, h, obj_id]], axis=0)

            # Getting the corresponding segmentation masks
            all_polygons = img_annotations.get_polygons()
            for pol in all_polygons:
                if self._classes[0] == "rumex":
                    obj_id = 0
                else:
                    label = pol.get_label()
                    if label in self._classes:
                        obj_id = self._classes.index(label)
                    else:
                        continue
                polygons.append(pol)
        return {"bboxes": bboxes, "polygons": polygons, "img_info": img_info}

    def load_anno(self, index):
        return self.annotations[index]

    def load_image(self, index):
        file_name = self.annotations[index]["img_info"]["file_name"]

        img_file = os.path.join(self.data_dir, file_name)

        img = cv2.imread(img_file)
        assert img is not None

        return img

    def __getitem__(self, index):
        ann = self.load_anno(index)
        bboxes = ann["bboxes"]
        img = self.load_image(index)

        # Let's generate the mask from the polygons
        mask = np.zeros((img.shape[0], img.shape[1], len(self._classes)), dtype=np.uint8)
        polygons = ann["polygons"]
        for pol in polygons:
            pol_points = pol.get_polygon_points_as_array()
            label = pol.get_label()
            label_int = self._classes.index(label)
            color = [0, 0]
            color[label_int] = 1
            cv2.fillPoly(mask, [np.array(pol_points)], tuple(color))

        if self.preproc:
            transformed = self.preproc(image=img, bboxes=bboxes[:, :4], labels=bboxes[:, 4], mask=mask)
            img = transformed["image"]
            mask = transformed["mask"]
            if len(bboxes) > 0:
                bboxes[:, :4] = transformed["bboxes"]
                bboxes[:, 4] = transformed["labels"]

        return img, bboxes, mask, ann["img_info"]

