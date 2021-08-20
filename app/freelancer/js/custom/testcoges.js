

(function ($) {

  Drupal.behaviors.EndPoints = {
    attach: function(context, settings) {

//            $.ajax({
//              url : "/testcoges",
//              type : "GET",
//        //      contentType: "application/json",
//        //      dataType: 'json',
////              data : {'dabId': 'test' },
//              success: getStoredEndPointsData,
//            });

            $.ajax({
              url : "/coges_engine",
              type : "POST",
              contentType: "application/json",
              data : JSON.stringify({'command_code': '20' }),
              success: getStoredEndPointsData,
            });

          function getStoredEndPointsData (data, textStatus, jqXHR) {
              console.log(data)
            $('#cogesresp').html(data.response);

          };

   }
  };

})(jQuery);