import os
import pypexels
import requests
from keys import pexels_api_key

py_pexel = pypexels.PyPexels(api_key = pexels_api_key)

def select(search_term):

    results = py_pexel.search(query = search_term,page=1,per_page=25)
    pid=[]
    for img in results.entries:
        pid.append(img.id)
        used_ids = load_ids()
        x = random.choice(pid)
        while (x in used_ids):
            x = random.choice(pid)
        selected.append(x)    

def select_photos():
    for search_term in search_terms:
        select(search_term)
    print('Pexels stuff done!') 

def get_image_data(selected):
    for pid in selected:
        photo = py_pexel.single_photo(photo_id = pid)
        sources.append(photo.src.get('medium'))
        photographer.append(photo.photographer)
    return photo,sources,photographer

def get_images(sources):
    filenames=[]
    for index in range(len(sources)):        
        filename = 'photo'+str(index)+'.jpg'
        request = requests.get(sources[index], stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            filenames.append(filename)        
        else:
            print("Unable to download image")


