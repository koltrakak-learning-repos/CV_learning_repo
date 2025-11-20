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
