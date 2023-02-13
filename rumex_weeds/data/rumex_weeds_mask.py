#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
from torch.utils.data import Dataset

from annotation_converter.AnnotationConverter import AnnotationConverter
from rumex_weeds.data import RumexWeedsDataset


class RumexWeedsMask(RumexWeedsDataset):

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
        super().__init__(data_dir, image_list, preproc, classes_to_consider, annotation_files)


    def _load_anno_from_ids(self, id_):
        polygons = []
        img_info = {}

        for ann_file in self.annotation_files:    
            annotation_file = f"{os.path.dirname(f'{self.data_dir}/{id_}')}/{ann_file}"
            img_annotations = AnnotationConverter.read_cvat_by_id(annotation_file, os.path.basename(id_))
            img_info["img_height"] = img_annotations.get_img_height()
            img_info["img_width"] = img_annotations.get_img_width()
            img_info["file_name"] = id_   
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
        return {"polygons": polygons, "img_info": img_info}

    def __getitem__(self, index):
        ann = self.load_anno(index)
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
            transformed = self.preproc(image=img, mask=mask)
            img = transformed["image"]
            mask = transformed["mask"]

        return img, mask, ann["img_info"]

