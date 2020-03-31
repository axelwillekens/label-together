import os
import cv2
import json

inputdir = 'input'
outputdir = 'output'
# Create output Directory if don't exist
if not os.path.exists(outputdir):
    os.mkdir(outputdir)

input_names_json = [x for x in os.listdir(inputdir) if x[-5:] == ".json"]

labels = {}

for filename in input_names_json:
    with open("%s/%s" % (inputdir, filename), 'r') as f:
        datastore = json.load(f)

    img = cv2.imread(inputdir + '/' + datastore["imagePath"])
    for shape in datastore["shapes"]:
        outputpathname = "%s/%s" % (outputdir, shape["label"])
        if shape["label"] not in labels.keys():
            labels[shape["label"]] = 0
            # create other foldername if foldername already exists
            while os.path.exists(outputpathname):
                outputpathname += "_new"
            os.mkdir(outputpathname)
        else:
            labels[shape["label"]] += 1

        p1 = shape["points"][0]
        p2 = shape["points"][1]

        crop_img = img[int(p1[1]):int(p2[1]), int(p1[0]):int(p2[0])]
        extention = datastore["imagePath"][datastore["imagePath"].rfind('.'):]
        cv2.imwrite("%s/%s_%s_%d%s" % (outputpathname, "cropped", shape["label"], labels[shape["label"]], extention),
                    crop_img)









