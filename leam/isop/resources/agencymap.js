      var agencyList = function() {
        var panel = document.createDocumentFragment();
        var table = document.createElement("table");
        table.setAttribute("class", "agency-control");
        panel.appendChild(table);

        var features = this.getFeatures();
        for (var i=0; i<features.length; i++) {
          console.log(features[i].get('NAMELSAD10'));
          var arr = [
            '<a href="blah" class="agency-name">' + 
                 features[i].get('NAMELSAD10') + "</a>",
            features[i].get('AffordOwn') + " of 5",
            features[i].get('AffordRent'),
          ];
          var row = document.createElement("tr");
          row.innerHTML = "<td>" + arr.join("</td><td>") + "</td>";
          /*
          var cell = document.createElement("td");
          cell.appendChild( document.createTextNode(
                features[i].get('NAMELSAD10')));
          row.appendChild(cell);
          var cell = document.createElement("td");
          cell.appendChild( document.createTextNode("n of 5"));
          row.appendChild(cell);
          var cell = document.createElement("td");
          cell.appendChild( document.createTextNode("#"));
          row.appendChild(cell);
          */
          table.appendChild(row);
        };
        document.getElementById('controlp').appendChild(panel);
      };

      var controlPanel = function(opt_options) {
      
        var options = opt_options || {};
        var element = document.getElementById('controlp')
        var this_ = this;

        ol.control.Control.call(this, {
          element: element,
          target: options.target,
        });

      };
      ol.inherits(controlPanel, ol.control.Control);

      var style = new ol.style.Style({
        fill: new ol.style.Fill({
          color: 'rgba(255, 255, 255, 0.6)'
        }),
        stroke: new ol.style.Stroke({
          color: '#319FD3',
          width: 1
        }),
        text: new ol.style.Text({
          font: '12px Calibri,sans-serif',
          fill: new ol.style.Fill({
            color: '#000'
          }),
          stroke: new ol.style.Stroke({
            color: '#fff',
            width: 3
          })
        })
      });
      var styles = [style];
      var agencyLayer = new ol.layer.Vector({
        source: new ol.source.GeoJSON({
          projection: 'EPSG:3857',
          url: '++resource++leam.isop/flinthills.geojson'
        }),
        style: function(feature, resolution) {
          style.getText().setText(resolution < 5000 ? feature.get('name') : '');
          return styles;
        }
      });

      var map = new ol.Map({
        /*controls: ol.control.defaults().extend([ new controlPanel() ]), */
        target: 'map',
        layers: [
          new ol.layer.Tile({
            source: new ol.source.MapQuest({layer: 'osm'})
            }),
        ],
        view: new ol.View({
          center: ol.proj.transform([-96.5917, 39.1917], 
            'EPSG:4326', 'EPSG:3857'),
          zoom: 6,
        })
      });

      agencyLayer.getSource().once('change', agencyList);
      map.addLayer(agencyLayer);
      map.addControl( new controlPanel());

