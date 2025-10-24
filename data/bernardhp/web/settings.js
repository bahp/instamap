

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
    PASTEL : {
        'blue1': '#96B6C5',
        'blue2': '#447af2',
        'purple': '#616dbe',
        'red': '#e33a36',
        'orange': '#FFD580',
        'gray': '#D3D3D3',
        'green': '#85A389',
        'brown': '#CDC2AE',
        /*'yellow': '#FDFD96'*/
        'yellow': '#fff5be' //'#C2B280'
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