import cv2
import time
import numpy as np
import test
import requests
import json
from flask import Flask, request
from firebase import firebase
from flask_cors import CORS, cross_origin

DEBUG = True
app = Flask(__name__)
CORS(app)
app.secret_key ="123asd"

firebase = firebase.FirebaseApplication("https://choreocoach.firebaseio.com/", None)


@app.route('/api', methods=['GET', 'POST'])
def getVideoData():
    labels = ['rightarm ', 'leftarm ', 'rightleg ', 'leftleg ']

    session = firebase.get('/', None)
    skip = 7
    print(request.args)
    print(session)
    input_source = session[request.args.get('teacher')]
    model_source = session[request.args.get('student')]
    inp_cap = cv2.VideoCapture(input_source['downloadURL'])
    mod_cap = cv2.VideoCapture(model_source['downloadURL'])

    inp_hasFrame, inp_frame = inp_cap.read()
    mod_hasFrame, mod_frame = mod_cap.read()
    #print('fps', inp_cap.get(cv2.CAP_PROP_FPS))
    wrongs = []
    wrong_inp_frames = []
    wrong_mod_frames = []
    wrong_diffs = []
    allscores = []
    model_poses = []
    input_poses = []
    ratios_i = {}
    ratios_m = {}
    alldiffs = []
    t = 0
    while inp_hasFrame and mod_hasFrame:
        input_frame = cv2.resize(inp_frame, (0, 0), fx=0.5, fy=0.5)
        model_frame = cv2.resize(mod_frame, (0, 0), fx=0.5, fy=0.5)
        diff, model_points, input_points, ratio_i, ratio_m = test.getDiffs(model_frame, input_frame)
        adjdiff = []
        for i in diff:
            if i > .12:
                asdf = 3
            elif i > .06:
                asdf = 2
            else:
                asdf = 1
            adjdiff.append(asdf)
        ratios_i[t] = ratio_i
        ratios_m[t] = ratio_m
        model_poses.append(model_points)
        input_poses.append(input_points)
        if max(diff) > .12:
            wrongs.append(inp_cap.get(cv2.CAP_PROP_POS_MSEC))
            wrong_diffs.append(diff)
            wrong_inp_frames.append(input_frame)
            wrong_mod_frames.append(model_frame)
            allscores.append(3)
        elif max(diff) > .06:
            allscores.append(2)
        else:
            allscores.append(1)
        for i in range(skip):
            inp_cap.read()
            mod_cap.read()
            t+=1
        alldiffs.append(adjdiff)
        inp_hasFrame, inp_frame = inp_cap.read()
        mod_hasFrame, mod_frame = mod_cap.read()
        t+=1
        print(allscores)
    print(allscores)

    #scr = str(" ".join(str(i) for i in allscores))
    scr = alldiffs
    t,s = request.args.get('teacher'), request.args.get('student')
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
