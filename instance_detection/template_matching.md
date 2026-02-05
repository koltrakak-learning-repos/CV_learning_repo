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

a volte, ci interessano più gli edges per riconoscere una specifica instance

- es: pezzi meccanici con la stessa texture ma contour diversi

# Shape-based matching

compare gradient direction in the control points

- the more the gradients are aligned the more the shapes are similar (and the more the similarity measure would have to be high)

We can compute the dot product to see the similarity

- Gk = gradient of the chosen points in the template
- Gk~ = gradient of the corresponding control points in the window
- uk = unit gradient

come interpretiamo il thresholding?

- es: t=0.8 -> troviamo un match se l'80% dei gradienti sono aligned

why are we only using gradient direction in detection?

- this makes the algorythm robust to brightness changes/different lighting conditions
- if the image is dark the gradients have the same direction but smaller magnitude

why are we not computing the edges in the target image?

- pretty much again for robustness to brightness changes
- to compute the edges also in the target image we would need to tune the threshold for every target image

...

skip di qualche slide

# The Hough (pronunciato Huff) transform

non abbiamo studiato i dettagli, solo l'idea a pagina 16

se vuoi trovare lines and circles in una edge map hai funzioni in una edge map

## GHT

questo funziona anche con arbitrary shapes

# Star Model

slide 28

these template matching approaches don't really handle rotation and scale changes

- bisogna provarle tutte con un approccio a forza bruta ... non possiamo fare di meglio? SI! Possiamo

scale changes are not really important in Industrial Vision (condizioni stabili -> scale uguali)

rotation changes invece sono importanti

**Possiamo combinare le idee che abbiamo visto in local invariant features con la GHT per ottenere instance detection rotation and scale invariant**

Idea:

- In the template that we want to detect in the target image, rather than detecting edges we detect keypoints (es. DoG keypoints)
- ogni feature è una quadrupla che contiene
  - position (punto)
  - detector
  - canonical orientation
  - scala
- then we compute a reference point as the baricentre of the features
- then we compute a joining vector for every feature
  - every feature comes with a joining vector that tells us in the target image where the baricentre is
- **NB**: i joining vector ci aiutano a fare instance detection dato che ci dicono che abbiamo trovato un'istanza, non solo se abbiamo le feature, ma anche se sono posizionate in maniera coerente con i joining vectors rispetto al baricentro calcolato nel template
  - the more matches i have, the more hypotheses i have on the position of the baricentre
  - if many hypotheses predict the baricentre to be in the same position, ho una buona certezza di aver trovato l'oggetto da detectar
  - se i joining vector nel target trovano tutti baricentri diversi non ho trovato la mia instance
- **NB**: devo fare il tuning di una soglia minima del numero minimo di joining vector coerenti per poter affermare di aver trovato un'istanza del mio oggetto

**NB**: La formulazione sopra non funziona però se nella target image abbiamo rotation and scale changes

- dobbiamo ruotare e scalare i joining vectore nella target image utilizzando
  - le canonical orientation delle feature trovate
  - le scale delle feature trovate

2d accumulator array non va bene dato che accumula nello stesso bin voti provenienti da diverse rotazioni/scale

- però è comodo computazionalmente (e good enough in molti casi) e quindi si gestisce con un RANSAC approach

alternativa può essere 4d accumulator array

**Interessante notare che lo stear model può essere utilizzato anche per filtrare wrong correspondences**
