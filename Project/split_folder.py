import split_folders
from configurations import *
# Split with a ratio.
# To only split into training and validation set, set a tuple to `ratio`, i.e, `(.8, .2)`.
OUTPUT_DIR = os.path.join(ADMIN_DIR, "Output")
split_folders.ratio(DATASET_DIR, output=OUTPUT_DIR, seed=1337, ratio=(.8, .2)) # default values