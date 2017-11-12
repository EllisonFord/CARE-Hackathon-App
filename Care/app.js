
let _userToken = "M2YyZjFkNDgtZjdmNi00ZDY4LTg2NGQtYmY0OWQ3M2VlN2IyOWE5OWYzODUtNDgw";
let _logSpace = "Y2lzY29zcGFyazovL3VzL1JPT00vZTQwYjY0ZjAtYzZlMi0xMWU3LWE2MTMtMjMxNTZlYmRjZDQw";
let _commSpace = "Y2lzY29zcGFyazovL3VzL1JPT00vZTQwYjY0ZjAtYzZlMi0xMWU3LWE2MTMtMjMxNTZlYmRjZDQw";

function createSpace(_element, space){

    if ( space === "log" ) {
        spaceId = _logSpace;
    } else if ( space === "communication" ) {
        spaceId = _commSpace;
    } else {
        return;
    }

    ciscospark.widget(_element).spaceWidget({
      accessToken: _userToken,
      spaceId: _spaceId
    });
}
