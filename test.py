import PoseImage
import cv2
import math as math
import numpy as np

def absAngle(points, arr):
	try:
		return (360 + math.degrees(math.atan2(-1 * (points[arr[1]][1] - points[arr[0]][1]), points[arr[1]][0] - points[arr[0]][0]))) % 360
	except:
		print(points)
		print(arr)

def relAngle(points, arr):
	# return absAngle(points, [arr[1], arr[0]]) - absAngle(points, [arr[1], arr[2]])

	p0 = points[arr[0]]
	p1 = points[arr[1]]
	p2 = points[arr[2]]

	v0 = np.array(p0) - np.array(p1)
	v1 = np.array(p2) - np.array(p1)

	angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
	return np.degrees(angle)

def getDiffs(mod_frame, inp_frame):
	model_points, ratios_m = PoseImage.getPoints(mod_frame)
	input_points,ratios_i = PoseImage.getPoints(inp_frame)

	attr_names = ["Big Sublimb", "Small Sublimb", "Overall", "Joint"]
	rightarm = [[2, 3], [3, 4], [2, 4], [2, 3, 4]]
	leftarm = [[5, 6], [6, 7], [5, 7], [5, 6, 7]]
	rightleg = [[8, 9], [9, 10], [8, 10], [8, 9, 10]]
	leftleg = [[11, 12], [12, 13], [11, 13], [11, 12, 13]]
	funcs = [absAngle, absAngle, absAngle, relAngle]
	limbs = [rightarm, leftarm, rightleg, leftleg]
	limb_diffs = []
	limb_diff = []
	#0-1 weights
	weights = [.5, .5, .75, .25]
	for limb in limbs:
		input_angles = []
		model_angles = []
		for i in range(len(limb)):
			model_angles.append(funcs[i](model_points, limb[i]))
			input_angles.append(funcs[i](input_points, limb[i]))
		#diffs not rlly needed but kept for debugging
		diffs = []
		total_diff = 0
		for i in range(len(model_angles)):
			di = abs(model_angles[i] - input_angles[i])
			diffs.append(min([di, 360-di]))
			total_diff += diffs[i] / 360.0 * weights[i]
		total_diff /= len(diffs)
		limb_diffs.append(diffs)
		limb_diff.append(total_diff)
	return limb_diff, model_points, input_points, ratios_i, ratios_m
	"""
	if limb == leftarm:
		print('input_angles', input_angles)
		print('model_angles', model_angles)
	"""

#TEST CODE
"""
model_img = "IMG_0095.jpg"
input_img = "IMG_0102.jpg"
model_frame = cv2.resize(cv2.imread(model_img), (0, 0), fx=0.1, fy=0.1)
input_frame = cv2.resize(cv2.imread(input_img), (0, 0), fx=0.1, fy=0.1)
diffs = getDiffs(model_frame, input_frame)

print(diffs)
"""

"""
print("model", model_angles)
print("input", input_angles)
print('diffs', diffs)
print('diff', total_diff)
if total_diff < .05:
	print('basically perfect')
elif total_diff < .1:
	print('somewhat similar')
else:
	print('fucking wrong')

"""

"""
rightbicep_angle = math.degrees(math.atan2(-1 * (model_points[rightbicep[1]][1] - model_points[rightbicep[0]][1]), model_points[rightbicep[1]][0] - model_points[rightbicep[0]][0]))
rightforearm_angle = math.degrees(math.atan2(-1 * (model_points[rightforearm[1]][1] - model_points[rightforearm[0]][1]), model_points[rightforearm[1]][0] - model_points[rightforearm[0]][0]))
rightoverall_angle = math.degrees(math.atan2(-1 * (model_points[rightoverall[1]][1] - model_points[rightoverall[0]][1]), model_points[rightoverall[1]][0] - model_points[rightoverall[0]][0]))

'''rightforearm_angle
right_angle
right_ratio'''

print(model_points)
print('Right Bicep Angle:', rightbicep_angle)
print('Right Forearm Angle', rightforearm_angle)
print('Right Overall Angle', rightoverall_angle)"""