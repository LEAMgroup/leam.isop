      var agencyList = function() {
        var panel = document.createDocumentFragment();
        var table = document.createElement("table");
        table.setAttribute("class", "agency-control");
        panel.appendChild(table);
        var row = document.createElement("tr");
        row.innerHTML = '<th class="span3">Agency</th>' +
            '<th class="span1">Plans</th><th class="span1">Maps</th>';
        table.appendChild(row);

        var f = this.getFeatures();
        for (var i=0; i<f.length; i++) {
          console.log("agency="+f[i].get('name')+" url="+f[i].get('url'));
          var arr = [
            '<a href="' + f[i].get('url') + '" class="agency-name">' + 
                 f[i].get('name') + "</a>",
            f[i].get('plans') + " of 5",
            f[i].get('maps'),
          ];
          var row = document.createElement("tr");
          row.innerHTML = "<td>" + arr.join("</td><td>") + "</td>";
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

      var iconStyle = new ol.style.Style({
        image: new ol.style.Icon({
          positioning: 'bottom-center',
          src: '++resource++leam.isop/marker.png',
        }),
      });

      console.log('adding county layer');
      var countyLayer = new ol.layer.Vector({
        source: new ol.source.GeoJSON({
          projection: 'EPSG:3857',
          url: '++resource++leam.isop/flinthills.geojson'
          }),
        style: styles,
          /*
        style: function(feature, resolution) {
          style.getText().setText(resolution < 5000 ? feature.get('name') : '');
          return styles;
        }
        */
      });

      console.log('adding layer');
      var agencyLayer = new ol.layer.Vector({
        source: new ol.source.GeoJSON({
          projection: 'EPSG:3857',
          /*url: '++resource++leam.isop/flinthills.geojson' */
          url: '@@agencylocs',
          }),
        style: iconStyle,
          /*
        style: function(feature, resolution) {
          style.getText().setText(resolution < 5000 ? feature.get('name') : '');
          return styles;
        }
        */
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
          zoom: 7,
        })
      });

      map.on('pointermove', function(e) {
        var pixel = map.getEventPixel(e.originalEvent);
        var hit = map.hasFeatureAtPixel(pixel);
        if (hit) { console.log('HIT'); }
      });

      agencyLayer.getSource().once('change', agencyList);
      map.addLayer(agencyLayer);
      map.addControl( new controlPanel());

