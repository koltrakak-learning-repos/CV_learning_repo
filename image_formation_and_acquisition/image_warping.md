# warping

A warping is an image processing operation defined by two transformations (functions)

- one for the horizontal pixel coordinate, one for the vertical
- u' = f_u(u, v)
- v' = f_v(u, v)

**A warping transforms only pixel coordinates of the image, not intensity or colors**

Esempi di warping:

- removal of lense distortion
- removal of perspective deformation
- stereo rectification
- rotation

they are in fact transformations between pixel coordinates (guarda le formule)

## Forward/Backward mapping

A warping could be defined in two ways

**Forward mapping**: a transformation from the source image to the target image

- source = old image
- target = new/warped image
- for example wrt lense distortion where we want to undistort an image:
  - the source would be the distorted image
  - the target the undistorted image

**NB**: The **warping outputs real values** as coordinates since the transformations at play are stuff like: rotation matrixes, homographies, ...

- this means that in the target we get a real value coordinate **in between four pixel coordinates**
- we need to approximate

We have two problems with forward mapping whatever approximation approach we choose:

- we cannot be sure that all pixels in the output image are gonna be "hit" (be the target of the transformation)
- also some pixels are gonna be hit multiple times

These problems are called **holes and folds** and are caused by il bisogno di dover fare un'approssimazione

**To solve this problem we need to do the warping backwards**:

- invece di scandire la source image e applicare la funzione di warping forward
- scandiamo le coordinate della target image e applichiamo la funzione di warping backward per capire dove finiamo nella source image
  - utilizziamo sempre le stesse formule, ma cambia cosa scandiamo
    - nota che se non ci fosse approssimazione, non ci sarebbe differenza
  - this way we can be sure that we're assigning a value to every pixel in the target (no holes)
  - this avoids holes and folds because every pixel in the target image is gonna have by construction a corresponding pixel in the input image

**NB**: che possiamo fare i warping backward dato che le coordinate delle target image sono note anche se i valori dei suoi pixel non lo sono

**NB**: We define warping as a transformation from the new coordinate to the old one

- questo spiega perchè le formule di lense distortion, rectification, ... sembravano avere senso opposto
- era giusto per ricordare il fatto che facciamo i warping backward

## Mapping strategies

Anche con backward mapping, ho comunque il problema delle coordinate reali dato che il warping mi tira fuori coordinate di questo tipo

Stavolta, devo scegliere tra quattro pixel della SOURCE IMAGE quello che voglio usare per il mio warping

Stavolta però **conosco l'intensità dei pixel tra cui devo scegliere** -> **posso fare interpolazione delle intensità**

- con forward mapping: il colore era settato e dovevo decidere quale tra quattro destinazioni scegliere (holes and folds)
- con backward mapping: la destinazione è settata e devo decidere come interpolare quattro colori dalla sorgente

**Keypoint**: posso fare interpolazione solo con backward mapping! Altrimenti non avrei valori da interpolare

Posso fare vari tipi di interpolazione:

- bilinear interpolation: peso di più i pixel più vicini a dove sono caduto

PS: non farti confondere dall'esempio finale su lense distortion, quella è la formula con le pixel coordinates invece che con le continuous image coordinates
