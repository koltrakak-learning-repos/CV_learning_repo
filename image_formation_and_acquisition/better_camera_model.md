le coordinate 3d del 3d point sono (x,y,z)

le coordinate 2d dell'image point sono (u, v)

ricorda poi la formule della perspective projection

queste coordinate sono sensate solo dentro a dei sistemi di riferimento
- gli assi di entrambi devono avere verso congruente
- camera reference frame is the 3d one
    - it's called camera reference frame because it's linked to the camera
- image reference frame is the 2d one
    - origine al centro dell'immagine

we don't like this model too much

to better model ... we need to switch from eucledian spaces to projective spaces


# Projective spaces
a limitation of eucledian spaces is that there is no way to represent and handle points at infinity. This is not the case with projective spaces
- this is not the main reason we use this kind of space

...

Homogeneous coordinates
- possiamo usare un vettore colonna e uno scalare per rappresentare un punto in projective space
- lo spazio che otteniamo con queste coordinate è un Projective space
- possiamo mappare qualsiasi punto in Rn in Pn, e viceversa, facilmente
    - basta aggiungere un 1 in fondo al vettore colonna e moltiplica questo vettore per lo scalare k
    - per tornare in uno spazio euclideo mi basta dividere le prime n coordinate per l'ultima (n+1-esima) coordinata

### Point at infinity of a 3d line
we represent a line in 3d space with the **parametric equation of a 3d line**.
- M0: vettore che rappresenta un punto qualsiasi sulla linea che usiamo come base
- M: è un punto a caso sulla linea
- lambda*D: per ottenere M dobbiamo sommare a M0, il vettore D scalato per lambda 
    - le coordinate di D si ottengono con trigonometria

Passiamo a projective space e indichiamo con M~ la versione in projective space

We would like to represent the point at infinity of this line
- this is a limit with lamda -> inf

**Points at infinity in projective spaces are the points with the last coordinate equal to zero**

Here we have ininitely many points at inifinity
- uno per le infinite direzioni che le linee possono avere



### Why do we care about projective spaces?
if we model perspective projection as a mapping between P3 and P2, **this mapping becomes linear!!** (unlike Eucledian space)
- it is easier to solve linear systems

(vectors are notated in bold)

...


a camera is the thing that turns 3d coordinates into 2d coordinates. The matrix does this as well. **The matrix describes the camera!** (ha come parametro proprio f)

considera sempre nell'equazione lo scalare k che non fa cambiare niente
- se scalo tutto di k in projective space continuo a descrivere lo stesso punto


### vanishing point
With projective spaces and with the matrix, now we can represent the vanishing point
- mi basta moltiplicare la matrice per il punto a infinito (che abbiamo detto essere la direzione con uno zero in fondo)
- per tornare in spazio euclideo mi basta di nuovo dividere tutto per l'ultima coordinata

casi speciali
- il vanishing point of the lines parallel to the optical axes is the centre of the image
- if the 3d line is perpendicular to the optical axis, the vanishing point is at infinity
    - indescrivibile in R2

Interessante: il vanishing point serve a capire l'orientamento della camera


### PPM
...

questa forma canonica della ppm ci dimostra l'essenza della perspective projection
- [x,y,z,1] diventa [x/z, y/z]
- this is what perspective projection does, it scales objects down the farther they are from the camera
- a specific camera introduces other parameters (focal lenght)

This standard form in convenient because it standardizes perspective projection

# a more comprhensive camera model

we have gained
- linear equations
- being able to compute vanishing points

What are we still lacking with this model?
- as it is now, this model is useless
    - there is no way to compute 3d coordinates because the camera reference frame is an abstraction
    - we can measure 3d coordinats in a reference frame that is convinient to us (world reference frame)
    - but with the world reference frma is invalid with perspective projection 
    - we need a way to transform coordinates from a reference frame to the other
- otteniamo coordinate 2d continue
    - ma noi abbiamo solo pixel coordinates (discrete)
    - dobbiamo tenere conto della digitalizzazione dell'immagine

we need to incorporate in the ppm 2 things
- rototranslation from the world reference frame (wrf)
- image digitization

### image digitization
basta dividere per delta_u e dalta_v (quantizzazione)

e traslare il tutto per avere come origine l'angolo in alto a sinistra dell'immagine
- sommo il vettore dall'angolo fino al centro con il vettore dal centro fino al punto (u0, v0) per ottenere il vettore delle pixel coordinates

Modifichiamo la ppm inserendo i 4 parametri per tenere conto della digitalizzazione
- posso anche rappresentare il tutto come prodotto tra due matrici
- possiamo pensare al processo come 2 trasformazioni separate: una per ottenere le image coordinates continue, e l'altra per digitalizzare quest'ultime
- abbiamo 4 parametri che definiscono una camera (intrinsic parameter matrix)
    - alpha_u = f/delta_u = focal length measured in horizontal pixel sizes
    - alpha_v = ...

### rigid motion between CRF and WRF
Dobbiamo fare una rototraslation

M = RW + T
- R = matrice di rotazione
- T = vettore di traslazione
















