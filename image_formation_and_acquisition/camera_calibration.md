now we know how image formation works

our model has a lot of parameters, if we don't know them we can't do anything

camera calibration's purpose is to get to know these parameters

this is a complex process

- with opencv we calla function and camera calibration is done
- the goal of this chapter is to see what's under the hood

# Camera calibration

In camera calibration we try to estimate all the parameters of the image formation model

- intrinsic parameters
- extrinsic parameters
- lens distorsion parameters

based on a set of 3d-2d correspondences

What all camera calibration methodologies have in common is that:

- what is know is correspondences between 3d coordinates and pixel coordinates (M and m)
- what is not know is the parameters of the camera (P)
- we use correspondences to estimate camera parameters (stesso discorso fatto prima nel pacchetto precedente)
  - ricorda che m~ = P~ * M~

To obtain the required correspondences specific physical objects (referred to as calibration targets) providing easily detectable image features (such as, e.g., chessboard or dot patterns) are typically deployed.

Di quante immagini abbiamo bisogno?

- minimo 3 (capiremo perchè)
- tipicamente 15/20
- indichiamo con n il numero di immagini

Di quante corrispondenze abbiamo bisogno?

- P è una matrice 3x4 in projective space
- 11 parametri
- abbiamo bisogno quindi di un sistema di almeno 11 corrispondenze dato che ogni corrispondenza ci da un'equazione
- in pratica più ne abbiamo meglio è

Che immagine usiamo?

- una con una scacchiera
- con m (internal) corners

In Zhang's method we use a planar pattern because in this way perspective projection boils down to a simpler transformation called homography

to have an homography we need to choose carefully the WRF

- asse z perpendicolare al piano
- origine sul piano
- asse x e asse y asimmetrici per evitare ambiguità (numero di quadrati neri diversi)

the control points are the internal corners (non cosideriamo gli angoli sul bordo della scacchiera)

Siccome, costruiamo noi la scacchiera:

- sappiamo la dimensione dei quadrati (i.e 1cm)
- e quindi **sappiamo la posizione dei control points nella scacchiera**

Ora come facciamo a sapere le relativa coordinate nell'immagine dei control plane?

- esiste un semplice algoritmo di image processing che riesce a rilevare i corner nell'immagine

Quando sccattiamo le immagini di calibrazione, la camera è fissa mentre muoviamo l'immagine di calibrazione

- abbiamo quindi un WRF per immagine
- e quindi una matrice di extrinsic parameters per immagine

# Estimating H

Per ogni internal corner ho un equazione che mi mette in relazione le coordinate 3d con quelle 2d

- Per ogni internal corner abbiamo quindi 3 equazioni (una per ogni riga)
- con 9 unknown (8 really dato che siamo in projective space)

**NB**: since we have a lot of internal corners (m=64 tipically) we have an **overconstrained linear system**  of equations

- this can be solved with linear algebra although not always exactly since overconstrained linear systems are likely to contain contradicting constrains
- we can always approximate a solution that minimizes the error with something like a least square approach and SVD (vedi dopo)

**We have a little problem**
we have a k which can be an arbitrary (non-zero) value. We would like to get rid of the k to get a simple solution to our system

How to get rid of k

- km~ = Hw~ sono vettori 3x1 in P^2 uguali (ricorda che l'uguaglianza vale anche up to scale in projective space)
- **consideriamo questi vettori 3x1 come se fossero in euclidean space**
- abbiamo ky = x (con y = m~ e x = Hw~); due **vettori paralleli**
- il loro prodotto vettoriale e quindi 0
- possiamo allora considerare m~ e Hw~ due vettori paralleli in spazio euclideo e impostare un equazione più comoda per ottenere l'omografia H: `m~ x Hw~ = 0`

A questo punto ci basta espandere il prodotto vettoriale per ottenere un sistema di equazioni per le incognite dell'omografia:

- **come si computa il prodotto vettoriale?** Usiamo la "matrix form"
  - consideriamo le righe dell'omografia come vettori colonna trasposti

La tecnica che abbiamo utilizzato che elimina la k trasformando l'equazione iniziale in quella con il prodotto vettoriale prende il nome di DLT algorythm

- Direct Linear Transformation
- one of the most popular methods to estimate H given correspondences

Possiamo riscrivere la nostra equazione come Ah = 0

- dove A è una matrice 9x9 di termini noti
- h è una matrice 9x1 di incognite dell'omografia

Otteniamo un sistema di 3 equazioni in 9 unknowns; e ne abbiamo uno per ogni corrispondenza (m)

- abbiamo poi la stessa cosa in ogni calibration image (un omografia per calibration image)
  - qua ci siamo concentrati su una calibration image e la sua omografia
  - nello stimare l'omografia delle altre calibration images dovremo ripetere i passaggi

Notiamo che alcune righe non sono linearmente indipendenti (guarda la prima forma non quella Ah = 0)

Considerando tutte gli internal corners, otteniamo un sistema di 2m equazioni in 9 incognite

- A diventa una matrice 2m * 9
- questo sistema non ha una soluzione esatta in quanto overconstrained
  - non si riesce a trovare 9 numeri che soddisfano tutti vincoli
- utilizziamo un least squared approach
  - troviamo un vettore h* che minimizza l'errore
  - più rigorosamente, vogliamo trovare un vettore h*: argmin || Ah* ||
    - argmin means: the argument that minimizes the function that follows
    - la soluzione perfetta h, produrrebbe un Ah = 0
    - siccome questa soluzione non esiste, ci accontentiamo di una soluzione h \*che minimizza la norma di Ah*
  - la norma di Ah* is called **algebraic error**

**OSS**: It would also be possible to solve the system exactly but we would need to use the least number of correspondences (4, 2 equazioni per corrispondenza per le 8 incognite di H)

- this is solution is not robust to noisy measurements
- when there is noise a better solution is to use more measurements than strictly necessary and use a least square estimation

**Where is the noise coming from?**

- our measurements are the wrf and image coordinates of the internal corners
- our printed chessboard is not perfect (some squares maybe bigger than others), this means that our wrf coordinates are noisy
- our image coordinates are subject to noise aswell since pixel intensity is noisy, di conseguenza anche il corner detection algorythm is noisy

```
Una soluzione in forma chiusa significa che:

si può esprimere la soluzione esplicitamente con un insieme finito di operazioni matematiche “note” (addizione, moltiplicazione, divisione, radici, funzioni standard, ecc.), senza bisogno di iterazioni o approssimazioni numeriche.

In altre parole, hai una formula diretta per la soluzione, non un algoritmo iterativo che la calcola approssimando.
```

**Come troviamo il vettore h\*?**
finding a solution to an overconstrained system of linear equations that minimizes the error is a standard problem in linear algebra and is solved with the SVD method

- Singular Value Decomposition
- la soluzione è l'ultima colonna della matrice V
- non penso mi interessi più di tanto

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

# Stereo camera calibration

to calibrate a stereo camera, a naive approach could be to calibrate the two of them independently with zhang.

- this way we get the intrinsic, extrinsic and lens distortion parameters for the two cameras
- but, we don't get the rototranslation between the two cameras, or better CRF!
- this is a key piece of information that we need to get depth information from disparity of corresponding points
  - we also need the rototranslation to find correspondences (remember epipolar lines)

we can leverage

if show to both cameras at least one calibration image

gli extrinsic parameters trasformano da WRF a CRF

se mostriamo la stessa immagine ad entrambe le camere abbiamo che la matrice dei parametri esterni ... [è più facile guardare la registrazione]

- Pl = Gl Pw
- Pr = Gr Pw
- Gr Gl^-1 = Grl è la rototranslation che mi trasforma coordinate from the left to the right

teoricamente basta mostrare una singola immagine, ma non c'è nessun motivo per cui non debba mostrare ad entrambe tutte le immagini di calibrazione

se mostro tutte le immagini di calibrazione (n)

- ottengo una rototranslation per ogni immagine
- posso farne la media per essere più robusto wrt noise
- buona idea, purtroppo non posso fare una semplice media aritmetica tra rotation matrixes ed ottnere un'altra rotation matrix

Come definiamo la mediana in un insieme di vettori?

- il vettore che ha la distanza minore rispetto a tutti gli altri

come definiamo la mediana in un insieme di rotation matrixes?

- si trasformano le matrici in vettori

Nota: in questo passaggio possiamo scegliere se ottimizzare ulteriormente le matrici intrinseche, i parametri per la distorsione della lente, ...,
oltre che alla matrice di rototranslation tra le due camere

### Stereo reference frame

dopo la calibrazione possiamo incominciare ad usare la camera... bisogna però scegliere un WRF

chiamiamo SRF il WRF della stereo camera calibrata: tipicamente CRF della camera sinistra

###

tutti questi problemi di ottimizzazione non lineare non sono troppo computazionalmente costosi???
