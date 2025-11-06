In the segmentation part of this chapter we've seen

- how we binarize an image
- some operators on binary images

Segmentation is not only about binaryizing images. We also want to label the different objects in the foreground

We want to label the connected components of the binary image (the foreground regions where all foreground pixels are adjacent one another)

Nota: for debugging purposes we would like to have a look at the labeled image and that's why we need pseudo-colors

### connectivity and connected-component definition

**premessa**: all these definitions apply to a binary image

the pixels connected to a determined one are either the n4 or n8 neighbourhoods

- the choice of neighbourhood is arbitrary but determines the type of connectivity you're gonna be using

path: percorso in cui pixel adiacenti sono connessi secondo la nozione di connettività decisa (4-path, 8-path)

connected region: ...

connected foreground region: ...

**Connected component**: a maximal connected foreground region

- we cannot add any pixels without it stop being a connected foreground region
- la scelta di connectivity cambia la regione massima

### labelling by flood-fill

1. we scan the image
2. when we find a foreground pixel, we label its connected component recursively
3. we go back to the loop that scans the image and find another foreground pixel that is not already labeled (appartenente ad un altro connected component) and label its connected componente come al passo due
4. e così via

NB: molto poco computazionalmente efficente! Utilizzare altri algoritmi più svegli
