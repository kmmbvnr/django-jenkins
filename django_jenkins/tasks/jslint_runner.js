/* JSLint Rhino Runner */

/*global
     load: true
     JSLINT: true
     readFile: true
     print: true
     process: true
     require: true
     global: true
 */

if (typeof process !== 'undefined') {
    var fs = require('fs');

    var jslint =  process.argv[2];
    var filename = process.argv[3];
    var format = process.argv[4];
    var fileContent = fs.readFileSync(filename, 'utf8');

    /* Loading jslint */
    var vm = require('vm');
    var jslintSrc = fs.readFileSync(jslint, 'utf8');
    vm.runInThisContext(jslintSrc);
    var JSLINT = global.JSLINT;
    delete global.JSLINT;    

    var print = console.log;
} else {
    var jslint = arguments[0];
    var filename = arguments[1];
    var format = arguments[2];
    var fileContent = readFile(filename);

    load(jslint);
}


JSLINT(fileContent, {
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
var report = JSLINT.data();

function escapeSpecialCharacters(str) {
    if (!str || str.constructor !== String) {
        return "";
    }
    return str.replace(/\"/g, "'").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/&/g, "&amp;");
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

