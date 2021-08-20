

(function ($) {

  Drupal.behaviors.EndPoints = {
    attach: function(context, settings) {

            $.ajax({
              url : "/testcoges",
              type : "GET",
        //      contentType: "application/json",
        //      dataType: 'json',
//              data : {'dabId': 'test' },
              success: getStoredEndPointsData,
            });

          function getStoredEndPointsData (data, textStatus, jqXHR) {
              console.log(data)
//            $().html();

          };

   }
  };

})(jQuery);