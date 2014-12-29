# Open Computer Time
*A complete RescueTime replacement, for the open world with Zenobase.*

Logs the time spent by the user in different tasks on the computer.

Should log the system and how/when the user uses it.
Then upload to Zenobase or export to JSON (in Zerobase format).


## What it does
Logs every activity on a computer. Page title, name of executable should be included.
Dump all to CSV or upload to Zenobase.

### Why this is important
We think we need logs on our lives, so that we know what we said, did and how much time we spent doing it. Not just so we know, but so that we can improve upon it.


## Output datastructure
Each item has the following data
 - Page title
 - Path of executable (including name of executable) with timestamp as well as label if idle/afk.
 - Optional metadata
    - App Store URL (For Android and iOS)
    - Package identifier (Android)

Should also perhaps also contain the following metadata
 - Date of first and last entry
 - Operating system
 - Device name (especially if mobile)
 - Date of export
 - User

### Filters
 - Filters could be adding labels by some form of clustering
 - It should be possible to filters away all idle/afk entries before export (or not create them to begin with)
 - Zenobase viewer buckets could be used

### Software design
 - Should support different OS's (Linux, Windows, Android), do this by the strategy pattern for (get (page title and name of executable)).
 - Remember to separate the raw exported data from the viewport


## Stories

### Must have
 - Log activity
 - Label AFK/away time

### Nice to have
 - Controller support
 - Log tmux activity (Use `tmux server-info` and others to get data)
 - Log console commands


## Name propositions
 - Activity Watcher (small, it could do more than that)
 - System Logger (lacks the focus on activity monitoring)
 - Computer Time (taken by [these guys](http://www.softwaretime.com/computertime/))
