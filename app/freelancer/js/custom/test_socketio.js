
(function ($) {

  Drupal.behaviors.TestSI = {
    attach: function(context, settings) {

    var socket = io();
    socket.on('connect', function() {
        console.log('connected');
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    socket.on('my response', function(msg) {
        console.log(msg)
//        $('#log').append('<p>Received: ' + msg.data + '</p>');
    });

    // Button
    $('#emit').click(function(event) {
        console.log('EMIT')
        // socket.emit('my event', {data: $('#emit_data').val()});
        socket.emit('my event', {data: 'CIAO CIACIO'});
        return false;
    });


    $('#ping').click(function(event) {
        console.log('PING')
        // socket.emit('my event', {data: $('#emit_data').val()});
            $.ajax({
              url : "/ping",
              type : "GET",
//              contentType: "application/json",
//              data : JSON.stringify({'command_code': '20' }),
              success: getStoredEndPointsData,
            });

            function getStoredEndPointsData (data, textStatus, jqXHR) {
              console.log(data)
            $('#cogesresp').html(data.response);

          };


        return false;
    });



   }
  };

})(jQuery);