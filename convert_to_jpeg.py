from pdf2image import convert_from_path
import concurrent.futures
from tqdm import tqdm
import multiprocessing

cores = multiprocessing.cpu_count()
import glob

out = r'.\bridge_out'
files =glob.glob(r'.\bridge\*')
print(len(files))

# function that converts pdfs to jpegs
def convert_to_jpg(path):
    pages = convert_from_path(path, poppler_path=r'.\poppler-0.68.0\bin')
    file_name = path.split('\\')[-1].strip('.pdf')
    for num, page in enumerate(pages):
        page.save(f'{out}\{file_name}-{num}.jpg', 'JPEG')



def run(f, my_iter):
    with concurrent.futures.ThreadPoolExecutor(max_workers=cores) as executor:
        results = list(tqdm(executor.map(f, my_iter), total = len(my_iter)))


run(convert_to_jpg, files)
