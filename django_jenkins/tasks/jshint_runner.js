/* JSLint Rhino Runner */

/*global
 load: true
 JSLINT: true
 readFile: true
 print: true
 */

var jshint_fn = process.argv[2];
var filename = process.argv[3];
var format = process.argv[4];

var jshint = require(jshint_fn);
var fs = require('fs');

jshint.JSHINT(fs.readFileSync(filename, 'utf8'), {
  white: true,
  onevar: true,
  undef: true,
  newcap: true,
  nomen: true,
  regexp: true,
  plusplus: true,
  bitwise: true,
  devel: true,
  maxerr: 50,
  browser: true,
  indent: 4
});
var report = jshint.JSHINT.data();

function escapeSpecialCharacters(str) {
  if (!str || str.constructor !== String) {
    return "";
  }
  return str.replace(/\"/g, "'").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/*
 * Output in jslint-xml format
 */
if (format === 'xml') {
  console.log("<file name=\"" + filename + "\">");
}

var i = 0;
if (report.errors) {
  for (i = 0; i < report.errors.length; i += 1) {
    var entry = report.errors[i];
    if (entry) {
      if (isFinite(entry.line)) {
        if (format === 'xml') {
          console.log('<issue line="' + entry.line + '"' +
            ' char="' + entry.character + '"' +
            ' reason="' + escapeSpecialCharacters(entry.reason) + '"' +
            ' evidence="' + escapeSpecialCharacters(entry.evidence) + '"/>');
        } else {
          console.log(filename + ':' + entry.line + ': [E] ' + entry.reason);
        }
      }
    }
  }
  if (report.unused) {
    for (i = 0; i < report.unused.length; i += 1) {
      var entry = report.unused[i];
      if (entry) {
        if (isFinite(entry.line)) {
          if (format === 'xml') {
            console.log('<issue line="' + entry.line + '"' +
              ' reason="Unused variable"' +
              ' evidence="' + escapeSpecialCharacters(entry.name) + '"/>');
          } else {
            console.log(filename + ':' + entry.line + ': [W] Unused variable ' + entry.name);
          }
        }
      }
    }
  }
}

if (format === 'xml') {
  console.log('</file>');
}

