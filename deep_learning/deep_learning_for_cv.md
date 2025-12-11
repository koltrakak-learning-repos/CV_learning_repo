**FC layers are very BAD at processing images!**

We want our layers, given an input image, to output a different image where some kind of feature is highlighted (the pixels where the feature is present receive a high score)

If we use FC layers, **the number of parameters and the number of FLOPs required to compute a single feature map is ridicolous**

What is the main reason that having a high number of parameters is bad?

- we're sure to overfit
- remember, overfitting depends on model capacity vs training data
  - if the training data is small wrt the model capacity, the model memorizes every bit of the training data and we're sure to overfit

# Convolutional layers

Differences of conv layers from fc layers:
    - here we don't flatten the image into a vector
        - the input and output of this layers are both 2d
    - instead of connecting every output pixel with every input pixel, we connect it with only its neighbourhood in the input image
        - this is called a **local receptive field**
        - in FC layers we would have global receptive fields
    - we reuse the same set of weights for every
        - **shared weights**

in summary a conv layer has two properties:

- local receptive fields
- and shared weights

**Inductive biases**:

Conv layers embody inductive biases dealing with the structure of images: pixels exhibit informative local patterns that may appear everywhere across the image

we want to apply constraints to accelerate training

- local receptive fields make sense because features are usually detectable looking only at a neighbourhood of a pixel
- shared weights make sense because we want to detect a feature everywhere inside an image
  - translation invariance in feature detection

This is called a convolutional layers because to compute the feature map we're just doing a convolution

- here though the kernel is learned during training and not decided a priori

the number of parameters is fixed, but the number of FLOPs depends on the size of the output feature map

## Multiple input channels

if the image has multiple channels (color images) should we use the same kernel for all the channels?

- no, this would be an inductive bias, and there isn't a reason to apply it

di conseguenza, con multiple channels abbiamo un kernel tridimensionale (tensore) per la nostra convoluzione

l'output della convoluzione continua ad essere un singolo pixel

### Why do we need biases?

nell'applicare la convoluzione abbiamo di nuovo anche un bias

we've already discussed the importance of non linearity for learning important features. The output of conv layers will need to be passed through an activation function (ReLU or whatever else)

the activation (non-linear) functions trigger at zero. **By using biases we allow more freedom in the weights**

- we can make the activation trigger at b and not zero
- this increases model capacity

### output activations/feature maps

output activations are smaller than the input image because at the borders we don't have the neighbourhs

to avoid shrinking the activations too much throughout the many conv layers of a model, we usually use padding the preserve size

## Multiple output channels

there's no reason to restrict ourselves to detect only one feature in a conv layer

the filters of a conv layers detect different features but they all have the same shape

**the number of filters of a conv layers determines the depth of the output activation and its an hyperparameter**

- we can see the output of a convolutional layer as an image (it has a 2d structure) with a number of channels defined by the number of kernels in the conv layer

# General structure of a conv layer

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

- senza padding H_out e W_out sono uguali a : H_in - (H_k-1); stessa cosa per W_out

### hyperparameters

the hyperparameters in a conv layers are:

- the number of kernels
- the size of the kernels
- the size of the padding (most typical choice is to avoid shrinking)

## Chaining conv layers

A convolutional layer is a special form of linear layer. Thus, to take advantage of depth by chaining multiple layers we need **to introduce non-linear activations (typically ReLU)**.

## Receptive fields

the receptive field of an operator is the region of the input image that contributes to a single value (pixel) in the output image

in CNNs we have a sequence of conv layers

- the first layer detects **very local features** because the receptive field is very small
- the next layers depend on the receptive fields of the previous layers

**moving across the layers makes the receptive field grow**

- the first layers detect very local features
- moving away from the initial layers makes the receptive field grow, this means that the kernels of the deeper layers detect larger and larger features

OSS: ricorda che le features che vengono rilevata sono definite dal processo di ottimizzazione con gradient descent e backprop

NB: c'è una formula per capire la size del receptive field del L-esimo layer

- receptive field grows linearly... this is a **slow growth**
- if we wanted a big receptive field we would need a lot of conv layers
- there is something suboptimal in having only

## how can we accelerate the growth of the receptive field?

facciamo come abbiamo gia visto in classical computer vision -> downsampling

a downsampling of 2 doubles the receptive field of the next layer

there are different ways to realize this downsampling

### strided convolution

sparse convolution computed at strided position

### Pooling layers

facciamo una dense convolution, consideriamo dei neighbourhood e prendiamo uno di questi pixel (max pooling) oppure ne computiamo uno nuovo (avg pooling)

- anche i pooling layers hanno uno stride

what about the depth?

- per ogni canale prendiamo uno delle attivazioni nel canale

spesso un 2x2 neighbourhood con stride 2 (considero non overlapping finestre 2x2)

- con questa configurazione abbiamo un downsampling di un fattore 2

### strided convolution vs pooling

in pooling there are no learnable parameters

strided convolution can be seen as a learned downsampling

uno non è migliore dell'altro

- con strided convolution ho più flessibilità dato che il downsampling non è fisso ma viene imparato (model capacity maggiore), ma più rischio di overfitting
- con pooling il contrario

altra scelta di iperparametro, si decide usando il validation set

# final CNN architecture

the spacial size decreases, the depth increases

we flatten the final activations and process them with one or more **FC layers** (now that the size of the image is small)

the final layer is the classifier, the previous layers are all feature extractors

il penultimo vettore (prima dell'output finale del classificatore) viene chiamato **representation vector**

- questo vettore riassume tutte le feature dell'immagine

##

a network architecture with the same performance as another one, but with fewer parameters is preferable

- requires less FLOPs
  - faster training and inference
- less model capacity and less prone to everfitting

conv layers

- require less parameters
- require more FLOPs since the process big tensors

FC layers

- the opposite

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

notion of a stage

- 3 conv layer di file con kernel 3x3 sono equivalenti a un singolo conv layer con kernel 7x7
- tuttavia, 3 conv layer separati sono meglio dato che abbiamo meno parametri e flop (scala con n^2) e introduciamo più non linearità il che aumenta l'espressività
