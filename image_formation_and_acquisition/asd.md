how do we get an image? with a camera

what is a camera? a device that captures light that gets bounced back from a scene

in a sense, the goal of computer vision is giving back information about the scene from an image
- in computer graphics the goal goes the opposite way



### Geometry of image formation
even the most complex camere can be modeled as a pinhole camera as far as image formation geometry is concerned

photosensitive material

come funziona la luce?
- ogni punto riflette la luce che riceve in tutte le direzioni
- molti raggi in direzione radiale

come faccio a formare un immagine con una pinhole camera
- collect a single ray per image point
- this is because only a ray of light can fit through the pinhole

#### Perspective projection
the geometric model of image formation of the pinhole camera
- it applies to all kinds of cameras not only the pinhole one
- it describes how to map a 3d point to its corresponding image point

C is the hole of the pinhole camera -> optical centre

f è la distanza tra il pinhole e il materiale fotosensibile

convenzione:
- lettere maiuscole rappresentano punti della scena
- lettere minuscole rappresentano punti dell'immagine

how does a 3d point map to its corresponding image point


abbiamo bisogno di due sistemi di riferimento
- uno per la scenda 3d con origine nel pinhole
    - sistema di riferimento tridimensionale
    - detto camera reference system (world reference system è un altro)
- e l'altro per l'immagine
    - sistema di riferimento 2d

Le equazioni si ottengono considerando due dimensioni per volta e **notando che ci sono due triangoli simili**
- u/x = -f/z -> u = -x*f/z
- stessa cosa per la v -> v = -y*f/z

NB: il modello suggerisce che c'è una specchiatura e infatti c'è un segno meno. 
- Tuttavia, nella pratica si preferisce eliminare il segno meno
    - questo si traduce nel porre l'image plane davanti al pinhole e non dietro 

Considerazioni:
- le coordinate nell'immagine sono identiche a quelle 3d, scalate per un fattore che dipende dalla distanza dal pinhole (detta anche profondità)
    - più z è grande più il fattore di scaling è piccolo
    - questo ci dice che oggetti vicini vengono catturati come grandi e oggetti lontani vengono catturati come piccoli
- NB: scale in CV pertains the apparent size of objects in images, which depends on the true size, the distance from the camera and the focal length. In many image recognition applcations we wish to achieve scale-invariance.
    - questo processo di image formation introduce quindi ambiguità sulla dimensione effettiva di un oggetto catturato. Oggetti piccoli vinici, vengono catturati come grandi, e oggetti grandi lontani, vengono catturati come piccoli
    - scala != dimensione
    - c'è una perdita di informazione. Prevedibile dato che stiamo comprimendo un punto 3d in uno 2d.
    - la funzione che ci fa passare da 3d a 2d non è invertibile! (guarda l'immagine in slide 6)

#### How do we capture depth and get a notion of size?
aggiungiamo una camera (stereo) e triangoliamo

punti di due camere distinte che corrispondono allo stesso punto 3d, vengono detti corrispondenti

come faccio a capire quali coppie di due punti sono corrispondenti? Questo è il problema principale da risolvere in stereo imaging per recuperare informazioni sulla profondità
- esistono algoritmi per farlo

l'output di una stereo camera è una depth map
- per ogni punto ottengo un valore di profondità

interessante: stereo cameras spesso includono dei proiettori che sporcano appositamente l'immagine per facilitare la ricerca di corrispondenze


#### standard stereo geometry:
- configurazione particolare delle due camere in una camera stereo
    - gli assi sono allineati
    - le due camere sono a una distanza b
    - basta traslare di b sull'asse orizzontale x per ottenere lo stesso punto

equazioni:
- i due punti hanno la stessa altezza dato che le variabili L/R in gioco sono uguali
- le coordinate orizzontali invece sono diverse 
    - x diversi
    - ma so che sono diversi di solo una traslazione

disparity = differenza tra le coordinate orizzonatali di due punti corrispondenti
- misura quanto nell'immagine 2d i punti catturati dalle camere sono diversi orizzontalmente
- ci dà la formula per la profondità
- cio che non è noto per trovare la profondità di un punto è proprio la disparità

Maggiore è la disparità, più vicino è l'oggetto

Come si calcola la disparità? Bisogna trovare il punto corrispondente... lasciamo stare, algoritmi
- possiamo però notare che, data la nostra configurazione standard, il punto corrispondente sarà sicuramente alla stessa altezza, o, detta in un altro modo, sulla stessa orizzontale
    - lo spazio di ricerca è 1-dimensionale
- una intuizione però è che possiamo costruire una finestra attorno ad un punto su questo asse e far scorrere la finestra. Il punto con la finestra più simile a quella dell'altro lato è il punto corrsipondente
    - cosa significa "più simile" lo lasciamo stare

#### epipolar geometry
the search space is still a line, just not horizontal
- this is the epipolar line
- esisteva anche prima, ma quello era un caso speciale in cui l'epipolar line era orizzontale. In generale questa linea è obliqua

this is just to say, the search space of the stereo correspondence problem is always 1-dimensional!

epipolo = punto in cui tutte le linee epipolari convergono
- si ottiene come intersezione tra piano e segmento che congiugne i due optical centres

chiaramente cercare punti di corrispondenza in una geometria standard è chiaramente più facile. Ma allora perchè stiamo introducendo la geometria epipolare?
- perchè è impossibile ottenere una geometria standard mediante allineamento meccanico delle camere?

ma allora dobbiamo rinunciare alla geometria standard?
- no, possiamo fare una trasformazione (warping) che ci permette di ottenere una geometria standard virtuale
- l'immagine destra subisce un warping diverso rispetto a quella sinistra
- una volta rettificate entrambe, possiamo cercare la corrispondenza come con una geometria standard

rectification
- in stereo imagine we always have this step, again, because perfect mechanical alignment is impossible


vanishing point definition [importante]
- abbiamo bisogno di una singola linea e di una pinhole camera
- the point at the infinity of the line ???
- boh, dovrai cercartelo

- nota che per la definizione, linee parallele nel modo 3d, risultano nello stesso vanishing point nel piano 2d



#### can we use a pinhole camera?
no, because the amount of light per unit time that we can gather through a pinhole is very small. To get a bright enough image we would then need a long exposure time. That in turn means that we could only capture static scenes otherwise we would get motion blur

in summary a pinhole camera is impractical to caputre dynamic scenes, its strength is that is has an infinite DOF, that means that a point in the 3d scene gets mapped to a single point in the image. A bigger hole doesn't have this property.


usiamo le lenti per ottenere abbastanza luce e quindi ottenendo i due pregi
- non abbiamo più infinte DOF però... capisci meglio!!!

















### Image digitazion process
