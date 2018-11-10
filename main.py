import cv2
from flask import Flask, request
from flask_cors import CORS

from firebase import firebase
from algorithms.angles import get_diffs, diff_to_error

DEBUG = True
app = Flask(__name__)
CORS(app)
app.secret_key = "123asd"

firebase = firebase.FirebaseApplication("https://choreocoach.firebaseio.com/", None)


@app.route('/api', methods=['GET', 'POST'])
def analyze_video():
    session = firebase.get('/', None)
    skip = 7
    inp_cap = cv2.VideoCapture(session[request.args.get('teacher')]['downloadURL'])
    mod_cap = cv2.VideoCapture(session[request.args.get('student')]['downloadURL'])
    inp_has_frame, inp_frame = inp_cap.read()
    mod_has_frame, mod_frame = mod_cap.read()
    all_scores = []
    poses_i, poses_m, ratios_i, ratios_m = {}, {}, {}, {}
    all_diffs = []
    t = 0
    while inp_has_frame and mod_has_frame:
        input_frame = inp_frame
        model_frame = mod_frame
        diff, model_points, input_points, ratio_i, ratio_m = get_diffs(model_frame, input_frame)
        ratios_i[t] = ratio_i
        ratios_m[t] = ratio_m
        poses_i[t] = input_points
        poses_m[t] = model_points
        all_scores.append(diff_to_error(max(diff)))
        for i in range(skip):
            inp_cap.read()
            mod_cap.read()
            t += 1
        all_diffs.append([diff_to_error(d) for d in diff])
        inp_has_frame, inp_frame = inp_cap.read()
        mod_has_frame, mod_frame = mod_cap.read()
        t += 1
    scr = all_diffs
    t, s = request.args.get('teacher'), request.args.get('student')
    ts = session[t]
    ts[s] = scr
    ts['poses'] = ratios_m
    firebase.put('/', t, ts)
    std = session[s]
    std['poses'] = ratios_i
    firebase.put('/', s, std)
    return "Updated Firebase"


if __name__ == '__main__':
    app.run()
