
# Function to fetch book dimensions from Open Library API
#param isbn: ISBN number of the book
#return: number of pages and thickness in cm
def fetchBookDim(isbn):
    url = "https://openlibrary.org/api/books"
    params = {
        "bibkeys": f"ISBN:{isbn}",
        "format": "json",
        "jscmd": "data"
    }

    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        isbn = f"ISBN:{isbn}"

        if isbn not in data:
            return None, None

        book = data[isbn]
        pages = book.get("number_of_pages")

        # Try to extract thickness from dimensions (in cm)
        #Format: "physical_dimensions": "20.3 x 13.3 x 1.5 cm"
        raw_dims = book.get("physical_dimensions", "")
        thickness = None
        if "cm" in raw_dims:
            try:
                parts = raw_dims.replace("cm", "").split("x")
                dims = []
                for p in parts:
                    p = p.strip()
                    if p.replace('.', '', 1).isdigit():
                        dims.append(float(p))
                if dims:
                    thickness = min(dims)
            except:
                pass

        return pages, thickness

    except Exception:
        return None, None
