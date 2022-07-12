# takes tiff images and converts them into pdf
# this made going through old microfish files at work much easier
# would be cool to be able to index the files someday
from PIL import Image, ImageSequence
import os
import multiprocessing as mp
from tqdm import tqdm
import glob
import gc
import shutil

Image.MAX_IMAGE_PIXELS = 100000000000    # supresses and buffer overflow warning
CORES = 2

SAVE_PATH = 'C:\micro_out'

files = glob.glob(r'C:\Microfiche Scans\*\*.tif')


# found like half of this on stackoverflow
def tiff_to_pdf(tiff_path):
    #print(tiff_path)
    images = []
    pdf_path = tiff_path.replace('.TIF', '.pdf')
    name = pdf_path.split('\\')[-1]
    folder = pdf_path.split('\\')[-2]
    pdf_path = SAVE_PATH + '\\' + folder + '\\' + name
    #print(pdf_path)
    if not os.path.exists(tiff_path): raise Exception(f'{tiff_path} does not find.')
    open_image = Image.open(tiff_path)

    
    for i, page in enumerate(ImageSequence.Iterator(open_image)):
        page = page.convert("RGB")
        images.append(page)
    open_image.close()
    if len(images) == 1:
        #print(pdf_path)
        images[0].save(pdf_path)
    else:
        images[0].save(pdf_path, save_all=True,append_images=images[1:])
        #print(pdf_path)
    #shutil.rmtree(tiff_path)
    os.remove(tiff_path)
    del images
    del open_image
    del page
    gc.collect()    

progress = tqdm(files, unit = 'files')
for file in progress:
    name = file.split('\\')[-1]
    progress.set_postfix_str(name)
    tiff_to_pdf(file)


# not enough ram to use multiplecores
'''
if __name__ == "__main__":


    pool = mp.Pool(CORES)

    for _ in tqdm(pool.imap_unordered(tiff_to_pdf, [file for file in files]), total = len(files)):
        pass

        pool.close()

'''
