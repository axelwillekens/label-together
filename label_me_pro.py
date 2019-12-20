import os
import cv2
import numpy as np
import argparse


def add_point_to_line(event, x, y, flags, param):
    # if the left mouse button is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Add point to line and draw the line
        line.append((x, y))
        n = len(line)
        if n > 1:
            cv2.line(im, line[n-2], line[n-1], (0, 0, 255), line_width)
            cv2.imshow("Label me", im)


def redraw_lines(img):
    # Used for changing the width of the lines
    copy = img.copy()
    # Loop over lines to redraw them on a clean image
    for l in lines:
        line_length = len(l)
        if l:
            for point in range(line_length-1):
                cv2.line(copy, l[point], l[point+1], (0, 0, 255), line_width)
    cv2.imshow("Label me", copy)
    return copy


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--image_directory", help="Directory containing the images")
parser.add_argument("-r", "--output_directory", help="Directory where the labels will be written to")

print('Welcome to label me!\n')
print('Click on te crop rows to draw lines')
print('To start a new line press "n"')
print('Made a mistake? No problem! Press "u" to undo')
print('To save the image and the label press "s"')
print('You can use "x" to skip an image, so no label will be saved')
print('Finally press "q" to quit\n\n')

if __name__ == '__main__':
    # read arguments from the command line
    args = parser.parse_args()
    img_dir = args.image_directory
    res_dir = args.output_directory
    # Make res Directories
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    if not os.path.exists(res_dir + '/JPEGImages'):
        os.makedirs(res_dir + '/JPEGImages')
    if not os.path.exists(res_dir + '/SegmentationClass'):
        os.makedirs(res_dir + '/SegmentationClass')
    if not os.path.exists(res_dir + '/Overlay'):
        os.makedirs(res_dir + '/Overlay')
    i = 0
    line_width = 1
    cv2.namedWindow("Label me")
    cv2.setMouseCallback("Label me", add_point_to_line)
    stop = False
    for filename in os.listdir(img_dir):
        if stop:
            break
        lines = []
        line = []
        lines.append(line)
        source_im = cv2.imread(img_dir + '/' + filename)
        im = source_im.copy()
        cv2.imshow('Label me', im)
        while True:
            key = cv2.waitKey()
            if key == ord('s'):
                # press s to save the label
                print('Saving label')
                cv2.imwrite(res_dir + '/JPEGImages/' + '{0:04}'.format(i) + '.jpeg', source_im)
                labels = np.zeros(source_im.shape)
                labels = redraw_lines(labels)
                cv2.imwrite(res_dir + '/SegmentationClass/' + '{0:04}'.format(i) + '.png', labels)
                cv2.imwrite(res_dir + '/Overlay/' + '{0:04}'.format(i) + '.png', im)
                i += 1
                break
            if key == ord('q'):
                # Press g to stop labeling
                stop = True
                break
            if key == ord('n'):
                # press n to start drawing a new line
                line = []
                lines.append(line)
            if key == ord('u'):
                # Use u to undo
                if len(line) > 0:
                    line.pop()
                im = redraw_lines(source_im)
            if key == ord('x'):
                # Use t to skip an image without labeling it
                print('Skipping image')
                break
            # if key == ord('o'):
            #     if line_width > 2:
            #         line_width -= 2
            #     im = redraw_lines(source_im)
            # if key == ord('p'):
            #     line_width += 2
            #     im = redraw_lines(source_im)
    cv2.destroyAllWindows()
