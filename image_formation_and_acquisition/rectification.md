
# Rectification

con la calibrazione fatta sopra otteniamo una rototranslation

ricordiamo però che il stereo correspondence problem diventa molto più facile se tra le due camere c'è solo una traslazione (cerchiamo su una linea retta)

Ma adesso dobbiamo anche tenere conto della digitalizzazione dell'immagine (matrice dei parametri intrinseci)

Queste camere non esistono, le creiamo virtualmente by rectification modificando le PPM delle due camere

- in questa maniera trasformiamo le due immagini come se fossero state prese da una configurazione stereo standard

Quello che vogliamo fare è:

- rendere le due matrici di intrinseci uguali
- ruotare le camere about the optical centre so that gli assi y e z sono paralleli e l'asse x attraversa i loro optical centre
  - (in questo modo la traslazione è solo along the x-axis)

**NB**: la trasformazione che mi porta dall'immagine di partenza a quella rettificata è un omografia (le due trasformazioni sono due casi di omografia)

- questo significa che rettificare significa computare due omografie

Oss: le immagini che stiamo rettificando sono già state undistorted

### The new PPMs

...

rotazion è crazy [15:30]

le righe di una matrice di rotazione sono gli unit vectors che rappresentano i nuovi asse con coordinate relative ai vecchi assi

the new x axis is gonna be the line between Cl and Cr

- this way the translation between the two cameras is gonna be only among this new x-axis (b = Cr - Cl(=0))

...

because R is a rotation matrix its inverse is the same as its transpose

the direction of the y axis has a degree of freedom as long as its perpendicular to the new x axis

- a sensible choice is to choose the new y-axis to be perpendicular to both the new x-axis and the old z-axis

r3, the new z-axis, is given by the vector product of the new x and y axis

### computing the homography

...

(nella seconda omografia ml' dovrebbe essere mr')

Nota: una volta calibrata la stereo camera abbiamo tutto il necessario per calcolare queste omografie (R, T, and old A)

**NB**: noi vogliamo andare da unrectified verso rectified; la formula che abbiamo ottenuto sembra però andare nel verso opposto. Possiamo sempre invertire tutto, ma vedremo che in realtà noi vogliamo proprio così la nostra trasformazione (centra con il concetto di warping)

# From pixels to 3d coordinates

considero una depth image

...

rgb-d camera sono una combo tra una depth camera (e.g. time of flight camera) e una color camera in maniera tale da ottenere una colored pointcloud
