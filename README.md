# ibex - Intelligence Based Entity Xtraction

This service is a wrapper for the spaCy named entity recognition tool. Given a text document, `ibex.get_entites(text, language='english')` will return a list of the named entities detected. A key weakness of spaCy's NER is that it may not recognize proper nouns that are not properly capitalized.

## Docker

To run in development mode with Docker: 

```
./run-dev.sh
```

## Flask API
As a health-check, the base route `/` will return a description of the service. 

GET or POST requests can be made to the `/entities` route with `text` and `lang` parameters given as query string arguments (for GET requests) or as field values (for POST requests). `text` defines the content of the document and `lang` specifies the language. Currently only `english` and `spanish` are supported values.

examples:
```
localhost:5000/entities?text=This%20is%20a%20setence%20about%20Paris.
localhost:5000/entities?text=%C2%BFHola,%20qu%C3%A9%20hora%20es,%20Paul?&lang=spanish.
```

## Tests
Run tests using 
```
nosetests
```
add -s to not supress print statements. 