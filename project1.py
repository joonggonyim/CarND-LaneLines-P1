from util import *
from moviepy.editor import VideoFileClip
from IPython.display import HTML

import os
imList = os.listdir("test_images/")
print(imList)



def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)
    
    # convert to different color scales
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    im_HSV  = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    imY,imX = im_gray.shape

    # extract yellow
    yellow_low = np.uint8([80,100,100])
    yellow_high = np.uint8([100,255,255])
    
    mask_yellow = cv2.inRange(im_HSV,yellow_low,yellow_high)

    # extract white
    white_low = np.uint8([200])
    white_high = np.uint8([255])
    mask_white = cv2.inRange(im_gray,white_low,white_high)

    mask_color = cv2.bitwise_or(mask_white,mask_yellow)
    
    img_maskColor = cv2.bitwise_and(im_gray,mask_color)


    



    # gaussian blur
    kernel_size = 5
    im_blur = gaussian_blur(img_maskColor, kernel_size)
    
    # canny
    low_threshold = 50
    high_threshold = 150
    im_edge = canny(im_blur, low_threshold, high_threshold)

    # mask area
    pbm = 0.3 # percent below mid
    pfb = 0.0 # percent from border
    vertices = np.array([ [(imX*pfb,imY*(1-pfb)), 
                           (imX/2*(1-pbm),imY/2*(1+pbm)),
                           (imX/2*(1+pbm),imY/2*(1+pbm)),
                           (imX,imY*(1-pfb))] ],dtype=np.int32)
    
    im_mask = region_of_interest(im_edge, vertices)
    

    

    # hough line
    # Define the Hough transform parameters
    # Make a blank the same size as our image to draw on
    rho = 1 # distance resolution in pixels of the Hough grid
    theta = np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 20     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 10 #minimum number of pixels making up a line
    max_line_gap = 50    # maximum gap in pixels between connectable line segments
    
    im_hough = hough_lines(im_mask, rho, theta, threshold, min_line_length, max_line_gap,pbm)
    
    im_final = weighted_img(im_hough, image, α=0.8, β=1., λ=0.)

    return im_final
    # return result


# img_fname = "test_images/" + imList[2]

# img = mpimg.imread(img_fname)
# imFinal = process_image(img)
# # plt.imshow(imFinal,'gray')

challenge_output = 'extra.mp4'
clip2 = VideoFileClip('challenge.mp4')
challenge_clip = clip2.fl_image(process_image)
challenge_clip.write_videofile(challenge_output, audio=False)