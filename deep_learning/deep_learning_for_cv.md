**FC layers are very BAD at processing images!**

We want our layers, given an input image, to output a different image where some kind of feature is highlighted (the pixels where the feature is present receive a high score)

- we're doing representation learning so our layers do a series of (non-linear) transformations that allow us to linearly discriminate classes

If we use FC layers, **the number of parameters and the number of FLOPs required to compute a single feature map is ridicolous**

- every neuron of the preceding layer is connected to every neuron of the next layer -> params = size1 * size2
- the activations of the next layer are obtained through a matmul
  - 2 flops per parametro (pensa al dot product di una riga, ho una moltiplicazione per parametro e poi sommo tutti i termini)

**NB**: What is the main reason that having a high number of parameters is bad?

- we're sure to overfit because the model capacity is proportional to the number of parameters
- **if we use FC layers to detect features, the model gets too big**
- remember, overfitting depends on model capacity vs training data
  - if the training data is small wrt the model capacity, the model memorizes every bit of the training data and we're sure to overfit

# Convolutional layers

Similarly to what we do in classical computer vision, in deep learning we use convolutions to detect features and patterns

- the difference is that in DL the filters are not handcrafted, **butlearned by minimizing a loss function**

The convolution operation is encapsulated in a convolutional layer that given an input image (tensor), and a learned filter, outputs a feature map that is the result of the convolution (correlation really) of the kernel with the input image

Differences of conv layers from fc layers:

- here we don't flatten the image into a vector
  - the input and output of this layers are both 2d
- instead of connecting every output pixel with every input pixel, we connect it with only its neighbourhood in the input image
  - this is called a **local receptive field**
  - in FC layers we would have global receptive fields
- we reuse the same set of weights for every output pixel
  - **shared weights**
  - we do the convolution with the same kernel

In summary a conv layer has two properties:

- local receptive fields
- and shared weights

**Inductive biases**:

We want to apply constraints to accelerate training

- local receptive fields make sense because **features are usually detectable looking only at a neighbourhood of a pixel**
- shared weights make sense because **we want to detect a feature everywhere inside an image**
  - vogliamo trovare tutti gli edge pixel e non solo quelli di una regione
  - translation invariance in feature detection

Conv layers embody inductive biases dealing with the structure of images: pixels exhibit informative local patterns that may appear everywhere across the image

This is called a convolutional layers because to compute the feature map we're just doing a convolution

- here though the kernel is learned during training and not decided a priori

In a conv layer:

- the number of parameters is fixed (size of the kernel) **and much smaller in confronto ad un FC layer**
  - se dimensione di input è 3\*H\*W e dimensione di output è H\*W
  - FC layer avrà (3\*H\*W) * (H\*W) parametri
  - mentre un conv layer avrà H_k * W_k parametri indipendentemente dalle dimensioni dell'input e dell'output
- but the number of FLOPs depends on the size of the output feature map and is **usually higher in confronto ad un FC layer**
  - FC layer avrà 2*(3\*H\*W) \* (H\*W) FLOPs
  - conv layer avrà 2*(H_k\*W_k) FLOP per posizione e ci sono H*W posizioni, quindi: 2\*(H_k\*W_k) * (H\*W) FLOPs

Tradeoff tra numero di parametri e compute necessaria, avere meno parametri è meglio per evitare overfitting

### Biases, non-linearities and why we need biases

Nell'applicare la convoluzione abbiamo di nuovo anche un bias

- ad ogni posizione nella output image ottenuta tramite la convoluzione, aggiungo il valore di un bias
- i parametri sono quindi H_k*W_k + 1

We've already discussed the importance of non linearity for learning important features

Come prima quindi, the output of conv layers will need to be passed through an activation function (ReLU or whatever) to produce the output activations of the next layer

The activation (non-linear) functions trigger at zero. **By using biases we allow more freedom in the weights**

- we can make the activation trigger at b and not zero
- this increases model capacity

### output activations/feature maps

output activations are smaller than the input image because at the borders we don't have the neighbours

to avoid shrinking the activations too much throughout the many conv layers of a model, we usually **use padding the preserve size**

## Multiple input channels

If the image has multiple channels (color images) should we use the same kernel for all the channels?

- no, this would be an inductive bias, and there isn't a reason to apply it

Di conseguenza, **con multiple channels abbiamo un kernel tridimensionale (tensore) per la nostra convoluzione**

l'output della convoluzione continua ad essere un singolo pixel

## Multiple output channels

there's no reason to restrict ourselves to detect only one feature in a conv layer. **We can have multiple kernels in a single conv-layer**

the filters of a conv layers detect different features but they all have the same shape

**the number of filters of a conv layers determines the depth of the output activation and its an hyperparameter**

- we can see the output of a convolutional layer as an image (it has a 2d structure) with a number of channels defined by the number of kernels in the conv layer
- the convolution with each kernel adds a channel in our output image with the corresponding activations

Each kernel has associated with it **his bias**

- the number of parameters of a conv layers becomes: (H_k\*W_k*D_k)\*num_kernels + num_kernels

## General structure of a conv layer

A conv layer:

- receives a multi-channel (C_in) input activation
- produces a multi-channel (C_out) output activation
  - by applying as many filters as the output channels
    - all the filters have the same size H_k*W_k
  - with the depth of the filters given by the number of input channels

### shapes

the shape of the conv layer is thus: C_in\*H_k\*W_k (shape of a single kernel) * C_out (how many kernels there are)

the input activation has shape: C_in \* H_in \* W_in

the output activation has shape: C_out \* H_out \* W_out

- senza padding H_out e W_out sono uguali a : H_in - (H_k-1); W_in - (W_k-1);

### hyperparameters

the hyperparameters in a conv layers are:

- the number of kernels
- the size of the kernels
- the size of the padding (most typical choice is to avoid shrinking)

## Chaining conv layers

A convolutional layer is a special form of linear layer (we're just doing MADs).

Thus, to take advantage of depth by chaining multiple layers we need **to introduce non-linear activations (typically ReLU)**.

Moreover, to avoid shrinking the activations along the chain we may (zero)pad the input to each layer

## Receptive fields

the receptive field of an operator is the region of the input image that contributes to a single value (pixel) in the output image

in CNNs we have a sequence of conv layers

- the first layer detects **very local features** because the receptive field is very small
- the next layers depends on the receptive fields of the previous layers
  - i layer successivi considerano attivazioni che riassumono la receptive field in una posizione nel layer precedente
  - il receptive field di un layer successivo considera più attivazioni e quindi è come se considerasse un receptive field più grande nel layer precedente

**moving across the layers makes the receptive field grow**

- the first layers detect very local features
- moving away from the initial layers makes the receptive field grow, this means that the kernels of the deeper layers detect larger and larger features
- **from local to global features**

OSS: ricorda che le features che vengono rilevata sono definite dal processo di ottimizzazione con gradient descent e backprop

NB: c'è una formula per capire la size del receptive field del L-esimo layer

Receptive field grows linearly... this is a **slow growth**

- if we wanted a big receptive field we would need a lot of conv layers

**How can we accelerate the growth of the receptive field?**

- facciamo come abbiamo gia visto in classical computer vision -> downsampling
- **To obtain larger receptive fields with a limited number of layers we down-sample the activations.**
- a downsampling of 2 doubles the receptive field of the next layer

there are different ways to realize this downsampling

### strided convolution

Sparse convolution computed at strided position

- invece di calcolare una convoluzione per ogni posizione nell'input image
- calcolo una convoluzione ogni stride (es 2) posizioni/pixel

I pesi della convoluzione (learned) decidono cosa preservare dell'intorno

### Pooling layers

In alternativa, possiamo continuare a fare una dense convolution, e fare downsampling aggregando dei neighbourhood

- max pooling: consideriamo l'attivazione massima nel neighbourhood
- avg pooling: computiamo un nuovo valore come media del neighbourhood

The pooling kernel is applied **channel-wise and with a stride (s>1)** to get a down-sampled output.

- Spesso un 2x2 neighbourhood con stride 2 (considero non overlapping finestre 2x2) con max-pooling
  - con questa configurazione abbiamo un downsampling di un fattore 2

iperparametri del pooling layer

- dimensione del pooling kernel
- pooling function
- stride

We can think of max-pooling as a way for the network to ask whether a given feature is found anywhere in a region of the image.

- it then throws away the exact positional information. As it isn't as important as its presence

### strided convolution vs pooling

In pooling there are no learnable parameters

Strided convolution can be seen as a learned downsampling

Uno non è migliore dell'altro

- con strided convolution ho più flessibilità dato che il downsampling non è fisso ma viene imparato (model capacity maggiore), ma più rischio di overfitting
- con pooling il contrario

**altra scelta di iperparametro**, si decide usando il validation set quello che da le performance migliori

# Final CNN architecture

The general pattern, as we move throug conv layer to conv layer, is that:

- the spacial size decreases
  - larger receptive field as we move thorugh the conv layers
  - we consider more global/general features in the deeper layers
- while the depth increases
  - we consider more features
  - there aren't as many local features (edges, corners, ...) as there are global features (eye, mouth, ...)
    - with a larger receptive field there are more interesting patterns

We flatten the final activations and process them with one or more **FC layers**

- now that the size of the input image is small this is feasible without too many parameters
- ricorda global average pooling per gestire i molti canali

The final layer is the **classifier**, the previous layers are all **feature extractors**

- the final layer that does the classification is linear since we've done all the feature extraction and we just need to linearly discriminate the classes

Il penultimo vettore (prima dell'output finale del classificatore) viene chiamato **representation vector**

- questo vettore riassume tutte le feature dell'immagine

**NB**: sembra che una buona idea sia mettere gli FC layers alla fine della rete dopo che si sono computate delle feature generali con vari conv layers

- innanzitutto, gli fc layers alla fine diventano fattibili dato che l'input è stato shrinkato a sufficenza da non richiedere un numero ridicolo di parametri
  - (il numero di canali tende a crescere, però di solito si applica global average pooling)
- more importantly, gli FC layers hanno un ruolo di ricombinazione delle feature globali detected alla fine dei layer convoluzionali
  - (ho delle attivazioni di una bocca, due occhi, un naso -> ricombino per ottenere un'attivazione di un volto umano)

Introduciamo anche come termini:

- backbone
  - la parte della rete che fa representation learning e quindi che **impara feature utili**
- (classification) head
  - la parte della rete che produce la produzione finale (task-specific)

Distinguere queste due parti è utile considerando **transfer learning**

- la backbone può essere pretrained, riconosce feature utili per una varietà di task
- possiamo allenare una head per i nostri obiettivi task-specific
  - la head impara a ricombinare le feature riconosciute dal backbone per raggiungere i nostri scopi

vedi meglio dopo

## CNN parameter and FLOP count

A network architecture with the same performance as another one, but with fewer parameters is preferable

- requires less FLOPs
  - faster training and inference
- less model capacity and less prone to overfitting

**conv layers**

- require less parameters
- require more FLOPs since they process big tensors
- C_out * (C_in\*H_k\*W_k) parameters
  - numero di kernel * dimensione del singolo kernel
- (H_out\*W_out) \* ( C_out \* (C_in\*H_k\*W_k) \* 2 ) FLOPs
  - ogni pixel dell'immagine di output viene computato dalla convoluzione per un kernel, questo richiede una moltiplicazione e una somma, e viene fatto per C_out immagini di output

**FC layers**

- require more parameters
- require less FLOPs
- abbiamo che ogni neurone nel layer di output è collegato a tutti i neruoni nel layer di input
  - N = D_in * D_out
- ogni attivazione di un neurone nel layer di output è data una somma pesata (dot product con riga di W) delle attivazioni del layer di input
  - FLOPs = D_out * (2\*D_in)

**OSS**: solitamente la definizione di nuove architetture è incrementale, nel senso che si tende a mantenere tutto uguale se non per alcune modifiche che si vuole dimostrare siano migliorative

- altrimenti non si saprebbe a cosa ricondurre un aumento delle performance

# esempi di reti

## Lenet

normalization of the input is always done because of numerical reasons (the optimizer works better)

usa sparse connections con i canali di input nel secondo conv layer

## Alexnet

breakthrough multipli

- gpgpu discovered
- big dataset
- cnn funzionano
- massive data augmentation per evitare overfitting del (primo) modellone grande che avevano costruito
  - senza data augmentation il modello couldn't be trained con il solo 1M di immagini, overfitting assurdo

the input images had different sizes

- they were rescaled to the same size
- how do you do that?
- we keep the aspect ratio
  - the smallest lato defines the amount of rescaling
  - both sizes get rescaled
  - the larger size gets cropped

utilizza model (prediction) ensembling dato alla rete più input per immagine in ingresso

**notion of a stage**

- 3 conv layer di file con kernel 3x3 sono equivalenti a un singolo conv layer con kernel 7x7
- tuttavia, 3 conv layer separati sono meglio dato che abbiamo meno parametri e flop (scala con n^2) e introduciamo più non linearità il che aumenta l'espressività

## VGG (visual geometry group)

vgg were able to go very deep with their network (19 layers)

it showed that going deep helps performance (if you can train the network)

it also showed how to build deep networks with a very **regular design**

- 3x3 conv layers with S=1, P=1
  - padding preserva la dimensione dell'immagine di output
- 2x2 max-pooling, S=2, P=0
- \#Filters (\#channels) double after every pool
  - quando shrinkiamo compensiamo con più profondità

Idea of **stages**: a chain of layers that process activations at the same spatial resolution (stessa dimensione dell'input)

- (conv-conv-pool, conv-conv-conv-pool and conv-conv-conv-conv-pool)
  - stesso motivo di alexnet
  - potremmo utilizzare un'unica convoluzione con un receptive field più grande...
  - ... ma, così facendo, abbiamo meno parametri, FLOPs e introduciamo più non linearità
- we build a network by stacking stages
- after a bunch of stages we have some FC layers

VGG-16 -> 16 numero di learnable layers
VGG-19 -> ha 19 learnable layers

Siccome questa archietttura è molto profonda, è suscettibile all'instabilità del gradiente durante il training

- per risolvere il problema hanno sfruttato, inizialmente, tecniche di pretraining per inizializzazione della rete
- in seguito si sono poi scoperte tecniche di inizializzazione che funzionano anche senza fare pretraining con modelli meno profondi

# Global Average Pooling

We've seen that most of the parameters of a network reside at the interface between the last conv layer's activations and the first fc layer

Global average pooling is a way to reduce the number of parameters (and thus the FLOPs) at this interface

- the last conv layer produces many small activation maps (something like 512\*3\*3)
- if we don't do anything we flatten this activations into a vector and FC with every neuron of the next FC layer
- to reduce the number of parameters we just do a avg-pool/max-pool across the channels
  - this way the flattened input vector of activations becomes 512 elements long instead of 512\*3\*3

Ha senso

- abbiamo detto che gli FC layers hanno un ruolo di ricombinazione delle feature globali detected alla fine dei layer convoluzionali
  - globali perchè gli ultimi conv layer hanno un receptive field grande
- **ci interessa solo la presenza o meno delle feature globali**, non tanto dove siano
  - perdere l'informazione spaziale non ci interessa per le feature globali
  - l'informazione spaziale è utile per arrivare alle feature globali
    - se devo riconoscere un volto umano, voglio 2 occhi sopra un naso che sono sopra ad una bocca
    - questo significa che il filtro che riconosce i volti umani dorà:
      - pesare molto in alto il canale di input relativo agli occhi
      - dovrà pesare molto in mezzo il canale di input relativo al naso
      - dovrà pesare molto in basso il canale di input relativo alla bocca
