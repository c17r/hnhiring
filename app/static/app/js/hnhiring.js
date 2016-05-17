var FilterLibrary = (function($) {

    function create(cbAdd, cbRemove, cbFilter) {

        var filters = [];

        function add(newFilter) {
            if (findExisting(newFilter))
                return;
            filters.push(newFilter);
            setStorage();
            cbAdd(newFilter);
            cbFilter(filters);
        }

        function remove(oldFilter) {
            if (!findExisting(oldFilter))
                return;
            removeEntry(oldFilter);
            setStorage();
            cbRemove(oldFilter);
            cbFilter(filters);
        }

        function load() {
            getStorage();
            $.each(filters, function(i, v) {
                cbAdd(v);
            });
            cbFilter(filters);
        }

        function clear() {
            var old = filters.slice();

            filters = [];
            setStorage();
            $.each(old, function(i, v) {
                cbRemove(v);
            });
            cbFilter(filters);
        }

        return {
            add: add,
            remove: remove,
            load: load,
            clear: clear
        };

        function findExisting(needle) {
            return $.inArray(needle, filters) != -1;
        }

        function removeEntry(needle) {
            var idx = $.inArray(needle, filters);

            if (idx == -1)
                return;

            filters.splice(idx, 1);
        }

        function setStorage() {
            var storage = $.localStorage;
            storage.set('filters', filters)
        }

        function getStorage() {
            var storage = $.localStorage;
            if (storage.isEmpty('filters'))
                filters = [];
            else
                filters = storage.get('filters');
        }
    }

    return {
        create: create
    }

})(window.jQuery);

var contents = [];

$(document).on('ready', function() {
    
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
        e.preventDefault();

        $('#filter input').val('');
        filters.clear();
    });

    $('#filter #add_filter').on('click', processAdd);
    $('#filter input').on('keyup', function(e) {
        if (e.keyCode == 13)
            processAdd(e);
    });
    function processAdd(e) {
        e.preventDefault();

        var $input = $('#filter input'),
            filter = $input.val();

        $input.val('');
        filters.add(filter);
    }

    $('#filters ul').on('click', '.remove_filter', function(e) {
        e.preventDefault();

        var remove = $(this).parents("li").attr('data');
        filters.remove(remove);
    });

    var filters = FilterLibrary.create(
        addFilter,
        removeFilter,
        filterWords);

    function addFilter(text) {
        var $li = $('<li/>');

        $li.attr('data', text);
        $li.html("&nbsp;<button class='remove_filter'>-</button>&nbsp;" + text);
        $('#filters ul').append($li);
    }

    function removeFilter(text) {
        $('#filters ul li').each(function(idx, li) {
            var $li = $(li),
                data = $li.attr('data');

            if (data == text) {
                $li.remove();
                return false;
            }
        });
    }

    function filterWords(filters) {
        var needles = [],
            cssClass = 'row1';
        
        $.each(filters, function(idx, text) {
           needles.push(new RegExp(text, 'gi')); 
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
        $entriesList.find('li').each(function() {

                var id = $(this).attr('id'),
                    content = $(this).find('.content')[0].innerText;

                contents[id] = content;

            });

        filters.load();

        updateCounts();
    }
    main();

});
