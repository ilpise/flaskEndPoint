

(function ($) {

  Drupal.behaviors.CustomerMail = {
    attach: function(context, settings) {

//    $('.softkeys').once().each(function() {
//        $('#step2').hide()
//        $('#s_cs').show()
//        return false;
//    });

$('.softkeys').softkeys({
                    target : $('.softkeys').data('target'),
                    layout : [
                        [
                            ['`','~'],
                            ['1','!'],
                            ['2','@'],
                            ['3','#'],
                            ['4','$'],
                            ['5','%'],
                            ['6','^'],
                            ['7','&amp;'],
                            ['8','*'],
                            ['9','('],
                            ['0',')'],
                            ['-', '_'],
                            ['=','+'],
                            'delete'
                        ],
                        [
                            'q','w','e','r','t','y','u','i','o','p',
                            ['[','{'],
                            [']','}']
                        ],
                        [
                            'capslock',
                            'a','s','d','f','g','h','j','k','l',
                            [';',':'],
                            ["'",'&quot;'],
                            ['\\','|']
                        ],
                        [
                            'shift',
                            'z','x','c','v','b','n','m',
                            [',','&lt;'],
                            ['.','&gt;'],
                            ['/','?'],
                            ['@','@']
                        ]
                    ]
                });

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