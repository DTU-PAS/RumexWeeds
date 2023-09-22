#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os

from annotation_converter.AnnotationConverter import AnnotationConverter
from rumex_weeds.data import RumexWeedsDataset


class RumexWeedsEllipse(RumexWeedsDataset):

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
    ):
        super().__init__(data_dir, image_list, preproc, classes_to_consider)

    def _load_anno_from_ids(self, id_):
        annotation_file = f"{os.path.dirname(f'{self.data_dir}/{id_}')}/../annotations.xml"
        img_annotations = AnnotationConverter.read_cvat_by_id(annotation_file, os.path.basename(id_))
        img_info = {}
        img_info["img_height"] = img_annotations.get_img_height()
        img_info["img_width"] = img_annotations.get_img_width()
        img_info["file_name"] = id_

        ellipses = np.zeros((0, 5))
        all_ellipses = img_annotations.get_ellipses()
        for i, ell in enumerate(all_ellipses):
            if self._classes[0] == "rumex":
                obj_id = 0
            else:
                label = ell.get_label()
                if label in self._classes:
                    obj_id = self._classes.index(label)
                else:
                    continue
            x, y, w, h = ell.get_x(), ell.get_y(), ell.get_width(), ell.get_height()
            if x < 0 or y < 0 or x > img_info["img_width"] or y > img_info["img_height"]:
                continue
            w = min(w, img_info["img_width"] - x)
            w = min(w, x)
            h = min(h, img_info["img_height"] - y)
            h = min(h, y)

            ellipses = np.append(ellipses, [[x, y, w, h, obj_id]], axis=0)

        return {"ellipses": ellipses, "img_info": img_info}
    
    def __getitem__(self, index):
        ann = self.load_anno(index)
        ellipses = ann["ellipses"]
        img = self.load_image(index)

        if self.preproc:
            transformed = self.preproc(image=img, bboxes=ellipses[:, :4], labels=ellipses[:, 4])
            img = transformed["image"]
            if len(ellipses) > 0:
                ellipses[:, :4] = transformed["bboxes"]
                ellipses[:, 4] = transformed["labels"]

        return img, ellipses, ann["img_info"]

