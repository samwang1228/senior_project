$(document).ready(function(){
    document.querySelector("#getFile").onchange = function(){
    document.querySelector("#file-name").textContent = this.files[0].name;
    }
});