# ActivityWatch
*A complete RescueTime replacement, for the open world with [Zenobase](http://zenobase.com).*

[![Build Status](https://travis-ci.org/ErikBjare/activitywatch.svg?branch=master)](https://travis-ci.org/ErikBjare/activitywatch)

**NOTE: UNDER DEVELOPMENT**

Logs the time spent by the user in different tasks on the computer.

## Usage
Install the package with `sudo pip3 setup.py install` and then run `python3 start-activitywatch.py`.

Alternatively, you can install and run it from a virtualenv.

#### Configuration
The first time you run the program, a configuration file will be created as `$HOME/.activitywatch.json`.

#### Future usage
A more user friendly approach to installation and usage might become available in the future.
Such a release would have Python bundled for non-Linux systems.

## About

#### What it does
Logs every activity on a computer and saves it to a JSON file or uploads it to Zenobase. It is designed to be easily extendable. 

#### Why this is important
We think we need logs on our lives, so that we know what we said, did, how well we did it and how much time we spent doing it. Not just so we know, but so that we can improve upon it.

There are already services doing something similar such as [RescueTime](https://www.rescuetime.com/), [Time Doctor](http://www.timedoctor.com/) and [ManicTime](http://www.manictime.com/). But they are often closed source, costly, lack mobile support, buggy and feature incomplete. For a programmer closed source is very frustrating as it prevents one from solving the imperfections of existing solutions. So this is an attempt to start from scratch with the intention to make what came before obsolete, with the hopes that what might one day make this obsolete has taken advantage of our code and published it under a free license so others may follow.


## Architecture
**Watchers** deliver raw data, **filters** transform the data (with the [chain of responsibility pattern](https://en.wikipedia.org/wiki/Chain-of-responsibility_pattern)) and **loggers** save the data locally or to an external source (such as Zenobase).

 - Support for different OS's (Linux, Windows, OS X, Android, iOS)
 - Some platforms might need a custom implementation of a watcher which can report to a server with a RESTWatcher, this solution is easier but not very user friendly.

#### Watchers
These are the (planned) official watchers.

 - **AFKWatcher** Checks if user if AFK by monitoring keyboard and mouse
 - **X11Watcher** - Watches current window (Linux/X11)
 - **WindowsWatcher** - Watches current window (Windows)
 - **OSXWatcher** - Watches current window (OS X)
 - **RESTWatcher** - Can be used to log activities from outside the application process (Watcher with REST-API interface)
 - **ChromeWatcher** - Watches the current tab (Uses the RESTWatcher)
 - **FirefoxWatcher** - Watches the current tab (Uses the RESTWatcher, *Will only be done if there is enough interest*)

#### Loggers
These are the official loggers.

 - **StdOutLogger** - Logs to stdout
 - **JSONLogger** - Logs to JSON file
 - **ZenobaseLogger** - Logs to Zenobase

#### Filters
 - Filters act as loggers/listeners and watchers/reporters, taking input from watchers and/or filters and sending their output to loggers and/or filters.
 - Filters could be adding labels by some form of clustering
 - It should be possible to filters away all idle/afk entries before export (or not create them to begin with)
 - Zenobase viewer buckets could be used as external filters

Official filters:
 - **AFKFilter** filters away all events which occurred when the user was AFK. Events which the user was partially AFK from has only their AFK time cut away.
 - **IntervalFilter** clusters activities into intervals (several activities during the same interval get merged).
 - **DurationFilter** filters away activities with short duration.

#### Extensions
Core **EventWatch** package should only include basic loggers (which?), no event handlers.

Standard **ActivityWatch** package should include core and X11Watcher/WindowsWatcher/OSXWatcher.

Extensions may include extra watchers and loggers. Such as ChromeWatcher or FTPLogger.


## Stories

#### Must have
 - Log activity
 - Label AFK/away time
    - No activity for 15 min -> T-00:15 and beyond is AFK until activity resumes
 - Activity detector needs to be extendable with details (for browser activity, terminal multiplexers, bash/zsh, etc.)

#### Nice to have
 - Aggregate activity clientside (by hour/minute) to reduce upload size to Zenobase for people who aren't subscribers
   - Acts as an incentive for people to subscribe by allowing for easily upgrading by reuploading at a higher resolution.
 - Controller support (so controller usage is detected as activity)
 - Detect if media is playing (VLC, YouTube, Netflix, Plex, etc.)
    - Could this be done by checking for audio + if window title indicated media?
 - Log tmux activity (Use `tmux server-info` and others to get data)
 - Log console commands
 - Android & iOS support
    - asd
 - Application identification
    - Using Wikidata/Wikipedia?
    - Using crowdsourced reporting?
    - Detect category. 
    - Website etc. (using Wikidata/Freebase?)
    - *Wikimedia Commons* has a great set of categories. Google Chrome for example has the category [Google Chrome](https://commons.wikimedia.org/wiki/Category:Google_Chrome), with parent category [Web Browsers](https://commons.wikimedia.org/wiki/Category:Web_browsers) with parent category [Application software by type](https://commons.wikimedia.org/wiki/Category:Google_Chrome) which should be considered the root directory of all categories.
    - Not all applications have easily identifiable categories via Wikidata, for those it might be easiest to parse the first sentence(s) of the Wikipedia article and check for clues.
 - Productivity score
    - Assign discrete or continuous productivity scores to categories, then rate activities according to their category.
    - The ability to manually add productivity 
