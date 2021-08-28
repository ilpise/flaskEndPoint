

(function ($) {

  Drupal.behaviors.Operator = {
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
                $('#step1').hide()
                $('#step2').show()
            } else {
                $('#mbresponse').html('The PIN you entered is invalid');
                $('#pin').val('')
            }
        };

        return false;
    });

    $('#s2_carico').click(function(event) {
        $('#step2').hide()
        $('#s_cs').show()
        return false;
    });


   }
  };

})(jQuery);