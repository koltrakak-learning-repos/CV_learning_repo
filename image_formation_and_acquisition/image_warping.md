# warping

A warping is an image processing operation defined by two transformations (functions)

**A warping transforms only pixel coordinates of the image, not intensity or colors**

Esempi di warping:

- removal of lense distortion
- stereo rectification
- they are in fact transformations between pixel coordinates (guarda le formule)

### Forward/Backward mapping

A warping could be defined in two ways

Forward mapping: a transformation from the source image to the target image

- source = old image
- target = new/warped image
- for example wrt lense distortion:
  - the source would be the distorted image
  - the target the undistorted image

**NB**: The warping outputs real values as coordinates since the transformations at play are stuff like: rotation matrixes, homographies, ...

- this means that in the target we get a real value coordinate in between four pixel coordinates that we need to approximate

We have two problems with forward mapping whatever approximation approach we choose:

- we cannot be sure that all pixels in the output image are gonna be "hit" (be the target of the transformation)
- also some pixels are gonna be hit multiple times

These problems are called holes and folds

**To solve this problem we need to do the warping backwards**

- we scan the target image
  - this way we can be sure that we're assigning a value to every pixel in the target (no holes)
  - this avoids holes and folds because every pixel in the target image is gonna have by construction a corresponding pixel in the input image

**NB**: We define warping as a transformation from the new coordinate to the old one

Oss: questo spiega perchè le formule di lense distortion, rectification, ... sembravano avere senso opposto

### Mapping strategies

Anche con backward mapping, ho comunque il problema delle coordinate reali dato che il warping mi tira fuori coordinate di questo tipo

Continuo a dover scegliere tra quattro pixel della source image quello che voglio usare per il mio warping

Stavolta però dato che i pixel tra cui devo scegliere esistono davvero, **posso fare interpolazione**

**Keypoint**: posso fare interpolazione solo con backward mapping! Altrimenti non avrei valori da interpolare

Posso fare vari tipi di interpolazione:

- bilinear interpolation: peso di più i pixel più vicini a dove sono caduto

# chiedi per la perdita di pixel dopo rectification
