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
    - Oggetti piccoli vinici, vengono catturati come grandi, e oggetti grandi lontani, vengono catturati come piccoli
    - In many image recognition applications we wish to achieve **scale-invariance**.

- scala != dimensione
    - c'è una perdita di informazione. Prevedibile dato che stiamo comprimendo un punto 3d in uno 2d.
    - a given scene point is mapped into a unique image point, but a given image point is mapped onto a 3D line (i.e. the line through the point, m, and the pinhole C)
    - la funzione che ci fa passare da 3d a 2d non è invertibile! (guarda l'immagine in slide 6)





### How do we capture depth and get a notion of size?
aggiungiamo una camera (stereo) e triangoliamo
- abbiamo due camera reference frames
- con il secondo punto di riferimento si vede bene con un disegno che punti 3d a profondità diversa corrispondono a punti 2d distinti nella seconda immagine
    - disegna le linee che congiungono il pinhole della seconda comaera con i vari punti possibili

punti di due camere distinte che corrispondono allo stesso punto 3d, vengono detti **corrispondenti**

come faccio a capire quali coppie di due punti sono corrispondenti (particolarmente difficile su superfici piane e regolari tipo muri)?
- Questo è il problema principale da risolvere in stereo imaging per recuperare informazioni sulla profondità
- esistono algoritmi per farlo

l'output di una stereo camera è una depth map
- per ogni punto ottengo un valore di profondità

interessante: stereo cameras spesso includono dei proiettori che sporcano appositamente l'immagine per facilitare la ricerca di corrispondenze

### standard stereo geometry:
- configurazione particolare delle due camere in una camera stereo
    - gli assi sono allineati
    - le due camere sono a una distanza b
    - basta traslare di b sull'asse orizzontale una delle due immagini per ottenere gli stessi punti

equazioni:
- i due punti hanno la stessa altezza dato che le variabili per le due camere L/R in gioco sono uguali
- le coordinate orizzontali invece sono diverse
    - x diversi
    - ma so che sono diversi di solo una traslazione grande b

**disparity** = differenza tra le coordinate (2d) orizzonatali di due punti corrispondenti
- misura quanto nell'immagine 2d i punti catturati dalle camere sono diversi orizzontalmente
- ci dà la formula per la profondità: z = b*f/d

Mentre b e f sono parametri noti/misurabili, cio che non è noto per trovare la profondità di un punto è la disparità
- ma per trovare la disparità ci serve trovare il punto corrispondente nell'altra immagine
- torniamo allo stesso problema difficile menzionato sopra

notiamo che la disparità è proprorzionale allo scostamento tra le due camere scalato per lo stesso fattore di profondità di prima
- Maggiore è la disparità, più vicino è l'oggetto

Come si calcola la disparità? Bisogna trovare il punto corrispondente...
- possiamo però notare che, data la nostra configurazione standard, il punto corrispondente sarà sicuramente alla stessa altezza, o, detta in un altro modo, **sulla stessa linea orizzontale nell'altra immagine**
    - lo spazio di ricerca è 1-dimensionale
- ora però abbiamo capire quand'è che scorrendo questa linea riusciamo a trovare la corrispondenza
    - intuitivamente, possiamo costruire una finestra scorrevole attorno ai punti di questa linea. Il punto con la finestra più simile a quella del punto dell'altro lato è il punto corrsipondente
    - cosa significa "più simile" lo lasciamo stare

#### epipolar geometry
qui i camera reference frames non sono coplanari

the search space is still a line, just not horizontal
- this is the epipolar line
- esisteva anche prima, ma quello era un caso speciale in cui l'epipolar line era orizzontale.
- In generale l'epipolar line è obliqua

All the epipolar lines in an image meet at a point called **epipole**
- each camera has its own epipole and epipolar line
    - it depends on which camera you're using to estimate depth
- the epipole is the projection of the optical center of the other image through the image plane

this is just to say, the search space of the stereo correspondence problem is always 1-dimensional!


Chiaramente cercare punti di corrispondenza in una geometria standard è chiaramente più facile rispetto alla ricerca in una linea obliqua di una geometria epipolare. Ma allora perchè stiamo introducendo la geometria epipolare?
- perchè è **impossibile ottenere una geometria standard mediante allineamento meccanico delle camere**

ma allora dobbiamo rinunciare alla geometria standard?
- no, possiamo fare una trasformazione (warping) che ci permette di ottenere una geometria standard virtuale: **rectification**
- l'immagine destra subisce un warping diverso rispetto a quella sinistra
- una volta rettificate entrambe, possiamo cercare la corrispondenza come con una geometria standard

**rectification**
- in stereo imagine we always have this step, again, because perfect mechanical alignment is impossible



#### vanishing point definition (importante)
considerazioni preliminari:
- Perspective projection maps 3D lines into image lines.
- Ratios of lengths are not preserved (unless the scene is planar and parallel to the image plane).
- Parallelism between 3D lines is not preserved (except for lines parallel to the image plane)

The images of parallel 3D lines (che non sono più parallele in Perspective projectino) meet at a point, which is referred to as vanishing point.

The vanishing point of a 3D line is the image of the point at the infinity of the line (i.e. the image of the point on the line which is infinitely distant from the optical centre).
- linee 3d infinte non parallele all'image plane terminano in un punto infinitamente distante
- As such, it can be determined by the intersection between the image plane and the line parallel to the given one and passing through the optical centre. 
    - copia la linea 3d, falla passare per l'optical centre, e vedi dove interseca il piano dell'image plane

Proprietà:
Nota che per la definizione, linee parallele nel mondo 3d, risultano nello stesso vanishing point nel piano 2d
- all parallel 3D lines will share the same vanishing point, i.e. they “meet” at their vanishing point in the image (facilmente verificabile traslando le varie linee nell'optical centre)
- tranne nel caso in cui such a point is at infinity (i.e. the 3D lines are parallel to the image plane).

NB: dire che il vanishing point è il punto in cui tutto le linee parallele convergono non è una definizione, piuttosto una proprietà (utile per trovare il vanishing point velocemente), la definizione è quella sopra che necessità di solo una pinhole camera e di una singola linea.


### lenses
A scene point is **on focus** when all its light rays gathered by the camera hit the image plane at the same point.
- In a pinhole device this happens to all scene points because of the very small size of the hole (che lascia passare un singolo raggio per punto)
    - In other terms, the pinhole camera features an infinite **Depth of Field (DOF)**

**Depth of field:**
La Depth of Field è l’intervallo di distanze (davanti alla fotocamera) in cui i punti della scena appaiono nitidi nell’immagine.
- Con una pinhole camera la DOF è infinita dato che ogni punto ha sempre e solo un raggio di luce associato e quindi non ci sono mai sovrapposizioni
- Con un obiettivo reale (a lenti), solo gli oggetti posti a una certa distanza sono perfettamente a fuoco; gli altri risultano sfocati.
- La DOF misura quanto è esteso questo intervallo di distanze per cui l’immagine appare accettabilmente nitida.

Tuttavia, can we use a pinhole camera in real life?
- no, because the amount of light per unit time that we can gather through a pinhole is very small.
- To get a **bright** enough image we would then need a long **exposure** time.
- That in turn means that we could only capture static scenes otherwise we would get **motion blur**

Therefore, cameras rely on **lenses** to gather more light from a scene point and focus it on a single image point.
- This enables much smaller exposure times, as required, e.g., to avoid motion blur in dynamic scenes.
- However, with lenses, **the DOF is no longer infinite**
    - only points across a limited range of distances can be simultaneously on focus in a given image.


In summary:
- a pinhole camera alone is impractical to capture dynamic scenes
- its strength is that is has an infinite DOF
- usiamo le lenti per ottenere abbastanza luce e quindi per catturare anche scene dinamiche
- così facendo però, perdiamo la infinte DOF

















### Image digitazion process
