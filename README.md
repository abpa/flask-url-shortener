##Simple Backend In Flask

Maps url to base64 strings and stores them in-memory. 

- `/shorten` methods=['POST', 'OPTIONS']

    Returns unique uuids for the input url


- `/all` methods=['GET']

    Returns all mappings stored in-memory


- `/<hash>` methods=['GET']

    Redirects to the url