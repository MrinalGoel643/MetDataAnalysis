import requests
import random

URL = "https://collectionapi.metmuseum.org/public/collection/v1/"

'''
Need to add error handling
'''

# gets information on a single object
def get_object(objectID):
    return requests.get(f"{URL}/objects/{objectID}").json()

# gets all the objects that have some sort of image
def get_objectsWithImages():
    response = requests.get(f"{URL}search?hasImages=true&q=*").json()
    total = response["total"]
    objectIDs = response["objectIDs"]
    return total, objectIDs

# gets the urls for 3 random objects with images
def get_images(totalObjects, objectIDs, limit):
    images = []
    # grabbing extra in case a primary image is blank (Works best on small limits)
    rand_indexes = random.sample(range(totalObjects), limit + 20)

    for i in rand_indexes:
        obj = get_object(objectIDs[i])
        if obj["primaryImage"]:
            images.append((obj["primaryImage"], obj["title"]))
            limit += 1
        if limit == 3:
            break

    return images
