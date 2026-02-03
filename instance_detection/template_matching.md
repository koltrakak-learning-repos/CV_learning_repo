we want to detect a specific instance in an image

- non un telefono ma uno specifico telefono
- questo è un problema limitato più facile di riconoscere una determinata categoria di oggetti (in questo caso abbiamo bisogno di NN)

# Template matching or Pattern matching

NCC

- numeratore = dot product
- denominatore = norma dei due vettori
- similarity function
- invariant to light changes

...

```
btw, template matching along epipolar lines is the standard stereo algorythm
```

...

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
