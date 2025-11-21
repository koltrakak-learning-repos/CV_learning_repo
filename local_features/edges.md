Segmentation can be applied when object of interest and background are clearly diverse!

But in many applications this is not true! What do we do then?

-> Rely on local features directly extracted from the input gray-scale/colour image!

- local features are special point in the image that convey some information

# Edges

The simplest local feature are edges

Edges don't have a rigorous definition

- Intuitive definition: edges are pixels that are localized between regions of different intensities

A lot of CV tasks can be solved by relying on edges

- vedi misurazioni

An edge map is a binary image

## A model of an edge

when we detect edges we typically want one pixel for our edge (no thick edges)

- for this reason we put the edge at the (absolute value) of the peak of the derivative

finding edges in an image is equivalent to finding extrema of the derivative of the image

an edge is a STRONG change

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

the key idea is to compute a difference (per fare la derivata) of means (per rimuovere il rumore)

however not naive means but **orthogonal to the direction of differentiation**

- this way we're not smoothing across the edge

## non-maxima suppression

(non ci siamo soffermati sui dettagli)

after computing the gradient we need to find the peaks of this function, the local maxima

- this step is called NMS because it suppresses points that are not local maxima

Dopo il calcolo del gradiente dell'immagine i "bordi" che si ottengono risultano "spessi"

Il compito della Non-Maxima Suppression (NMS) è sottigliare i bordi, mantenendo solo i pixel che sono veri massimi locali lungo la direzione del gradiente.

**NMS happens along the gradient direction**

- altrimenti elimineremmo pixel appartenenti ad un vertical/horizontal edge adiacenti ad un edge pixel
- è una funzione 1d; non guarda il 2d neighbourhood

## Thresholding

After NMS we threshold the survivors because we want strong edges

# Canny's edge detector

OSS: Sobel filtering is just a way to compute smooth derivatives (possiamo usarlo per computare il gradiente di un'immagine), it's **NOT a full edge-detector**

by far the most used edge detector is Canny

three properties we want:

1. good detection
    - basically we want to be robust to noise
    - we want to find true edges and not edges that appear due to noise
2. good localization
    - good precision on the edge position
3. One response to one edge
    - thin edges

It can be shown (through some heavy math) that the optimal function that Canny find is the first derivative of a Gaussian... but this is in 1d

- the gaussian's purpose is handling noise
- **the most common 2d canny implementation is basically a gaussian filter that removes noise and then computing the gradient of the image**
- one response to an edge is obtained through NMS

## smart thresholding

One more ingredient to canny's filter is a smart filter

`edge streaking is when the contour of an object becomes dashed`

- edge streaking is more prone to happen when the lighting isn't uniform, in altre parole abbiamo regioni ad alto contrasto (edge forti) e regioni a basso contrasto (edge deboli)

what canny says is that choosing only one threshold leads to edge streaking. So let's choose 2 thresholds

but now we have to tune 2 parameters?

- the rule of thumb is taking the high threshold to be twice as much as the low one

## How is canny implemented in ocv?

it's not implemented well

manca un gaussian filter iniziale per rimuovere il rumore

- ricorda che sobel serve solo a computare le derivate
