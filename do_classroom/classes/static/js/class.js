jQuery(function ($) {

    $(document).ready(function() {
        $('.power').each(function(){
          status = $(this).parent().parent().siblings().children('.status').html()

          if (status == "new") {
            $(this).addClass('disabled');
            $(this).siblings().addClass('disabled');
          }
        });
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('.power').on('click', function() {
      event.preventDefault();

      if ( $(this).hasClass('on') ) {
        $(this).children('span').removeClass('glyphicon-play');
        $(this).removeClass('btn-success');
        $(this).removeClass('on');
        $(this).children('span').addClass('glyphicon-off');
        $(this).addClass('btn-primary');
        $(this).addClass('off');
        $(this).attr("title","Power off");
        $(this).parent().parent().siblings().children('.status').html('active');

        var csrftoken = getCookie('csrftoken');
        droplet_id = $(this).parent().parent().parent().attr('id');
        $.ajax({
            type: "POST",
            url: $(location).attr('pathname'),
            data: {
                    csrfmiddlewaretoken:csrftoken,
                    droplet:droplet_id,
                    action: 'on'
                  },
            success: function (data) {
                console.log("Powering on " + droplet_id);
            }
        });
      }
      else if ( $(this).hasClass('off') ) {
        $(this).children('span').removeClass('glyphicon-off');
        $(this).removeClass('btn-primary');
        $(this).removeClass('off');
        $(this).children('span').addClass('glyphicon-play');
        $(this).addClass('btn-success');
        $(this).addClass('on');
        $(this).attr("title","Power on");
        $(this).parent().parent().siblings().children('.status').html('off');

        var csrftoken = getCookie('csrftoken');
        droplet_id = $(this).parent().parent().parent().attr('id');
        $.ajax({
            type: "POST",
            url: $(location).attr('pathname'),
            data: {
                    csrfmiddlewaretoken:csrftoken,
                    droplet:droplet_id,
                    action: 'off'
                  },
            success: function (data) {
                console.log("Powering of " + droplet_id);
            }
        });

      };
    });

    $('.destroy').on('click', function() {
      event.preventDefault();
      $(this).parent().parent().parent().hide();
      var csrftoken = getCookie('csrftoken');
      droplet_id = $(this).parent().parent().parent().attr('id');
      $.ajax({
          type: "POST",
          url: $(location).attr('pathname'),
          data: {
                  csrfmiddlewaretoken:csrftoken,
                  droplet:droplet_id,
                  action: 'destroy'
                },
          success: function (data) {
              console.log("Destroying " + droplet_id);
          }
      });
    });

    $('.add-droplet').on('click', function() {
      event.preventDefault();
      var $btn = $(this).button('loading')
      var csrftoken = getCookie('csrftoken');

      $.ajax({
          type: "POST",
          url: $(location).attr('pathname'),
          data: {
                  csrfmiddlewaretoken:csrftoken,
                  action: 'add-droplet'
                },
          success: function (data) {
              console.log("Add new droplet...");
              window.location.reload()
          }
      });
    });

    $(document).on("click", ".end-class", function(e) {
      event.preventDefault();
      console.log("Clicked end-class")
      msg = "<h3><p>Are you sure you want to do this?</p></h3><p>Ending the class will destroy all droplets associated with it.</p>"
      bootbox.confirm(msg, function(result) {
          if (result == true) {
            var $btn = $(this).button('loading')
            var csrftoken = getCookie('csrftoken');

            $.ajax({
                type: "POST",
                url: $(location).attr('pathname'),
                data: {
                        csrfmiddlewaretoken:csrftoken,
                        action: 'end-class'
                      },
                success: function (data) {
                    console.log("Ending class and cleaning up...");
                    window.location.replace($(location).attr('origin'));
                }
            });
          }
          else {
            console.log("Oh hell, no...");
          }
      });
    });
});