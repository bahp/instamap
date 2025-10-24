

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

var COLORMAP = COLORS .PASTEL

/** Use only hexadecimal colors so that the function
 * above to ligthen or darker the color works. If use
 * use named colors, it returns 0.
 */
var MARKER_STYLE = {

    // ---------------------
    // Class
    // ---------------------
    tourism: {
        backgroundColor: COLORMAP.orange
    },
    boundary: {
        backgroundColor: COLORMAP.gray
    },
    place: {
        backgroundColor: COLORMAP.orange
    },
    aeroway: {
        backgroundColor: COLORMAP.orange
    },
    leisure: {
        backgroundColor: COLORMAP.orange
    },
    highway: {
        backgroundColor: COLORMAP.gray
    },
    amenity: {
        backgroundColor: COLORMAP.orange
    },
    landuse: {
        backgroundColor: COLORMAP.orange
    },
    historic: {
        backgroundColor: COLORMAP.brown
    },
    natural: {
        backgroundColor: COLORMAP.green
    },
    waterway: {
        backgroundColor: COLORMAP.blue1
    },
    building: {
        backgroundColor: COLORMAP.brown
    },
    shop: {
        icon: 'bag-shopping',
        backgroundColor: COLORMAP.orange
    },
    mountain_pass: {
        backgroundColor: COLORMAP.green
    },
    railway : {
        backgroundColor: COLORMAP.gray
    },
    office : {
        backgroundColor: COLORMAP.gray
    },
    man_made: {
        backgroundColor: COLORMAP.gray
    },


    // ---------------------
    // Type
    // ---------------------
    'administrative': {
        backgroundColor: '#DBDFEA'
    },
    'island': {
        icon: 'sun',
        backgroundColor: COLORMAP.yellow
    },
    'ceremonial': {},
    'aerodrome': {
        icon: 'plane-departure'
    },
    'nature_reserve': {
        'icon': 'tree',
        backgroundColor: COLORMAP.green
    },
    'suburb': {},
    'pedestrian': {},
    'continent': {
        icon: 'globe',
    },
    'path': {},
    'townhall': {},
    'village': {
        icon: 'building-wheat',
        backgroundColor: COLORMAP.gray
    },
    'locality': {
        icon: 'building-wheat',
        backgroundColor: COLORMAP.gray
    },
    'city': {
        icon: 'city',
        backgroundColor: COLORMAP.gray
    },
    'province': {},
    'hamlet': {},
    'winter_sports' : {
        icon: 'snowflake'
    },
    'restaurant': {
        'icon': 'utensils',
        backgroundColor: COLORMAP.orange
    },
    'castle': {
        icon: 'chess-rook',
        backgroundColor: COLORMAP.brown,
    },
    'quarter': {},
    'track': {},
    'residential': {},
    'information': {},
    'volcano': {
        icon: 'volcano',
        backgroundColor: COLORMAP.green
    },
    'church ruins': {
        icon: 'church',
        backgroundColor: COLORMAP.brown
    },
    'peak': {
        icon: 'mountain',
        backgroundColor: COLORMAP.green
    },
    'water': {
        icon: 'water',
        backgroundColor: COLORMAP.blue1
    },
    'region': {
        backgroundColor: COLORMAP.gray
    },
    'river': {
        icon: 'water',
        backgroundColor: COLORMAP.blue1
    },
    'yes': {},
    'farm': {
        icon: 'wheat-awn'
    },
    'attraction': {
        icon: 'landmark'
    },
    'car_parts': {},
    'park': {
        icon: 'tree',
        backgroundColor: COLORMAP.green
    },
    'square': {},
    'natural_tourist_attraction_changed_by_humans.': {},
    'saddle': {
        icon: 'mountain',
        backgroundColor: COLORMAP.green
    },
    'museum': {
        icon: 'landmark',
        backgroundColor: COLORMAP.brown
    },
    'train_station': {
        icon: 'train'
    },
    'political': {},
    'place_of_worship': {
        icon: 'church',
        backgroundColor: COLORMAP.brown
    },
    'folly': {},
    'town': {
        icon: 'building-wheat',
        backgroundColor: COLORMAP.gray
    },
    'beach': {
        icon: 'umbrella-beach',
        backgroundColor: COLORMAP.yellow,
        textColor: '#D3D3D3'
    },
    'alpine_hut': {
        icon: 'mountain',
        backgroundColor: COLORMAP.green
    },
    'mountain_range': {
        icon: 'mountain',
        backgroundColor: COLORMAP.green
    },
    'university': {
        icon: 'building-columns',
        backgroundColor: COLORMAP.brown
    },
    'viewpoint': {
        icon: 'eye',
        backgroundColor: COLORMAP.green
    },
    'bar': {
        icon: 'martini-glass',
        backgroundColor: COLORMAP.orange
    },
    'isolated_dwelling': {},
    'clock' : {},
    'dock': {},
    'traffic_signals': {},
    'station' : 'train',
    'footway': {},
    'construction': {},
    'archaeological_site': {},
    'hotel': {
        icon: 'square-h',
        backgroundColor: COLORMAP.red
    },
    'memorial': {},
    'hairdresser': {},
    'waterfall': {
        icon: 'water',
        backgroundColor: COLORMAP.green
    },
    'administration': {},
    'city_block': {},
    'supermarket': {
        icon: 'cart-shopping',
        backgroundColor: COLORMAP.blue2
    },
    'service': {},
    'primary': {},
    'golf_course': {},
    'mall': {},
    'gorge': {},
    'stadium': {},
    'meadow': {},
    'diplomatic': {},
    'ruins': {},
    'ticket': {},
    'company': {},
    'neighbourhood': {},
    'peninsula': {},
    'historic': {
        backgroundColor: COLORMAP.brown
    },
    'archipelago': {},
    'clothes': {
        icon: 'bag-shopping',
        backgroundColor: COLORMAP.orange
    },
    'bare_rock': {},
    'secondary': {},
    'valley': {},
    'lighthouse': {},
    'church': {
        icon: 'church',
        backgroundColor: COLORMAP.brown
    },
    'tertiary': {},
    'national_park': {
        backroundColor: COLORMAP.green
    },
    'fast_food': {},
    'bus_stop': {},
    'bridge': {
        icon: 'bridge',
        backgroundColor: COLORMAP.gray
    },
    'courthouse': {},
    'unclassified': {},
    'land_area': {},
    'cafe': {
        icon: 'mug-saucer',
        backgroundColor: COLORMAP.orange,
    },
    'parking': {
        icon: 'square-parking',
        backgroundColor: COLORMAP.purple
    },
    'plain': {},



    // Other manual from bard... how to make this consistent?
    // probably need to query Nominatum, or Google or something
    'temple': {
        icon: 'church',
        backgroundColor: COLORMAP.brown
    },
    'lake': {
        icon: 'water',
        backgroundColor: COLORMAP.blue1
    },
    'religious_site': {
        icon: 'church',
        backgroundColor: COLORMAP.brown
    },
    'bookstore': {
        icon: 'book',
        backgroundColor: COLORMAP.orange
    },
    'shrine': {
        icon: 'church',
        backgroundColor: COLORMAP.brown
    },
    'national park': {
        icon: 'tree',
        backgroundColor: COLORMAP.green
    },
    'mountain pass': {
        icon: 'tree',
        backgroundColor: COLORMAP.green
    },
    'mountain range': {
        icon: 'tree',
        backgroundColor: COLORMAP.green
    },
    'mountain': {
        icon: 'tree',
        backgroundColor: COLORMAP.green
    },
    'valley': {
        icon: 'tree',
        backgroundColor: COLORMAP.green
    },
    'trail race': {
        icon: 'tree',
        backgroundColor: COLORMAP.green
    },
    'forest': {
        icon: 'tree',
        backgroundColor: COLORMAP.green
    },
    'buddha statue': {
        icon: 'vihara',
        backgroundColor: COLORMAP.purple
    },
    country: {
        backgroundColor: COLORMAP.gray
    },
    monastery: {
        icon: 'church',
        backgroundColor: COLORMAP.brown
    },
    palace: {
        icon: 'chess-rook',
        backgroundColor: COLORMAP.brown,
    },


}



MARKER_STYLE = {

    // --------------------------------------------------------
    // Class (Primary Color Base)
    // --------------------------------------------------------
    tourism: { backgroundColor: COLORMAP.orange, icon: 'camera' },
    boundary: { backgroundColor: COLORMAP.gray, icon: 'map' },
    place: { backgroundColor: COLORMAP.gray, icon: 'location-dot' },
    aeroway: { backgroundColor: COLORMAP.gray, icon: 'plane-departure' },
    leisure: { backgroundColor: COLORMAP.orange, icon: 'heart' },
    highway: { backgroundColor: COLORMAP.gray, icon: 'road' },
    amenity: { backgroundColor: COLORMAP.orange, icon: 'location-dot' },
    landuse: { backgroundColor: COLORMAP.orange },
    historic: { backgroundColor: COLORMAP.brown, icon: 'landmark' },
    natural: { backgroundColor: COLORMAP.green, icon: 'tree' },
    waterway: { backgroundColor: COLORMAP.blue1, icon: 'water' },
    building: { backgroundColor: COLORMAP.brown, icon: 'building' },
    shop: { icon: 'bag-shopping', backgroundColor: COLORMAP.orange },
    mountain_pass: { backgroundColor: COLORMAP.green, icon: 'mountain' },
    railway : { backgroundColor: COLORMAP.gray, icon: 'train-tram' },
    office : { backgroundColor: COLORMAP.gray, icon: 'building-o' },
    man_made: { backgroundColor: COLORMAP.gray, icon: 'gear' },
    landmark: { backgroundColor: COLORMAP.brown, icon: 'monument' },

    // Handling specific/mixed classes
    'protected_area': { backgroundColor: COLORMAP.green, icon: 'shield-halved' },
    'place_of_worship': { backgroundColor: COLORMAP.brown, icon: 'church' },
    'religious': { backgroundColor: COLORMAP.brown, icon: 'cross' },
    'historic_building': { backgroundColor: COLORMAP.brown, icon: 'archway' },
    'bridge': { backgroundColor: COLORMAP.gray, icon: 'bridge' },


    // --------------------------------------------------------
    // Type (Specific Overrides - Includes all new entries)
    // --------------------------------------------------------

    // Settlements / Administrative (Gray)
    'administrative': { backgroundColor: COLORMAP.gray },
    'country': { icon: 'flag', backgroundColor: COLORMAP.gray },
    'region': { backgroundColor: COLORMAP.gray },
    'city': { icon: 'city', backgroundColor: COLORMAP.gray },
    'town': { icon: 'building-wheat', backgroundColor: COLORMAP.gray },
    'village': { icon: 'building-wheat', backgroundColor: COLORMAP.gray },
    'locality': { icon: 'building-wheat', backgroundColor: COLORMAP.gray },
    'continent': { icon: 'globe', backgroundColor: COLORMAP.gray },
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
    'city (former name)': { icon: 'city', backgroundColor: COLORMAP.gray },
    'ghost town': { icon: 'house-crack', backgroundColor: COLORMAP.gray },
    'island commune': { icon: 'house', backgroundColor: COLORMAP.gray },
    'island nation': { icon: 'flag', backgroundColor: COLORMAP.gray },
    'Overseas Collectivity': { icon: 'flag', backgroundColor: COLORMAP.gray },

    // Historic & Cultural (Brown)
    'World Heritage site, traditional architecture, earthen building': { icon: 'gopuram', backgroundColor: COLORMAP.brown },
    'historic district': { icon: 'city', backgroundColor: COLORMAP.brown },
    'castle': { icon: 'chess-rook', backgroundColor: COLORMAP.brown },
    'pagoda': { icon: 'gopuram', backgroundColor: COLORMAP.brown },
    'shrine': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown },
    'buddhist temple': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown },
    'cathedral': { icon: 'church', backgroundColor: COLORMAP.brown },
    'temple': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown },
    'archaeological site': { icon: 'archway', backgroundColor: COLORMAP.brown },
    'necropolis': { icon: 'tombstone', backgroundColor: COLORMAP.brown },
    'ancient city': { icon: 'gopuram', backgroundColor: COLORMAP.brown },
    'historic site': { icon: 'landmark', backgroundColor: COLORMAP.brown },
    'cultural landscape': { icon: 'tree-city', backgroundColor: COLORMAP.brown },
    'tower': { icon: 'tower-observation', backgroundColor: COLORMAP.brown },
    'ruined abbey': { icon: 'house-damage', backgroundColor: COLORMAP.brown },
    'hermitage': { icon: 'house-user', backgroundColor: COLORMAP.brown },
    'basilica': { icon: 'church', backgroundColor: COLORMAP.brown },
    'tomb': { icon: 'tombstone', backgroundColor: COLORMAP.brown },
    'monument': { icon: 'monument', backgroundColor: COLORMAP.brown },
    'museum': { icon: 'landmark', backgroundColor: COLORMAP.brown },
    'shrine gate': { icon: 'torii-gate', backgroundColor: COLORMAP.brown },
    'national_forest': { backgroundColor: COLORMAP.green }, // Overridden to Green
    'monastery': { icon: 'church', backgroundColor: COLORMAP.brown },
    'palace': { icon: 'chess-rook', backgroundColor: COLORMAP.brown },
    'royal palace': { icon: 'chess-rook', backgroundColor: COLORMAP.brown },
    'fort': { icon: 'fort-awesome', backgroundColor: COLORMAP.brown },
    'stately home': { icon: 'building-user', backgroundColor: COLORMAP.brown },
    'Underground city': { icon: 'city', backgroundColor: COLORMAP.brown },
    'amphitheatre': { icon: 'people-group', backgroundColor: COLORMAP.brown },
    'historic building': { icon: 'archway', backgroundColor: COLORMAP.brown },
    'historical site': { icon: 'landmark', backgroundColor: COLORMAP.brown },
    'historic house': { icon: 'house-user', backgroundColor: COLORMAP.brown },
    'pagoda complex': { icon: 'gopuram', backgroundColor: COLORMAP.brown },
    'villa': { icon: 'house', backgroundColor: COLORMAP.brown },
    'abbey': { icon: 'church', backgroundColor: COLORMAP.brown },
    'stairs': { icon: 'stairs', backgroundColor: COLORMAP.brown },
    'grottoes': { icon: 'mountain', backgroundColor: COLORMAP.brown },
    'mausoleum': { icon: 'monument', backgroundColor: COLORMAP.brown }, // when changing to monument a tombstone appears...
    'gate': { icon: 'archway', backgroundColor: COLORMAP.brown },
    'historic_cottages': { icon: 'house-chimney', backgroundColor: COLORMAP.brown },
    'stave church': { icon: 'church', backgroundColor: COLORMAP.brown },
    'heritage': { icon: 'landmark', backgroundColor: COLORMAP.brown },
    'historic_site': { icon: 'landmark', backgroundColor: COLORMAP.brown },
    'temple complex': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown },
    'temple ruin': { icon: 'dharmachakra', backgroundColor: COLORMAP.brown },
    'ruined abbey': { icon: 'church', backgroundColor: COLORMAP.brown },
    'rock-hewn church': { icon: 'church', backgroundColor: COLORMAP.brown },
    'World Heritage Site': { icon: 'earth-americas', backgroundColor: COLORMAP.brown },


    // Nature & Landscape (Green)
    'national park': { icon: 'tree', backgroundColor: COLORMAP.green },
    'mountain range': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'alpine pasture': { icon: 'seedling', backgroundColor: COLORMAP.green },
    'plateau': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'mountain': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'park': { icon: 'tree', backgroundColor: COLORMAP.green },
    'volcano': { icon: 'volcano', backgroundColor: COLORMAP.green },
    'karst landscape': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'geological park': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'waterfall': { icon: 'water', backgroundColor: COLORMAP.green },
    'valley': { icon: 'tree', backgroundColor: COLORMAP.green },
    'natural monument': { icon: 'tree', backgroundColor: COLORMAP.green },
    'natural park': { icon: 'tree', backgroundColor: COLORMAP.green },
    'canyon': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'Volcano': { icon: 'volcano', backgroundColor: COLORMAP.green }, // Capitalized duplicate
    'vineyard': { icon: 'grape', backgroundColor: COLORMAP.green },
    'flower garden': { icon: 'seedling', backgroundColor: COLORMAP.green },
    'gorge': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'garden': { icon: 'seedling', backgroundColor: COLORMAP.green },
    'mountain_hut': { icon: 'house-chimney', backgroundColor: COLORMAP.green },
    'mountain_range': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'mountain peak': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'natural_feature': { icon: 'tree', backgroundColor: COLORMAP.green },
    'natural formation': { icon: 'tree', backgroundColor: COLORMAP.green },
    'national_forest': { icon: 'tree', backgroundColor: COLORMAP.green },
    'alpine meadow': { icon: 'seedling', backgroundColor: COLORMAP.green },
    'mountain group': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'glacier': { icon: 'snowflake', backgroundColor: COLORMAP.green },
    'fjord': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'geopark': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'state park': { icon: 'tree', backgroundColor: COLORMAP.green },
    'mountain pass': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'alpine meadow': { icon: 'seedling', backgroundColor: COLORMAP.green },
    'mountain_pass': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'peak': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'alpine hut': { icon: 'house-chimney', backgroundColor: COLORMAP.green },
    'mountain hut': { icon: 'house-chimney', backgroundColor: COLORMAP.green },
    'hut': { icon: 'house-chimney', backgroundColor: COLORMAP.green },
    'marine protected area': { icon: 'water', backgroundColor: COLORMAP.green }, // Marine green
    'memorial park': { icon: 'tree', backgroundColor: COLORMAP.green },
    'reservation': { icon: 'tree', backgroundColor: COLORMAP.green },
    'territorial park': { icon: 'tree', backgroundColor: COLORMAP.green },

    // Water, Coast, and Infrastructure (Blue1, Yellow, Gray)
    'coastal region': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'sea': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'coastline': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'lake': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'lighthouse': { icon: 'lighthouse', backgroundColor: COLORMAP.blue1 },
    'archipelago': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'island': { icon: 'sun', backgroundColor: COLORMAP.yellow },
    'cliff': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'cliffs': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'rock formation': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'rock_formation': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'peninsula': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'bay': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'river': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'canal': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'harbor': { icon: 'anchor', backgroundColor: COLORMAP.blue1 },
    'lagoon': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'cove': { icon: 'water', backgroundColor: COLORMAP.blue1 },
    'salt flat': { icon: 'mountain', backgroundColor: COLORMAP.yellow },
    'salt flats': { icon: 'mountain', backgroundColor: COLORMAP.yellow },
    'beach': { icon: 'umbrella-beach', backgroundColor: COLORMAP.yellow, textColor: '#FFFFFF' },
    'road': { icon: 'road', backgroundColor: COLORMAP.gray },
    'highway': { icon: 'road', backgroundColor: COLORMAP.gray },
    'scenic route': { icon: 'car', backgroundColor: COLORMAP.gray },
    'avenue': { icon: 'road', backgroundColor: COLORMAP.gray },
    'path': { icon: 'person-hiking', backgroundColor: COLORMAP.gray },
    'trail': { icon: 'person-hiking', backgroundColor: COLORMAP.gray },

    // Amenities, Commerce, & Leisure (Orange, Red, Purple)
    'observation wheel': { icon: 'ferry', backgroundColor: COLORMAP.orange },
    'shopping street': { icon: 'bag-shopping', backgroundColor: COLORMAP.orange },
    'market': { icon: 'store', backgroundColor: COLORMAP.orange },
    'department store': { icon: 'building-o', backgroundColor: COLORMAP.orange },
    'theme park': { icon: 'roller-coaster', backgroundColor: COLORMAP.orange },
    'festival': { icon: 'champagne-glasses', backgroundColor: COLORMAP.orange },
    'restaurant': { 'icon': 'utensils', backgroundColor: COLORMAP.orange },
    'bookshop': { icon: 'book', backgroundColor: COLORMAP.orange },
    'bookstore': { icon: 'book', backgroundColor: COLORMAP.orange },
    'cafe': { icon: 'mug-saucer', backgroundColor: COLORMAP.orange },
    'promenade': { icon: 'shoe-prints', backgroundColor: COLORMAP.orange },
    'riverbank_walk': { icon: 'shoe-prints', backgroundColor: COLORMAP.orange },
    'theatre': { icon: 'masks-theater', backgroundColor: COLORMAP.orange },
    'attraction': { icon: 'landmark', backgroundColor: COLORMAP.orange },
    'tourist_attraction': { icon: 'landmark', backgroundColor: COLORMAP.orange },
    'square': { icon: 'place-of-interest', backgroundColor: COLORMAP.orange },
    'plaza': { icon: 'place-of-interest', backgroundColor: COLORMAP.orange },
    'hot spring': { icon: 'bath', backgroundColor: COLORMAP.orange },

    // Accommodation (Red)
    'hotel': { icon: 'square-h', backgroundColor: COLORMAP.red },
    'tourist cabin': { icon: 'house-chimney', backgroundColor: COLORMAP.red },
    'resort': { icon: 'square-h', backgroundColor: COLORMAP.red },
    'ski resort': { icon: 'skiing', backgroundColor: COLORMAP.red },
    'Ski resort': { icon: 'skiing', backgroundColor: COLORMAP.red },
    'accommodation': { icon: 'bed', backgroundColor: COLORMAP.red },
    'glamping': { icon: 'tent', backgroundColor: COLORMAP.red },
    'campground': { icon: 'campground', backgroundColor: COLORMAP.red },
    'cabin': { icon: 'house-chimney', backgroundColor: COLORMAP.red },
    'guesthouse': { icon: 'house', backgroundColor: COLORMAP.red },
    'mountain_hut': { icon: 'house-chimney', backgroundColor: COLORMAP.red },
    'alpine_hut': { icon: 'house-chimney', backgroundColor: COLORMAP.red },
    'chalet': { icon: 'house-chimney', backgroundColor: COLORMAP.red },

    // Unique/Other
    'basin': { backgroundColor: COLORMAP.green },
    'statue': { icon: 'user-o', backgroundColor: COLORMAP.brown },
    'folly': { icon: 'hat-wizard', backgroundColor: COLORMAP.purple },
    'library': { icon: 'book-open', backgroundColor: COLORMAP.blue2 },
    'meditation_center': { icon: 'hand-sparkles', backgroundColor: COLORMAP.purple },
    'clock tower': { icon: 'clock', backgroundColor: COLORMAP.gray },
    'clock_tower': { icon: 'clock', backgroundColor: COLORMAP.gray },
    'building': { icon: 'building', backgroundColor: COLORMAP.brown }, // Default building type

    // Duplicates/Consolidations (Ensuring all lower-case types from your list are handled)
    'national_park': { icon: 'tree', backgroundColor: COLORMAP.green },
    'mountain_range': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'mountain_peaks': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'rock_formation': { icon: 'mountain', backgroundColor: COLORMAP.green },
    'island; region': { icon: 'sun', backgroundColor: COLORMAP.yellow },
    'island_group': { icon: 'sun', backgroundColor: COLORMAP.yellow },
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
