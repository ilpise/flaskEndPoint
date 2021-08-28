

(function ($) {

  Drupal.behaviors.CheckPin = {
    attach: function(context, settings) {

    $('#checkPin').click(function(event) {
        console.log('PING')
        console.log($('#pin').val())

        $.ajax({
          url : "/operator/checkpin",
          type : "GET",
          success: readModbusResponse,
        });

        function readModbusResponse (data, textStatus, jqXHR) {
            console.log(data)
//            $('#mbresponse').html(data.response);
            $('#mbresponse').html(data.response);
        };

        return false;
    });



   }
  };

})(jQuery);