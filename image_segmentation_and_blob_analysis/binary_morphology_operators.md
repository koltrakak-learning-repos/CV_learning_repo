Binarization may leave some mistakes:

- false positives: background pixels classified as foreground
- false negatives: foreground pixels classified as background

Binary morphology operators are operators that handle these mistakes **they improve the binary image**

- they take as input: a binary image and a kernel
- they ouotput a new processed binary image

They look pretty much like filters

- we slide a kernel across the image to compute a new image
- kernels are instead called structuring elements

## Dilation

the structuring element is **translated over all black pixels** and computes the new image imprinting its shape at every translation

dilation is useful because it **recovers false negatives**, pixels not detected as foreground while they should've been

## Erosion

erosion translates the structuring element B **everywhere in the image** A and keeping only those pixels where B fits into the foreground of A.

erosion shrinks the foreground, this means that it **helps recovering false positives**, background pixels classified as foreground

**NB**: ci sono degli operatori/filtri che sono troppo sofisticati (inutilmente computazionalmente costosi) per una binary image

- ad esempio, se volessi i countours DI UNA BINARY IMAGE, **sarebbe un errore applicare un sobel filter** quando basta applicare erosion e sottrarre

## Opening and Closing

Opening and closing can be understood as more focused versions of erosion and dilation

Smarter operators to remove selectively from either foreground (opening) or background (closing) **those parts that do not match exactly the structuring element**.

- opening is like erosion in the sense it **removes foreground pixels**
- closing is like dilation in the sense it **removes background pixels**

non li capisco molto bene, interpretali così:

- Erosion followed by Dilation is known as Opening
- Dilation followed by Erosion is known as Closing

Analogie:

- Opening
  - l’erosione come far passare una pallina all’interno della forma
  - se la pallina non entra, quella parte sparisce
  - la dilatazione successiva non fa ricrescere ciò che è stato eliminato
- Closing
  - la dilatazione come gonfiare la forma
  - piccoli buchi e fessure si chiudono
  - l’erosione finale non riapre ciò che è stato sigillato

gli esempi non sono male per farsi un'idea

There exists a duality between opening and closing.

- Closing can be understood as opening the background
- we throw away the background pixel (equivalente ad aggiungerli nel foreground) that don't match exactly the FLIPPED structuring element

**NB**: opening and closing sono operatori idempotenti; applicarli 10 volte è equivalente applicarli una sola volta

Nota: more often that not we're gonna be using opening and closing instead of erosion and dilation
