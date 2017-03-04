#**Finding Lane Lines on the Road** 

**Finding Lane Lines on the Road**

The goals / steps of this project are the following: 

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


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

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
