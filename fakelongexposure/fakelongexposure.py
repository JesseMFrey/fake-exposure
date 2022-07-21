#!/usr/bin/env python
import cv2 as cv
import numpy as np
import argparse
import os.path

# Author: Scott Manley / @djsnm
# updates by Jesse Frey
# code to generate a fake long exposure image using a video

def main():
    parser = argparse.ArgumentParser(description='Generate a fake long exposure from a video.')

    parser.add_argument('video', metavar='F',
                        help='Video file to read in.')
    parser.add_argument('--fcount', type=int, default=30,
                        help='number of bright points to select and average, '
                        'reduces noise, but makes trails less intense.')
    parser.add_argument('-o', '--output', type=str, default="fake_long_exposure.png",
                        help='Output filename.')

    args = parser.parse_args()

    mImg = []
    idx = 0

    # open video file and read each image, assume 8bits/pixel
    cap = cv.VideoCapture(args.video)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if(ret == True):
            if(idx < args.fcount):
                mImg.append(frame)
            else:
                mImg[idx%args.fcount] = np.maximum(frame,mImg[idx%args.fcount])
        else:
            break
        idx += 1
        # output progress
        if(idx %100 == 0):
            print(idx)

    # now create an average
    avgImg = None
    for img in mImg:
        #cv.imwrite(str(idx) + "_test.png",img)
        if avgImg is None:
            avgImg = img.astype("float64")
        else:
            avgImg = avgImg + img.astype("float64")

    # average and scale this to 16 bit range
    avgImg = avgImg *256 / args.fcount
    avgImg = avgImg.astype(np.uint16)

    out_args = []

    _, out_ext = os.path.splitext(args.output)

    cv.imdecode(avgImg,cv.CV_LOAD_IMAGE_COLOR)
    rv, encoded = cv.imencode(out_ext, avgImg)

    print(encoded)

    #cv.imwrite(args.output,encoded,out_args)

    with open(args.output,'wb') as f:
        f.write(encoded)

if __name__ == '__main__':
    main()

