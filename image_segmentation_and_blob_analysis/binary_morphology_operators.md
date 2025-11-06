binarization may leave out some mistakes:

- false positives: background pixels classified as foreground
- false negatives: foreground pixels classified as background

binary morphology operators are operators thatn handle these mistakes

- they take as input: a binary image and a kernel
- they ouotput a new processed binary image

they look pretty much like filters

- kernels are instead called structuring elements

## Dilation

the structuring element is translated over all black pixels

dilation is useful because it recovers pixels not detected as foreground while they should've been (false negatives)

## Erosion

erosion translates the structuring element everywhere in the image

erosion shrinks the foreground, this means that it helps recovering false positives, background pixels classified as foreground

**NB**: ci sono degli operatori/filtri che sono troppo sofisticati (inutilmente computazionalmente costosi) per una binary image

- ad esempio, se volessi i countours di una binary image, **sarebbe un errore applicare un sobel filter** quando basta applicare erosion e sottrarre.

## Opening and Closing

Opening and closing can be understood as more focused versions of erosion and dilation

- opening is like erosion in the sense it removes foreground pixels
- closing is like dilation in the sense it removes background pixels
- let's consider Opening, by smart erosion we mean that we can choose to cancel out pieces of foreground selectively

opening is like matching all the possible parts of the foreground that match exactly the structuring element

- union of translation of structuring elements

there exists a duality between opening and closing. Closing can be understood as opening the background

- we throw away the background pixel (equivalente ad aggiungerli nel foreground) that don't match exactly the FLIPPED structuring element

**NB**: opening and closing sono operatori idempotenti; applicarli 10 volte è equivalente applicarli una sola volta

nota: more often that not we're gonna be using opening and closing instead of erosion and dilation because they
