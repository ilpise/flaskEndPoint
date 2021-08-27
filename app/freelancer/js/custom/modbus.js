
(function ($) {

  Drupal.behaviors.Modbus = {
    attach: function(context, settings) {

    $('button').click(function(event) {
        console.log('PING')
        console.log($(this).attr("value"))

        $.ajax({
          url : "/modbus/api/",
          type : "GET",
          success: readModbusResponse,
        });

        function readModbusResponse (data, textStatus, jqXHR) {
            console.log(data)
            $('#mbresponse').html(data.response);
        };

        return false;
    });



   }
  };

})(jQuery);