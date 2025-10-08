# Reminder
le coordinate del 3d point sono (x,y,z)

le coordinate 2d dell'image point sono (u, v)

queste coordinate sono sensate solo dentro a dei sistemi di riferimento
- gli assi di entrambi devono avere verso congruente
- camera reference frame is the 3d one
    - it's called camera reference frame because it's linked to the camera
- image reference frame is the 2d one
    - origine al centro dell'immagine

perspective projection ci da un modo per mappare punti 3d in 2d
- le formule sono **NON lineari**

we don't like this model too much

to have a better model ... we need to switch from eucledian spaces to projective spaces

# Projective spaces
a limitation of eucledian spaces is that there is **no way to represent and handle points at infinity**.

This is not the case with projective spaces

**Homogeneous coordinates**
- possiamo usare un vettore colonna e uno scalare per rappresentare un punto in projective space
- lo spazio che otteniamo con queste coordinate è un Projective space
    - un punto in questo spazio è rappresentato da una classe di quadruple che differiscono solo per un termine moltiplicativo
- possiamo mappare qualsiasi punto in Rn in Pn, e viceversa, facilmente
    - basta aggiungere un 1 in fondo al vettore colonna e moltiplica questo vettore per lo scalare k
    - per tornare in uno spazio euclideo mi basta dividere le prime n coordinate per l'ultima (n+1-esima) coordinata

### Point at infinity of a 3d line
we represent a line in 3d space with the **parametric equation of a 3d line**.
- M0: vettore, usato come base, che rappresenta un punto qualsiasi sulla linea
- M: è un punto a caso sulla linea (anche questo è un vettore)
- D: è la differenza tra M e M0 (anche questo un vettore)
- lambda*D: per ottenere M dobbiamo sommare a M0, il vettore D scalato per lambda 

Passiamo a projective space e indichiamo con M~ la versione in projective space

We would like to represent the point at infinity of this line
- this is a limit with lamda -> inf

**Points at infinity in projective spaces are the points with the last coordinate equal to zero**
- le altre coordinate sono quelle di D che rappresentano la linea 3D in considerazione

per ottenere il punto ad infinito di una linea 3d in projective space, basta prendere le coordinate 3d della linea e aggiungere 0 come quarto elemento
- questi punti NON possono essere rappresentati in Euclidean space!

Abbiomo quindi che punti in projective space:
- con quarta coordinata == 0 -> non hanno un corrispondente in Eucledian space
- con quarta coordinata != 0 -> hanno un corrispondente in Eucledian space
- Projective spaces allow us to handel both point homogeneously

In projective space we have ininitely many points at inifinity
- uno per le infinite direzioni che le linee possono avere

Point (0, 0, 0, 0) is undefined.
- indeed, the above point is NOT the origin of the Euclidean Space (0, 0, 0), for such point is represented in homogeneous coordinates as (0, 0, 0, k), k≠0.

### Why do we care about projective spaces?
if we model perspective projection as a mapping between P3 and P2, **this mapping becomes linear!!** (unlike Eucledian space)
- (it is easier to solve linear systems than non-linear ones)

... per capire come è più facile guardare dalle slide

(vectors are notated in bold)

Oss:
- a camera is the thing that turns 3d coordinates into 2d coordinates following the rules of perspective projection. 
- The matrix we get by applying perspective projection in the projective space does this as well.
- **The matrix describes the camera!** (ha come parametro proprio f)

considera sempre nell'equazione lo scalare k che non fa cambiare niente
- se scalo tutto di k in projective space continuo a descrivere lo stesso punto

### vanishing point
With projective coordinates and with the matrix, now we can represent the 2d coordinates of the vanishing point
- mi basta moltiplicare la matrice (trasformazione che mi applica perspective projection ad un punto) per il punto a infinito (che abbiamo detto essere il vettore che rappresenta la retta con uno zero in fondo come quarta coordinata) ottenendo così le coordinate 2d del vanishing point in projective space
- per ottenere le coordinata 2d del vanishing point in spazio euclideo mi basta di nuovo dividere tutto per l'ultima coordinata

Casi speciali:
- il vanishing point of the lines parallel to the optical axes is the centre of the image
    - moltiplica la matrice per il vettore dirizione [0, 0, 1] delle linee perpendicolari all'optical axis
- if the 3d line is perpendicular to the optical axis, the vanishing point is at infinity (indescrivibile in R2)
    - come prima, ma stavolta il vettore direzione è [a, b, 0] in quanto parallelo all'optical axis z

### PPM
Matrix represents the geometric camera model and is known as Perspective Projection Matrix (PPM).
- If we assume distances to be measured in focal lenght units (f = 1), the PPM becomes una matrice identità orlata con una colonna di zeri
- questa è la standard/canonical PPM

questa forma canonica della ppm ci dimostra l'essenza della perspective projection
- [x,y,z,1] moltiplicato per la PPM canonica diventa [x,y,z], che in coordinate cartesiane equivale a [x/z, y/z]
- this is what perspective projection does, it scales objects down the farther they are from the camera
- a specific camera introduces other parameters (focal length)

This standard form in convenient because it standardizes perspective projection



# a more comprhensive camera model
with projective coordinates we have gained:
- linear equations to apply perspective projection 
    - by going through projective space and doing a matmul with the PPM
- being able to compute vanishing points
    - moltiplico la PPM con il vettore della mia linea 3d con uno zero in fondo
    
What are we still lacking with this model?
- as it is now, this model is useless
    - there is no way to compute 3d coordinates because the camera reference frame is an abstraction
    - we can measure 3d coordinats in a reference frame that is convenient to us (world reference frame)
    - but world reference frame coordinates are invalid for perspective projection because this model assumes CRF coordinates
    - we need a way to transform coordinates from WRF to CRF -> rototranslation
- otteniamo coordinate 2d continue
    - ma noi abbiamo solo pixel coordinates (discrete)
    - dobbiamo tenere conto della digitalizzazione dell'immagine

We need to incorporate in the ppm 2 things
- rototranslation from the world reference frame (wrf)
- image digitization

### image digitization
questo è facile, basta dividere le coordinate orizzontali e verticali dell'immagine per la dimensione del pixel
- basta dividere per delta_u e dalta_v (quantizzazione)

e traslare il tutto per avere come origine l'angolo in alto a sinistra dell'immagine
- sommo il vettore dall'angolo fino al centro con il vettore dal centro fino al punto (u0, v0) per ottenere il vettore delle pixel coordinates

**Intrinsic Parameter Matrix**
Modifichiamo la PPM inserendo i 4 parametri per tenere conto della digitalizzazione
- posso anche rappresentare il tutto come prodotto tra due matrici A * [I|0]
- Matrix A, which models the characteristics of the image sensing device, is called Intrinsic Parameter Matrix (or Camera Matrix).

Otteniamo quindi che per ottenere le coordinate digitized di un punto 3d nel CRF, dobbiamo fare: k * m~ = A * [I|0]M~

Possiamo pensare al processo come 2 trasformazioni separate: una per ottenere le image coordinates continue, e l'altra per digitalizzare quest'ultime
- abbiamo 4 parametri che definiscono una camera (intrinsic parameter matrix)
    - alpha_u = f/delta_u = focal length measured in horizontal pixel sizes
    - alpha_v = ...
    - u0 e v0

### rigid motion between CRF and WRF
3D coordinates are measured into a World Reference Frame (WRF) external to the camera. The WRF will be related to the CRF by:
- A rotation around the optical centre (e,g. expressed by a 3x3 rotation matrix R)
- A translation (expressed by a 3x1 translation vector T)

Indichiamo con M le coordinate 3d nel CRF e con W le coordinate nel WRF

La rototranslation che dobbiamo fare ha quindi questa forma: M = RW + T

Se esprimiamo il tutto in coordinate omogenee otteniamo M = G*W 
- dove G è una matrice 4x4 che include R e T

Matrix G, which encodes the position and orientation of the camera with respect to the WRF, is called **Extrinsic Parameter Matrix**

Aggiungiamo quindi questa terza matrice a quelle già descritte arrivando ad ottenere la **forma generale per la PPM**
- PPM~ = A[I|0]G

As a rotation matrix (3x3=9 entries) has indeed only 3 independent parameters (DOF), which correspond to the rotation angles around the axis of the RF, the total number of extrinsic parameter is 6 (3 translation parameters, 3 rotation parameters).

Hence, the general form of the PPM can be thought of as encoding:
- the position of the camera wrt the world into G
- the perspective projection carried out by a pinhole camera into the canonical PPM [ I | 0 ] and,
- the actual characteristics of the camera into A.

# conclusioni
questo modello non serve tanto a fare image analysis (es. classificazione). 

Piuttosto serve in tutte le applicazioni che devono elaborare informazioni del mondo 3d a partire da un'immagine. 
- fondamentale ad esempio in robotica














