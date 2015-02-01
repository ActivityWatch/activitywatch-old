function renderStatus(text) {
    document.getElementById('status').textContent = text;
}

document.addEventListener('DOMContentLoaded', function() {
    getTabHistory(function(tabs) {
        var text = "";
        for(var i=0; i<tabs.length; i++) {
            text += "Title: " + tabs[i].title + "\n" + 
                "Url: " + tabs[i].url + 
                "\n- - - - - - - - - - - -\n";
        }
        renderStatus(text);
    });
});
