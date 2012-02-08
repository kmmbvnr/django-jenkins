/* JSLint Rhino Runner */

/*global
 load: true
 JSLINT: true
 readFile: true
 print: true
 */
var filename, jslint_fn, _JSLINT, format, config_fn;

if (typeof process !== 'undefined') {  // node.js
  jslint_fn = process.argv[2];
  var node = true
    , jslint = require(jslint_fn)
    , fs = require('fs')
    , path = require('path')
    , print = console.log;

  if (typeof jslint.JSLINT === 'undefined') {
    _JSLINT = jslint.JSHINT;
  } else {
    _JSLINT = jslint.JSLINT;
  }

  filename = process.argv[3];
  format = process.argv[4];
  config_fn = process.argv[5];

} else {  // rhino
  jslint_fn = arguments[0];
  filename = arguments[1];
  format = arguments[2];
  config_fn = arguments[3];
  load(jslint_fn);

  if (typeof JSLINT === 'undefined') {
    _JSLINT = JSHINT;
  } else {
    _JSLINT = JSLINT;
  }
}


function _existsFile(filename) {
  if (node) {
    return path.existsSync(filename);
  } else {
    var f = new java.io.File(filename);
    return f.exists();
  }
}


function _readFile(filename) {
  if (node) {
    return fs.readFileSync(filename, 'utf8');
  } else {
    return readFile(filename);
  }
}


function _removeJsComments(str) {
  str = str || '';
  str = str.replace(/\/\*[\s\S]*(?:\*\/)/g, ''); //everything between "/* */"
  str = str.replace(/\/\/[^\n\r]*/g, ''); //everything after "//"
  return str;
}


function _loadAndParseConfig(filePath) {
  return _existsFile(filePath) ?
    JSON.parse(_removeJsComments(_readFile(filePath))) : {};
}


function _mergeConfigs(dest, source) {
  var prop;
  for (prop in source) {
    if (typeof prop === 'string') {
      dest[prop] = source[prop];
    }
  }
  return dest;
}


var defaults = {
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
}
  , options = _mergeConfigs(defaults, _loadAndParseConfig(config_fn));




_JSLINT(_readFile(filename), options);
var report = _JSLINT.data();

function escapeSpecialCharacters(str) {
  if (!str || str.constructor !== String) {
    return "";
  }
  return str.replace(/&/g, "&amp;").replace(/"/g, "'").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/*
 * Output in jslint-xml format
 */
if (format === 'xml') {
  print("<file name=\"" + filename + "\">");
}

var i = 0;
if (report.errors) {
  for (i = 0; i < report.errors.length; i += 1) {
    var entry = report.errors[i];
    if (entry) {
      if (isFinite(entry.line)) {
        if (format === 'xml') {
          print('<issue line="' + entry.line + '"' +
            ' char="' + entry.character + '"' +
            ' reason="' + escapeSpecialCharacters(entry.reason) + '"' +
            ' evidence="' + escapeSpecialCharacters(entry.evidence) + '"/>');
        } else {
          print(filename + ':' + entry.line + ': [E] ' + entry.reason);
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
            print('<issue line="' + entry.line + '"' +
              ' reason="Unused variable"' +
              ' evidence="' + escapeSpecialCharacters(entry.name) + '"/>');
          } else {
            print(filename + ':' + entry.line + ': [W] Unused variable ' + entry.name);
          }
        }
      }
    }
  }
}

if (format === 'xml') {
  print('</file>');
}

