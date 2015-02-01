/**
 * Runs whenever active tab was changed
 */
chrome.tabs.onActivated.addListener(function(activeInfo) {
    getTab(function(tab) {
        console.log("Active tab changed");
        console.log(tab);

        getTabHistory(function(tabs) {
            tabs = [tab].concat(tabs);
            console.log(tabs);

            setTabHistory(tabs, function() {
                console.log("tabhistory saved, length: " + tabs.length);
            });
        });
    });
});
