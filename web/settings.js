

function LightenDarkenColor(col, amt) {

    var usePound = false;
    if (col[0] == "#") {
        col = col.slice(1);
        usePound = true;
    }

    var num = parseInt(col,16);
    var r = (num >> 16) + amt;

    if (r > 255) r = 255;
    else if  (r < 0) r = 0;

    var b = ((num >> 8) & 0x00FF) + amt;

    if (b > 255) b = 255;
    else if  (b < 0) b = 0;

    var g = (num & 0x0000FF) + amt;

    if (g > 255) g = 255;
    else if (g < 0) g = 0;

    return (usePound?"#":"") + (g | (b << 8) | (r << 16)).toString(16);

}



var COLORS = {
    GMAP : {
        'blue1': '#1ba6bf',
        'blue2': '#447af2',
        'purple': '#616dbe',
        'red': '#e33a36',
        'orange': '#ed8608',
        'gray': '#5b6e7b',
        'green': '#2f8c41',
        'brown': '#CDC2AE',
        /*'yellow': '#FDFD96'*/
        'yellow': '#fff5be' //'#C2B280'
    },
    /*
    PASTEL : {
        'blue1': '#96B6C5',
        'blue2': '#447af2',
        'purple': '#616dbe',
        'red': '#e33a36',
        'orange': '#FFD580',
        'gray': '#D3D3D3',
        'green': '#85A389',
        'brown': '#CDC2AE',
        'yellow': '#fff5be' //'#C2B280'
    }*/
    // ... existing GMAP palette
    PASTEL : {
        'blue1': '#96B6C5',    // Water / Deep Sky Blue
        'blue2': '#779ECB',    // Service / Utility Blue
        'purple': '#A29BCC',   // Unique / Parking / Spiritual Lavender
        'red': '#FF6961',      // Accommodation / High Priority Salmon
        'orange': '#FFB347',   // General POI / Amenity Orange
        'gray': '#BDBDBD',     // Infrastructure / Settlement Gray
        'green': '#A7D4AE',    // Nature / Landscape Green
        'brown': '#B59C8F',    // Historic / Cultural Brown
        'yellow': '#FFD166'    // Coast / Sun Yellow
    }
}

var COLORMAP = COLORS.PASTEL

/** Use only hexadecimal colors so that the function
 * above to ligthen or darker the color works. If use
 * use named colors, it returns 0.
 */

const MARKER_STYLE = {

    // --------------------------------------------------------
    // Class (Primary Color Base)
    // --------------------------------------------------------
    tourism: { backgroundColor: COLORMAP.orange, icon: 'camera', unicode: '\uf030' },
    boundary: { backgroundColor: COLORMAP.gray, icon: 'map', unicode: '\uf279' },
    place: { backgroundColor: COLORMAP.gray, icon: 'location-dot', unicode: '\uf3c5' },
    aeroway: { backgroundColor: COLORMAP.gray, icon: 'plane-departure', unicode: '\uf5b0' },
    leisure: { backgroundColor: COLORMAP.orange, icon: 'heart', unicode: '\uf004' },
    highway: { backgroundColor: COLORMAP.gray, icon: 'road', unicode: '\uf018' },
    amenity: { backgroundColor: COLORMAP.orange, icon: 'location-dot', unicode: '\uf3c5' },
    landuse: { backgroundColor: COLORMAP.orange },
    historic: { backgroundColor: COLORMAP.brown, icon: 'landmark', unicode: '\uf66f' },
    natural: { backgroundColor: COLORMAP.green, icon: 'tree', unicode: '\uf1bb' },
    waterway: { backgroundColor: COLORMAP.blue1, icon: 'water', unicode: '\uf773' },
    building: { backgroundColor: COLORMAP.brown, icon: 'building', unicode: '\uf1ad' },
    shop: { icon: 'bag-shopping', backgroundColor: COLORMAP.orange, unicode: '\uf290' },
    mountain_pass: { backgroundColor: COLORMAP.green, icon: 'mountain', unicode: '\uf6fc' },
    railway : { backgroundColor: COLORMAP.gray, icon: 'train-tram', unicode: '\ue5b4' },
    office : { backgroundColor: COLORMAP.gray, icon: 'building-o', unicode: '\uf1ad' },
    man_made: { backgroundColor: COLORMAP.gray, icon: 'gear', unicode: '\uf013' },
    landmark: { backgroundColor: COLORMAP.brown, icon: 'monument', unicode: '\uf5a6' },

    // Handling specific/mixed classes
    'protected_area': { backgroundColor: COLORMAP.green, icon: 'shield-halved', unicode: '\uf3ed' },
    'place_of_worship': { backgroundColor: COLORMAP.brown, icon: 'church', unicode: '\uf51d' },
    'religious': { backgroundColor: COLORMAP.brown, icon: 'cross', unicode: '\uf654' },
    'historic_building': { backgroundColor: COLORMAP.brown, icon: 'archway', unicode: '\uf557' },
    'bridge': { backgroundColor: COLORMAP.gray, icon: 'bridge', unicode: '\ue4d7' },


    // --------------------------------------------------------
    // Type (Specific Overrides - Includes all new entries)
    // --------------------------------------------------------

    // Settlements / Administrative (Gray)
    'administrative': { backgroundColor: COLORMAP.gray },
    'country': { icon: 'flag', backgroundColor: COLORMAP.gray, unicode: '\uf024' },
    'region': { backgroundColor: COLORMAP.gray },
    'city': { icon: 'city', backgroundColor: COLORMAP.gray, unicode: '\uf64f' },
    'town': { icon: 'building-wheat', backgroundColor: COLORMAP.gray, unicode: '\ue4da' },
    'village': { icon: 'building-wheat', backgroundColor: COLORMAP.gray, unicode: '\ue4da' },
    'locality': { icon: 'building-wheat', backgroundColor: COLORMAP.gray, unicode: '\ue4da' },
    'continent': { icon: 'globe', backgroundColor: COLORMAP.gray, unicode: '\uf0ac' },
    'district': { backgroundColor: COLORMAP.gray },
    'borough': { backgroundColor: COLORMAP.gray },
    'province': { backgroundColor: COLORMAP.gray },
    'county': { backgroundColor: COLORMAP.gray },
    'suburb': { backgroundColor: COLORMAP.gray },
    'hamlet': { backgroundColor: COLORMAP.gray },
    'state': { backgroundColor: COLORMAP.gray },
    'administrative region': { backgroundColor: COLORMAP.gray },
    'autonomous community': { backgroundColor: COLORMAP.gray },
    'autonomous province': { backgroundColor: COLORMAP.gray },
    'municipality': { backgroundColor: COLORMAP.gray },
    'territory': { backgroundColor: COLORMAP.gray },
    'neighborhood': { backgroundColor: COLORMAP.gray },
    'neighbourhood': { backgroundColor: COLORMAP.gray },
    'city (former name)': { icon: 'city', backgroundColor: COLORMAP.gray, unicode: '\uf64f' },
    'ghost town': { icon: 'house-crack', backgroundColor: COLORMAP.gray, unicode: '\ue539' },
    'island commune': { icon: 'house', backgroundColor: COLORMAP.gray, unicode: '\uf015' },
    'island nation': { icon: 'flag', backgroundColor: COLORMAP.gray, unicode: '\uf024' },
    'Overseas Collectivity': { icon: 'flag', backgroundColor: COLORMAP.gray, unicode: '\uf024' },

    // Historic & Cultural (Brown)
    'World Heritage site, traditional architecture, earthen building': { icon: 'gopuram', backgroundColor: COLORMAP.brown, unicode: '\uf664' },
    'historic district': { icon: 'city', backgroundColor: COLORMAP.brown, unicode: '\uf64f' },
    'castle': { icon: 'chess-rook', backgroundColor: COLORMAP.brown, unicode: '\uf447' },
    'pagoda': { icon: 'gopuram', backgroundColor: COLORMAP.brown, unicode: '\uf664' },
    'shrine': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown, unicode: '\uf655' },
    'buddhist temple': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown, unicode: '\uf655' },
    'cathedral': { icon: 'church', backgroundColor: COLORMAP.brown, unicode: '\uf51d' },
    'temple': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown, unicode: '\uf655' },
    'archaeological site': { icon: 'archway', backgroundColor: COLORMAP.brown, unicode: '\uf557' },
    'necropolis': { icon: 'tombstone', backgroundColor: COLORMAP.brown, unicode: '\uf720' },
    'ancient city': { icon: 'gopuram', backgroundColor: COLORMAP.brown, unicode: '\uf664' },
    'historic site': { icon: 'landmark', backgroundColor: COLORMAP.brown, unicode: '\uf66f' },
    'cultural landscape': { icon: 'tree-city', backgroundColor: COLORMAP.brown, unicode: '\ue587' },
    'tower': { icon: 'tower-observation', backgroundColor: COLORMAP.brown, unicode: '\ue58a' },
    'ruined abbey': { icon: 'house-damage', backgroundColor: COLORMAP.brown, unicode: '\ue539' },
    'hermitage': { icon: 'house-user', backgroundColor: COLORMAP.brown, unicode: '\ue065' },
    'basilica': { icon: 'church', backgroundColor: COLORMAP.brown, unicode: '\uf51d' },
    'tomb': { icon: 'tombstone', backgroundColor: COLORMAP.brown, unicode: '\uf720' },
    'monument': { icon: 'monument', backgroundColor: COLORMAP.brown, unicode: '\uf5a6' },
    'museum': { icon: 'landmark', backgroundColor: COLORMAP.brown, unicode: '\uf66f' },
    'shrine gate': { icon: 'torii-gate', backgroundColor: COLORMAP.brown, unicode: '\uf6a1' },
    'national_forest': { backgroundColor: COLORMAP.green, icon: 'tree', unicode: '\uf1bb' },
    'monastery': { icon: 'church', backgroundColor: COLORMAP.brown, unicode: '\uf51d' },
    'palace': { icon: 'chess-rook', backgroundColor: COLORMAP.brown, unicode: '\uf447' },
    'royal palace': { icon: 'chess-rook', backgroundColor: COLORMAP.brown, unicode: '\uf447' },
    'fort': { icon: 'fort-awesome', backgroundColor: COLORMAP.brown, unicode: '\uf447' },
    'stately home': { icon: 'building-user', backgroundColor: COLORMAP.brown, unicode: '\ue4d9' },
    'Underground city': { icon: 'city', backgroundColor: COLORMAP.brown, unicode: '\uf64f' },
    'amphitheatre': { icon: 'people-group', backgroundColor: COLORMAP.brown, unicode: '\ue54d' },
    'historic building': { icon: 'archway', backgroundColor: COLORMAP.brown, unicode: '\uf557' },
    'historical site': { icon: 'landmark', backgroundColor: COLORMAP.brown, unicode: '\uf66f' },
    'historic house': { icon: 'house-user', backgroundColor: COLORMAP.brown, unicode: '\ue065' },
    'pagoda complex': { icon: 'gopuram', backgroundColor: COLORMAP.brown, unicode: '\uf664' },
    'villa': { icon: 'house', backgroundColor: COLORMAP.brown, unicode: '\uf015' },
    'abbey': { icon: 'church', backgroundColor: COLORMAP.brown, unicode: '\uf51d' },
    'stairs': { icon: 'stairs', backgroundColor: COLORMAP.brown, unicode: '\ue289' },
    'grottoes': { icon: 'mountain', backgroundColor: COLORMAP.brown, unicode: '\uf6fc' },
    'mausoleum': { icon: 'monument', backgroundColor: COLORMAP.brown, unicode: '\uf5a6' },
    'gate': { icon: 'archway', backgroundColor: COLORMAP.brown, unicode: '\uf557' },
    'historic_cottages': { icon: 'house-chimney', backgroundColor: COLORMAP.brown, unicode: '\ue3af' },
    'stave church': { icon: 'church', backgroundColor: COLORMAP.brown, unicode: '\uf51d' },
    'heritage': { icon: 'landmark', backgroundColor: COLORMAP.brown, unicode: '\uf66f' },
    'historic_site': { icon: 'landmark', backgroundColor: COLORMAP.brown, unicode: '\uf66f' },
    'temple complex': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown, unicode: '\uf655' },
    'temple ruin': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown, unicode: '\uf655' },
    'rock-hewn church': { icon: 'church', backgroundColor: COLORMAP.brown, unicode: '\uf51d' },
    'World Heritage Site': { icon: 'earth-americas', backgroundColor: COLORMAP.brown, unicode: '\uf57d' },


    // Nature & Landscape (Green)
    'national park': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'mountain range': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'alpine pasture': { icon: 'seedling', backgroundColor: COLORMAP.green, unicode: '\uf4d8' },
    'plateau': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'mountain': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'park': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'volcano': { icon: 'volcano', backgroundColor: COLORMAP.green, unicode: '\uf770' },
    'karst landscape': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'geological park': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'waterfall': { icon: 'water', backgroundColor: COLORMAP.green, unicode: '\uf773' },
    'valley': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'natural monument': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'natural park': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'canyon': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'Volcano': { icon: 'volcano', backgroundColor: COLORMAP.green, unicode: '\uf770' },
    'vineyard': { icon: 'spa', backgroundColor: COLORMAP.purple, unicode: '\uf5bb' },
    'flower garden': { icon: 'seedling', backgroundColor: COLORMAP.green, unicode: '\uf4d8' },
    'gorge': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'garden': { icon: 'seedling', backgroundColor: COLORMAP.green, unicode: '\uf4d8' },
    'mountain_hut': { icon: 'house-chimney', backgroundColor: COLORMAP.green, unicode: '\ue3af' },
    'mountain_range': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'mountain peak': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'natural_feature': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'natural formation': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'alpine meadow': { icon: 'seedling', backgroundColor: COLORMAP.green, unicode: '\uf4d8' },
    'mountain group': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'glacier': { icon: 'snowflake', backgroundColor: COLORMAP.green, unicode: '\uf2dc' },
    'fjord': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'geopark': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'state park': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'peak': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'alpine hut': { icon: 'house-chimney', backgroundColor: COLORMAP.green, unicode: '\ue3af' },
    'mountain hut': { icon: 'house-chimney', backgroundColor: COLORMAP.green, unicode: '\ue3af' },
    'hut': { icon: 'house-chimney', backgroundColor: COLORMAP.green, unicode: '\ue3af' },
    'marine protected area': { icon: 'water', backgroundColor: COLORMAP.green, unicode: '\uf773' },
    'memorial park': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'reservation': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'territorial park': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },

    // Water, Coast, and Infrastructure (Blue1, Yellow, Gray)
    'coastal region': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'sea': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'coastline': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'lake': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'lighthouse': { icon: 'lighthouse', backgroundColor: COLORMAP.blue1, unicode: '\ue54a' },
    'archipelago': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'island': { icon: 'sun', backgroundColor: COLORMAP.yellow, unicode: '\uf185' },
    'cliff': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'cliffs': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'rock formation': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'rock_formation': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'peninsula': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'bay': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'river': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'canal': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'harbor': { icon: 'anchor', backgroundColor: COLORMAP.blue1, unicode: '\uf13d' },
    'lagoon': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'cove': { icon: 'water', backgroundColor: COLORMAP.blue1, unicode: '\uf773' },
    'salt flat': { icon: 'mountain', backgroundColor: COLORMAP.yellow, unicode: '\uf6fc' },
    'salt flats': { icon: 'mountain', backgroundColor: COLORMAP.yellow, unicode: '\uf6fc' },
    'beach': { icon: 'umbrella-beach', backgroundColor: COLORMAP.yellow, textColor: '#FFFFFF', unicode: '\uf5ca' },
    'scenic route': { icon: 'car', backgroundColor: COLORMAP.gray, unicode: '\uf1b9' },
    'avenue': { icon: 'road', backgroundColor: COLORMAP.gray, unicode: '\uf018' },
    'path': { icon: 'person-hiking', backgroundColor: COLORMAP.gray, unicode: '\uf6ec' },
    'trail': { icon: 'person-hiking', backgroundColor: COLORMAP.gray, unicode: '\uf6ec' },

    // Amenities, Commerce, & Leisure (Orange, Red, Purple)
    'observation wheel': { icon: 'ferry', backgroundColor: COLORMAP.orange, unicode: '\ue1a2' },
    'shopping street': { icon: 'bag-shopping', backgroundColor: COLORMAP.orange, unicode: '\uf290' },
    'market': { icon: 'store', backgroundColor: COLORMAP.orange, unicode: '\uf54e' },
    'department store': { icon: 'building-o', backgroundColor: COLORMAP.orange, unicode: '\uf1ad' },
    'theme park': { icon: 'ticket', backgroundColor: COLORMAP.orange, unicode: '\uf145' },
    'festival': { icon: 'champagne-glasses', backgroundColor: COLORMAP.orange, unicode: '\uf79f' },
    'restaurant': { 'icon': 'utensils', backgroundColor: COLORMAP.orange, unicode: '\uf2e7' },
    'bookshop': { icon: 'book', backgroundColor: COLORMAP.orange, unicode: '\uf02d' },
    'bookstore': { icon: 'book', backgroundColor: COLORMAP.orange, unicode: '\uf02d' },
    'cafe': { icon: 'mug-saucer', backgroundColor: COLORMAP.orange, unicode: '\uf0f4' },
    'promenade': { icon: 'shoe-prints', backgroundColor: COLORMAP.orange, unicode: '\uf54b' },
    'riverbank_walk': { icon: 'shoe-prints', backgroundColor: COLORMAP.orange, unicode: '\uf54b' },
    'theatre': { icon: 'masks-theater', backgroundColor: COLORMAP.orange, unicode: '\uf630' },
    'attraction': { icon: 'landmark', backgroundColor: COLORMAP.orange, unicode: '\uf66f' },
    'tourist_attraction': { icon: 'landmark', backgroundColor: COLORMAP.orange, unicode: '\uf66f' },
    'square': { icon: 'place-of-interest', backgroundColor: COLORMAP.orange, unicode: '\uf276' },
    'plaza': { icon: 'place-of-interest', backgroundColor: COLORMAP.orange, unicode: '\uf276' },
    'hot spring': { icon: 'bath', backgroundColor: COLORMAP.orange, unicode: '\uf2cd' },

    // Accommodation (Red)
    'hotel': { icon: 'square-h', backgroundColor: COLORMAP.red, unicode: '\uf0fd' },
    'tourist cabin': { icon: 'house-chimney', backgroundColor: COLORMAP.red, unicode: '\ue3af' },
    'resort': { icon: 'square-h', backgroundColor: COLORMAP.red, unicode: '\uf0fd' },
    'ski resort': { icon: 'skiing', backgroundColor: COLORMAP.red, unicode: '\uf7c9' },
    'Ski resort': { icon: 'skiing', backgroundColor: COLORMAP.red, unicode: '\uf7c9' },
    'accommodation': { icon: 'bed', backgroundColor: COLORMAP.red, unicode: '\uf236' },
    'glamping': { icon: 'tent', backgroundColor: COLORMAP.red, unicode: '\ue57d' },
    'campground': { icon: 'campground', backgroundColor: COLORMAP.red, unicode: '\uf6bb' },
    'cabin': { icon: 'house-chimney', backgroundColor: COLORMAP.red, unicode: '\ue3af' },
    'guesthouse': { icon: 'house', backgroundColor: COLORMAP.red, unicode: '\uf015' },
    'alpine_hut': { icon: 'house-chimney', backgroundColor: COLORMAP.red, unicode: '\ue3af' },
    'chalet': { icon: 'house-chimney', backgroundColor: COLORMAP.red, unicode: '\ue3af' },

    // Unique/Other
    'basin': { backgroundColor: COLORMAP.green },
    'statue': { icon: 'user-o', backgroundColor: COLORMAP.brown, unicode: '\uf007' },
    'folly': { icon: 'hat-wizard', backgroundColor: COLORMAP.purple, unicode: '\uf6e8' },
    'library': { icon: 'book-open', backgroundColor: COLORMAP.blue2, unicode: '\uf518' },
    'meditation_center': { icon: 'hand-sparkles', backgroundColor: COLORMAP.purple, unicode: '\ue05f' },
    'clock tower': { icon: 'clock', backgroundColor: COLORMAP.gray, unicode: '\uf017' },
    'clock_tower': { icon: 'clock', backgroundColor: COLORMAP.gray, unicode: '\uf017' },

    // Duplicates/Consolidations
    'national_park': { icon: 'tree', backgroundColor: COLORMAP.green, unicode: '\uf1bb' },
    'mountain_range': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'mountain_peaks': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'rock_formation': { icon: 'mountain', backgroundColor: COLORMAP.green, unicode: '\uf6fc' },
    'island; region': { icon: 'sun', backgroundColor: COLORMAP.yellow, unicode: '\uf185' },
    'island_group': { icon: 'sun', backgroundColor: COLORMAP.yellow, unicode: '\uf185' },

    // Other
    'route': { icon: "route", backgroundColor: COLORMAP.green, unicode: '\uf4d7'}
};

// contains shop (e.g. donuts shop)
// contains mountain (e.g. mountain range)

/*

'city' 'instagram_user' 'park' 'town' 'religious_site' 'tower'
 'neighborhood' 'website' 'church' 'train' 'hotel' 'libro' 'island' '商店街'
 'karst landscape' 'country' 'scenic route' 'location' 'monastery'
 'public swimming pool' 'bookstore' 'botanical garden' 'village' 'street'
 'shop' 'region' 'Christmas market' 'restaurant' 'bicycle' 'tent'
 'mountain pass' 'state' 'national park' 'district' 'bridge' 'beach'
 'mountain' 'forest' 'abandoned hut' 'palace' 'buddha statue' 'lake'
 'roads' 'temple' 'area' 'shrine' 'clock tower' 'tourist attraction'
 'castle' 'waterfall' 'valley' 'mountain ridge' 'indigenous tribe'
 'convenience store' 'shopping street' 'river delta' 'workshop'
 'ancient town' 'glacier' 'cafe' 'garden square' 'charity' 'mountain peak'
 'hiking trail' 'mountain range' 'landslide' 'pool' 'shopping district'
 'residential neighborhood' 'mountain hut' 'hostel' 'canyon' 'icefield'
 'warehouse store' 'archipelago' 'train route' 'fjord' 'cliff'
 'walled town' 'doughnut_shop' 'hilltop town' 'bookstore-café' 'coastline'
 'library' 'trail' 'sea cliff' 'island chain' 'lighthouse' 'rice terraces'
 'mountain group' 'mountain peaks' 'pagoda' 'glacier lagoon' 'peninsula'
 'cave' 'trail race' nan 'peak' 'rock formation' 'square' 'food'
 'building' 'river' 'salt flat' 'cathedral' 'sea stack']
 */
