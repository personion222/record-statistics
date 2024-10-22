import numpy as np
import cv2

METRIC_COUNT = 7
METRIC_NAMES = [
    "hue",
    "saturation",
    "value",
    "edginess",
    "iqr_contrast",
    "stddev_contrast",
    "hist_colors"
]


def iqr(arr: np.array) -> int:
    return np.subtract(*np.percentile(arr, (75, 25)))


def get_hist(points: np.array, range: tuple[int, int], map_len: int) -> np.array:
    map = np.empty(map_len)
    point_range = range[1] - range[0]
    point_width = round(point_range / len(map))

    for point in points:
        band = point % point_width
        map[band] += 1

    return map / np.max(map)


def DoG_edge(img: np.array, rad: int) -> np.array:
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (rad, rad), 0).astype(np.int16)

    diff = np.abs((gray - blur).astype(np.int16)).astype(np.uint8)
    return diff


def get_metrics(img: np.array) -> list:
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV_FULL)
    img_color = cv2.cvtColor(cv2.resize(img, (1, 1), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2HSV_FULL)[0][0]
    edginess = int(np.average(DoG_edge(img, 3)))
    iqr_contrast = int(iqr(hsv[:, :, 2].flatten()))
    stdev_contrast = int(np.std(hsv[:, :, 2].flatten()))
    color_points = np.sort(hsv[:, :, 0].flatten())
    color_hist = get_hist(color_points, (0, 255), 16)
    hist_colors = round(np.sum(color_hist))

    return [
        str(img_color[0]),
        str(img_color[1]),
        str(img_color[2]),
        str(edginess),
        str(iqr_contrast),
        str(stdev_contrast),
        str(hist_colors)
    ]
