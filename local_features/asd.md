segmentation can be applied when object of interest and background are clearly diverse!

but in many applications this is not true! What do we do then?

rely on local features directly extracted from the input gray-scale/colour image !

- local features are special point in the image that convey some information

# Edge

The simplest local feature are edges

Edges don't have a rigorous definition

Intuitive definition: edges are pixels that are localized between regions of different intensities

A lot of CV tasks can be solved by relying on edges

- an edge map is a binary image

## A model of an edge

when we detect edges we typically want one pixel for our edge (no thick edges)

- for this reason we put the edge at the (absolute value) of the peak of the derivative

finding edges in an image is equivalent to finding extrema of the derivative of the image

an edge is a strong change

- for this reason we threshold what peaks are high enough to be considered edges

### detecting images in images (2d signals)

usiamo il gradiente per trovare la direzione di maximum change

- the magnitude of the gradient is the absolute derivative along the direction of maximum image change
- btw: knowing the gradient is equivalent to knowing the derivative along any direction (basta fare il dot product tra gradiente e unit vector della direzione)

finding edges in images is then equivalent to Detecting (strong) maxima of gradient magnitude

- this is the basic edge detector

## How do we compute the discrete gradient of an image?

**we approximate the partial derivates with differences**

- (solo il delta, stiamo considerando una distanza in pixel-size unitaria)

this is also equivalent to computing a correlation with a specific kernel. **This means that we can compute the derivative of an image by using a filter!**

- finding the gradient means computing two correlations (one for each partial derivative)
- (nelle slide le frecce specificano le anchor del filtro)

### Dealing with noise

if we try to find edges by computing derivatives without thinking about noise first, there isn't any chance that our edge detector is gonna work

- provare per credere

we MUST get rid of noise before computing the derivatives

- we can filter out noise before computing the derivatives

we can do this in one pass with a single kernel -> this operators are called smooth derivatives

## Smooth derivatives

the key idea is to compute a difference of means

however not naive means but orthogonal to the direction of differentiation

- this way we're not smoothing across the edge
