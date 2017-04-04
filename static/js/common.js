$(window).load(init());

function init() {
  $("#upload").click(function() {
    var message = function(text) {
       $.blockUI({
           message: text,
           fadeIn: 200,
           fadeOut: 0,
           overlayCSS:  {
                backgroundColor: '#aaa',
                opacity:         0.6,
                cursor:          'wait'
           },
           css: {
             padding: '10px',
             margin:  '0, auto',
             height:  '50px',
             border:  '2px none #aaa',
             backgroundColor: '#aaa',
             opacity: 0.8
           }
       });
    };
    message('<img src="static/img/busy.gif" /> Now Processing...');
    var formData = new FormData($('#uploadForm')[0]);
    $.ajax({
                url: '/upload',
                type: 'post',
                data: formData,
                dataType: "json",
                processData: false,
                contentType: false,
            }).done(function (data) {
                console.log('done');

            }).fail(function (data) {
                console.log('fail');

            }).always(function (data) {
                var start = data.indexOf('<span id="result">');
                console.log(start);
                var fin = data.lastIndexOf("</span>");
                console.log(fin);
                var body = data.slice(start, fin+7);
                $('span').replaceWith(body);
                $.unblockUI();
            });
    return false;
  });
}
