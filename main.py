import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("Bad_Apple_Frames/bad_apple_237.png", cv2.IMREAD_GRAYSCALE)

HORI_RES = 1440 # must be multiple of 9
ROWS = 10

#chrom chromStart chromEnd name score strand thickStart thickEnd itemRgb blockCount blockSizes blockStarts

def frame_to_base(hori_res, frame):
    full_length = int(hori_res / .9) # This is the length (bp) of the frame plus both left and right buffer
    buffer_length = int(full_length * .05) # This is the length (bp) of left or right buffer
    scroll_length = int(full_length * .95) # This is the number of (bp) that are scrolled

    # computing actual frame boundaries
    start = scroll_length * (frame + 2) + buffer_length # linear function. Gradient is scroll_length. offset + 2 because 0th and 1st frame are alignment and blank. Add buffer length to get to actual start
    end = start + hori_res 

    start -= 1 # pad 1 extra bp
    end += 1 #pad 1 extra bp 
    return (int(start), int(end))

def alignment_frame(hori_res):
    full_length = int(hori_res / .9) # This is the length of the frame plus both left and right buffer

    return f"chr22 0 {full_length} bad_apple 1000 . 0 {full_length} 0 1 {full_length} 0"

def resize(img, hori_res):
    return cv2.resize(img, (hori_res, hori_res * img.shape[0] // img.shape[1]))    

def merge_rows_vertically(img, num_rows):
    return np.stack([np.mean(img[i:i+num_rows, ], axis = 0) for i in range(0, img.shape[0], num_rows)])

def black_white(img):
    return ~np.round(img / 255).astype(bool)

def img_to_bed(img, hori_res, frame):
    bed_list = []

    for row in img:
        padded_row = np.pad(row, (1,1), constant_values=0) # detect start and ends of frame
        
        shifted_row = np.roll(padded_row, 1) # shift and XOR to detect block edges 
        xor = np.logical_xor(padded_row,shifted_row)
        xor = xor[1:]

        where = np.where(xor)[0] # extract edge positions
        where += 1 # account for the left pad of 1 base pair

        blockCount = len(where) // 2
        blockSizes =  ",".join(map(str, where[1::2] - where[::2]))
        blockStarts = ",".join(map(str, where[::2]))

        if not blockSizes == "": # pad block sizes string by , if exists
            blockSizes += "," 
        if not blockStarts == "":
            blockStarts += "," 

        chrom = frame_to_base(hori_res, frame)

        bed_line = f"chr22 {chrom[0]} {chrom[1]} bad_apple 1000 . {chrom[0]} {chrom[1]} 0 {blockCount + 2} 1,{blockSizes}1 0,{blockStarts}1441"
        bed_list.append(bed_line)
    
    bed_list.reverse()

    return bed_list

img = resize(img, HORI_RES)
img = merge_rows_vertically(img, ROWS)
img = black_white(img)


print(alignment_frame(HORI_RES))
print("\n".join(img_to_bed(img, HORI_RES, 1)))


'''
chr22 0 1600 bad_apple 1000 . 0 1600 0 1 1600 0
chr22 3119 4561 bad_apple 1000 . 3119 4561 0 2 1,1 0,1441
chr22 4639 6081 bad_apple 1000 . 4639 6081 0 2 1,1 0,1441
'''