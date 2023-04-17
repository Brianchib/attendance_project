import datetime
import json
import sqlite3
import sys
import cv2
import numpy as np
from dsClass.align_custom import AlignCustom
from dsClass.face_feature import FaceFeature
from dsClass.mtcnn_detect import MTCNNDetect
from dsClass.tf_graph import FaceRecGraph


def take_attendance(course_code):
    face_rec_graph = FaceRecGraph()
    aligner = AlignCustom()
    extracted_face_feature = FaceFeature(face_rec_graph)
    face_detect = MTCNNDetect(face_rec_graph, scale_factor=2)
    con = sqlite3.connect("../attendance_db.sqlite")
    cur = con.cursor()
    todays_date = datetime.date.today()
    currentDate = datetime.datetime.utcnow()
    all_student_names = dict(cur.execute("SELECT name, index_number FROM student").fetchall())
    video_from_camera = cv2.VideoCapture(0)
    while True:
        _, frame = video_from_camera.read()
        rects, landmarks = face_detect.detect_face(frame, 80)
        aligns = []
        positions = []
        for i, rect in enumerate(rects):
            aligned_face, face_pos = aligner.align(160, frame, landmarks[i])
            if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                aligns.append(aligned_face)
                positions.append(face_pos)
        if len(aligns) > 0:
            features_arr = extracted_face_feature.get_features(aligns)
            recog_data = recognize_face(features_arr, positions)
            for i, rect in enumerate(rects):
                cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2, )
                cv2.putText(frame, recog_data[i][0] + " - " + str(recog_data[i][1]) + "%", (rect[0], rect[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA,)
                for name, index_number in all_student_names.items():
                    if name == recog_data[i][0]:
                        present_student_res = cur.execute("SELECT name FROM attendance").fetchall()
                        present_student_names = [each for (each,) in present_student_res]
                        if name not in present_student_names:
                            cur.execute("INSERT INTO attendance (name, index_number, time, present, course_code, course_date) VALUES (?, ?, ?, TRUE, ?,?)", (name,index_number,currentDate,course_code, todays_date,),)
                            con.commit()
                        else:
                            student_courses = cur.execute("SELECT course_code, course_date FROM attendance WHERE name = ?",(name,),).fetchall()
                            course_tuple = (course_code, str(todays_date))
                            if course_tuple not in student_courses:
                                cur.execute("INSERT INTO attendance (name, index_number, time, present, course_code, course_date) VALUES (?, ?, ?, TRUE, ?,?)",(name,index_number,currentDate,course_code,todays_date,),)
                                con.commit()

        cv2.imshow("Taking Attendance, Pres 'q' to save and close window", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
            break
    video_from_camera.release()
    cv2.destroyAllWindows()


# RecognizeFace function performs a linear search for 128D vector on the screen to that of the file
def recognize_face(face_feature_from_screen, positions, threshold=0.6, percent_threshold=70):
    face_rec_file = open("../dsClass/facerec_128D.txt", "r")
    data_from_face_rec_file = json.loads(face_rec_file.read())
    student_name_percentage = []
    for i, face_feature in enumerate(face_feature_from_screen):
        student_result = "Unregistered Student"
        smallest = sys.maxsize
        for student in data_from_face_rec_file.keys():
            student_data = data_from_face_rec_file[student][positions[i]]
            for data in student_data:
                distance = np.sqrt(np.sum(np.square(data - face_feature)))
                if distance < smallest:
                    smallest = distance
                    student_result = student
        percentage = min(100, 100 * threshold / smallest)
        if percentage <= percent_threshold:
            student_result = "Unregistered Student"
        student_name_percentage.append((student_result, percentage))
    return student_name_percentage

