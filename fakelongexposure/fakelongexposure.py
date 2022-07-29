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
    parser.add_argument('-p', '--progress', action='store_true', 
                        help='Pring progress information.')
    parser.add_argument('-s', '--start-frame', type=int, default=1, metavar='S',
                        help='The first frame (1 is the first frame) to use in the picture.')
    parser.add_argument('-e', '--end-frame', type=int, default=-1, metavar='E',
                        help='The last frame (1 is the first frame) to use in the picture.')


    args = parser.parse_args()

    mImg = []
    fnum = 0

    if args.progress:
        print(f'Loading "{args.video}"')
    # open video file and read each image, assume 8bits/pixel
    cap = cv.VideoCapture(args.video)
    while(cap.isOpened()):
        fnum += 1
        # output progress
        if args.progress:
            print(f'Processing frame {fnum}')
        ret, frame = cap.read()
        #skip early frames
        if fnum >= args.start_frame :
            if(ret == True):
                #calculate index in used portion
                idx = fnum - args.start_frame
                if(idx < args.fcount):
                    mImg.append(frame)
                else:
                    mImg[idx%args.fcount] = np.maximum(frame,mImg[idx%args.fcount])
            else:
                break

        #exit loop once the end frame has been reached
        if args.start_frame != -1 and fnum >= args.end_frame :
            break

    # now create an average
    avgImg = None
    nAvg = len(mImg)
    for n, img in enumerate(mImg):
        if args.progress:
            print(f'Averaging {n + 1}/{nAvg}')
        #cv.imwrite(str(idx) + "_test.png",img)
        if avgImg is None:
            avgImg = img.astype("float64")
        else:
            avgImg = avgImg + img.astype("float64")

    if args.progress:
        print('Scaling values')
    # average and scale this to 16 bit range
    avgImg = avgImg *256 / args.fcount
    avgImg = avgImg.astype(np.uint16)

    out_args = []

    _, out_ext = os.path.splitext(args.output)

    if args.progress:
        print('Encoding image')
    #cv.imdecode(avgImg,cv.CV_LOAD_IMAGE_COLOR)
    rv, encoded = cv.imencode(out_ext, avgImg)

    #cv.imwrite(args.output,encoded,out_args)

    if args.progress:
        print(f'Writing "{args.output}"')
    with open(args.output,'wb') as f:
        f.write(encoded)

if __name__ == '__main__':
    main()

