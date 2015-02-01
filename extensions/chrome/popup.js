function renderStatus(text) {
  document.getElementById('status').textContent = text;
}

document.addEventListener('DOMContentLoaded', function() {
    chrome.storage.local.get("tabhistory", function(items) {
        var tabs = items.tabhistory;

        var text = "";
        for(var i=0; i<tabs.length; i++) {
            text += "Title: " + tabs[i].title + "\n" + 
                "Url: " + tabs[i].url + 
                "\n- - - - - - - - - - - -\n";
        }

        renderStatus(text);
    });
});
