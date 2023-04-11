import cv2
from dsClass.align_custom import AlignCustom
from dsClass.face_feature import FaceFeature
from dsClass.mtcnn_detect import MTCNNDetect
from dsClass.tf_graph import FaceRecGraph
import datetime
import sys
import json
import numpy as np
import sqlite3


def take_attendance(course_code):
    FRGraph = FaceRecGraph();
    aligner = AlignCustom();
    extract_feature = FaceFeature(FRGraph)
    face_detect = MTCNNDetect(FRGraph, scale_factor=2);
    con = sqlite3.connect("../attendance_db.sqlite")
    cur = con.cursor()
    todays_date = datetime.date.today()
    currentDate = datetime.datetime.utcnow()

    all_student_names = dict(cur.execute("SELECT name, index_number FROM student").fetchall())

    print("[INFO] camera sensor warming up...")
    vs = cv2.VideoCapture(0);  # get input from webcam
    while True:
        _, frame = vs.read();
        # u can certainly add a roi here but for the sake of a demo i'll just leave it as simple as this
        rects, landmarks = face_detect.detect_face(frame, 80);  # min face size is set to 80x80
        aligns = []
        positions = []

        for (i, rect) in enumerate(rects):
            aligned_face, face_pos = aligner.align(160, frame, landmarks[i])
            if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                aligns.append(aligned_face)
                positions.append(face_pos)
            else:
                print("Align face failed")  # log
        if (len(aligns) > 0):
            features_arr = extract_feature.get_features(aligns)
            recog_data = findPeople(features_arr, positions);
            for (i, rect) in enumerate(rects):
                cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0),
                              2)  # draw bounding box for the face
                cv2.putText(frame, recog_data[i][0] + " - " + str(recog_data[i][1]) + "%", (rect[0], rect[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                for name, index_number in all_student_names.items():
                    if name == recog_data[i][0]:
                        present_student_res = cur.execute("SELECT name FROM attendance").fetchall()
                        present_student_names = [each for (each,) in present_student_res]
                        if name not in present_student_names:
                            cur.execute(
                                "INSERT INTO attendance (name, index_number, time, present, course_code, course_date) VALUES (?, ?, ?, TRUE, ?,?)",
                                (name, index_number, currentDate, course_code, todays_date))
                            con.commit()
                        else:
                            student_courses = cur.execute("SELECT course_code, course_date FROM attendance WHERE name = ?",
                                                          (name,)).fetchall()
                            course_tuple = (course_code,str(todays_date))
                            if course_tuple not in student_courses:
                                cur.execute(
                                    "INSERT INTO attendance (name, index_number, time, present, course_code, course_date) VALUES (?, ?, ?, TRUE, ?,?)",
                                    (name, index_number, currentDate, course_code, todays_date))
                                con.commit()


        cv2.imshow("Capturing Face", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
            break
    vs.release()  # camera release
    cv2.destroyAllWindows()


'''
facerec_128D.txt Data Structure:
{
"Person ID": {
    "Center": [[128D vector]],
    "Left": [[128D vector]],
    "Right": [[128D Vector]]
    }
}
This function basically does a simple linear search for 
^the 128D vector with the min distance to the 128D vector of the face on screen
'''


def findPeople(features_arr, positions, thres=0.6, percent_thres=70):
    '''
    :param features_arr: a list of 128d Features of all faces on screen
    :param positions: a list of face position types of all faces on screen
    :param thres: distance threshold
    :return: person name and percentage
    '''
    f = open('../dsClass/facerec_128D.txt', 'r')
    data_set = json.loads(f.read());
    returnRes = [];
    for (i, features_128D) in enumerate(features_arr):
        result = "Unknown";
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person][positions[i]];
            for data in person_data:
                distance = np.sqrt(np.sum(np.square(data - features_128D)))
                if (distance < smallest):
                    smallest = distance;
                    result = person;
        percentage = min(100, 100 * thres / smallest)
        if percentage <= percent_thres:
            result = "Unknown"
        returnRes.append((result, percentage))
    return returnRes


take_attendance("CSIT123")
