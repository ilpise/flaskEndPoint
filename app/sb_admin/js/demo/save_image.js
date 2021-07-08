(function($) {
    "use strict"; // Start of use strict

    $( "#bkgr" ).click(function() {
        console.log('button clicked');
        var stream = $("#bg");
        console.log(stream.width());
        console.log(stream.height());

        let imageCanvas = document.createElement('canvas');
        let imageCtx = imageCanvas.getContext("2d");

        //Make sure the canvas is set to the current video size
        imageCanvas.width = stream.width();
        imageCanvas.height = stream.height();

        console.log(imageCanvas);

        imageCtx.drawImage(v, 0, 0, stream.width(), stream.height());

        //Convert the canvas to blob and post the file
        imageCanvas.toBlob(postFile, 'image/jpeg');
    });


    let v = document.getElementById("bg");
//    let v = $("#bg");
    console.log(v);

    //create a canvas to grab an image for upload
//    let imageCanvas = document.createElement('canvas');
//    let imageCtx = imageCanvas.getContext("2d");

    //Add file blob to a form and post
    function postFile(file) {
        let formData = new FormData();
        formData.append("image", file);

//        let xhr = new XMLHttpRequest();
//        xhr.open('POST', 'http://localhost:5000/image', true);
//        xhr.onload = function () {
//            if (this.status === 200)
//                console.log(this.response);
//            else
//                console.error(xhr);
//        };
//        xhr.send(formdata);

        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", "http://localhost:5000/image");

        // check when state changes,
        xmlhttp.onreadystatechange = function() {

            if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
//                alert(xmlhttp.responseText);
                console.log(xmlhttp.responseText);
            }
        }

        xmlhttp.send(formData);

    }

    //Get the image from the canvas
    function sendImagefromCanvas() {
        console.log('sendImagefromCavas');
        console.log(v.videoWidth);

        //Make sure the canvas is set to the current video size
        imageCanvas.width = v.videoWidth;
        imageCanvas.height = v.videoHeight;

        console.log(imageCanvas);

        imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight);

        //Convert the canvas to blob and post the file
        imageCanvas.toBlob(postFile, 'image/jpeg');
    }

    //Take a picture on click
    v.onclick = function() {
        console.log('click');
        sendImagefromCanvas();
    };

 })(jQuery); // End of use strict