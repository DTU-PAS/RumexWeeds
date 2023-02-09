#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
from torch.utils.data import Dataset

from annotation_converter.AnnotationConverter import AnnotationConverter
from rumex_weeds.data import RumexWeedsDataset


class RumexWeedsBBox(RumexWeedsDataset):

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

        bboxes = np.zeros((0, 5))
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
        img_info = {}
        img_info["img_height"] = img_annotations.get_img_height()
        img_info["img_width"] = img_annotations.get_img_width()
        img_info["file_name"] = id_
        return {"bboxes": bboxes, "img_info": img_info}
    
    def __getitem__(self, index):
        ann = self.load_anno(index)
        bboxes = ann["bboxes"]
        img = self.load_image(index)

        if self.preproc:
            transformed = self.preproc(image=img, bboxes=bboxes[:, :4], labels=bboxes[:, 4])
            img = transformed["image"]
            if len(bboxes) > 0:
                bboxes[:, :4] = transformed["bboxes"]
                bboxes[:, 4] = transformed["labels"]

        return img, bboxes, ann["img_info"]

