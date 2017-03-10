#**Finding Lane Lines on the Road** 

[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"
[RGB_im]: ./writeup_img/RGBscale.jpg
[mask_y]: ./writeup_img/mask_yellow.jpg
[mask_w]: ./writeup_img/mask_white.jpg
[im_maskColor]: ./writeup_img/im_maskColor.jpg
[im_blur]: ./writeup_img/gaussianBlur.jpg
[im_canny]: ./writeup_img/CannyEdge.jpg
[mask_region]: ./writeup_img/maskRegion.jpg
[im_maskRegion]: ./writeup_img/im_maskRegion.jpg
[hough_lines]: ./writeup_img/houghLines.jpg
[interp_lines]: ./writeup_img/interpolated.jpg
[im_final]: ./writeup_img/finalImage.jpg

**Finding Lane Lines on the Road**

The goals / steps of this project are the following: 
> Original Image
![alt text][RGB_im] 

* generate a yellow color mask and white color mask using the HSV scaled image
* mask the image to display only the white and yellow
* transform the color image with the mask to gray scale
* use Gaussian blur on the image
* using Canny edge detector, extract edges from the masekd gray-scaled image
* only focus on the region of interest by masking the area of interest with a polygon
* using the edge within the region of interest, use Hough lines to extract lines
* put higher weight on lines proportional to the line length
* group the points in left and right side of the image and perform linear regression on two groups
* mix the line with the original color image 
---

### Reflection

###1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 6 major steps and the intermediate images between each step is displayed above. 
####1.1) Masking Yellow and White
The first step I took was masking with a white mask and yellow mask. By creating these two color masks, I can focus on parts of the image where the colors are white or yellow. Creating a mask for the white color was relatively trivial because I could convert the image into gray scale and specify the lower and upper boundary of pixel values from 0 to 255 to specify different shades of white. 
```python
im_gray    = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
white_low  = np.uint8([200])
white_high = np.uint8([255])
mask_white = cv2.inRange(im_gray,white_low,white_high)
```
Specifying the range of colors for the yellow mask was relatively more difficult. In order to identify wide range of yellow, I converted the image into the HSV scale and specified the range as below. 
```python
im_HSV      = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
yellow_low  = np.uint8([80,100,100])
yellow_high = np.uint8([100,255,255])
mask_yellow = cv2.inRange(im_HSV,yellow_low,yellow_high)
``` 
The resulting masks from the above codes are shown in the table below.

yellow mask           | white mask
:--------------------:|:--------------------:
![alt-text-1][mask_y] | ![alt-text-2][mask_w]

After obtaining the masks for both white and yellow, I combined the two masks and masked the original image with the combined mask.
> color masked image
![][im_maskColor]

#####1.2) Gaussian Blur
Sometimes, too much information could be harmful. In the case of image processing, too much information, which is high resolution, can lead to very noisy interpretation. For example, a lane marking on the ground should ideally be interpreted as a straight line. However, if the resolution is too high, the roungh surface is captured and yields very noisy straight line. In order to prevent too much resolution distorting our perception of the image, I used the Gaussian filter to blur the image with the kernel size of 5.

```python
kernel_size = 5
im_blur = gaussian_blur(img_maskColor, kernel_size)
```

The resulting image is 

> Gaussian Blur
![][im_blur]

####1.3) Canny Edge detector
Now that we have a processed image that only captures white and yellow in reasonable resolution, I decided to extrapolate edges from the image using the Canny edge detector. 

```python
low_threshold  = 50
high_threshold = 150
im_edge        = canny(im_blur, low_threshold, high_threshold)
```

The edge extracted from the image is shown below. 

> Canny Edge
![][im_canny]

####1.4) Masking a region.
When driving a car, the lane lines are usually visibile within relatively constant region. A simple triangle starting from the bottom nodes of the image converging at the center is a good generalization of the region where you will see the lane lines. In order to fine tune the region to reject other white and yellow objects (mostly cars), I specified a trapezoid to create the mask. The parameters of the trapezoid are 

```python
pbm      = 0.3 # percent below mid
pfb      = 0.0 # percent from border
vertices = np.array([ [(imX*pfb,imY*(1-pfb)), 
                       (imX/2*(1-pbm),imY/2*(1+pbm)),
                       (imX/2*(1+pbm),imY/2*(1+pbm)),
                       (imX,imY*(1-pfb))] ],dtype=np.int32)
```


The mask specified with the above vertices and the image masked with the region mask is shown in the table below.

region mask                | region masked image
:-------------------------:|:-------------------------:
![alt-text-1][mask_region] | ![alt-text-2][im_maskRegion]

It should be noted that a white car that was traveling on your right lane is masked because it appears outside of the region of interest. 

####1.5) Hough Transform
Now that I was able to extract the edges from the image in specified color range and region, I can start extrapolating lines from the edges. 

```python
rho = 1 # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 20     # minimum number of votes (intersections in Hough grid cell)
min_line_len = 10 #minimum number of pixels making up a line
max_line_gap = 50    # maximum gap in pixels between connectable line segments

lines = cv2.HoughLinesP(masked_image, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
```

>Plot of Hough Lines
![][hough_lines]

####1.6) Weighted Interpolation
Thhe lines defined by hough transform should be divided into two groups, left and right. In order to ensure that longer lines have more weight on creating the final line, I duplicate the lines proportional to their line length. Afterwards, all the points in each group are interpolated to generate a single line. Since the lines start and end at different locations for each frame, the end points of the two lines are specified. 

>Interpolated Lines
![][interp_lines]

####1.7) Weighted mix
Finally, the image of the line and original RBG images are mixed withe the weight of 0.8:1.0 (line:original).

>FINAL IMAGE
![][im_final]

###2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when there is a white or yellow car very close to my car in my lane. This car will not be masked in and the edges from the car will be interpolated to generate wrong line.  

Another shortcoming could be there may be a car crossing the line to the next lane and cover up the lane lines from vision. 

###3. Suggest possible improvements to your pipeline

A possible improvement would be to let remember the slope and y-intercept values from each slope and perform running average through out the frame. The problem with this approach is that the number of frames to choose as window size have be fine tuned.
