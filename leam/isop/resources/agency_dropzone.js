    var plans = new Dropzone("div#add-plan", {
        url: "add-plan",
        previewsContainer: "#add-plan",
        maxFiles:1,
        acceptedFiles:"application/pdf",
        init: function() {
          this.on("complete", function(file) {
            console.debug("plan upload complete");
            window.location = file.xhr.responseURL;
            });
          },
        });

    var layers = new Dropzone("div#add-layer", {
        url: "add-layer",
        previewsContainer: "#add-layer",
        maxFiles:1,
        init: function() {
          this.on("complete", function(file) {
            console.debug("layer upload complete");
            window.location = file.xhr.responseURL;
            });
          },
        });
 
