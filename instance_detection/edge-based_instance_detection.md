A volte, è più appropriato usare solamente degli edges per fare instance detection di un oggetto

- es: pezzi meccanici con la stessa texture ma contour diversi
- l'informazione è data dal countour dell'oggetto non dalla sua texture che è simili agli altri

Consideriamo due metodi:

# Shape-based matching

This is basically **edge-based template matching**

- Instead of comparing colors with the template image, we compare edges
  - più nel dettaglio, **we compare gradient direction in the control points** (vedi meglio a breve)

Il procedimento è il seguente:

- calcoliamo una edge map del tamplate (ad esempio con Sobel)
- scegliamo n control point e consideriamo la direzione (e non anche l'intensità) di quest'ultimi
- **the model of the template consists of the control points and the gradient directions**
- when we compare the template with the sub-image:
  - we considere the points in the sub-image at the offsets defined by the control-points in the template
  - utilizziamo una similarity function che in queste posizioni confronta gli edge del template con gli edge nella sub-image
    - nota che non facciamo un'intera edge detection nella sub-image, computiamo solamente i gradienti nei control point
  - **the more the gradients are aligned the more the shapes are similar** (and the higher the similarity)
  - **we probe at the control points how much gradients of the control points are aligned between the template and the sub-image**

How can we check for similarity between the gradients? We can compute the dot product

- as we care only about direction, we consider the normalized gradients
- Gk = gradient of the chosen points in the template
- Gk~ = gradient of the corresponding control points in the window
- uk, uk~ = the normalized versions of the gradients above (unit gradients)

**The similarity function is the mean dot product of all the unit gradients of the control points**

- since it's a dot product between unit vectors we end up with a mean cosine function that gives us the idea of **average alignement**
- this produces values between zero and one, and so it's easily thresholdable

**If the average alignment surpasses our threshold we accept the match and we say the we have detected the object instance**

Come interpretiamo il thresholding?

- es: t=0.8 -> troviamo un match se l'80% dei gradienti sono aligned
- bisogna anche considerare eventuali occlusioni, in questi casi la threshold definisce quanto della forma dell'oggetto abbiamo bisogno di trovare

Un alta threshold massimizza la precisione -> siamo strict, e non produciamo false positives -> tuttavia potremmo non accorgerci di false negatives

- bisogna fare tuning

**Why are we only using gradient direction in detection?**

- this makes the algorythm robust to brightness changes/different lighting conditions
- if the image is dark the gradients have the same direction but smaller magnitude
- stessa cosa for bright images

Why are we not computing the edges in the target image?

- pretty much again for robustness to brightness changes
- to compute the edges also in the target image we would need to tune the threshold for every target image

---

# The Hough (pronunciato Huff) transform

Questo è l'altro metodo che vediamo circa per fare edge-based instance detection.

- non abbiamo studiato i dettagli, solo l'idea a pagina 16

Questo metodo, data una edge-map, permette di trovare analytical shapes:

- circles
- ellipses
- lines
- shapes that we can describe analytically

## Generalized Hough Transform (GHT)

Generalized dato che questo **funziona anche con arbitrary shapes**

Se ho un oggetto che voglio rilevare, ma la sua forma non è descrivibile con una formula, posso usare GHT per trovarlo nella edge-map dell'immagine

# Star Model (GHT with Local invariant features)

Shape-based matching and the GHT don't really handle rotation and scale changes

- bisogna provarle tutte con un approccio a forza bruta ... non possiamo fare di meglio? SI! Possiamo

Scale changes are not really important in Industrial Vision (condizioni stabili -> scale uguali)

Rotation changes invece sono importanti, as object might appear in the images arbitrarily rotated

**Possiamo combinare le idee che abbiamo visto in local invariant features, con le idee della GHT, per ottenere ROTATION AND SCALE INVARIANT INSTANCE DETECTION**

- instead of applying GHT to an edge map we use it with local invariant features

```
Nei lab abbiamo visto che possiamo fare rotation and scale invariant instance detection semplicemente calcolando i keypoint sift e trovando un certo numero di match

Questo però non è super robusto dato che le feature non sono uniche nel mondo per solo quell'oggetto, altri oggetti potrebbero avere feature simili e quindi considerare solo la presenza delle feature a volte non è sufficiente per essere sicuri di aver trovato l'oggetto
```

Idea:

- In the template that we want to detect in the target image, **rather than detecting edges we detect keypoints (features)** (es. DoG keypoints)
- Ogni feature è una quadrupla che contiene:
  - position (punto)
  - descriptor
  - canonical orientation
  - scale
- **the template that we shall search in the target image is a set of features**
- then we compute a reference point as the **baricentre** of the features as the average of the positions of the features
- then we compute a **joining vector for every feature**
  - every feature comes with a joining vector that tells us in the target image where the baricentre is
- **NB**: i joining vector ci aiutano a fare una instance detection robusta!
  - questo, dato che ci dicono che abbiamo trovato un'istanza, non solo se abbiamo le feature, ma anche se sono posizionate in maniera coerente con i joining vectors rispetto al baricentro calcolato nel template
  - the more matches i have, the more hypotheses i have on the position of the baricentre
  - if many hypotheses predict the baricentre to be in the same position, ho una buona certezza di aver trovato l'oggetto da detectare
  - se i joining vector nel target trovano tutti baricentri diversi non ho trovato la mia instance
  - **non è sufficiente che ci siano le features, bisogna anche che siano posizionate in maniera coerente con il template** (questo è quello che mancava nell'algoritmo del lab)

This is the start model:

- una lista che consiste nella quadrupla delle feature, insieme ai relativi joining vectors

At training time, we compute this list of features and joining vectors on the template image

At inference time:

- we compute the feature of the target image
- then we match the features with the descriptor (NN with lowe's ratio etc.)
  - only some features will be matched (the target image may have more features, or the instance in the target image may be occluded)
- then we use the joining vectors to predict the position of the baricentre
  - if many of the matches predict the baricentre in the same position, then i can conclude that i have an instance of the object
  - if the joining vectors cannot agree on a coherent position of the baricentre, then the object isn't there
- to see if the joining vectors agree we use an **accumulator array**
  - an array with the same shape of the image, where every pixel position is a bin where each feature can vote when it check where its joining vector ends up
  - c'è un po' di tolleranza, così le feature non devono proprio concordare con pixel precision sulla posizione del baricentro

- **NB**: devo fare il tuning di una soglia minima del numero minimo di joining vector coerenti per poter affermare di aver trovato un'istanza del mio oggetto

**La formulazione sopra non funziona però se nella target image abbiamo rotation and scale changes**

- dobbiamo ruotare e scalare i joining vectore nella target image utilizzando
  - le canonical orientation delle feature trovate
    - se nella template image la feature ha una canonical orientation di 30°, mentre il suo match nella target image ha una canonical orientation di 60°, allora è possibile che l'oggetto sia stato ruotato di 30°
    - in questo caso, ruoto il joining vector di quella feature della differenza tra le due canonical orientation, cioè 30°
  - le scale delle feature trovate
    - discorso simile per le scale; se conosco le scala di una feature nel template e nel target
    - allora so di quanto dovrò scalare il joining vector

2d accumulator array non va bene dato che accumula nello stesso bin voti provenienti da rotazioni/scale scale

- però è comodo computazionalmente (e good enough in molti casi) e quindi si gestisce con un RANSAC approach

alternativa può essere 4d accumulator array

**Interessante notare che lo star model può essere utilizzato anche per filtrare wrong correspondences** (even after lowe's ration)

- scarto i match che non hanno un joining vector che finisce nel baricentro concordato dalla maggioranza (main peak of the accumulator array)
- **star model filters out wrong matches because they won't accumulate coherently in the accumulator array**
