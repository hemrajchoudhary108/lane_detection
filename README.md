# Project Name

https://github.com/user-attachments/assets/4b80647f-48ab-4c24-b751-017c1363ba1c


## What's This Project About?
Hey there! This project is all about detecting lanes in a video using OpenCV. It's a fun way to see how computer vision can help in real-world scenarios like self-driving cars.

## Cool Features
- Detects lanes in videos
- Uses edge detection and Hough transforms
- Simple and lightweight, powered by OpenCV

## How It Works (Lane Detection 101)

This is how we make the magic happen:

**Step 1:** Pick the region of interest. Right now, it's hardcoded, but in the future, we could use a CNN to do this automatically.

**Step 2:** Convert the image to grayscale. It helps speed things up and makes lane detection easier.

**Step 3:** Detect edges! We use the Canny edge detection method to highlight lane lines.

**Step 4:** Apply a little Gaussian blur to smooth out the image and reduce noise.

**Step 5:** Use the Hough Line Transform to detect lane lines from the edges.

**Step 6:** Separate left and right lanes based on the slope of the detected lines.

**Step 7:** Extend the detected lines to form clean, continuous lanes.

**Step 8:** Highlight the lanes visually by drawing the final lane boundaries.

## License
Feel free to use and modify this project! It's under the MIT License.

