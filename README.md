# named-entity-recognition

This repo is an implementation of a class that employs spaCy for named entity recognition.

See main.py for detailed demonstration of use. In this example, a database of tweets is loaded (from data/ subfolder), a random tweet is drawn and named-entities extracted and printed to screen. Run this a few times to get a good sense of performance strengths and weaknesses. Consider analyzing your own tweet database as well, using this as a template...

Note a key weakness of spaCy NER -> proper nouns that are not properly capitalized may not be interpreted. This is state of the art, so we will need to enhance it if this is a big issue for our purposes.

More detailed instructions will be provided as this repository evolves.

Run main.py simply as 

```bash
python3 main.py
```
