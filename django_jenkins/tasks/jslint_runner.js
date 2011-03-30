/* JSLint Rhino Runner */

/*global
     load: true
     JSLINT: true
     readFile: true
     print: true
 */

var jslint = arguments[0];
var filename = arguments[1];

load(jslint);

JSLINT(readFile(filename), {
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

/*
 * Output in pylint format
 */
var i = 0;
if (report.errors) {
    for (i = 0; i < report.errors.length; i += 1) {
        var entry = report.errors[i];
        if (entry) {
            if (isFinite(entry.line)) {
                print(filename + ':' + entry.line + ': [E] ' + entry.reason);
            }
        }
    }
}

if (report.implieds) {
    for (i = 0; i < report.implieds.length; i += 1) {
        var entry = report.implieds[i];
        if (entry) {
            if (isFinite(entry.line)) {
                print(filename + ':' + entry.line + ': [W] Implied global ' + entry.name);
            }
        }
    }
}

if (report.unused) {
    for (i = 0; i < report.unused.length; i += 1) {
        var entry = report.unused[i];
        if (entry) {
            if (isFinite(entry.line)) {
                print(filename + ':' + entry.line + ': [W] Unused variable ' + entry.name);
            }
        }
    }
}
