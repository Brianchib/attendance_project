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
    face_rec_graph = FaceRecGraph()
    aligner = AlignCustom()
    extracted_face_feature = FaceFeature(face_rec_graph)
    face_detect = MTCNNDetect(face_rec_graph, scale_factor=2)
    video_from_camera = cv2.VideoCapture(0)
    face_rec_file = open("../dsClass/facerec_128D.txt", "r")
    data_from_face_rec_file = json.loads(face_rec_file.read())
    student_images = {"Left": [], "Right": [], "Center": []}
    student_face_features = {"Left": [], "Right": [], "Center": []}
    # Extract face features from the video feed.
    while True:
        _, frame = video_from_camera.read()
        rects, landmarks = face_detect.detect_face(frame, 80)
        for i, rect in enumerate(rects):
            aligned_frame, pos = aligner.align(160, frame, landmarks[i])
            if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                student_images[pos].append(aligned_frame)
                cv2.imshow("Recording Face, Pres 'q' to save and close window", aligned_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 30 or key == ord("q"):
            break
    # Save the name of the student to the student table in database.
    cur.execute("INSERT INTO student(name, index_number) VALUES(?, ?)",(student_name, student_index_number),)
    con.commit()
    # Append the new face feature to a text files' content.
    for pos in student_images:
        student_face_features[pos] = [np.mean(extracted_face_feature.get_features(student_images[pos]), axis=0).tolist()]
    data_from_face_rec_file[student_name] = student_face_features
    face_rec_file = open("../dsClass/facerec_128D.txt", "w")
    face_rec_file.write(json.dumps(data_from_face_rec_file))
    return True
