/*
================================================================
KML EXPORT JAVASCRIPT
================================================================
*/

/**
 * Attaches the click listener to the KML export button.
 * Should be called inside your $(document).ready().
 */
function setupKmlExportListener() {
    $('#export-kml-button').on('click', function() {
        exportToKML(allMarkers);
    });
}


/**
 * Generates the full KML file content from the markers.
 * @param {Array<L.Marker>} markers - The global 'allMarkers' array.
 */
function exportToKML(markers) {
  if (!markers || markers.length === 0) {
        console.error("KML Export Error: 'allMarkers' array is empty.");
        alert("Cannot export: No markers have been created yet.");
        return;
    }
    console.log("Generating KML for", markers.length, "filtered markers...");

    // 1. Generate the <Style> tags from your MARKER_STYLE object
    const kmlStyles = generateKMLStyles(MARKER_STYLE);

    // 2. Create the <Placemark> tags
    // The list is ALREADY filtered, so we just map.
    const placemarks = markers
        .map(marker => createPlacemark(marker)) // Pass the marker object
        .join('\n');

    // 3. Build the final KML file string
    const kmlContent = `<?xml version="1.0" encoding="UTF-8"?>
      <kml xmlns="http://www.opengis.net/kml/2.2">
        <Document>
          <name>My Exported Map</name>
          
          ${kmlStyles}
          
          ${placemarks}
          
        </Document>
      </kml>
    `;

    // 4. Create a "blob" and trigger the download
    const blob = new Blob([kmlContent], { type: 'application/vnd.google-earth.kml+xml' });
    const a = document.createElement('a');
    const url = URL.createObjectURL(blob);
    a.href = url;
    a.download = 'my-map-export.kml';
    document.body.appendChild(a);
    a.click();

    // Clean up
    setTimeout(() => {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }, 0);
}

/**
 * Creates the KML content for a single marker.
 * @param {L.Marker} marker - The Leaflet marker to export.
 * @returns {string} The KML <Placemark> string.
 */
function createPlacemark(marker) {

    console.log(marker);
    // Get data from the marker's OPTIONS
    const options = marker.options;
    const latLng = marker.getLatLng();

    // --- Build KML coordinates (longitude,latitude,altitude) ---
    const coordinates = `${latLng.lng},${latLng.lat},0`;

    // --- Get KML data from options ---
    const name = options.location.title || 'No Title';
    const hierarchy = options.location.hierarchy || [];
    const placeId = null; // = options.googlePlaceId
    const shortcode = options.post_shortcode;
    const description = options.description;
    const caption = options.postCaption;
    const confidence = options.location.confidence;
    const locClass = options.location.class;
    const type = options.location.type || 'default';
    const rank = options.location.rank;
    const link = options.post_url;
    const date = options.date ? new Date(options.date).toLocaleDateString() : 'N/A';
    const imageUrl = options.display_url || '';

    // --- Build the Google Maps Link ---
    const baseUrl = "https://maps.google.com/maps";
    let gmapsUrl = '';

    if (placeId) {
        // BEST: Links to the official Google Place
        gmapsUrl = `${baseUrl}?q=${encodeURIComponent(name)}&query_place_id=${placeId}`;
    } else if (name) {
        // GOOD: Searches for the name near the coordinates
        gmapsUrl = `${baseUrl}/place/${encodeURIComponent(name)}@${latLng.lat},${latLng.lng}`;
    } else {
        // FALLBACK: Just shows the coordinates
        gmapsUrl = `${baseUrl}?ll=${latLng.lat},${latLng.lng}`;
    }

    // --- Create the Instagram link ---
    const instaUrl = shortcode ? `https://www.instagram.com/p/${shortcode}/?img_index=1` : null;

    // --- 3. Build the KML HTML <description> (Re-ordered) ---
    const kmlDescription = `
      <div style="font-family: Arial, sans-serif; max-width: 350px; font-size: 14px;">
      
        ${imageUrl ? `
          <img src="${imageUrl}" 
               alt="Location Image" 
               style="width:100%; height:auto; max-height:200px; object-fit:cover; border-radius:4px; margin-bottom:10px;">
        ` : ''}
        
        <h3 style="margin: 0 0 4px 0;">${name}</h3>
        
        ${hierarchy.length > 1 ? `
            <p style="margin:0 0 8px 0; font-style: italic; color: #555; font-size: 0.9em;">
                ${hierarchy.slice(1).join(', ')}
            </p>
        ` : ''}

        <div>
            <strong>Date:</strong> ${date}<br>
            <strong>Class:</strong> ${locClass || 'N/A'} | 
            <strong>Type:</strong> ${type || 'N/A'} | 
            <strong>Rank:</strong> ${rank || 'N/A'}<br>
            <strong>Confidence:</strong> ${confidence || 'N/A'}
            ${shortcode}
        </div>
        
        <br>

        <div>
            <a href="${gmapsUrl}" target="_blank" style="text-decoration: none;">
                See in Google maps
            </a><br>
            ${instaUrl ? `
                <a href="${instaUrl}" target="_blank" style="text-decoration: none;">
                   See original post
                </a>
            ` : ''}
        </div>

        <br>

        <hr">

        ${description ? `<p style="margin: 8px 0; font-size: 0.95em;">${description}</p>` : ''}
        
        ${caption ? `
            <p style="margin:8px 0; padding: 8px; background: #f4f4f4; 
              border-radius: 4px; font-size: 0.9em; border-left: 3px solid #ddd;">
                <strong>Caption:</strong> ${caption}
            </p>
        ` : ''}
        
      </div>
    `;

    // --- 4. Return the final KML Placemark ---
    return `
    <Placemark>
      <name><![CDATA[${name}]]></name>
      <description><![CDATA[${kmlDescription}]]></description>
      <styleUrl>#style_${type}</styleUrl>
      <Point>
        <altitudeMode>relativeToGround</altitudeMode>
        <coordinates>${coordinates}</coordinates>
      </Point>
    </Placemark>
  `;
}

/**
 * Sanitizes a string to be a valid KML ID and filename.
 * Replaces spaces, slashes, and other invalid chars with an underscore.
 * @param {string} str The string to sanitize.
 * @returns {string} A sanitized string.
 */
function sanitizeForKmlId(str) {
  if (!str) {
    return "default";
  }
  // Replaces one or more invalid characters (not letter, number, hyphen, underscore)
  // with a single underscore.
  return str.replace(/[^a-zA-Z0-9_-]+/g, '_');
}

/**
 * Loops over MARKER_STYLE and generates KML <Style> tags
 * that point to custom PNG icons.
 * @param {object} markerStyle - Your MARKER_STYLE global variable.
 * @returns {string} A string of all <Style> definitions.
 */
function generateKMLStyles(markerStyle) {
    let styles = [];

    // --- 1. SET YOUR ICON'S BASE URL ---
    // This is the public URL where you will upload your generated PNGs.
    // (You MUST change this to your actual URL)
    const ICON_BASE_URL = 'https://raw.githubusercontent.com/bahp/instamap/refs/heads/master/web/static/img/markers/';

    // --- 2. Add a Default Style ---
    // This points to a 'default.png' icon you must also upload.
    styles.push(`
    <Style id="style_default">
      <IconStyle>
        <scale>1.0</scale>
        <Icon>
          <href>${ICON_BASE_URL}default.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>0.0</scale>
      </LabelStyle>
    </Style>
    `);
    // --- End of Default Style ---

    Object.entries(markerStyle).forEach(([type, style]) => {
        // Sanitize the type name to match the style ID AND the filename
        // e.g., "department store" -> "department_store"
        const kmlId = sanitizeForKmlId(type);

        // Create the full URL to the icon
        // e.g., https://.../icons/department_store.png
        const iconHref = `${ICON_BASE_URL}${kmlId}.png`;

        styles.push(`
    <Style id="style_${kmlId}">
      <IconStyle>
        <scale>0.9</scale>
        <Icon>
          <href>${iconHref}</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>0.0</scale>
      </LabelStyle>
    </Style>
    `);
    });

    return styles.join('\n');
}

/**
 * Converts a CSS hex color (#RRGGBB) to a KML color (AABBGGRR).
 * @param {string} hex - The CSS hex color (e.g., "#FF0000").
 * @returns {string} The KML color (e.g., "ff0000ff").
 */
function cssHexToKmlColor(hex) {
    // Fallback to a solid light gray if hex is invalid
    if (!hex || hex.length !== 7 || hex[0] !== '#') {
        return 'ffd3d3d3';
    }

    // Remove the hash
    const rr = hex.substring(1, 3);
    const gg = hex.substring(3, 5);
    const bb = hex.substring(5, 7);

    // KML is AABBGGRR (AA = Alpha/Opacity, we'll use 'ff' for solid)
    return `ff${bb}${gg}${rr}`.toLowerCase();
}

// --- Don't forget to call this inside $(document).ready() ---
// setupKmlExportListener();