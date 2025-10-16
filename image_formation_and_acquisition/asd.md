now we know how image formation works

our model has a lot of parameters, if we don't know them we can't do anything

camera calibration's purpose is to get to know these parameters

this is a complex process

- with opencv we calla function and camera calibration is done
- the goal of this chapter is to see what's under the hood

# Camera calibration

what all camera calibration methodologies have in common is that:

- what is know is correspondences between 3d coordinates and pixel coordinates (M and m)
- what is not know is the parameters of the camera (P)
- we use correspondences to estimate camera parameters (stesso discorso fatto prima nel pacchetto precedente)
  - ricorda che m~ = P~ * M~

To obtain the required correspondences specific physical objects (referred to as calibration targets) providing easily detectable image features (such as, e.g., chessboard or dot
patterns) are typically deployed.

Di quante immagini abbiamo bisogno?

- minimo 3 (capiremo perchè)
- tipicamente 15/20
- indichiamo con n il numero di immagini

Di quante corrispondenze abbiamo bisogno?

- P è una matrice 3x4 in projective space
- 11 parametri
- abbiamo bisogno quindi di un sistema di almeno 11 corrispondenze
- in pratica più ne abbiamo meglio è

Che immagine usiamo?

- una con una scacchiera
- con m (internal) corners

in Zhang's method we use a planar pattern because in this way perspective projection boils down to a simpler transformation called homography

to have an homography we need to choose carefully the WRF

- asse z perpendicolare al piano
- origine sul piano
- asse x e asse y asimmetrici per evitare ambiguità (numero di quadrati neri diversi)

the control points are the internal corners (non cosideriamo gli angoli sul bordo della scacchiera)

siccome, costruiamo noi la scacchiera:

- sappiamo la dimensione dei quadrati (i.e 1cm)
- e quindi **sappiamo la posizione dei control points nella scacchiera**

Ora come facciamo a sapere le relativa coordinate nell'immagine dei control plane?

- esiste un semplice algoritmo di image processing che riesce a rilevare i corner nell'immagine

Quando sccattiamo le immagini di calibrazione, la camera è fissa mentre muoviamo l'immagine di calibrazione

- abbiamo quindi un WRF per immagine
- e quindi una matrice di extrinsic parameters per immagine

Le cose più importanti sono

- lens distorsion parameters
- instrinsic parameters
- zhang ci da proprio questo

# Estimating H

Per ogni internal corner ho un equazione che mi mette in relazione le coordinate 3d con quelle 2d

- per ogni internal corner abbiamo quindi
  - 3 equazioni (una per ogni riga)
  - con 9 unknown (8 really dato che siamo in projective space)
  - since we have a lot of internal corners (m=64 tipically) we have an overconstrained linear system of equation which can be solved with linear algebra

### comincia una parte incasinata [9:50]

we have a little problem, we have a k which can be an arbitrary value. We would like to get rid of the k to get a

km~ = Hw~ sono matrici 3x1

- considerandole in euclidean space abbiamo ky = x
- due vettori paralleli
- il loro prodotto vettoriale e quindi 0
- possiamo eliminare k

consideriamo le righe dell'omografia come vettori colonna trasposti

**come si computa il prodotto vettoriale?** Usiamo la tecnica della matrice [9:58]

...

questo è il DLT algorythm, one of the most popular methods to estimate H given correspondences

A questo punto, per ogni internal corner otteniamo 3 equazioni in 9 unknowns

Notiamo però che alcune righe non sono linearmente indipendenti (?)

Considerando tutte gli internal corners, otteniamo un sistema di 2m equazioni in 9 incognite

- questo sistema non ha una soluzione esatta
- utilizziamo un least squared approach

It would also be possible to solve the system exactly but we would need to use the least number of correspondences (4)

- this is solution is not robust to noisy measurements
- when there is noise a better solution is to use more measurements than strictly necessary and use a least square estimation

Where is the noise coming from

- our measurements are the wrf and image coordinates of the internal corners
- our printed chessboard is not perfect (some squares maybe bigger than others)
- our image coordinates are subject to noise aswell since pixel intensity is noisy, di conseguenza anche il corner detection algorythm is noisy

### Estimating H by SVD

A = matrice rettangolare 2m*9

significa:

“Trova il valore di
𝐻 (una matrice o vettore) che minimizza la somma dei quadrati degli errori”.

👉 Quindi argmin restituisce il valore di
𝐻 che rende minima la funzione, non l’indice dell’errore minimo.

# Non-linear Refinement

with the DLT algorythm we estimate one homograpyh per calibration image

con ogni immagine minimizziamo la norma di ||A * h||

- questo vettore non ha un'interpretazione immediata
- viene detto algebraic error

Quello che vogliamo è ottenere una buona stima dell'omografia

- dato un punto 3d, applicando l'omografia vogliamo ottnere un punto 2d molto vicino a quello 2d corrispondente

Ma minimizzando A*h stiamo minimizzanso qualcosa che non sembra correlato

minimzzando l'errore algebrico non otteniamo una buona omografia

piuttosto vogliamo minimizzare la norma del vettore distanza tra corner nell'immagine e corner nell'immagine ottenuto da H*w, per tutti i corner

**why don't we do this directly?**

- why do we do first linearly estimate the homography
- and only after the obtaing a first rough homography, we can apply a refinement that more closely matches our intuiton of calibration
- because the cost function is not convex, we have many bad local minimums that we may and up in if we start from an unlucky starting point
- the first estimation gives us a good starting point that allows to reach a global optimum (?) with the refinement

we minimize the error with an algorythm that is mix between gradient descent and newton something

### Estimating the intrinsic parameters [di nuovo crazy 11:00]

Now we have estimated homographies, but our goal was estimating intrinsic parameters. Those homographies allow use to do that

...

exploiting the properties of the rotation matrix, we come up with 2 equations that factor out the extrinsic parameters

knowing B is the same as knowing A (c'è una formula); so its all about estimating B

studiando parametri e unknowns di B otteniamo che abbiamo bisogno di almeno 3 calibration images

- nuovamente, ne usiamo 20 per essere più robusti al rumore con un least square approach

slide 14 non richiesta

### Estimating the extrinsic parameters

once we have estimated the homographies and the intrinsic parameters, we can estimated the (many) extrinsic parameters (one for every calibration image)

### Lens distorsion casino [11:30]

...

we would like to have undistorted continuos image coordinates but what we have are distorted pixel coordinates

...

per approssimare le undistorted pixel coordinates utilizziamo le homographies ottenute prima
