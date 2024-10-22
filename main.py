import scrape_image as si
import img_proc as ip
import numpy as np
import csv

np.set_printoptions(edgeitems=8)

data = list()

album_reader = open("albums.csv", mode='r')
csv_reader = csv.reader(album_reader)
for row in csv_reader:
    data.append(row)

headers = data[0]
content = data[1:]

ncsv = np.empty((len(data) + ip.METRIC_COUNT, len(data[0]))).tolist()
ncsv[0] = headers + ip.METRIC_NAMES

for idx, point in enumerate(content):
    name = f"{point[2]} {point[3]}"
    print(name)
    try:
        img = si.get_img(name, (128, 128))
        metrics = ip.get_metrics(img)
        row = point + metrics
        print(' '.join(row) + '\n')
        ncsv[idx + 1] = row

    except Exception:
        pass


album_writer = open("albums_img.csv", mode='w', newline='')
csv_writer = csv.writer(album_writer)
for row in ncsv:
    csv_writer.writerow(row)
