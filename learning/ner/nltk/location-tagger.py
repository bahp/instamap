

def method_location_tagger(text):
    """"""
    import nltk
    import spacy
    import locationtagger

    # essential entity models downloads
    nltk.downloader.download('maxent_ne_chunker')
    nltk.downloader.download('words')
    nltk.downloader.download('treebank')
    nltk.downloader.download('maxent_treebank_pos_tagger')
    nltk.downloader.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    # Read text
    # file = open(':saved/CzD6fazOqTe/item.txt', "r")
    # text = file.read()
    # file.close()

    # Extracting entities.
    place_entity = locationtagger.find_locations(text=text)

    # Getting all countries
    print("The countries in text : ")
    print(place_entity.countries)

    # Getting all states
    print("The states in text : ")
    print(place_entity.regions)

    # Getting all cities
    print("The cities in text : ")
    print(place_entity.cities)

    print("The country regions : ")
    print(place_entity.country_regions)

    print("The country cities : ")
    print(place_entity.country_cities)

    print("The cities in text : ")
    print(place_entity.other_countries)

    print("The cities in text : ")
    print(place_entity.region_cities)

    print("The cities in text : ")
    print(place_entity.other_regions)