# Image digitazion process
the image is acquired already digitized (pixels), there isn't an analog image that gets converted

the pixels produce and analog electric output that gets read by the electronic circuitry and an ADC
- the intensity/brightness of the pixels gets quantized as an 8bit value

what are the important parameters of a camera?
- signal to noise ratio (SNR)
    - what is image noise in the first place?
        - scattando immagini in momenti diversi, lo stesso punto verrà catturato con intensità diverse, nonostante la scena non sia cambiata (scena stazionaria)
        - I_t(p) = I'_t(p) + n_t
            - con I'_t(p) deterministico e n_t realizzazione di una variabile casuale
    - is noise bad?
        - yes, it makes computer vision more difficult
        - it's better observed in uniform scenes (low variation)
    - a good camera has a high SNR
        - SNR = media del segnale / deviazione standard del segnale
    - why does it happen?
        - photon noise, it's due to the nature of light itself
            - the number of photons that hit a pixel during exposure time is a Poisson random variable
            - a variation in the number of photon hits shows up in the image as a variation of the intensity of the pixel
            - this is an ineliminable noise, we can't do anything about it. Light is this noisy by nature 
            - SNR = sqrt(E[luce]) -> maggiore la scena è luminosa (o equivalentement, maggiore è l'esposizione), minore è il rumore della luce
        - altre variabili casuali dovute a elettronica, materiali e quantizzazione...
        - tutte queste vengono sommate in n_t che viene quindi modellata tramite il teorema del limite centrale con una gaussiana
    - what can we do?
        - gather more light per photon noise
        - cool the camera for dark current noise

- dynamic range (DR)
    - a pixel has un upper bound and a lower bound on the amount of light it can receive
        - the lower bound is determined by the minimum amount of light needed to distnguish the signal from noise
            - if the light a pixel receives is lower than this threshold, the pixel doesn't fire and we don't get any intensity in the image pixel
            - this means that different dark pixels may look the same if all of them don't surpass the threshold
        - the upper bound is determined by the maximum amount of light that a pixel can capture
    - DR è il rapporto tra queste due grandezze
    - why is a high dynamic range good?
        - if we want to see better in the dark regions of the image we need to increase the exposure time
        - by doing so though, the bright regions don't get that much brighter and it can become difficult to see in the bright regions of the image if they saturate
        - by having a high DR we can see well in both dark and bright regions of an image
    - what can we do (computationally) to increase the dyanmic range?
        - HDR
            - short exposure time can capture well bright areas
            - long exposure time can capture well dark areas
            - we can merge them to capture well both

- non uniformity of the sensitivity of the pixels (spatial / pattern noise)


# Colour cameras
every pixel comes with three channels

there are
- red pixels
- green pixels
- blue pixels

how does a pixel get the other colors?
- by neighbouring pixels through interpolation

why do we use twice as many green pixels?
- this better matches how humans perceive colors (perceived brightness is more dependant on the green)

This approach has a disadvantage
- the spacial resolution of the color sensor is less than the resolution of a grayscale sensor
- i don't have 3*W*H pixels because many of them are obtained through interpolation 



### Colour spaces
cameras capture images in this colour space???

HSI colour space
- intensità = altezza
- hue = angolo
- saturation = distanza dal centro

RGB è un entangled colour scheme; HSI è detangled; dove quello che entagled sono le informazioni riguardanti il colore (cromaticità) con l'intensità
- HSI è più comodo per i nostri scopi in quanto detangled
- potrebbe quindi essere necessario trasformare l'immagine catturata dalla camera (RGB) in un altro colour space

RGB e HSI sono dei colour space in cui le distanze tra colori non corrispondono a quanto i colori si assomigliano effettivamente
- se ho tre colori c1, c2, c3, e c1-c2 è una distanza uguale a c1-c3 non è detto che c2 sia percepito tanto simile a c1 quanto c3 o viceversa

Lab colour space ha questa proprietà invece

Conclusione
- don't always stick to RGB
- quando l'applicazione ha a che fare con i colori, potrebbe essere utile considerare altri colour spaces dato che alcune caratteristiche che si stanno cercando potrebbe rivelarsi più chiaramente rispetto ad RGB































