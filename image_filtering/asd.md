we're gonna be studying the same kind of filters that are used in CNNs

the difference between filters in image processing and in CNNs is that:

- in image processing the filters are defined by the users
- in CNNs the filters are learned by the network

the dimension of the neighbourhood of the filter is an (hyper)parameter

why do we filter an image?

- to improve its quality
  - we'll focus on denoising
    - noise looks particularly bad on uniform areas (it should be uniform but in the image it's not)

if the filter is LTE, its application is a 2d convolution

# Definizione di filtri come operatori

a two dimensional signal is just a function of two variables: i(x, y)

- we can imagine the image to be continuous

the response of the operator is the application of the operator to an image

L'operatore si dice lineare se vale la sovrapposizione degli effetti

L'operatore si dice Translation-Equivariant se: traslare l'input prima della applicazione dell'operatore, è equivalente a traslare direttamente l'output

The impulse response of the operator is the output that we get if we input to the operator la delta di dirac (anche chiamato point-spread function)

- ricorda la definizione della delta di dirac: { d(0,0) != 0;  0 altrove; doppio integrale deve fare 1}
- è zero dappertuttto tranne che nell'origine
- nell'origine è tanto grande da far valere l'integrale 1

Di nuovo, if the filter is LTE the response of the operator, applying the operator to the image, is the convolution with the impulse response

- a noi quindi interessa qual'è l'h() dell'operatore per poterlo applicare

## Convoluzioni 2D

**Come interpretiamo questa convoluzione?**

- the core operation in convolution is MAD (multiply and add/multiply and accumulate)
  - l'integrale somma
  - dentro all'integrale moltiplichiamo
- l'immagine è non zero solo dentro alla regione grigio chiaro
- stessa cosa vale per h()
  - qua, specifichiamo con a,b,c,d delle sottoregioni non-zero di h()
- osserviamo l'integrale
  - i è invariata
  - h è manipolata
  - -alpha e -beta mi specchiano i punti di h che prendo rispetto all'origine
  - con x e y faccio una traslazione verso x, y

**Varie proprietà delle convoluzioni**
la quarta proprietà è particolarmente importante

## Correlation

formula molto simile a convoluzione: abbiamo un + al posto di un -

correlation is NOT commutive unlike convolution

the main difference between convolution and correlation is that

- in convolution we flip the point spread function h()
- in correlation we don't

# Discrete convolution

clearly, we can't use continuous images and continuous filters

definiamo la convoluzione discreta sostituendo agli integrali delle sommatorie

nel caso discreto abbiamo che una matrice che contiene i valori della point spread function viene chiamata kernel

## Convolution in practice

siccome la convoluzione è commutativa, posso scambiare I e K; questo mi da una formula più vicina alla computazione di una convoluzione nella pratica

Per le sommatorie, è sufficente che vadano da -k a +k, con 2k+1 dimensione del kernel (tutto il resto è 0)

nota (difficile dalla slide) come nell'immagine gli indice del kernel subiscono un flip di segno

NB: fare attenzione nell'implementazione a non sovrascrivere i valori dell'input matrix con quelli della convoluzione

Attenzione ai bordi

- it's not possible to compute correctly the convolution sui bordi
- abbiamo due soluzioni
  - produciamo un output più piccolo riespetto all'input, corrispondente a dove riesco a computare la convoluzione
    - cropping
    - non desiderabile se dobbiamo applicare più filtri
  - usiamo del padding
    - we enlarge the input image with one of many rules
    - which kind of padding doesn't make that much of a difference
    - in CNNs we apply sequences of filters, there we use padding to preserve the size of the image

**NB**: la funzione di opencv per i filter di fatto computa una correlation e non una convolution

- non fa il flip (segno + invece che meno nell'immagine)
- per avere una convolution basta flippare il kernel
- se il kernel è simmetrico non c'è neanche bisogno
- btw anche nell CNNs quello che viene computato è una correlation

**NB**: il numero di MAD che devo fare è uguale alla dimensione del kernel (es 7x7 -> 49 MAD)

- il numero di MAD è o(n^2) rispetto alla dimensione del kernel

# Denoising filter

Come modelliamo il rumore?

- siccome il rumore proviene da tante fonti, modelliamo quest'ultimo come un rumore gaussiano di media 0 e varianza sigma^2
- pensiamo all'intensità di un pixel come la somma tra: intensità ideale noiseless (che non esiste) + realizzazione della gaussiana che mi modella il rumore
- il rumore di tutti i pixel è i.i.d (Indipendent and Identically Distributed)
  - non posso indovinare il rumore di un pixel dato il rumore di un altro pixel

To remove noise we can take an average across time of multiple images of the same scene?

- if we can, this is the best way to remove noise
- but we need to have multiple images and for the scene to be perfectly static

Guardando la formula abbiamo che per la legge dei grandi numeri il rumore tende a zero al crescere dei samples N

- the variance decreases with N

What if we are given a single image?

- we can do a mean across space instead of time
- guardando la formula
  - abbiamo di nuovo che più è grande K (kernel), più il rumore approccia la sua media (0) e quindi si annulla
  - tuttavia, stavolta le intensità dei pixel non fanno riferimento allo stesso punto p di cui vogliamo rimuovere il rumore
    - se prendo un kernel piccolo, più o meno l'intensità sarà la stessa
    - se invece prendo un kernel grande potrei includere dei pixel associati ad altre entità nella scena con intensità diverse da p; e quindi otterrò un intensità risultate divers (blur)
- c'è un tradeoff sulla dimensione del kernel per spatial filtering

## Mean filter

The Mean Filter is an LTE operator as it can be described by a kernel, and applied as a convolution

- tuttavia, non applichiamo un mean filter come convoluzione
- non c'è bisogno di fare tutte le divisioni, è sufficente sommare e fare una divisione alla fine (media)
- applying the mean filter as a convolution would require 9 MAD, fare la media invece necessita di 9 somme e una divisione

blurring is caused by pixels in the neighbour with different intensity, being averaged into the central one

the mean filter is the fastest denoiser

- even though it blurs, if the application doesn't mind, it can be very useful

anche nelle immagine c'è il concetto di frequenze (sia verticali che orizzontali)

**NB**: Il mean filter può essere visto da due punti di vista

- denoising
- semplificazione dell'immagine tramite **smoothing**
  - a causa del blur i dettagli piccolini vengono eliminati, questo può essere un bene
  - in altre parole il mean filter diminuisce anche il livello di dettaglio dell'immagine lasciando solo large scale objects

**NB**: a volte un livello di dettaglio troppo alto potrebbe essere fastidioso per algoritmi di image processing

## Gaussian filter

the gaussian filter is the filter such that:

- h(x,y) = G(x, y)
- il filtro che ha come impulse response function una gaussiana 2d
- proprietà interessante è la circular simmetry

### practical implementation

nel mean filter i pesi del kernel sono uniformi

nel gaussian filter i pesi del kernel sono distribuiti come la gaussiana 2d

- near 0 sui bordi
- big numbers nel centro
- immagino che anche qui la simmetria circolare si noti

gaussian filter causes less blur because of its distribution in the kernel

The discrete Gaussian kernel can be obtained by sampling the corresponding continuous function, which is however of infinite extent.

- To capture the whole function i would need to choose a kernel of infinite size
- we definetly can't do that

A finite size must therefore be properly chosen.

- the bigger the filter the better the approximation of the gaussian
- the smaller the filter the less computation

We should pick as many samples as needed (vogliamo sample !~ 0)

- questo dipende dalla deviazione standard della gaussiana
  - se la deviazione standard è alta -> la gaussiana è schiacciata -> devo prendere più samples
  - se la deviazione standard è bassa -> la gaussiana è secca -> devo prendere meno samples
- sigma è il parametro che regola lo smoothing
  - larger sigma = more smoothing

As the interval [-3sigma, +3sigma] captures 99% of the area (“energy”) of the Gaussian function

A typical rule-of-thumb dictates taking a (2k+1)×(2k+1) kernel with: k = lower(3*sigma)

**NB**: di nuovo valgono le considerazioni su smoothing e semplificazione dell'immagine

**NB**: it can be proved that gaussian filtering is the only kind of filtering that doesn't introduce artifacts (something that wasn't present in the original image)

- for this reason it's the main tool for processing images at various kinds of detail
  - variando il livello di smoothness con sigma non introduciamo comunque artifatti

# Impulse noise (salt & pepper noise)

al contrario di gaussian noise, qua abbiamo molti pixel senza rumore

inoltre qua la corruzione causata dal rumore o è totale o è assente; al contrario del caso gaussiano che corrompe con un rumore piccolino

- noise has created outliars (pixels that are totally different from the others)

Il Gaussian noise modella il rumore cumulativo di tutte le sorgenti di rumore nel processo di acquisizione dell'immagine

quand'è che un immagine può essere corrotta da impulse noise invece?

- quando alcuni sensori nella camera sono rotti
- quando l'immagine viene trasmessa su un canale rumoroso
- oppure anche quando l'immagine che stiamo cercando di processare non è un'immagine vera e propria ma piuttosto un risultato di una computazione intermedia
  - vedi disparity map in stereo matching
  - se sbaglio a matchare due pixel ottengo una disparity strana che è un outliar

Come si rimuove l'impulse noise?

linear filters di qualsiasi tipo non funzionano

- con mean filter spargiamo gli outliar across an area rendendoli meno evidenti
- con gaussian piu o meno la stesssa cosa

## Median Filter

Per eliminare impulse noise l'idea è buttar via il pixel che è outliar e sostituirlo con uno che non lo è

la domanda diventa quindi come facciamo a riconoscere che un pixel è un outliar?

con median filter scegliamo la mediana dell'intorno (dopo sort)

- outliars are never in the middle

This is NOT a linear operator

- this means that this filter doesn't apply any convolutions (d'altronde non stiamo facendo delle MAD, stiamo facendo delle mediane)

The median preserves edges better than mean/gaussian filters

The median filter however doesn't work well with gaussian noise

### What if i have an image with both gaussian noise and impulse noise

we first get rid of outliars with a median filter

- this way we're substituing an outliar with another pixel subject to gaussian noise

after that we eliminate gaussian noise with a gaussian/mean filter

# gaussian denoisers that preserve edges

## Bilateral filter

now i want a filter that denoises like a gaussian filter but without blurring

A gaussian filter considers bright pixels while the pixel we're computing the new value for is dark

- when i'm close to an edge i mix together bright and dark pixels

we would like a weight function that adapts to the kind of neighbour we're within

- when we're on a uniform region we would like a full gaussian
- wehn we're near an edge we want to consider only the pixels in the neighbour with a similar intensity

A bilateral filter weighs nieghbours highly considering

- distance from the center
- intensity difference
- this filter weighs highly pixels that are near the center and close in intensity to the one we're computing a new value for

Facciamo di nuovo una somma pesata dell'intensità di un intorno

- stavolta però per i pesi non campioniamo una singola gaussiana
- Usiamo due gaussiane
  - una che decresce con spatial distance
  - l'altra che decresce con intensity distance
- abbiamo anche un termine che mi normalizza dividendo ogni peso con la somma di tutti i pesi dell'intorno
  - this way all the weights sum up to one and are all between 0 and 1
  - filters with this property are said to have **unitary gain**
  - this is means that in an area the average intensity doesn't change (in an uniform area the intensity doesn't grow or shrink)

A gaussian filter considers only distance from the center

A bilateral filter is more computationally expensive than a gaussian filter because we have to compute the (intensity distance) weights at each position in the image

- way slower than the gaussian filter

## Non-local means filter

even more computationally expensive than the bilateral filter

I can calculate a new intensity for a pixel considering every other pixel in the image

- again we use weights to

we can weigh more, pixels that have a similar neighbourhood to the one that we're trying to compute a new value for

- the idea is that we want to weigh more pixel that are part of the same surface of the given one

# riguarda meglio la spiegazione della formula (ultima mezz'ora)

Questo filtro ha come vantaggio la possibilità di considerare molti pixel per fare denoising

- per la legge dei grandi numeri questo ci permette di avvicinarci alla media di zero della distribuzione del rumore

considerare tutta l'immagine però è crazy slow

- per questo motivo aggiungiamo un ulteriore parametro che definisce la regione dell'immagine in cui andiamo a guardare
