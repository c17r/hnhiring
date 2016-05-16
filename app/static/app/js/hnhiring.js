
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

    $('#filter #clear_all').on('click', function(e) {
        e.preventDefault()

        $('#filter input').val('');
        $("#filters ul").empty();

        filterWords();
    });

    $('#filter #add_filter').on('click', addFilter);
    $('#filter input').on('keyup', function(e) {
        if (e.keyCode == 13)
            addFilter(e);
    });

    function addFilter(e) {
        e.preventDefault();

        var $input = $('#filter input'),
            filter = $input.val(),
            $li = $('<li/>');

        $li.attr('data', filter)
        $li.html("&nbsp;<button class='remove_filter'>-</button>&nbsp;" + filter)
        $('#filters ul').append($li)

        $input.val('');

        filterWords();
    }

    $('#filters ul').on('click', '.remove_filter', function(e) {
        e.preventDefault();

        $(this).parents("li").remove()
        filterWords();
    });

    function filterWords() {
        var needles = [],
            cssClass = 'row1';

        $('#filters ul li').each(function(idx, li) {
            $li = $(li)
            needles.push(new RegExp($li.attr('data'), 'gi'));
        });

        $("#entries ul li:visible .content").highlightRegex();

        $.each(contents, function(idx, text) {

            var elem = $('#' + idx);
            elem.removeClass('row1');
            elem.removeClass('row2');

            var found = true;
            $.each(needles, function(i, needle) {
                if (!needle.test(text))
                    found = false
            });

            if (found) {
                elem.show();
                elem.addClass(cssClass);
                cssClass = (cssClass == 'row1') ? 'row2' : 'row1';
            } else {
                elem.hide();
            }

        });

        $.each(needles, function(idx, needle) {
            $("#entries ul li:visible .content").highlightRegex(needle);
        });

        updateCounts();
    }

    function updateCounts() {
        var items = $("#entries ul li"),
            total = items.length,
            visible = items.filter("li:visible").length;

        $("#counts").text(visible + "/" + total);
    }

    function main() {
        updateCounts();
    }
    main();

});
