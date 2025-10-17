A warping is an image processing operation defined by two transformations

**A warping transforms only pixel coordinates**

- not intensity or colors

...

the warping outputs real values as coordinates, this means that we get a real coordinate in between four pixel coordinates that we need to approximate

we have two problems with forward mapping

- we cannot be sure that all pixels in the output image
- also some pixels are gonna be hit multiple times
- holes and folds

to solve this problem we do the warping backwards

- this avoids holes and folds because every pixel in the target image is gonna have by construction a corresponding pixel in the input image
