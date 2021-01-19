/*
	Fractal by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

function prepCSVRow(arr, columnCount, initial, delimiter) {
    var row = ''; 
    var newLine = '\r\n'; 
    function splitArray(_arr, _count) {
      var splitted = [];
      var result = [];
      _arr.forEach(function(item, idx) {
        if ((idx + 1) % _count === 0) {
          splitted.push(item);
          result.push(splitted);
          splitted = [];
        } else {
          splitted.push(item);
        }
      });
      return result;
    }
    var plainArr = splitArray(arr, columnCount);
    plainArr.forEach(function(arrItem) {
      arrItem.forEach(function(item, idx) {
        row += item + ((idx + 1) === arrItem.length ? '' : delimiter);
      });
      row += newLine;
    });
    return initial + row;
  }

  
(function($) {

	var	$window = $(window),
		$body = $('body');

	// Breakpoints.
		breakpoints({
			xlarge:   [ '1281px',  '1680px' ],
			large:    [ '981px',   '1280px' ],
			medium:   [ '737px',   '980px'  ],
			small:    [ '481px',   '736px'  ],
			xsmall:   [ '361px',   '480px'  ],
			xxsmall:  [ null,      '360px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Mobile?
		if (browser.mobile)
			$body.addClass('is-mobile');
		else {

			breakpoints.on('>medium', function() {
				$body.removeClass('is-mobile');
			});

			breakpoints.on('<=medium', function() {
				$body.addClass('is-mobile');
			});

		}

	// Scrolly.
		$('.scrolly')
			.scrolly({
				speed: 1500
			});


function exportCSVTSV(titles, data, delimiter, extension) {
  var CSVString = prepCSVRow(titles, titles.length, '', delimiter);
  CSVString = prepCSVRow(data, titles.length, CSVString, delimiter);

  var downloadLink = document.createElement("a");
  var blob = new Blob(["\ufeff", CSVString]);
  var url = URL.createObjectURL(blob);
  downloadLink.href = url;
  downloadLink.download = "data." + extension;

  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
}

//Export
$('#export').click(function() {
    var titles = [];
    var data = [];
  
    $('#table_results th').each(function() {
      titles.push($(this).text());
    });
  
    $('#table_results td').each(function() {
      data.push($(this).text());
    });

    exportCSVTSV(titles, data, ",", "csv");
  });

//Export TSV
$('#exportTSV').click(function() {
  var titles = [];
  var data = [];

  $('#table_results th').each(function() {
    titles.push($(this).text());
  });

  $('#table_results td').each(function() {
    data.push($(this).text());
  });

  exportCSVTSV(titles, data, "\t", "tsv");
});  
    
})(jQuery);