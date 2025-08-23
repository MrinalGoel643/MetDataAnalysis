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

# gets the urls for random objects with images
def get_images(totalObjects, objectIDs, limit):
    images = []
    # grabbing extra in case a primary image is blank (Works best on small limits)
    rand_indexes = random.sample(range(totalObjects), limit + 20)
    for i in rand_indexes:
        obj = get_object(objectIDs[i])
        if obj["primaryImage"]:
            images.append((obj["primaryImage"], obj["title"]))
        if len(images) == limit:
            break

    return images

def department_counts(q="*", max_ids=200):
    """
    Analytic: return a list of (department, count) for search results.
    - q: search query (default '*' = anything)
    - max_ids: cap how many object IDs to inspect (keeps it fast)

    Uses the Met search endpoint (images only), then tallies the 'department'
    field from each object's metadata.
    """
    try:
        resp = requests.get(f"{URL}search", params={"q": q, "hasImages": True}, timeout=15)
        resp.raise_for_status()
        ids = (resp.json().get("objectIDs") or [])[:max_ids]
    except Exception:
        return []

    counts = {}
    for oid in ids:
        try:
            obj = get_object(oid)  # uses your existing helper
            dep = obj.get("department") or "(unknown)"
            counts[dep] = counts.get(dep, 0) + 1
        except Exception:
            continue

    # return sorted (department, count) pairs, highest first
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)
