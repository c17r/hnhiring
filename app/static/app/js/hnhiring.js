
var contents = [];

$(document).on('ready', function() {

    $('#entries ul li').each(function(li) {

        var id = $(this).attr('id'),
            content = $(this).find('.content')[0].innerText;

        contents[id] = content;

    });

    $('#about a').on('click', function(e) {
        e.preventDefault();

        $('#about-page').toggle();

    });

    $('#about-page .header a').on('click', function(e) {
        e.preventDefault();

        $('#about-page').hide();
    });

    $('#months select').on('change', function(e) {
        e.preventDefault();

        var monthId = $(this).val();
        window.location = '/month/' + monthId;

    });

    $('#filter input').on('keyup', $.debounce(250, filterWords));

    function filterWords(e) {
        e.preventDefault();

        var needleVal = $(this).val(),
            needle = new RegExp(needleVal, "gi"),
            cssClass = 'row1';

        $("#entries ul li:visible .content").highlightRegex();

        $.each(contents, function(idx, text) {

            var elem = $('#' + idx);
            elem.removeClass('row1');
            elem.removeClass('row2');

            if (needle.test(text)) {
                elem.show();
                elem.addClass(cssClass);
                cssClass = (cssClass == 'row1') ? 'row2' : 'row1';
            } else {
                elem.hide();
            }

        });

        $("#entries ul li:visible .content").highlightRegex(needle);

    }

});
