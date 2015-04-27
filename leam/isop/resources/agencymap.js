
var map = new ol.Map({
  target: 'map',
  layers: [
     new ol.layer.Tile({
       source: new ol.source.MapQuest({layer: 'osm'})
     }),
  ],
  view: new ol.View({
    center: ol.proj.transform([-96.5917, 39.1917], 'EPSG:4326', 'EPSG:3857'),
    zoom: 6,
  })
});

/* getLongLat extracts the long, lat values from the document
 * and returns the projected array
 */
function getLongLat() {
  var longval = parseFloat(document.getElementById('param-long').innerHTML);
  var latval = parseFloat(document.getElementById('param-lat').innerHTML);

  return ol.proj.transform([longval, latval], 'EPSG:4326', 'EPSG:3857');
};

/* getBoundary extracts the URL for the geoJSON boundary file from
 * the document and returns the layer.
 */
function getBoundary() {

  var jsonurl = document.getElementById('param-url').innerHTML;

  var style = new ol.style.Style({
    fill: new ol.style.Fill({
      color: 'rgba(255, 255, 255, 0.6)'
    }),
    stroke: new ol.style.Stroke({
      color: '#319FD3',
      width: 1,
    }),
    text: new ol.style.Text({
      font: '12px Calibri,sans-serif',
      fill: new ol.style.Fill({
        color: '#000',
      }),
      stroke: new ol.style.Stroke({
        color: '#fff',
        width: 3,
      })
    })
  });
  var styles = [style];

  var boundary = new ol.layer.Vector({
    source: new ol.source.GeoJSON({
      projection: 'EPSG:3857',
      url: jsonurl,
    }),
    style: function(feature, resolution) {
      style.getText().setText(resolution < 5000 ?  feature.get('name') : '');
      return styles;
    }
  });
  return boundary;
};


function getAgencyLayer() {

  var ll = getLongLat();

  var feature = new ol.Feature({
    geometry: new ol.geom.Point(ll),
    });

  var layer = new ol.layer.Vector({
    source: new ol.source.Vector({
      features: [feature],
      }),
    });

  return layer;
};
