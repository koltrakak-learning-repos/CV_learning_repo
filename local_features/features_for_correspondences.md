Finding correspondences is a key problem in CV. There are many CV tasks in which finding correspondences is the main problem

**DEF**: Correspondences are pixels in multiple images that are the projection of the same 3d point

interessante:

per fare panoramiche utilizziamo omografie... però non sembra la trasformazione giusta!

le omografie mappano immagini quando

- la scena è planare
- la camera ruota attorno al suo optical centre

qua queste condizioni non sono verificate

stiamo approssimando:

- scene con uno sfondo lontano possono essere approssimante come planari
- ruotare la camera senza traslare troppo è circa come ruotare rispetto all'optical centre

# come troviamo corrispondenze

- bisogna trovare salient points
  - punti particolarmente informativi (non regioni uniformi)
    - fingerprint of an image
  - we disregard all other non-salient points
  - troviamo le corrispondenze tra i salient points
  - come si trovano salient ponts? Anche questo è un problema

- confrontiamo neighbourhoods dei salient points
  - we compare neighbourhoods through a descriptor
    - vectors of real numbers
  - this is because the two images might have been taken in different lighting, or whatever else conditions
    - for example comparing neighbourhoods wrt to color intensities wouldn't be a good idea since the colors of the same neighbourhoods would be different if the lighting conditions were different

domanda: siamo sicuri che i salient points identificati nelle due immagini contengano effettivamente le corrispondenze?

Local INVARIANT features: we want to esablish correspondences between images despite images being quite different

- in particular we want to be invariant to scale
  - ricorda che scale è la perceived dimension di un oggetto nell'immagine, non la vera dimensione
  - la scale dipende dalla distanza, dalla focal length e dalla true dimension

# Come troviamo i keypoints?

un local feature che conosciamo già sono gli edges

a good salient point is one where its neighbourhoods is a good description that allows us to find the coorrespondence

an edge is NOT a good keypoint

- along the gradient direction there is a strong change
- along the orthogonal direction there is little change

per lo stesso motivo i punti appartenenti a uniform regions non sono good keypoints (anche peggio rispetto a edges)

**DEF**: A good salient point is a point where there is a strong change in both the direction along the gradient and the direction perpendicular to the gradient

- es: corners

# Corner detectors

## Moravec corner detector

distance between neighbours... why is this a good cornerness function?

- if p is in a uniform area the distances are all very small
- if p is an edge, moving along the edge produces small distances and we take the minimum
- the only way this function can be high is when p is a corner

## Harris corner detector

improves moravec

- continuous formulation of moravec
- its better because its less prone to quantization errors

(used by opencv for finding calibration points)

instead of comparing only to 8 neighbourhoods, we compare to the infinite neighbourhoods along all directions

L'errore di harris è lo square error tra l'intorno del punto considerato, e l'intorno shiftato infinitesamente in una direzione

- ogni punto dell'immagine ha il suo intorno e i suoi gradienti
  - la weight function sets to zero the points that are not the local neighbourhoods
- like Moravec but the shift is infinitesimal and the shift can be along any direction

 [11:03] spiegazione formula di taylor

Nota: otteniamo il dot product along the gradient and the shift; ovvero la derivata nella direzione dello shift

raggiungiamo una forma matriciale dell'errore in cui solo la matrice M dipende dall'immagine

- M riassume il contenuto dell'immagine
  - M viene chiamata structure matrix perchè cattura come l'intorno del pixel varia
- l'errore rispetto ad ogni shift viene parametrizzato dalla direzione dello shift ed ha M come variabile

ipotizziamo che M è diagonale (non c'è perdita di generalità (real and symmetric matrixes can always be diagonalized))

- i lambda sono eigenvalues
  - lambda1 is the larger one
  - lambda2 is the smaller one

**importante per l'esame!**

- se entrambi i lambda sono piccoli
  - l'errore è piccolo
  - **per ogni shift!** siamo in una regione uniforme!
  - gli intorni sono smili
- se lambda1 >> lambda2 (ricorda che lambda1 è sempre maggiore)
  - l'errore è grande solo se shiftiamo verso deltax
  - l'errore è piccolo se shiftiamo nella direzione perpendicolare

ricorda che il larger eigenvector (eigenvector associato al larger eigenvalue) rappresenta la direzione di maximal change

- se anche la direzione di maximal change è piccola, siamo in un area uniforme
- se variamo tanto nella direzione di maximal change, ma non nella direzione di minimal change -> siamo su un edge
- altrimenti siamo in un corner

## implementing harris

una implementazione naive potrebbe essere calcolare le derivate, ottenere M, e calcolare gli autovalori lambda

tuttavia calcolare gli autovalori di una matrica è computazionalmente costoso

harris offre una soluzione più efficente che richiede di calcolare solo determinante e traccia di M

- cornerness function (descriptor)

# Scale-invariance

**harris corner detector is not scale invariant**

- this is because of the use of a **fixed-size detection window**

**NB**: being a corner or not depends not only on the structure of the image, but also on its scale!

In an image there also exist features at different scales

- with harris we would need to decide the scale at which we want to detect the corners
- but we want to find corners (every feature really) at every scale
  - we want scale invariance
- why? because the more features we can detect the more points we have at our disposal for matching
  - also in different images, some features might disappear (vedi cima taj mahal che scompare nella foto lontana)
  - with more features we're more robust to features disappearing if we want to match them

All this is to say that we need a **dynamic-size detection window**

- in different images, features appear at different scales
- if we used fixes-size windows it would be impossible to detect them all
- and that would make finding correspondences difficult
- large scale features should use large detection windows, small scale features should use small ones

We have an issue. To match features at different scales we need to have similar descriptors

- but at different scales different features show up
- and so the resulting descriptor would be different for the same neighbourhoods in different images
- to solve this issue by applying a smoothing filter

We have an issue. To match features at different scales we need to have similar descriptors

- but at different scales different features show up
- and so the resulting descriptor would be different for the same neighbourhoods in different images
- we can solve this issue by applying a smoothing filter that eliminates small features (simplifies images) in large scale pictures
- this allows us to match to the small scale picture

## How do we detect multiscale features

do we really need a dynamic-size detection window? This could get computationally expensive con neighbourhoods grandi

Abbiamo due opzioni in realtà:

1. we can increase the size of the neighbourhood
2. we can change the size of the image (by downsampling) while keeping the neighbourhood size fixes
    - the more shrinkage the larger the scale of the features we look for

option 2 is way more computationally efficient because we work with less pixels (both considering the neighbourhood and the whole image)

we're introduced to a new concept

- receptive field of an operator: its the size region of the image that determines the output of an operator

NB: actually we combine downsampling with smoothing for the reasons above

# Feature detection and Scale selection

A **scale-space** is a stack of images each at different levels of smoothing (scale)

- the more smoothing is applied, the larger the scale of the features we detect

characteristic scale: the scale at which the feature is maximally salient

the only way to simplify an image correctly (smoothly and without introducing artifacts) increasing the scale is the gaussian filter

sigma è lo scale parameter

- più è grande maggiore è lo smoothing e maggiore è la scala delle features che rileviamo

NB: another way to realize the gaussian scale space is by thinking of the image as an heat-map and solving the heat equation through time

- the more time passes the more smoothing (relazione con sigma)
- k è un parametro che rappresenta la conduttività termica

conclusione: the way to simplify an image is through gaussian filters

## how do we detect features?

The Gaussian Scale-Space is the right tool to smooth an image in order to progressively simplify its content. However, it neither includes any criterion to detect features nor to select their characteristic scale

key finding: we can detect features across scales by finding extrema of certain combination of gaussian derivatives

- features are filtered by the derivative of the gaussian
- scale normalized because derivatives computed at larger scales sono più blurred e quindi hanno derivate per forza più piccole

we check for features by looking for extrema across space and scale

## LOG (Laplacian of Gaussian)

[14:52]

we're going to be finding extrema of the scale-normalized Laplacian of Gaussian

now a property of convolution becomes convenient: convolution commutes with differentiation

- this way we can just **filter with the laplacian of the gaussian**
- this is just a filter
- a circularly simmetric filter; this means that it can find features with invariance to rotation

a nice thing about LOG is that the ratio at which we find features in different images is the same as the ration of the scales of the two images.

- LOG exactly captures the concept of scale

this detector finds blobl like features

- ricordiamo che non ci interessa necessariamente che feature vengono trovate
- l'importante è che il nostro detector trovi le stesse features in immagini diverse in modo tale da fare matching (repeatability)

## DOG (Difference of Gaussians)

way more computationally efficient that the LOG

di nuovo le proprietà della convoluzione ci fanno comodo: stavolta utilizziamo la proprietà distributiva

the difference of the Gaussian approximates the LOG function

- the only difference is a scale factor
- since we care only about finding extrema (and not absolute values) DOG is useful for our purposes

Anche questo è circularly simmetric e quindi invariant to rotation

to probe 4 scales we need to compute 7 gaussian filtered images because we need to find extrema across the stack of filtered images

**NB**: if we want more octaves we don't compute more gaussians, that would become computationally expensive because the larger the sigma the larger the window of the kernel becomes

- once again, we use downsampling and keep using the same filters

# Scale and rotation invariance

we need both the detector and the descriptor scale and rotation invariant

per adesso ci siamo concentrati sui detector, consideriamo ora i descriptor

to compute a descriptor that is scale invariant we need to compute it at the scale at which the feature was detected

- this is because we need the right amount of smoothing to make features similar in different images at different scales

NB: the reason the DOG is more computationally efficient wrt the dog is because it has already at its disposal the gaussian filtered images at all the scales

what about rotation invariance?

we need to take into account the reference frame

to achieve rotation invariance we need to make the descriptors reason with a reference frame that is oriented with objects, we can't use a global reference frame

an intuitive way to define a local reference frame is to define the x-axis of the objects as the direction of maximal change, considerando però non il gradiente di un singolo punto ma l'informazione di tutto il neighbourhood

## Orientation Histogram

we need to chood a bin size to quantize the gradient directions into bins for the histogram

let's increment the bins proportionally to the magnitude of the gradients

- this way uniform regions, that have small gradients with kind of random directions, dont' count much
- we accumulate into the bins gradient magnitude

we can compute the orientation of the keypoints

slide 39 skip

# Sift descriptor

DoG and Sift are a good combo (best known and best working)

**NB**: The descriptor is rotation and scale invariant because

- we consider the scale at which the feature was found
- we consider the orientation of the neighbourhood found in the orientation histogram of the keypoint

**NB**:

- per calcolare l'orientamento della patch calcoliamo un orientation histogram con 36 bins
- per calcolare gli orientation histograms dei blocchi 4x4 di sift utilizziamo 8 bins

SIFT is a descriptors represented as a vector of 128 floats

# How do we establish correspondences given the descriptor vectors?

it's a nearest neighbour problem

if consider only the nearest neighbour we're gonna be matching every feature in the source image to a feature in the target image

- but this is not correct, we might even have a larger amount of features in the source image than in the target image

for this reason we threshold the distance

but what threshold do we choose?

- it's not easy to reason about (absolute) distances in highdimensional spaces

- the ratio of the 2 NN is bounded by one
  - it's easier to threshold this ratio since it's a value [0, 1]
  - Lowe's ratio

d_NN/d_2NN <= 0.1; questo significa che il miglior match deve essere 10 volte migliore del secondo miglior match

Con una soglia alta tipo 0.9 trovi tanti match, ma la maggior parte sono **falsi positivi**.

Con 0.9 Vuol dire: "Accetto il match se il migliore è **almeno solo il 10% migliore** del secondo" - una condizione molto lasca!

## Efficient NN-search

we borrow techniques from database theory

we use indexes

- in particular a k-d tree that is o(log n)
- this doesn't work with sift because the dimensionality is too high
- variant of k-d tree called BestBinFirst is an indexing technique that deals with high dimensional space
- however, unlike the k-d tree (that is equivalent to the exhaustive search), BBF is an approximate search, **it might find wrong correspondences!**

tipically fast means approximate (no free lunch D:)

```
chiedi per soluzioni a lab

slide
```
