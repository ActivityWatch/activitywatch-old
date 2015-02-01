function getTab(callback) {
    var queryInfo = {
        active: true,
        currentWindow: true
    };

    chrome.tabs.query(queryInfo, function(tabs) {
        callback(tabs[0]);
    });                                                                                 
}

function getTabHistory(callback) {
    chrome.storage.local.get("tabhistory", function(items) {
        callback(items.tabhistory);
    });
}

function setTabHistory(tabhistory, callback) {
    chrome.storage.local.set({"tabhistory": tabhistory}, callback);
}
