function getTab(callback) {
    var queryInfo = {
        active: true,
        currentWindow: true
    };

    chrome.tabs.query(queryInfo, function(tabs) {
        callback(tabs[0]);
    });                                                                                 
}

chrome.tabs.onActivated.addListener(function(activeInfo) {
    chrome.storage.local.get("tabhistory", function(items) {
        console.log(items);
    });

    getTab(function(tab) {
        console.log(tab);

        chrome.storage.local.get("tabhistory", function(items) {
            var tabs = items.tabhistory;
            tabs = [tab].concat(tabs);
            console.log(tabs);

            chrome.storage.local.set({"tabhistory": tabs}, function() {
                console.log("tabhistory saved, length: " + tabs.length);
            });
        });
    });
    
});
