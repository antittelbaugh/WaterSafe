from skimage.filters import threshold_mean
from skimage import io
from skimage.color import rgb2gray, label2rgb
from skimage.measure import label, regionprops_table
from skimage.morphology import closing
import matplotlib.pyplot as plt
import pandas as pd

fig, (ax1, ax2) = plt.subplots(1, 2)
img=io.imread('MP_PA_1.jpg')
img = rgb2gray(img)
thresh=threshold_mean(img)
bw=closing(img > thresh)
label_image = label(bw)
labeled_img = label2rgb(label_image,image=img,bg_label=0)
io.imshow(labeled_img)
props = regionprops_table(label_image,properties = ['label','feret_diameter_max'])
df = pd.DataFrame(props)
df['feret_diameter_max'] = df['feret_diameter_max'] * .58
df = df[df['feret_diameter_max'] >= 17.24]
hist = plt.hist(df['feret_diameter_max'],bins=10,edgecolor='black')
plt.xlabel('Size (um)')
plt.ylabel('Frequency')
plt.title('Size Distribution')
plt.show()
