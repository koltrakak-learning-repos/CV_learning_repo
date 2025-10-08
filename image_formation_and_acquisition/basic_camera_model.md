how do we get an image? with a camera

what is a camera? a device that captures light that gets bounced back from a scene. The light is captured by means of a photosensitive material

in a sense, the goal of computer vision is getting back information about the scene from an image
- in computer graphics the goal is the opposite, we already have all the information about a scene and we want to display an image 



# Geometry of image formation
even the most complex camera can be **modeled as a pinhole camera** as far as image formation geometry is concerned

come funziona la luce?
- ogni punto riflette la luce che riceve in tutte le direzioni
- abbiamo molti raggi di luce che vengono riflesso da un punto in direzione radiale

come faccio a formare un immagine con una pinhole camera
- collect a single ray per image point
- this is because only a single ray of light can fit through the pinhole



## Perspective projection
the geometric model of image formation of the pinhole camera
- it applies to all kinds of cameras not only the pinhole one
- it describes how to map a 3d point to its corresponding 2d image point

### glossario
- M: scene point
- m: corresponding image point
- I: image plane
    - dove è presente il materiale fotosensibile
- F: focal plane
    - piano parallelo all'image plane dove è presente il pinhole
- C: optical centre (pinhole)
- f: focal length
    - distanza tra pinhole e image plane (materiale fotosensibile)
- optical axis: Line through C and orthogonal to I
- c: intersection between optical axis and image plane (image centre or piercing point)

convenzione:
- lettere maiuscole rappresentano punti della scena
- lettere minuscole rappresentano punti dell'immagine

### how does a 3d point map to its corresponding image point
abbiamo bisogno di due **sistemi di riferimento**
- uno per la scenda 3d con origine nel pinhole
    - sistema di riferimento tridimensionale
    - detto camera reference system (world reference system è un altro)
- e l'altro per l'immagine
    - sistema di riferimento 2d

Le equazioni si ottengono considerando due dimensioni per volta e **notando che ci sono due triangoli simili**
- u/x = -f/z -> u = -x*f/z; per similitudine
- stessa cosa per la v -> v = -y*f/z

**NB**: il modello suggerisce che c'è una specchiatura e infatti c'è un segno meno.
- Tuttavia, nella pratica si preferisce eliminare il segno meno
- questo si traduce nel porre l'image plane davanti al pinhole e non dietro

**Considerazioni importanti**:
- le coordinate bidimensionali dell'immagine sono identiche a quelle 3d, scalate per un fattore che dipende dalla distanza dal pinhole (detta anche **profondità**)
    - profondità == z == distanza dell'oggetto nella scena dal pinhole
    - più z è grande più il fattore di scaling è piccolo
    - questo ci dice che oggetti vicini vengono catturati come grandi e oggetti lontani vengono catturati come piccoli

- NB: scale in CV pertains the apparent size of objects in images, which depends on 
    - the true size,
    - the distance from the camera 
    - and the focal length.

- questo processo di image formation introduce quindi ambiguità sulla dimensione effettiva di un oggetto catturato.
    - Oggetti piccoli vicini, vengono catturati come grandi, e oggetti grandi lontani, vengono catturati come piccoli
    - In many **image recognition** applications we wish to achieve **scale-invariance**.
        - scala-invariance è la capacità di un sistema di un CV system di riconoscere oggetti anche quando la loro dimensione nell’immagine cambia, a causa della distanza o della variazione della focal length.

- scala != dimensione
    - c'è una perdita di informazione. Prevedibile dato che stiamo comprimendo un punto 3d in uno 2d.
    - a given scene point is mapped into a unique image point, but a given image point is mapped onto a 3D line (i.e. the line through the point, m, and the pinhole C)
    - la funzione che ci fa passare da 3d a 2d non è invertibile! (guarda l'immagine in slide 6)



## How do we capture depth and get a notion of size?
aggiungiamo una camera (stereo) e triangoliamo
- abbiamo due camera reference frames
- con il secondo punto di riferimento si vede bene con un disegno che punti 3d a profondità diversa corrispondono a punti 2d distinti nella seconda immagine
    - disegna le linee che congiungono il pinhole della seconda camera con i vari punti possibili

punti di due camere distinte che corrispondono allo stesso punto 3d, vengono detti **corrispondenti**
- per ottenere informazioni sulla profondità di un punto in un'immagine, ho bisogno di trovare il suo corrispondente nell'immagine catturata dall'altra camera

**Come faccio a capire quali coppie di due punti sono corrispondenti?**
- Questo è il problema principale da risolvere in stereo imaging per recuperare informazioni sulla profondità
- particolarmente difficile su superfici piane e regolari tipo muri
- esistono algoritmi per farlo

l'output di una stereo camera è una depth map
- per ogni punto ottengo un valore di profondità

interessante: stereo cameras spesso includono dei proiettori che sporcano appositamente l'immagine per facilitare la ricerca di corrispondenze

### standard stereo geometry:
- configurazione particolare delle due camere in una camera stereo
    - gli assi (x,y,z) dei due camera reference systems sono paralleli
    - stesso focal length
    - le due camere sono a una distanza b
    - basta traslare di b sull'asse orizzontale una delle due immagini per ottenere gli stessi punti

equazioni:
- i due punti 3d hanno la stessa altezza e profondità dato che le variabili per le due camere L/R in gioco sono uguali
- le coordinate orizzontali invece sono diverse
    - x diversi
    - ma so che sono diversi di solo una traslazione grande b

**disparity** = differenza tra le coordinate (2d) orizzonatali di due punti **corrispondenti**
- misura quanto nell'immagine 2d i punti catturati dalle camere sono diversi orizzontalmente
- ci dà la formula per la profondità: z = b*f/d

Mentre b e f sono parametri noti/misurabili, **cio che non è noto per trovare la profondità di un punto è la disparità**
- ma per trovare la disparità ci serve trovare il punto corrispondente nell'altra immagine
- torniamo allo stesso problema difficile menzionato sopra

notiamo che la disparità è proprorzionale allo scostamento tra le due camere scalato per lo stesso fattore di profondità di prima
- **Maggiore è la disparità, più vicino è l'oggetto**

### Come si calcola la disparità? 
Bisogna trovare il punto corrispondente nell'altra immagine...

Possiamo però notare che, data la nostra configurazione standard, il punto corrispondente sarà sicuramente alla stessa altezza!
- detta in un altro modo, **sulla stessa linea orizzontale nell'altra immagine**
    - lo spazio di ricerca è 1-dimensionale
- ora però abbiamo capire quand'è che scorrendo questa linea riusciamo a trovare la corrispondenza
    - intuitivamente, possiamo costruire una finestra scorrevole attorno ai punti di questa linea.
    - Il punto con la finestra più simile a quella del punto dell'altro lato è il punto corrsipondente
    - cosa significa "più simile" lo lasciamo stare

### epipolar geometry
qui i camera reference frames non sono necessariamente paralleli

the search space is still a line, just not horizontal
- this is the **epipolar line**
- esisteva anche prima, ma quello era un caso speciale in cui l'epipolar line era orizzontale.
- In generale l'epipolar line è obliqua

All the epipolar lines in an image meet at a point called **epipole**
- each camera has its own epipole and epipolar lines depending on which camera you're using to estimate depth
- L’epipolo è il punto d’intersezione sul piano immagine di una camera della retta che unisce i due centri ottici delle camere.
    - L’epipolo e1 è la proiezione del centro ottico C2 sul piano immagine della prima camera.
    - L’epipolo e2 è la proiezione del centro ottico C1 sul piano immagine della seconda camera.
- Se le camere sono parallele l'epipolo si trova ad infinito dato che la linea che unisce i due optical centre non interseca mai nessuno dei due image planes
this is just to say, the search space of the stereo correspondence problem is always 1-dimensional!


Chiaramente cercare punti di corrispondenza in una geometria standard è chiaramente più facile rispetto alla ricerca in una linea obliqua di una geometria epipolare.
- Ma allora perchè stiamo introducendo la geometria epipolare?
- perchè è **impossibile ottenere una geometria standard mediante allineamento meccanico delle camere**

ma allora dobbiamo rinunciare alla geometria standard?
- no, possiamo fare una trasformazione (warping) che ci permette di ottenere una geometria standard virtuale: **rectification**
- l'immagine destra subisce un warping diverso rispetto a quella sinistra
- una volta rettificate entrambe, possiamo cercare la corrispondenza come con una geometria standard

**rectification**: in stereo imagine **we always have this step**, again, because perfect mechanical alignment is impossible



## vanishing point definition (importante)
considerazioni preliminari:
- Perspective projection maps 3D lines into image lines.
- Ratios of lengths are not preserved (unless the scene is planar and parallel to the image plane).
- Parallelism between 3D lines is not preserved (except for lines parallel to the image plane)

**NB**: The images of parallel 3D lines (che nell'immagine non sono più parallele (except for lines parallel to the image plane)) meet at a point, which is referred to as vanishing point.

The vanishing point of a 3D line is the image of the point at the infinity of the line (i.e. the image of the point on the line which is infinitely distant from the optical centre).
- il vanishing point è un image point (non necessariamente nell'immagine)
- il vanishing point è associato ad una singola 3d line
- linee 3d infinite, non parallele all'image plane, terminano in un punto infinitamente distante
- As such, the vanishing point can be determined by the intersection between the image plane and the line parallel to the given one and passing through the optical centre. 
    - copia la linea 3d, falla passare per l'optical centre, e vedi dove interseca il piano dell'image plane

**Proprietà**:
Nota che secondo la definizione, linee parallele nel mondo 3d, risultano nello stesso vanishing point nell'immagine
- all parallel 3D lines will share the same vanishing point, i.e. they “meet” at their vanishing point in the image 
    - facilmente verificabile traslando le varie linee nell'optical centre
    - in quanto parallele, intersecheranno per forza l'image plane nello stesso punto
- tranne nel caso in cui such a point is at infinity (i.e. the 3D lines are parallel to the image plane).
    - qua non c'è proprio intersezione

NB: dire che il vanishing point è il punto in cui tutto le linee parallele convergono non è una definizione, piuttosto una proprietà (utile per trovare il vanishing point velocemente), la definizione è quella sopra che necessità di solo una pinhole camera e di una singola linea.

**perchè ci interessa il vanshing point?**
è uno strumento che ci fornisce informazioni sull'orientamento della camera!
- se so che determinate linee nel mondo reale sono parallele (vedi guide in un circuito)
- posso orientare la camera in maniera tale che il vanishing point di queste linee risieda nel centro dell'immagine
- se il vanishing point si sposta so che la camera non è più orientata correttamente



## lenses, focus and depth of field
A scene point is **on focus** when all its light rays gathered by the camera hit the image plane at the same point.
- if this doesn't happen the image gets blurry (the rays from a point get spread in an area of the image plane, i.e. circle of confusion)
- In a pinhole device this happens to all scene points because of the very small size of the hole (che lascia passare un singolo raggio per punto)
    - In other terms, the pinhole camera features an infinite **Depth of Field (DOF)**

**Depth of field:**
La Depth of Field è l’intervallo di distanze in cui i punti della scena appaiono nitidi nell’immagine.
- Con una pinhole camera la DOF è infinita dato che ogni punto ha sempre e solo un raggio di luce associato e quindi non ci sono mai sovrapposizioni
- Con un obiettivo reale (a lenti), solo gli oggetti posti a una certa distanza sono perfettamente a fuoco; gli altri risultano sfocati.
- La DOF misura quanto è esteso questo intervallo di distanze per cui l’immagine appare accettabilmente nitida.

Tuttavia, can we use a pinhole camera in real life?
- no, because the amount of light per unit time that we can gather through a pinhole is very small.
- To get a **bright** enough image we would then need a long **exposure** time.
- That in turn means that we could only capture static scenes otherwise we would get **motion blur**

Therefore, cameras rely on **lenses** to gather more light from a scene point and focus it on a single image point.
- the lense captures many light rays from a point and converges them towards a single point
- This enables much smaller exposure times, as required, e.g., to avoid motion blur in dynamic scenes.
- However, with lenses, **the DOF is no longer infinite** (vedi thin lense equation)
    - only points across a limited range of distances can be simultaneously on focus in a given image.

In summary:
- a pinhole camera alone is impractical to capture dynamic scenes
- its strength is that is has an infinite DOF
- usiamo le lenti per ottenere abbastanza luce e quindi per catturare anche scene dinamiche
- così facendo però, perdiamo la infinte DOF

### how do we geometrically model a lense?
we can approximate the lense system of a camera (which can be complex) as a **single thin lense** positioned in the optical centre.
- That is, we use the thin lense model.
- il pinhole in questo modo ha un apertura pari al diametro della lente e lascia passare più luce, la lente concentrerà la luce in un unico punto nell'image plane
- we'll see that we can still use perspective projection even with this thin lense model.

Introduciamo un po' di nomenclatura:
- u : distance from P to the lens
    - object distance
- v : distance from p to the lens
    - image plane distance (ex focal length of the pinhole camera without lenses)
    - camera parameter
- f : focal length (parameter of the lens)
- F : focal point (or focus) of the lens
    - point on the optical axis at distance f from C
- C : centre of the lens (== pinhole)

... questo pezzo si capisce meglio dalle slide ...

how do we determine the (on focus) image point of the scene point with a thin lense?
- we just need to see where 2 lines coming frome the same point intersect
- usiamo due linee speciali quella parallela all'optical axis, e quella che tira dritto verso l'optical centre

Dov possiamo mettere l'image plane affinchè l'immagine sia on focus?
- l'unica possibilità è metterla a distanza v

**thin lense equation**
- 1/u + 1/v = 1/f
- di nuovo si ricava osservando similitudini tra triangoli
    - h/h' = u/v
    - h/h' = f/v-f

**NB**: se l'immagine è on focus, abbiamo lo stesso modello di prima.
- il pinhole diventa il centro della lente
- **possiamo continuare ad usare perspective projection per capire come 3d point vengono mappati in punti 2d**
- abbiamo una terminologia un po' diversa 
    - es. v viene anche detta **effective focal length** (che è diversa dalla focal length della lente)

If the image is out of focus, perspective projection doesn't apply. But this case doesn't concern us (we must make sure that we work with focused images)

### circles of confusion
**NB**: Due to the thin lens equation, **choosing the distance of the image plane u determines the distance at which scene points appear on focus in the image**:
- u = v*f/(v-f)
- notiamo quindi che con questo modello sembra che le uniche scene che possiamo catturare in maniera non sfocata siano quella ad una distanza ben precisa.
- Given the chosen position of the image plane, scene points **both in front and behind the focusing plane will result out-of-focus**, thereby appearing in the image as circles, known as Circles of Confusion or Blur Circles, rather than points
- Possiamo catturare solo un piano?

No! **As long as the circle of confusion is smaller than the pixel size we don't perceive the blurring effect**
- the DOF is the range of distances where this is true

**What if the DOF is not good enough?**
we use a **diaphram**, a mechanism which makes the lense larger or smaller by covering it
- this doesn't change the effective focal length, but it makes the circles of confusion smaller
- this way we capture less light, and so we need longer exposure times, and this make it harder to capture dynamic scenes without motion blur
    - to counteract this we can add more light through a flash on the camera, or more light on the scene
- by closing the diaphram we gain DOF but we lose brightness e viceversa

We can also use a **focusing mechanism** that changes the distance of the lense from the image plane v
- this way we can vary v and change the distance u at which objects appear focused
- this can be manual or automatic
- a sua volta, l'autofocus può essere passive or active
    - attivo significa che usiamo un sensore aggiuntivo (laser, sonar) per ottenere una misura della distanza dell'oggetto da mettere a fuoco con cui regolare l'image length 
        - veloce
    - passiva significa che non si usa alcun sensore, piuttosto si fanno tanti tentativi e si computa qual'è quello più a fuoco
















