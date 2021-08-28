

(function ($) {

  Drupal.behaviors.CheckPin = {
    attach: function(context, settings) {

    $('#checkPin').click(function(event) {
        console.log('PING')
        console.log($('#pin').val())
        var pin = $('#pin').val();

        $.ajax({
              url : "/operator/checkpin",
              type : "POST",
              contentType: "application/json",
              data : JSON.stringify({'pin': pin }),
              success: verifyCheckpin,
        });

        function verifyCheckpin (data, textStatus, jqXHR) {
            console.log(data)
            if(data.response == 'OK'){
                $('#mbresponse').html('Valid PIN');
            } else {
                $('#mbresponse').html('The PIN you entered is invalid');
            }
        };

        return false;
    });



   }
  };

})(jQuery);