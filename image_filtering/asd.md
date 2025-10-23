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
