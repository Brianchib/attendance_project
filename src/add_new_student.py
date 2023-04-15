import json
import sqlite3

import cv2
import numpy as np

from dsClass.align_custom import AlignCustom
from dsClass.face_feature import FaceFeature
from dsClass.mtcnn_detect import MTCNNDetect
from dsClass.tf_graph import FaceRecGraph


def add_new_student(student_name, student_index_number):
    con = sqlite3.connect("../attendance_db.sqlite")
    cur = con.cursor()
    FRGraph = FaceRecGraph()
    aligner = AlignCustom()
    extract_feature = FaceFeature(FRGraph)
    face_detect = MTCNNDetect(FRGraph, scale_factor=2)
    vs = cv2.VideoCapture(0)
    # get input from webcam

    f = open("../dsClass/facerec_128D.txt", "r")
    data_set = json.loads(f.read())
    person_imgs = {"Left": [], "Right": [], "Center": []}
    person_features = {"Left": [], "Right": [], "Center": []}
    print(
        "Please start turning slowly. Press 'q' to save and add this new user to the dataset"
    )
    while True:
        _, frame = vs.read()
        rects, landmarks = face_detect.detect_face(frame, 80)
        # min face size is set to 80x80
        for i, rect in enumerate(rects):
            aligned_frame, pos = aligner.align(160, frame, landmarks[i])
            if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                person_imgs[pos].append(aligned_frame)
                cv2.imshow("Pres 'q' to save and close window", aligned_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 30 or key == ord("q"):
            break

    # changes to be done here. write to db instead of excell file.

    cur.execute(
        "INSERT INTO student(name, index_number) VALUES(?, ?)",
        (student_name, student_index_number),
    )
    con.commit()
    for (
        pos
    ) in (
        person_imgs
    ):  # there r some exceptions here, but I'll just leave it as this to keep it simple
        person_features[pos] = [
            np.mean(extract_feature.get_features(person_imgs[pos]), axis=0).tolist()
        ]
    data_set[student_name] = person_features
    f = open("../dsClass/facerec_128D.txt", "w")
    f.write(json.dumps(data_set))
    return True


# add_new_student("Andea", 123443)
