import time
import requests
import random
import pandas as pd

URL = "https://collectionapi.metmuseum.org/public/collection/v1/"

'''
Need to add error handling
'''

# gets information on a single object
def get_object(objectID):
    try:
        response = requests.get(f"{URL}/objects/{objectID}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching object {objectID}: {e}")
        return None


# gets all the objects that have some sort of image
def get_objectsWithImages():
    try:
        response = requests.get(f"{URL}search?hasImages=true&q=*")
        response.raise_for_status()
        data = response.json()
        total = data.get("total", 0)
        objectIDs = data.get("objectIDs", [])
        return total, objectIDs
    except Exception as e:
        print(f"Error fetching objects with images: {e}")
        return 0, []

# gets the urls for random objects with images
def get_images(totalObjects, objectIDs, limit):
    try:
        images = []
        # grabbing extra in case a primary image is blank (Works best on small limits)
        rand_indexes = random.sample(range(totalObjects), limit + 20)
        for i in rand_indexes:
            obj = get_object(objectIDs[i])
            if obj and obj.get("primaryImage"):
                images.append((obj["primaryImage"], obj.get("title", "Untitled")))
            if len(images) == limit:
                break

        return images
    except Exception as e:
        print(f"Error in get_images: {e}")
        return []

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

"""
Get a list of departments
"""
def list_met_departments():
    """
    Return a DataFrame of all Met departments (id + name) to help you choose.
    """
    try:
        r = requests.get(f"{URL}/departments")
        r.raise_for_status()
        depts = r.json().get("departments", [])
        return pd.DataFrame(depts)[["departmentId", "displayName"]]
    except Exception as e:
        print(f"Error fetching departments: {e}")
        return pd.DataFrame(columns=["departmentId", "displayName"])

"""
returns a dataframe of list of objects with images and metadata that matches search term
To be polite, will only get default max 5 random results from each department,
but can be specified as parameter. Also, can choose the departments to search from.
"""
def search_for_images(query,
                    max_per_department=5,
                    departments=None):

    if not query or not query.strip():
        raise ValueError("Please provide a query.")

    # 1) Departments
    if departments is None:
        resp = requests.get(f"{URL}/departments")
        resp.raise_for_status()
        dept_list = resp.json().get("departments", [])
        dept_ids = [d["departmentId"] for d in dept_list]
        dept_id_to_name = {d["departmentId"]: d["displayName"] for d in dept_list}
    else:
        dept_ids = list(departments)
        # Names will be filled from object details; provide a generic fallback
        dept_id_to_name = {d: f"Department {d}" for d in dept_ids}

    # 2) Per-department search → random sample of IDs → fetch details
    rows = []
    #session = requests.Session()

    print("Searching for", query)
    print("Across departments:", dept_ids)

    for dept_id in dept_ids:
        # limit to only those with images and is highlighted
        params = {
            "q": query,
            "hasImages": "true",
            #"isHighlight": "true",
            "departmentId": dept_id,
        }
        try:
            r = requests.get(f"{URL}/search", params=params)
            #print(r.url)
            r.raise_for_status()
        except requests.RequestException:
            continue

        object_ids = (r.json() or {}).get("objectIDs") or []
        if not object_ids:
            continue

        sample_ids = random.sample(object_ids, k=min(max_per_department, len(object_ids)))

        for oid in sample_ids:
            #print(f"Found: {oid}")
            try:
                obj = requests.get(f"{URL}/objects/{oid}").json()
            except requests.RequestException:
                continue

            # skip if no image
            if not obj["primaryImage"]:
                continue

            rows.append({
                "objectID": obj.get("objectID"),
                "title": obj.get("title"),
                "artistDisplayName": obj.get("artistDisplayName"),
                "objectDate": obj.get("objectDate"),
                "culture": obj.get("culture"),
                "medium": obj.get("medium"),
                "department": obj.get("department") or dept_id_to_name.get(dept_id),
                "objectName": obj.get("objectName"),
                "classification": obj.get("classification"),
                "primaryImageSmall": obj.get("primaryImageSmall"),
                "primaryImage": obj.get("primaryImage"),
                "objectURL": obj.get("objectURL"),
                "isPublicDomain": obj.get("isPublicDomain"),
            })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(["department", "title"]).reset_index(drop=True)
    return df

"""
    CLI when run from command line
    Displays the departments to allow user to input a department
    Then searches the department based on input, and displays the results with images.
"""
def main():
    print("Welcome to Met Search.")
    departments = list_met_departments()
    print(departments.to_string(index=False))
    random.seed(time.time())
    while True:
        dept_no = input("Choose a departmentId #: (Type 'q', 'quit' to stop the program, or enter for all) ").strip()
        if dept_no.lower() in ['q', 'quit']:
            break
        elif dept_no == '':
            dept = None
        else:
            if not dept_no.isdigit():
                print("Invalid input. Please try again.")
                continue
            dept = [int(dept_no)]

        query = input("Search the Met for: ").strip()
        if query == '':
            print("Please enter a query.")
            continue
        results = search_for_images(query,2, departments=dept)
        if results.empty:
            print("No results found.")
            continue
        print(results.to_string(index=False))

if __name__ == '__main__':
    main()
