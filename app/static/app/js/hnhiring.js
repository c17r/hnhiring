var FilterLibrary = (function($) {

    function create(cbAdd, cbRemove, cbFilter) {

        function emptyData() {
            return {};
        }

        var filters = emptyData();

        function add(newFilter) {
            if (findExisting(newFilter))
                return;
            filters[newFilter] = 1;
            setStorage();
            cbAdd(newFilter, 1);
            cbFilter(filters);
        }

        function remove(oldFilter) {
            if (!findExisting(oldFilter))
                return;
            delete filters[oldFilter];
            setStorage();
            cbRemove(oldFilter);
            cbFilter(filters);
        }

        function load() {
            getStorage();
            $.each(filters, function(key, enabled) {
                cbAdd(key, enabled);
            });
            cbFilter(filters);
        }

        function clear() {
            $.each(filters, function(key, enabled) {
                cbRemove(key);
            });
            filters = emptyData();
            setStorage();
            cbFilter(filters);
        }

        function change(filter, enabled) {
            if (!findExisting(filter))
                return;
            filters[filter] = enabled
            setStorage();
            cbFilter(filters);
        }

        return {
            add: add,
            remove: remove,
            load: load,
            clear: clear,
            change: change
        };

        function findExisting(needle) {
            return $.inArray(needle, Object.keys(filters)) !== -1;
        }

        function setStorage() {
            var storage = $.localStorage;
            storage.set('filters', filters)
        }

        function getStorage() {
            var storage = $.localStorage;
            if (storage.isEmpty('filters'))
                filters = emptyData();
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

    var $topHat = $('#tophat'),
        $about = $topHat.find('#about'),
        $aboutPage = $('#about-page'),
        $months = $topHat.find('#months'),
        $filter = $topHat.find('#filter'),
        $filters = $('#filters'),
        $filterTable = $filters.find('table'),
        $entries = $('#entries'),
        $entriesList = $entries.find('ul'),
        $counts = $('#counts');

    $about.find('a').on('click', function(e) {
        e.preventDefault();

        $aboutPage.toggle();

    });

    $aboutPage.find('.header a').on('click', function(e) {
        e.preventDefault();

        $aboutPage.hide();
    });

    $months.find('select').on('change', function(e) {
        e.preventDefault();

        var monthId = $(this).val();
        window.location = '/month/' + monthId;

    });

    $filter.find('#clear_all').on('click', function(e) {
        e.preventDefault();

        $filter.find('input').val('');
        filters.clear();
    });

    $filter.find('#add_filter').on('click', processAdd);
    $filter.find('input').on('keyup', function(e) {
        if (e.keyCode === 13)
            processAdd(e);
    });
    function processAdd(e) {
        e.preventDefault();

        var $input = $filter.find('input'),
            filter = $input.val();

        $input.val('');
        filters.add(filter);
    }

    $filterTable.on('click', '.remove_filter', function(e) {
        e.preventDefault();

        var remove = $(this).parents("tr").attr('data');
        filters.remove(remove);
    });

    $filterTable.on('click', ':checkbox', function(e) {
        var enabled = this.checked ? 1 : 0,
            key = $(this).parents("tr").attr('data');

        filters.change(key, enabled);
    });

    var filters = FilterLibrary.create(
        addFilter,
        removeFilter,
        filterWords);

    function addFilter(text, enabled) {
        var $tr = $('<tr/>'),
            checkedText = enabled === 1 ? ' checked' : '',
            $checkBox = $('<td/>'),
            $textBox = $('<td/>'),
            $buttonBox = $('<td/>');

        $tr.attr('data', text);

        $checkBox.html('<input type="checkbox"' + checkedText + '>');
        $textBox.html(text);
        $buttonBox.html('<button class="remove_filter">-</button>')

        $tr.append($checkBox);
        $tr.append($textBox);
        $tr.append($buttonBox);
        $filterTable.append($tr);
    }

    function removeFilter(text) {
        $filterTable.find('tr').each(function(idx, tr) {
            var $tr = $(tr),
                data = $tr.attr('data');

            if (data === text) {
                $tr.remove();
                return false;
            }
        });
    }

    function filterWords(filters) {
        var needles = [],
            cssClass = 'row1';
        
        $.each(filters, function(text, enabled) {
            if (enabled === 1)
                needles.push(new RegExp(text, 'gi'));
        });
        
        $entriesList.find("li:visible .content").highlightRegex();

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
                cssClass = (cssClass === 'row1') ? 'row2' : 'row1';
            } else {
                elem.hide();
            }

        });

        $.each(needles, function(idx, needle) {
            $entriesList.find("li:visible .content").highlightRegex(needle);
        });

        updateCounts();
    }

    function updateCounts() {
        var items = $entriesList.find("li"),
            total = items.length,
            visible = items.filter("li:visible").length;

        $counts.text(visible + "/" + total);
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
