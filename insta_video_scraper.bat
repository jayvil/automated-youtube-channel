  @if (@X) == (@Y) @end /* JScript comment 
    @echo off   
    cscript //E:JScript //nologo "%~f0" %*
    exit /b %errorlevel%       
@if (@X)==(@Y) @end JScript comment */

// var days=parseInt(WScript.Arguments.Item(0));


Date.prototype.subtractDays = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() - days);
    return date;
}

var date = new Date();
// WScript.Echo(date.toDateString());
// WScript.Echo(date.subtractDays(days));
// WScript.Echo("Year: " + date.getFullYear());
// WScript.Echo("Month: " + date.getMonth());
// WScript.Echo("DayOfTeWEek: " + date.getDay());


WScript.Echo('Instagram Video Scraper: ' + date.getYear(), date.getMonth()+1, date.getDate());

var wshShell = new ActiveXObject("WScript.Shell");
// Get all videos from today from accounts followed
wshShell.Run('ins -l <account_name> @<account_name> --dirname-pattern=staging_folder/{profile} --filename-pattern={profile}+{date_utc}_UTC+{typename} --max-connection-attempts 1 --no-captions --no-metadata-json --no-profile-pic --no-pictures --no-video-thumbnails --post-filter="date_utc>datetime(' + date.getYear() + ',' + (date.getMonth()+1) + ',' + (date.getDate()-1) + ')"');



