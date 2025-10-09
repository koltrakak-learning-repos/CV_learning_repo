Abbiamo visto che nel nostro camera model la trasformazione da coordinate 3d a 2d avviene con una PPM
- questa può essere utilizzata come una singola 3x4 matrix
- oppure può essere fattorizzata in un prodotto tra 3 matrici

Ci sono anche dei casi in cui la PPM può essere semplificata in una matrice 3x3, ovvero una trasformazione chiamata Homography

Questi casi NON sono rari

casi:
- all the points we're imaging are on a plane (same depth)
    - for our convenience, we choose the origin of the WRF within the plane
    - we also choose the z axis of the WRF to be perpendicular to the plane
    - le coordinata z è sempre 0! 
    - le coordinate nel WRF diventano bidimensionali!
    - la terza colonna della PPM può essere eliminata dato che verrebbe sempre moltiplicata per 0!
    - this resulting matrix is called homography H
    
Homographies are a mapping between projective space planes
- We are mapping all the points in the scene plane to the points in the image plane

How many Parameters define an homography
- apparently 9 since it's a 3x3 matrix
- we have to remember that we are in projective space so the transformation are equivalent up to a scale factor
- that in turn means that we only need 8 parameters to define an homography and we can assume the 9th parameter to be 1


**NB**: an homography can be used to map the pixels of an image to the pixels of another image of the same scene but from a different viewpoint
- if i know the homography i can produce the image of a different viewpoint
- mapping between planes


# Homographies
Nelle omografie, il trucco sta sempre nel scegliere il WRF in maniera conveniente

CASO 1
... dalle slide è chiaro cosa succede, ma sono confuso sull'utilizzo di sta roba

a quanto pare è roba preliminare


CASO 2
- la scena non è più un piano
- camera rotates about the optical centre
- scegliamo il WRF coincidente con il CRF
    - non c'è la terza matrice G
    - la rotation matrix è un'identità
    - **NB**: nella slide utilizziamo la notazione in cui non c'è la matrice identità (vedi slide 15)
- nel secondo viewpoint abbiamo ruotato la camera e quindi abbiamo una matrice di rotazione R
- l'inversa di un prodotto tra matrici equivale al prodotto delle inverse
- di nuovo abbiamo una omografia

CASO 3
- scena qualunque
- WRF = CRF
- Adesso la seconda immagine è come se fosse stata fatta da un altra camera (con parametri diversi) nella stessa posizione
    - cambia solo la matrice dei parametri intrinseci A
    - impossibile fisicamente, ma possibile virtualmente. Questa possibilità è di interesse pratico
- di nuovo abbiamo una omografia

CASO 4
- scena qualunque
- WRF = CRF
- adesso facciamo le due trasformazioni descritte nel caso 2 e 3

we'll see later why we care about homographies

### Estimating homographies
Quanto descritto sopra, sembra indicare che possiamo calcolare esattamente le omografie

le omografie possono essere solo stimate e non calcolate esattamente dato che non riusciamo a conoscere esattamente la rotazione e la traslazione della camera rispetto al WRF



# Modeling lens distorsion
the model we have derived so far doesn't explain some phenomenomes like lens distorsion

in perspective projection we lose parallelism but lines stay lines

perspective projection works with the pinhole camera

we've seen that we need lenses to gather enough light, but with the thin lense model perspective projection still works

tuttavia, le lenti reali non sono thin e introducono una distorsione (non lineare) che rende invalido il modello di perspective projection

we need a model to warp distorted images to undistorted ones that can be explained with perspective projection

...

radial distorsion depends on the 3d shape of a lense

tangential distorsion depends on misalignment of the lense wrt the image plane


**Model**
L(r) models radial distorsion

dx, dy modella tangential distorsion

this model maps distorted 2d image coordinates to undistorted ones
- **NB**: qua abbiamo detto image coordinates deliberatamente, NON pixel coordinates. Questo modello opera prima della digitalizzazione

the center of distorsion is the point where radial distorsion = 0
- radial distorsion gets amplified the farther away we are from the center of distorsion



- L(r)
    - c'è un 1 dato che at the center of distorsione there's no distorsion
    - we seem to miss the odd terms of the taylor series expansion, questo perchè L(r) è una funzione pari (L(r) = L(-r))
    - di solito si arriva fino a k2/k3 come termini della serie
    - anche qua i parametri k vanno stiamati

Considerazione sul processo di estimation:
- at parameter estimation time:
    - we're trying to develop a model that given some inputs gives us some outputs
    - but we don't know the correct parameters of the model
    - to estimate them we need to have the corresponding outputs of a given input
- once we've estimated the parameters:
    - we can use the model to predict the output of a given input


- dx, dy
    - due parametri per stimare la tangential distorsion: p1, p2


### When does lens distorsion come into play in the image formation process?










