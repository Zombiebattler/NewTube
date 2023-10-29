// ==UserScript==
// @name         NewTube
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  replacec url with custom url
// @author       Zombiebattler
// @match        https://www.youtube.com/watch?v=*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=youtube.com
// @grant        none
// ==/UserScript==

// Eine Funktion, um das Video einzubetten


var currentURL = window.location.href;

console.log(currentURL);

var url = "http://127.0.0.1:6969/" + currentURL;

window.location.href = url;
