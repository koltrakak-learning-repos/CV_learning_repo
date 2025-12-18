# Residual Networks

abbiamo visto che vgg19 è migliore di vgg 16, che è migliore di vgg11, ...; **pur mantenendo la stessa architettura!**

going deeper suggests improved performance, but ...

with more layers we have more parameters and more capacity for the model -> we might worry about overfitting

However, **the deeper network also fits the training data worse than a shallower network**

- ma il deeper network ha più capacity, come è possibile?
- l'instabilità del gradiente non è il motivo dato che il rete di fatto sta imparando, non è stuck
- **le training performances, for some reason, degrade** -> training very deep networks turns out to be inherently hard -> **non c'è consenso sul motivo**

Notiamo che le performance del deeper network dovrebbero essere >= delle performance del shallower network

- una soluzione potrebbe essere tenere i layer del shallow network ed aggiungere degli identity layers che non fanno niente
- per qualche motivo l'optimizer non riesce trovare questa soluzione
- questo ha fatto pensare che una buona idea potesse essere rendere più facile per l'optimizer imparare questi identity layers -> residual learning

## Residual learning

we task the layer to learn not the H(x) function, invece imponiamo al layer di imparare la residual function

questo facilità la creazione di identity layers (basta mantenere i pesi del layer a zero)

...

[10:23] mi sono distratto sui residual blocks (che combinati vanno a formare uno stage)

### Batch norms

è una tecnica di normalizzazione

il batch è formato dai vari tensori in input (?)

la normalizzazione consiste in una channel-wise standardization combinata ad uno learned scale and shift factor

**NB**: il senso è di mantenere stabili i valori delle attivazioni per evitare gradient vanishing / explosion

- se normalizziamo l'input perchè non normalizzare anche le attivazioni intermedie
- i parametri di shift e scaling servono a ...

ad inference time sembra che non abbiamo i batch [guarda 10:33]

# ResNet architectures

di nuovo abbiamo architetture regolari in cui si combinano vari stages

parameter cheap dato che abbiamo un solo fc layer con global average pooling

`importante fare controllare i calcoli dei parametri e dei flop`

ResNets are a cheaper design that works much better

## problema shape

when we move from a stage to the next, skip connections creano tensori di attivazioni di shape diverse che non possono essere sommati rispetto al tensore in input

- questo perchè al primo layer degli stage facciamo downsampling e doubling of the number of channels

una prima soluzione è fare downsampling è padding

possiamo fare una projection skip connection applicando un convolution layer!

**oss**: this seems to defeat the purpose of making it easy to learn the identity

- however, it is still possible that the conv layer can learn the identity
- more importantly, the point of that intuition was to have a justification for a different kind of architecture
  - nobody has seen that some layers in ResNets do in fact learn an identity
  - empirically it just happened that ResNets perform better and can learn even in deep networks

guarda slide 38

- abbiamo conferma di quello che volevamo -> the deeper the better
- better validation error (solid) and better training error (dashed)

## bottleneck residual block

vogliamo diminuire i parametri dei blocchi

utilizziamo un solo 3x3 conv e due 1x1 conv (ricombinano across channels)

# favourite questions on CNNs

why do the activations get smaller and deeper?

- smaller because we want to recognize global features composed of more local features detected in the earlier layers
- this is the idea of **hierarchy of features**

why does it make sense that we need more features late than early in the network?

- because there are way more interesting complex features than simple features
- global features are inherently more than local features
- esempio che rende l'idea:
  - consideriamo una binary image
  - in un intorno 3x3 abbiamo 2^9 pattern
  - in un intorno 7x7 abbiamo 2^49 pattern

# Mobile net

they use grouped convolution

rather than having all kernels process all channels, we split the kernels into groups that process a subset of channels

why? cheaper

actually they use ...

mobile net v2 è una variante che non ci interessa -> saltiamo direttamente a transfer learning

# Transfer learning

sometimes we need a large capacity network because the problem we need to solve is complex

however we have only a small dataset

if we trained the large network with the small dataset we would surely overfit (the network will learn every detail of the training set)

What we can do is use our small dataset to finetune a pretrained bigger network that was already trained with a big dataset

## how do we adapt the downloaded pretrained model to our purposes?

we keep everything but the last layer, in altri termini il backbone

- se il modello è pretrained per imagenet abbiamo 1000 classi ma magari noi abbiamo bisogno di solo 10 classi

adesso abbiamo un pretrained backbone e un head di cui fare il training from scratch. Abbiamo due possibilità per il training (finetuning)

- possiamo fare il training del solo head mantenendo il backbone frozen
- oppure, possiamo fare il training di tutto
  - qua però dobbiamo fare attenzione all'overfitting
