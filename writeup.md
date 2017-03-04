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

yellow mask           | white mask
:--------------------:|:--------------------:
![alt-text-1][mask_y] | ![alt-text-2][mask_w]

* mask the image to display only the white and yellow
> color masked image
![][im_maskColor]

* transform the color image with the mask to gray scale
* use Gaussian blur on the image
> Gaussian Blur
![][im_blur]

* using Canny edge detector, extract edges from the masekd gray-scaled image
> Canny Edge
![][im_canny]

* only focus on the region of interest by masking the area of interest with a polygon

region mask                | region masked image
:-------------------------:|:-------------------------:
![alt-text-1][mask_region] | ![alt-text-2][im_maskRegion]

* using the edge within the region of interest, use Hough lines to extract lines

>Plot of Hough Lines
![][hough_lines]

* put higher weight on lines proportional to the line length
* group the points in left and right side of the image and perform linear regression on two groups
>Interpolated Lines
![][interp_lines]

* mix the line with the original color image 
>FINAL IMAGE
![][im_final]


---

### Reflection

###1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I .... 

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


###2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


###3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...
