
var agency_add_plans = new Dropzone("#add-plan", {
    url: "add-plan",
    previewsContainer: "#add-plan",
    autoProcessQueue: false,
    maxFiles:1,
    init: function() {
      var _this = this;

      jQuery("#plan-modal .plan-close").on("click", function() {
        jQuery("#plan-modal").modal('hide');
        _this.removeAllFiles();
      });

      jQuery("#plan-modal .plan-upload").on("click", function() {
        jQuery("#plan-modal").modal('hide');
        _this.processQueue();
      });

      _this.on("addedfile", function(file) {
        jQuery("#plan-modal").modal({'show':true});
      });

      _this.on("sending", function(file, xhr, data) {
        data.append('plan-title', jQuery('#plan-title').val());
        data.append('plan-type', jQuery('#plan-type').val());
      })

      _this.on("complete", function(file) {
        console.debug("plan upload complete");
        window.location = file.xhr.responseURL;
        });
      },
    });

var agency_add_layers = new Dropzone("#add-layer", {
    url: "add-layer",
    previewsContainer: "#add-layer",
    autoProcessQueue: false,
    maxFiles:1,
    init: function() {
      var _this = this;

      jQuery("#layer-modal .layer-close").on("click", function() {
        jQuery("#layer-modal").modal('hide');
        _this.removeAllFiles();
      });

      jQuery("#layer-modal .layer-upload").on("click", function() {
        jQuery("#layer-modal").modal('hide');
        _this.processQueue();
      });

      _this.on("addedfile", function(file) {
        jQuery("#layer-modal").modal({'show':true});
      });

      _this.on("sending", function(file, xhr, data) {
        data.append('layer-title', jQuery('#layer-title').val());
        data.append('layer-type', jQuery('#layer-type').val());
      })

      _this.on("complete", function(file) {
        console.debug("layer upload complete");
        window.location = file.xhr.responseURL;
        });
      },
    });
