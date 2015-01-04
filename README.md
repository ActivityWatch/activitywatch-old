# ActivityWatch
*A complete RescueTime replacement, for the open world with [Zenobase](http://zenobase.com).*

**NOTE: UNDER DEVELOPMENT**

Logs the time spent by the user in different tasks on the computer.

Should log the system and how/when the user uses it.
Then upload to [Zenobase](http://zenobase.com/) or export to JSON (in Zerobase format).


## What it does
Logs every activity on a computer. Page title, name of executable should be included.
Dump all to CSV or upload to Zenobase.

### Why this is important
We think we need logs on our lives, so that we know what we said, did and how much time we spent doing it. Not just so we know, but so that we can improve upon it.


## Output datastructure
Each item has the following data:
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

### Watchers
These are the (planned) official watchers.

 - **AFKWatcher** Checks if user if AFK by monitoring keyboard and mouse)
 - **X11Watcher** - Watches current window (Linux/X11)
 - **WindowsWatcher** - Watches current window (Windows)
 - **OSXWatcher** - Watches current window (OS X)
 - **RESTWatcher** - Can be used to log activities from outside the application process (Watcher with REST-API interface)
 - **ChromeWatcher** - Watches the current tab (Uses the RESTWatcher)
 - **FirefoxWatcher** - Watches the current tab (Uses the RESTWatcher, *Will only be done if there is enough interest*)

### Loggers
These are the official loggers.

 - **StdOutLogger** - Logs to stdout
 - **JSONLogger** - Logs to JSON file
 - **ZenobaseLogger** - Logs to Zenobase

### Filters
 - Filters act as loggers/listeners and watchers/reporters.
 - Filters could be adding labels by some form of clustering
 - It should be possible to filters away all idle/afk entries before export (or not create them to begin with)
 - Zenobase viewer buckets could be used as external filters

Official filters:
 - **AFKFilter** filters away all events which occurred when the user was AFK. Events which the user was partially AFK from has only their AFK time cut away.

#### Extensions
Core **EventWatch** package should only include basic loggers (which?), no event handlers.

Standard **ActivityWatch** package should include core and X11Watcher/WindowsWatcher/OSXWatcher.

Extensions may include extra watchers and loggers. Such as ChromeWatcher


### Software design
 - Should support different OS's (Linux, Windows, Android), use the strategy pattern for (get (page title and name of executable)).
   - Some platforms might need a rewrite in their respective language
 - Remember to separate the raw exported data from the viewport

### Restrictions
 - Only checks current activity once a second, this is to reduce database size and since resolution below this rarely matters.


## Stories

### Must have
 - Log activity
 - Label AFK/away time
    - No activity for 15 min -> T-00:15 and beyond is AFK until activity resumes
 - Activity detector needs to be extendable with details (for browser activity, terminal multiplexers, bash/zsh, etc.)

### Nice to have
 - Aggregate activity clientside (by hour/minute) to reduce upload size to Zenobase for people who aren't subscribers
   - Acts as an incentive for people to subscribe by allowing for easily upgrading by reuploading at a higher resolution.
 - Controller support (so controller usage is detected as activity)
 - Detect if media is playing (VLC, YouTube, Netflix, Plex, etc.)
    - Could this be done by checking for audio + if window title indicated media?
 - Log tmux activity (Use `tmux server-info` and others to get data)
 - Log console commands
 - Android & iOS support

-----------------

**DISCLAIMER**  
Not affiliated with Zenobase, just a fan.
