What CV problems we must use ML for (per forza)?

Problems with a high variability

consideriamo image classification

we can't handwrite the classification function

- it's too complex
- there would be no end to else blocks

but we can learn it

how much data do we need to learn this function?

- no answer
- the more the better
  - the more data we have the more we can capture variability

# General concepts about machine learning

- the test set is just a proxy for the real world to evaluate how well the model is gonna perform when deployed

- in traditional (shallow) learning for CV, the inputs aren't raw data but features that were chosen as relevant
- in deep learning for CV, the inputs are the raw data and the relevant features are learned

- the meaning of "learning a classification function" is learning the parameters of a chosen family of functions
  - we don't explore the space of all functions
  - we explore the parameter space of a family of parametric functions
  - the chosen family of functions is defined by the chosen ML model

- to learn the parameters we need to solve an optimization problem
  - loss function measures the performance of the current configuration of parameters of the model **on the training data**
  - learning == minimizing the loss function
  - **NB**: usually the whole loss function can be expressed as a function of per sample (training example) losses

- hyperparameters are hand-chosen and not learned as the parameters

- model capacity measures how powerful the model is
  - the higher the capacity, the higher the ability of the model to optimize the loss and learn the training set (fit the training data)
  - in polynomial regression, a regressor of degree 10 has a higher capacity than a regressor of degree 5
  - **NB**: si potrebbe pensare che a questo punto convenga scegliere gli iperparametri in maniera tale da massimizzare la model capacity.
    - SBAGLIATO! questa strategia non porta a generalizzare al training set
    - stiamo overfittando gli iperparametri al training set.

- Per capire come scegliere gli iperparametri abbiamo bisogno di un segnale che ci dica quanto stiamo riuscendo a generalizzare
  - Non possiamo utilizzare la loss sul test set per scegliere gli iperparametri.
  - Staremmo considerando la capacità del modello di generalizzare per una singola determinata istanza di test set, ma questo non sarebbe significativo per la generalizzazione nel mondo reale
  - Dobbiamo quindi utilizzare un ulteriore set chiamato validation set

- generalization is about compression
  - the model can generalize if it can capture features that all cats have
  - not features that this image of a cat has

- Oltre a model capacity, l'altra manopola principale con cui ridurre overfitting è la quantità dei dati con cui fare training
  - più dati ho, minore è il rischio di apprendere peculiarità specifiche non generalizzabili dai dati
  - pensa alla regressione polinomiale, se ho più datapoint la forma della funzione che il mio modello deve approssimare diventa più chiara

- **NB**: overfitting è una funzione che dipende da model capacity e training data
  - con la stessa model capacity, e più training data, il modello sarebbe meno suscettibile ad overfitting
  - durante il training si osserverebbe più diversità nei dati, e quindi sarebbe più difficile specializzarsi (overfittare) su peculiarità di alcune istanze

- Per problemi difficili, abbiamo bisogno di modelli enormi (alta model capacity)
  - data la loro dimensione questi modelli sono in grado di imparare molto
  - tuttavia, sempre a causa della loro dimensione, sono anche suscettibili ad overfitting
  - per questo motivo modelli grandi hanno anche bisogno di training set grandi
  - (questo è stato uno dei breakthrough nel deep learning: capire che si ottengono performance molto migliori utilizzando più dati e modelli più grandi)

# Regularization

Non è sempre possibile tornare indietro e ridurre la dimensione del modello (capacity) una volta che ci si è accorti che c'è dell'overfitting.

- bisognerebbe rifare il training
- magari poi si riduce troppo la dimensione, o non la si riduce abbastanza

Per questo motivo è più comune utilizzare un modello con una capacità più alta rispetto allo stretto necessario (prone to overfitting) e applicare delle tecniche di regularization per evitare overfitting

Con la loss penalty (che dipende solamente dai parametri del modello) esprimiamo una preferenza sui valori dei parametri

- tipicamente preferiamo dei parametri piccoli in magnitude.
- Perchè?
  - riduce il search space dei parametri. Non devo controllare parametri grandi dato che vengono penalizzati troppo
  - non possiamo scegliere la configurazione perfetta dei parametri che fitta perfettamente il training set. Questo riduce overfitting

Applicare regularization, in un certo senso, riduce la model capacity

- più è alto lambda più riduciamo la model capacity

NB: Chiaramente, dobbiamo configurare lambda cercando il valore che minimizza l'errore nel validation set (come con tutti gli altri iperparametri)

## Data augmentation

anche queste possono essere considerate regularization techniques, dato che riducono overfitting (più dati nel training set -> aumento training error, riduco validation (generalization) error)

# Linear Image classifiers

## Naive classifier

output continui non vanno bene

the class values are categorical values

we cannot measure the error of the classifier well by just comparing the output of the model with the ground truth

- we would weigh the mistakes differently just on the different numbers given to the labels
- any mistake is more or less the same
- 9 is not more wrong than 1 if the label should've been 2

**conclusione**: we CANNOT predict a categorical variable as if it were a continuous variable. We need another approach

## a better (Linear) classifier

Now our classifier doesn't output directly the categorical label.

Now it outputs a vector of scores

- one score for every possibile class
- the higher the score of a class the higher the chance of the image belonging to that class
- we take as the prediction the class with the highest score

### Linear classification as template matching

molto interessante notare che il classifier che abbiamo visto sopra è interpretabile come un'istanza di template matching in cui **i template delle varie classi (righe di pesi) vengono imparati durante il training**

notiamo nuovamente, con ML non dobbiamo più definire a priori i parametri dell'algoritmo (template), come facciamo in classical, CV ma questi vengono imparati

- l'underlying computation però è la stessa

**NB**: this approach is still linear (or affine, doesn't matter), and for this reason doesn't work well

- we're going to substitute linear-models with neural networks (which are just linear functions followed by a non-linear transformation organized in layers)
  - OSS: with non-linear functions biases are more significant

# Loss functions

how can we train a linear classifier?

**NB**: ricorda che usiamo sempre loss functions che sono la somma/media di per sample losses.

- We don't need to compute the whole training set to get the loss
- We can compute the loss incrementally (utilie per SDG)

## Softmax

We prefer, for the sake of TRAINING (in inferenza non ci interessa) the classifier, to convert the unnormalized scores (logits) to probabilities with the softmax function

- the exp function really highlights the difference between the scores, accentuando di molto lo score maggiore
  - per questo si chiama softmax, da praticamente tutto al massimo e poco al resto
- inoltre elimina score negativi
- otteniamo una distribuzione di probabilità in output

## Crossentropy loss

```
in information theory crossentropy captures the average surprise you get by observing a random variable governed by distribution P, while believing in its model Q

- H(p, q) = sum_states(p_s * log(1/q_s))
- È UNA SORTA DI DISTANZA TRA DISTRIBUZIONI DI PROBABILITÀ
- se il modello è perfetto -> q_s = p_s per ogni stato s -> crossentropy = entropy
```

A loss function is a comparison between the prediction of the model and the ground truth and should capture the discrepancy between the two.

- the lower the loss the more the two are similar

With softmax our prediction is a probability distribution. The ground truth, in turn, is another probability distribution with a probability of one assigned to the correct class and zero elsewhere (one-hot vector)

- we want a loss that gets lower as the probability given to the true class gets higher
- we use -log(x) as a per-sample loss; con x = probabilità della true class

```Domanda che capita spesso all'esame:
dato un vettore di output di un modello, qual'è il valore della cross-entropy loss?

importante far presente che dipende dalla true class
```

la loss dell'intero training set è data dalla somma delle per-sample losses -> questa è la cross-entropy loss

- this loss is trying to minimize the distance between the true distribution and the learned distribution (on a per sample basis ?)

OSS: durante il training abbiamo bisogno si un layer di output in cui applichiamo softmax in maniera tale da fare training con crossentropy.

- In inferenza non qusto softmax layer non è necessario
- possiamo prendere l'output più grande nel vettore
- softmax is there to compute crossentropy loss

### special case of binary cross-entropy loss for binary classifiers

with a multiclass classifiers

- i output a vector of s-scores
- and train with the crossentropy loss

with a binary classifier

- i output a single of s-score
- and train with the binary crossentropy loss

we could also use softmax and use two scores, but it's an unneded overparameterization

# Gradient descent

the loss is not a convex function

- there are many local minima

the goal of training is finding a good local minima not the global one (too hard)

- empiracally we have found that these loss functions have many good local minima. The situation is not too grim

how long should be the gradient step?

- this is a key-hyperparameter
- the gradient gives us a local information (we know that localy the function is decreasing)
- this means that we should take a small step, this way we're sure that we're moving to a point where the loss decreases

## Learning rate

too small of a learning rate requires too many iterations to train

**NB**: too high of a learning rate and we start jumping back and forth around a minimum

- the loss gets stuck at a certaing value

## batch vs stochastic gradient descent

we've said that in deep learning the models are big, and so the training set is large as well

this means that processing the whole training set just to compute a single gradient step makes the training too slow

for this reason we approximate BGD with SGD

...

why can we consider a part of the training set?

- **we can compute a gradient term per sample**
- with the whole training set we compute the best average gradient step
- with a small batch we can approximate this average gradient step

minibatch size is another CRITICAL hyperparameter (di solito un numero tra 16 e 256)

with SGD we update the parameters E*U times

## Beyond vanilla SGD

SGD is the most basic optimizer

there are many other, more complicated, optimizers that build on it

- momentum
- adaptive learning rate

# When do we stop training | Early stopping

We need to choose the epochs

It's not correct to decide when to stop training only looking at the training set

- we would go into overfitting

We should stop when there's no more improvement on the validation set -> this is called early stopping

**NB**: The model is chosen on the validation set, and is evaluated on the test set

# Limits of shallow linear classifiers

un shallow classifiers è linear classifier che abbiamo visto prima

- ha un solo layer di pesi
- fa template matching imparando tanti template quante sono le classi

this doesn't really work

## the importance of representation

**the main problem is that we're trying to solve classification by using only raw pixels as features**

guardiamo l'esempio nelle slide:

- if we keep the data as they come in the input space, **linear classification cannot happen**
- **NB**: but if we transform the data in a feature/representation space that better capture the differnce between the data, linear classification becomes possible

the choice of the space in which we perform classification is fundemental

## deep learning

in shallow machine learning the choice of the feature space is handcrafted

with deep learning the machine learning model learns:

- how to transform the raw data into a better feature space
- AND to classify the learned features

deep learning ~= representation learning

in deep learning we don't learn the representation in a single step, **we learn a higherarchy of representations**

### The importance of non linear functions

chaining linear transformations results in another linear transformation

- we could chain 1000 linear transformations and we wouldn't be able to do anything better than a single one
- the same  result could've been achieved with a single linear transfomration

![non linear transformations](img/non-linear_transformations.md)

**NB**: to be able to transform the features EFFECTIVELY (in a way that makes the learned features linearly separable) we need to be able to use non-linear functions inside the transformation layers

- this enables powerful representation learning
- vedi esempio

## Neural networks

le dimensioni dei vari layer (e quindi dei vettori di attivazione) sono iperparametri

### Shallow neural networks (diverse da shallow linear classifiers)

the smallest neural network

- has just one non-linear layer that does representation learning
- and one output layer that does the classification

### Activation functions

ReLU è la miglior activation function per deep learning

`ricorda di chiedere per i bias`

### FC layers

A neural network consisting of two or more FC layers is usually referred to as a **Multi-Layer Perceptron** (MLP).

### Universal approximation theorem

it is striking to discover that a NN with just one non-linear (hidden) can approximate any function to an arbitrary degree

- facciamo solo delle matmul
- the better the approximation, the higher the dimension of the hidden layer
