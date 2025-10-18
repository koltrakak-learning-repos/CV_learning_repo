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

nello stimare ogni omografia minimizziamo l'errore algebrico, ovvero la norma di ||A * h||

- questo vettore non ha un'interpretazione immediata

Quello che vogliamo è ottenere una buona stima dell'omografia

- dato un punto 3d, applicando l'omografia vogliamo ottenere un punto 2d molto vicino a quello del control point corrispondente
- Ma minimizzando ||Ah|| stiamo minimizzando qualcosa che non sembra direttamente correlato

**Minimzzando l'errore algebrico non otteniamo una buona omografia**

Quello che vogliamo minimizzare realmente è la norma del vettore distanza tra control point e punto nell'immagine ottenuto applicando l'omografia stimata h* **per tutti i corner della calibration image**

- questo viene chiamato **reprojection error** (detto anche geometric error), ed è questo che vorremmo minimizzare
- The rationale is that the “best” homography would predict with the best accuracy the positions of the corner features actually found in the image.

![reprojection error](./img/reprojection_error.png)

Quello che facciamo minimizzando l'algebraic error è calcolare una stima iniziale dell'omografia che raffiniamo adesso minimizzando il reprojection error

**why don't we do this directly?**

- why do we do first linearly estimate the homography and only after the obtaing a first rough homography, we apply a refinement that more closely matches our intuiton of calibration?
- because this is a **non linear optimization problem**
  - the cost function (reprojection error) is not convex, we have many bad local minimums that we may and up in if we start from an unlucky starting point
  - we use techniques similar to gradient descent
- the first estimation gives us a good starting point that allows to reach a convergence close to the global optimum with the refinement

Ricorda poi che per ogni calibration image otteniamo un omografia, e quindi per ogni omografia va effettuato questo passo di raffinamento

# Estimating the intrinsic parameters

Now we have estimated homographies, but our goal was estimating intrinsic parameters. Putting toggether all these (refined) homographies allows use to do that.

- Dentro alle omografia, da qualche parte, i parametri intrinseci ci sono dato che per definizione, l'omografia è il prodotto tra parametri intrinseci ed estrinseci
- we need to disentangle the intrinsic parameter

ricordiamoci che una PPM può essere fattorizzata come

- lambda A [R | T]; dove lambda è un fattore di scala arbitrario del projective space

definiamo poi

- p1, p2, p3, p4 come le colonne della PPM
- r1, r2, r3 le colonne della matrice di rotazione

fattorizzando l'omografia ed applicando uguaglianze con la PPM, otteniamo

- h1 = lambda A r1 (stessa cosa anche per h2 e h3)
- in questa equazione conosciamo h1, ma tutto il resto no

**Exploiting the properties of the rotation matrix, we come up with 2 equations that factor out the extrinsic parameters**

- r1, r2 e r3 sono perpendicolari
  - in particolare ci interessano r1 e r2
  - il loro prodotto scalare fa quindi 0 (esprimiamo il prodotto scalare come prodotto matriciale (non so perchè), aggiungiamo quindi una trasposta)
  - un po' di passaggi che ci portano ad ottenere la prima equazione... guarda screen

![rotation rows equations](img/rotation_matrix_row_equations.png)

![passaggi](img/passaggi.png)

- sappiamo anche che le colonne (e righe) di una matrice di rotazione hanno norma pari a 1
  - || r1 || = || r2 || = 1
  - lo stesso vale anche al quadrato || r1 ||^2 = || r2 ||^2
  - possiamo scrivere lo norma qudrata di un vettore come prodotto scalare di u vettore per se stesso: r1^T*r1
  - a questo punto con passaggi simili a prima, otteniamo la seconda equazione

A questo punto abbiamo:

- **due equazioni per ogni calibration image**  in cui le incognite sono gli elementi di A
- i parametri estrinseci sono stati tolti
- i parametri di A sono gli stessi per ogni omografia dato che la camera è la stessa
- chiamiamo B = A^-T* A^-1
- knowing B is the same as knowing A (c'è una formula); **so its all about estimating B**
  - si ottengono delle equazioni che ci permettono di ottenere gli elementi di A (parametri intrinseci) a partire dagli elementi di B
- it can be shown that **B is symmetric so its unknowns are only 6**
- **abbiamo quindi bisogno di minimo 3 calibration images** (in Zhang)
  - 2 equazioni per calibration image (omografia stimata)
  - 6 unknowns
- nuovamente, ne usiamo molte di più (20) per essere più robusti al rumore (che si propaga dalla stima delle omografia) con un least square approach

slide 14 non richiesta

- quello che succede è che utilizzando n calibration images con n > 3 otteniamo un sistema di 2n equazioni in 6 incognite
- di nuovo abbiamo un sistema di equazioni lineari overconstrained che non ammette soluzione esatta
- e quindi stimiamo B con un least square error approach e il metodo SVD

# Estimating the extrinsic parameters

once we have estimated the homographies and the intrinsic parameters, we can estimate the extrinsic parameters (one for every calibration image)

- ricorda che H = lambda A \[r1 r2 T\]
- equazione semplici

**attenzione però**:

- il lambda calcolato rende sicuramente r1 un unit vector (stiamo facendo v/||v||)
- non è detto però che utilizzando lo stesso lambda, il resto delle colonne siano anch'esse dei unit vector
  - per esempio: con r2 lambda dovrebbe essere || A^-1 h2 || non || A^-1 h1 ||
  - quindi, magari r2 non è proprio il vettore che mi serve

Otteniamo quindi un matrice di rotazione i cui vettori colonna sono probabilmente non esattamente ortonormali tra di loro.

Come otteniamo una matrice ortonormale a partire da una matrice leggermente non ortonormale?

- possiamo applicare SVD a R e decomporla nelle 3 matrici U sigma V^T
- siccome R non è ortonormale, si può dimostrare che sigma, che dovrebbe esssere una matrice identità, ha invece dei valori diversi da 1 sulla diagonale
- allora per ottenere the closest orthonormal matrix to R, R* basta sostituire sigma con la matrice identità I

# Lens distorsion

osservando la formula della lens distorsion abbiamo

- due equazioni (una per x e una per y)
- due incognite (k1 e k2)

se per un singolo control point avessimo le sue undistorted and distored continuous coordinates potremmo stimare di gia k1 e k2

- (con più control point potremmo ottenere una soluzione più robusta al rumore sempre con il metodo SVD che mi risolve un sistema overconstrained)
- tuttavia noi non abbiamo le coordinate continue, **abbiamo solo le distorted pixel coordinates**
- se avessi anche le undistorted pixel coordinates potremmo comunque utilizzare le due equazioni, però non abbiamo neanche quelle

Come procedere?

- Sicuramente dgitalizzo le mie coordinate continue con le formule che già conosco
  - sia undistorted che distorted
- posso sostituire nelle equazioni coordinate continue con le mie formule che dipendono solo da coordinate dei pixel
- arriviamo a due equazioni in cui abbiamo bisogno di sapere undistorted e distorted pixel coordinates
  - di nuovo, ricorda che abbiamo solo quelle distorte
- noi non possiamo però conoscere le pixel coordinates non distorte, **e quindi le approssimiamo con le coordinate che otteniamo applicando le omografie stimate precedentemente**
- a questo punto possiamo utilizzare tutte le calibration images e ottenere un sistema di 2mn equazioni in due incognite
- questo è di nuovo un overconstrained linear system che risolviamo con SVD stimando in questo modo i parametri della lens distortion
  - stavolta però il sistema non è omogeneo è quindi la soluzione del sistema (che non ci interessa) è un po' diversa

# Finale refinement step

come è stato fatto per le omografie, facciamo un ultimo passo di raffinamento finale in cui minimizziamo il reprojection error ottenuto vendendo dove viene mappato un punto nell'immagine utilizzando una PPM formata da tutti i parametri che abbiamo stimato

alla fine della calibrazione otteniamo quindi una PPM che funziona anche per scene non planari al contrario dell'omografia stimata inizialmente

### How do we know if a calibration is good or not?

we compute the mean square root of the sum of the reprojection errors across every calibration point and every calibration image

- if this is subpixel (0.5, 0.6) we have done a good calibration
- if it is larger than a pixel, the calibration is not good

we should always aim to have a subpixel mean reprojection error

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
