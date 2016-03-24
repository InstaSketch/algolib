config = {
    "img_types": ['.JPEG', '.JPG', '.jpg', '.png', '.jpeg', '.bmp', '.dcx', '.gif', '.pcx', '.ppm', '.psd', '.tga', '.tif', '.tiff', '.xpm'],
    "bow_dictionary_size": 200,
    # 8 bins for H, 12 bins for S, 3 bins for V
    # "color_histogram_bins": (8,12,3),
    "color_histogram_bins": (5, 8, 3),
    "compression_level": 3,
    "distance_metrics":  {'chisqr': 1, 'intersect': 2, 'bhattacharyya': 3, 'chisqr_alt': 4}
}
