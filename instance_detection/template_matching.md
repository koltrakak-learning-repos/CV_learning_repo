**Instance detection**: Given a reference image of a specific object (template), determine whether the object is present or not in the image under analysis (aka target image)

In **instance** detection we want to detect a specific instance in an image

- non un telefono qualsiasi, uno specifico telefono
- questo è un problema limitato più facile di riconoscere una determinata **categoria di oggetti**
  - in quest'ultimo caso abbiamo bisogno di NN che riesce a gestire variabilità
  - category-level object detection

Questo è un problema tipico di machine vision, dato che l'environment è constrained (devo trovare esattamente il template)

# Template matching or Pattern matching

This is a family of algorithms

- il paradigma comune è quello della sliding window
  - scorriamo il template nella target image fino a che non troviamo un match
  - ad ogni posizione confrontiamo il template con la relatia sub-image tramite una similarity/dissimilarity function
  - la posizione nella target image con lo score migliore determina se e dove l'istanza è stata individuata
- cio che cambia come computiamo la similarity/dissimilarity

## Similarity/Dissimilarity functions

SSD and SAD are the simplest ones

- both are dissimilarity functions
- possiamo pensare alla sub-image ed al template come vettori m*n-dimensionali
  - SSD rappresenta la distanza euclidea al quadrato di questi vettori
  - SAD rappresenta la distanza di manhattan di questi vettori

NCC (normalised cross-correlation)

- most widely used
- similarity function
  - numeratore = dot product between the two (flattened) vectors
  - denominatore = prodotto della norma dei due vettori
  - they cancel out -> NCC is the cos() of the angle between the two vectors
- this is better than the SSD and SAD because its **more robust to light changes**
  - pensa ad esempio ad un immagine in cui il template è presente ma con tutte le intensità scalate per uno scalare (ad esempio a causa di una variazione di illuminazione)
    - linear transformation
  - i due vettori continuano a puntare nella stessa direzione

ZNCC

- an even more robust to light changes version of the NCC
- rather than considering the initial intensities of the template and the current sub-image, we subtract the mean and then compute the NCC
  - this is a zero mean NCC
- with this we gain invariance to an affine light change (not just a linear one)

**NB**: But how do we know if the light changes are linear or affine or something else?

- we don't, if we know that there we're going to need to deal with light changes we just use the more robust function (this being ZNCC)
- **in settings where light changes might be an issue for template matching, ZNCC is the tool to go for**

```
btw, template matching along epipolar lines is the standard stereo matching algorithm
```
