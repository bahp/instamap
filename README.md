
Requirements
    - instaloader (download posts)
    - pandas (formatting)
    - requests (download images)
    - folium (display map)
    - spacey (named entity recognition)
    - nltk (named entity recognition)

Once you have installed the required libraries, download the posts in 
a folder using instaloader with the following command line.

```
$ instaloader --login=bernardhp :saved 
    --dirname-pattern=test 
    --filename-pattern={shortcode}/item 
    --no-compress-json 
    --no-videos --no-video-thumbnails 
    --no-pictures --no-caption
    --slide=1 
    --geotags 
```

Lets understand what this does
-- no-captions for no txt... also no coordinates?
The geotags are needed...
It only downloads first 50...?
What the hell

For more information check out https://instaloader.github.io/cli-options.html or type in
your terminal:

```
    instaloader --help
```

The folder created will have the following structure...

```
test
  |- shortcode
    |- item.json
  |- shortcode
    |- item.json
  |- shortcode
    |- item.json
```

If you decided to compress the json, it is easy to uncompress them by using

```
    python unzip.py
```

Then create a summary file with the posts

```
    python summary.py
```

Then create the display

```
    python display_map.py
```


To extractNER...

```
    python find_entities.py
```



instaloader --login=bernardhp :saved \
    --dirname-pattern=v1 \
    --filename-pattern={shortcode}/item \
    --no-compress-json \
    --no-videos --count 10
    --geotags --no-video-thumbnails
    --no-captions
    --slide 1
    
    
 When decompressing a _node appears!
 
 # Running gallery dl
 gallery-dl https://www.instagram.com/bernardhp/saved/ --config config.conf 

https://www.instagram.com/USERNAME/saved/ALBUMNAME
https://i.instagram.com/api/v1/collections/list


.. note:: Instagram API allows to download a json file with the display_url and thumbnail_src.
          However, this are URL have a signature and expire on a few days. Thus, either download
          the whole image and encode it in the HTML, or try to show the whole instagram POST.
          
.. note: Instagram embed sometimes give issues and it is not shown. And i think it is not 
         possible to use it within an iframe.

Ideas for NLP

.. note: What about hashtags? (e.g. #tuscany)
.. note: What about underscore (e.g. #visit_tuscany)
.. note: What if language is Japanish, Italian,  ...
.. note: What if they appear within parenthesis

    e.g. CstVx6CP_kO

    (Nozomi) (Mizuno)


For query google

combine any ORganization with first location?

CyknIJtI2k6

  value  confidence                   text
0   LOC    0.994525                 London
1   LOC    0.862039      St Katherine Dock
2   ORG    0.800922  Leighton House Museum
3   ORG    0.754580      Severndrog Castle
4   LOC    0.689347            Neal's Yard
5   LOC    0.563282     Alternative London
6   PER    0.535964                    God
7   ORG    0.526224           Kyoto Garden
8   LOC    0.462042      Hampstead Pergola