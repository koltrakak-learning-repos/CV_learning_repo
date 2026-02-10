import cv2
import numpy as np
from matplotlib import pyplot as plt
from pprint import pprint
import time

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parse_dataset_config(path):
    config = {}

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # salta righe vuote

            key, value = line.split() # split della linea ad ogni whitespace
            if is_int(value):
                config[key] = int(value)
            else:
                config[key] = value

    return config






def compute_cost_volume(im_ref, im_target, disparity_range, window_size):
    h, w, c = im_ref.shape
    cost_volume = np.zeros((h, w, len(disparity_range)), dtype=np.int32)

    for i, d in enumerate(disparity_range):
        shifted = np.zeros_like(im_target, dtype=np.int32)

        if d == 0:
            shifted = im_target
        elif d > 0:
            # Se disparità>0, l'immagine di riferimento è quella di destra, e le
            # corrispondenze vanno cercate nell'immagine di sinistra sulla destra.
            # Per allineare le posizioni tra immagine di riferimento e target, shifto
            # l'immagine target verso sinistra di d posizioni
            shifted[:, :-d] = im_target[:, d:]
        else:
            # Se disparità<0, l'immagine di riferimento è quella di sinistra, e le
            # corrispondenze vanno cercate nell'immagine di destra sulla sinistra.
            # Per allineare le posizioni tra immagine di riferimento e target, shifto
            # l'immagine target verso destra di d posizioni
            shifted[:, -d:] = im_target[:, :d]

        # calcolo le differenze punto punto che dovrò poi aggregare con la SAD
        diff = np.abs(im_ref - shifted) # (H, W, C)
        # boxFilter() non mi accetta ksize=(window_size, window_size, c)
        # quindi devo fare questo ulteriore step in cui sommo lungo la
        # direzione dei canali
        diff = np.sum(diff, axis=-1) # (H, W)

        # Date le differenze, posso calcolare le SAD di tutti
        # i punti con una convoluzione per box-filter.
        # Calcolo le somme con box filter dato che usa uno
        # schema incrementale (integral images) grazie al
        # quale la complessità per effettuare la somma in
        # una finestra diventa O(1) invece che O(k^2)
        sad = cv2.boxFilter(
            diff,
            ddepth=-1, # uso lo stesso tipo di dato in ingresso (int)
            ksize=(window_size, window_size),
            normalize=False # voglio solo la somma e non la media
        ) # (H, W)

        # l'i-esimo layer del cost volume è composto dalle sad di
        # tutti i punti associate alla disparità i-esima
        cost_volume[:, :, i] = sad

    return cost_volume


def find_correspondence_fast(cost_volume, row, col, disparity_range):
    # la corrispondenza di un punto si trova nel minimo
    # della colonna corrispondente del cost volume
    costs = cost_volume[row, col, :]
    best_idx = np.argmin(costs)

    return disparity_range[best_idx]






def S(disparity_map, ground_truth, tolleranza, valid_mask):
    copy = disparity_map.copy()
    print(1, np.array_equal(copy, disparity_map))

    # Anche qui attenzione ad underflow dovuti a uint
    diff_map = np.abs(disparity_map - ground_truth)

    print(2, np.array_equal(copy, disparity_map))

    # non considero i punti non validi
    diff_map[~valid_mask] = 0
    error_mask = diff_map>tolleranza
    # converto i boolean risultanti dall'operazione logica in interi e sommo
    error_sum = np.sum(error_mask.astype(int))
    # gia che ci sono costruisco anche una mappa per visulizzare dove sto
    # commettendo degli errori
    error_map = np.zeros(diff_map.shape)
    error_map[error_mask] = diff_map[error_mask]

    return error_sum, error_map

def compare_to_gt(disparity_map, ground_truth, tolleranza, valid_mask):
    copy = disparity_map.copy()
    print(np.array_equal(copy, disparity_map))

    error_sum, error_map = S(disparity_map, ground_truth, tolleranza, valid_mask)

    print(np.array_equal(copy, disparity_map))

    n_valid = np.sum(valid_mask)
    error_percentage = error_sum/n_valid

    return error_percentage, error_map






def show_stereo_pair(left_image, right_image, name=None):
    plt.subplot(1, 2, 1)
    plt.title(f"Left image: {name}")
    plt.imshow(cv2.cvtColor(left_image, cv2.COLOR_BGR2RGB))

    plt.subplot(1, 2, 2)
    plt.title(f"Right image: {name}")
    plt.imshow(cv2.cvtColor(right_image, cv2.COLOR_BGR2RGB))

    plt.tight_layout()
    plt.show()

def show_disparity_map_and_groundtruth(disparity_map, groundtruth, error_map):
    plt.figure(figsize=(10,8))

    plt.subplot(1, 3, 1)
    plt.title("My Disparity Map")
    plt.imshow(disparity_map, cmap="gray", vmin=0, vmax=255)

    plt.subplot(1, 3, 2)
    plt.title("Ground Truth")
    plt.imshow(groundtruth, cmap="gray", vmin=0, vmax=255)

    plt.subplot(1, 3, 3)
    plt.title("Error Map")
    plt.imshow(error_map, cmap="gray", vmin=0, vmax=255)

    plt.tight_layout()
    plt.show()

def compute_and_evaluate_disparity_sad(path_dataset, window_radius, show_stereo_img=True, show_disparity_maps=True):
    """
    Calcola la disparity map di una coppia di immagini stereo e la confronta con una groundtruth.

    Args:
        path_dataset: path alla directory che conterrà la coppia stereo, la groundtruth
                      e il file di configurazione contenenti i parametri per l'algoritmo.
                      Nomi dei file, e contenuto del file di configurazione devono essere
                      coerenti con quanto specificato in consegna (altrimenti si rompe tutto
                      dato che non faccio alcun controllo)

        window_radius: raggio della finestra usata per calcolare le SAD.

    Restituisce una mappa contenente le seguenti chiavi:
        groundtruth: la groundtruth caricata

        disparity_map: la disparity map calcolata ignorando i pixel vicino bordi (che vengono impostati a zero)

        error_map: la differenza tra groundtruth e disparity map per i soli pixel di cui si è calcolato la
                   disparity (zona centrale). Differenze sotto al valore di tolleranza non vengono considerate.

        error_percentage: percentuale di errore tra la disparity map calcolata e la groundtruth,
                          considerando una tolleranza di 1 pixel.
    """

    ### Leggiamo la configurazione e costruiamo path vari
    # Scelgo il penultimo dato che ./StereoDataset/map/
    # produce ['.', 'StereoDataset', 'map', '']
    scene = path_dataset.split("/")[-2]
    path_config = path_dataset + "param_in.txt"
    config = parse_dataset_config(path_config)
    path_groundtruth = path_dataset + config["groundtruth"]
    path_im_left = path_dataset + "imL.ppm"
    path_im_right = path_dataset + "imR.ppm"

    ### Carichiamo le immagini
    im_l = cv2.imread(path_im_left)
    im_r = cv2.imread(path_im_right)
    if show_stereo_img:
        show_stereo_pair(im_l, im_r, name=scene)

    ### Capiamo dal file di configurazione qual'è l'immagine a cui la disparity map fa
    ### riferimento, e qual'è quella in cui andiamo a cercare le corrispondenze (target).
    ### Gia che ci sono converto da uint in int per evitare errori di underflow quando
    ### andrò a calcolare le SAD tra finestre.
    im_ref = None
    im_target = None
    if path_im_left.removeprefix(path_dataset) == config["ref"]:
        im_ref = im_l.astype(np.int32)
        im_target = im_r.astype(np.int32)
    else:
        im_ref = im_r.astype(np.int32)
        im_target = im_l.astype(np.int32)

    ### Costruiamo gli indici da considerare nella reference image
    h, w, c = im_ref.shape
    print(f"Reference image ha shape {im_ref.shape}")
    ignored_border_pixels = window_radius
    print(f"- ignoro {ignored_border_pixels} border pixels")
    start_row = ignored_border_pixels
    end_row = h-ignored_border_pixels
    start_col = ignored_border_pixels
    end_col = w-ignored_border_pixels
    end_col_strict = w-ignored_border_pixels-config["disp_max"]
    considered_rows = list(range(start_row, end_row))
    considered_cols = list(range(start_col, end_col))
    print(f"- considero le righe [{start_row}, {end_row}[ e le colonne [{start_col}, {end_col}[\n")

    disparity_range = range(config["disp_min"], config["disp_max"]+1)
    print(f"Le corrispondenze verranno cercate nel disparity-range [{config["disp_min"]}, {config["disp_max"]}]\n")

    ### Calcolo la disparity map
    disparity_map = np.zeros((h, w), dtype=np.int32)

    start = time.perf_counter()
    cost_volume = compute_cost_volume(im_ref, im_target, disparity_range, window_size)
    for row in considered_rows:
        for col in considered_cols:
            # disp = find_correspondence(im_ref, im_target, row, col, window_radius, config["disp_min"], config["disp_max"], ignored_border_pixels)
            disp = find_correspondence_fast(cost_volume, row, col, disparity_range)
            disparity_map[row, col] = disp*config["disp_scale"]
    t_exec=time.perf_counter()-start
    print(f"Tempo impiegato a calcolare la disparity map di {scene}: {t_exec:.2f} s")

    ### Valuto la disparity map nella zona in cui
    ### l'intero rage di disparità è disponibile
    groundtruth = cv2.imread(path_groundtruth, cv2.IMREAD_GRAYSCALE)

    tolleranza = 1
    # Ho interpretato la tolleranza in pixel, e non in pixel/disp_scale.
    # Per questo motivo scalo la tolleranza per il fattore con cui scalo
    # la disparità.
    tolleranza *= config["disp_scale"]

    valid_mask_strict = np.zeros_like(disparity_map, dtype=bool)
    valid_mask_strict[start_row:end_row, start_col:end_col_strict] = True

    if show_disparity_maps:
        show_disparity_map_and_groundtruth(disparity_map, disparity_map, disparity_map)

    error_percentage, error_map = compare_to_gt(disparity_map, groundtruth, tolleranza, valid_mask_strict)

    if show_disparity_maps:
        show_disparity_map_and_groundtruth(disparity_map, groundtruth, error_map)
    print(f"Nella zona in cui l'intero range di disparità è disponibile, la disparity map calcolata ha un errore pari al {error_percentage*100:.2f}%\n\n")

    return {
        "groundtruth": groundtruth,
        "disparity_map": disparity_map,
        "error_map": error_map,
        "error_percentage": error_percentage,
    }



base_path = "./StereoDataset/"
scenes = ["map/", "sawtooth/", "tsukuba/", "venus/"]

### ATTENZIONE: questo è un parametro molto importante!
### Per adesso lo imposto ad un valore aribtrario; a breve
### discuterò di come regolarlo
window_size = 7
window_radius = (window_size-1) // 2

results_basic_sad = {}

# for scene in scenes:
for scene in ["map/"]:
    path_dataset = base_path + scene
    res = compute_and_evaluate_disparity_sad(path_dataset, window_radius)
    results_basic_sad[scene] = res
