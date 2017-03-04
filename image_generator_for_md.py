# image_generator_for_md.py

from util import *
testIm_fname = "test_images/solidYellowLeft.jpg"
saveDir = 'writeup_img/'

image = mpimg.imread(testIm_fname)



# convert to different color scales
im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
im_HSV  = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

fname_im_gray = saveDir + 'grayscale.jpg'
fname_im_HSV  = saveDir + 'HSVscale.jpg'
fname_im_original = saveDir + 'RGBscale.jpg'
plt.imsave(fname_im_gray,im_gray,cmap='gray')
plt.imsave(fname_im_original,image)

imY,imX = im_gray.shape

# 1) generate a yellow color mask and white color mask using the HSV scaled image
# extract yellow
yellow_low = np.uint8([80,100,100])
yellow_high = np.uint8([100,255,255])

mask_yellow = cv2.inRange(im_HSV,yellow_low,yellow_high)

# extract white
white_low = np.uint8([200])
white_high = np.uint8([255])
mask_white = cv2.inRange(im_gray,white_low,white_high)

mask_color = cv2.bitwise_or(mask_white,mask_yellow)
mask_color = np.stack((mask_color,mask_color,mask_color),axis=2)

img_maskColor = cv2.bitwise_and(image,mask_color)

fname_mask_yellow = saveDir + 'mask_yellow.jpg'
fname_mask_white  = saveDir + 'mask_white.jpg'
fname_mask_image  = saveDir + 'im_maskColor.jpg'
plt.imsave(fname_mask_yellow,mask_yellow,cmap='gray')
plt.imsave(fname_mask_white,mask_white,cmap='gray')
plt.imsave(fname_mask_image,img_maskColor)

img_maskColor = cv2.cvtColor(img_maskColor,cv2.COLOR_BGR2GRAY)
# 2) use Gaussian blur on the image
# gaussian blur
kernel_size = 5
im_blur = gaussian_blur(img_maskColor, kernel_size)

fname_im_blur = saveDir + 'gaussianBlur.jpg'
plt.imsave(fname_im_blur,im_blur,cmap='gray')

# 3) using Canny edge detector, extract edges from the masekd gray-scaled image
low_threshold = 50
high_threshold = 150
im_edge = canny(im_blur, low_threshold, high_threshold)

fname_im_edge = saveDir + 'CannyEdge.jpg'
plt.imsave(fname_im_edge,im_edge,cmap='gray')

# 4) only focus on the region of interest by masking the area of interest with a polygon

# mask area
pbm = 0.3 # percent below mid
pfb = 0.0 # percent from border
vertices = np.array([ [(imX*pfb,imY*(1-pfb)), 
                       (imX/2*(1-pbm),imY/2*(1+pbm)),
                       (imX/2*(1+pbm),imY/2*(1+pbm)),
                       (imX,imY*(1-pfb))] ],dtype=np.int32)

mask = np.zeros_like(im_edge)   
    
#defining a 3 channel or 1 channel color to fill the mask with depending on the input image
if len(im_edge.shape) > 2:
    channel_count = im_edge.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
else:
    ignore_mask_color = 255
    
#filling pixels inside the polygon defined by "vertices" with the fill color    
cv2.fillPoly(mask, vertices, ignore_mask_color)

# #returning the image only where mask pixels are nonzero
masked_image = cv2.bitwise_and(im_edge, mask)

fname_im_maskRegion = saveDir + 'im_maskRegion.jpg'
fname_mask_region   = saveDir + 'maskRegion.jpg'
plt.imsave(fname_im_maskRegion,masked_image,cmap='gray')
plt.imsave(fname_mask_region,mask,cmap='gray')

# 5) using the edge within the region of interest, use Hough lines to extract lines

rho = 1 # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 20     # minimum number of votes (intersections in Hough grid cell)
min_line_len = 10 #minimum number of pixels making up a line
max_line_gap = 50    # maximum gap in pixels between connectable line segments

lines = cv2.HoughLinesP(masked_image, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)

plt.figure()

for line in lines:
	for x1,y1,x2,y2 in line:
		plt.plot([x1,x2],[y1,y2],'x--')

plt.axis([0,imX,imY,0])
fname_hough_lines = saveDir + 'houghLines.jpg'
plt.savefig(fname_hough_lines)

# 6) put higher weight on lines proportional to the line length
#  group the points in left and right side of the image and perform linear regression on two groups
line_img = np.zeros((imY, imX, 3), dtype=np.uint8)
lines = interpolatedLines(lines, imX,imY,pbm)

# plt.figure()

# for line in lines:
# 	for x1,y1,x2,y2 in line:
# 		plt.plot([x1,x2],[y1,y2],'x--')

# plt.axis([0,imX,imY,0])
# fname_interpolated = saveDir + 'interpolated.jpg'
# plt.savefig(fname_interpolated)

plt.figure()
im_hough = hough_lines(masked_image, rho, theta, threshold, min_line_len, max_line_gap,pbm)
fname_interpolated = saveDir + 'interpolated.jpg'
plt.imsave(fname_interpolated,im_hough)

im_final = weighted_img(im_hough, image, α=0.8, β=1., λ=0.)
fname_final_image = saveDir + 'finalImage.jpg'
plt.imsave(fname_final_image,im_final)