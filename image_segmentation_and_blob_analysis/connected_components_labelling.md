In the segmentation part of this chapter we've seen

- how we binarize an image
- some operators to improve binary images

Segmentation is not only about binaryizing images.

- **We also want to label the different objects in the foreground**

We want to label the connected components of the binary image (connected perchè i pixel sono connessi, vedi dopo)

Nota: for debugging purposes we would like to have a look at the labeled image and that's why we need pseudo-colors

### Connectivity and connected-component definition

**premessa**: all these definitions apply to a binary image

**connected pixels**: The pixels connected to a determined one are either the n4 or n8 neighbourhoods

- the choice of neighbourhood is arbitrary but determines the type of connectivity you're gonna be using

**path**: percorso i cui pixel sono connessi secondo la nozione di connettività decisa (4-path, 8-path)

connected region: a set of pixels, R, is said to be a connected region if for ANY two pixels p,q in R there exists a path contained in R between p and q

**connected foreground region**: connected region that includes only foreground pixels

**Connected component**: a maximal connected foreground region

- we cannot add any pixels without it stop being a connected foreground region
- la scelta di connectivity cambia la regione massima

### labelling by flood-fill

Algorythm to label the connected components of a binary image

1. we scan the image
2. when we find a foreground pixel, we label its connected component recursively
3. we go back to the loop that scans the image and find another foreground pixel that is not already labeled (appartenente ad un altro connected component) and label its connected componente come al passo due
4. e così via

NB: molto poco computazionalmente efficente! Utilizzare altri algoritmi più svegli
