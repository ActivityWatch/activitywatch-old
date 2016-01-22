# ActivityWatch
*A complete RescueTime replacement, for the open world with [Zenobase](http://zenobase.com).*

[![Build Status](https://travis-ci.org/ErikBjare/activitywatch.svg?branch=master)](https://travis-ci.org/ErikBjare/activitywatch)

**NOTE**
 - This software is under development and is not stable.
 - There is only Linux support at the moment, feel free to contribute support for other platforms! (See [X11Watcher](./activitywatch/watchers/linux.py) for reference)

Logs the time spent by the user in different tasks on the computer.

## Usage
Install the package with `sudo python3 setup.py install`. Once installed you can run the program with the command `activitywatch`. If you wish to run it programatically you may either program your own `start()` function (see `main.py` for reference) or run the default one with the following code:


    import activitywatch
    activitywatch.start()

Alternatively, you can install and run it from a virtualenv. If you wish to run it from a virtualenv then you'll find the executable in `$your_virtualenv/bin/activitywatch` after installation.

#### Configuration

When you run the program the first time, a configuration file will be created at `$HOME/.activitywatch.json`, you must edit this file with correct settings in order to get some modules to load. This system will be improved upon in the future.

#### Early users

Since a stable version of activitywatch has yet to be released there are a few bugs every early user should know about, these are generally tagged with `high_priority` and you can find them all by following [this link](https://github.com/ErikBjare/activitywatch/labels/high%20priority).

#### Future usage
ActivityWatch currently only supports Linux systems using X11 (if you use Linux and don't know what X11 is, you are probably using it). It has not been extensively tested so keep an eye on the logs and report any bugs you find!

A more user friendly approach to installation and usage might become available in the future, depending on interest.
Such a release might have Python bundled for non-python3 systems (with py2app and py2exe, on Linux it will likely still depend on Python 3.3+ being installed since most users probably don't want bundled Python).

## About

#### What it does
Logs every activity on a computer and saves it to a JSON file or uploads it to Zenobase. It is designed to be easily extendable. 

#### Why this is important
We think we need logs on our lives, so that we know what we said, did, how well we did it and how much time we spent doing it. Not just so we know, but so that we can improve upon it.

There are already services doing something similar such as [RescueTime](https://www.rescuetime.com/), [Time Doctor](http://www.timedoctor.com/) and [ManicTime](http://www.manictime.com/). But they are often closed source, costly, lack mobile support, buggy and feature incomplete. For a programmer closed source is very frustrating as it prevents one from solving the imperfections of existing solutions. So this is an attempt to start from scratch with the intention to make what came before obsolete, with the hopes that what might one day make this obsolete has taken advantage of our code and published it under a free license so others may follow.

#### Other software that does similar things
I was aware of the existance of (most) of these when I started, but didn't find them satisfactory. I'm listing them here since I think it's important for me to disclose the alternatives you have if you are looking for something similar to this project. Also, having multiple datasources never hurt.

 - [selfspy](https://github.com/gurgeh/selfspy)
 - [arbtt](http://arbtt.nomeata.de/)
 - [WakaTime](https://wakatime.com/) (specializes in monitoring code editors, partially open source with centralized data storage)
 - [RescueTime](https://www.rescuetime.com/) (closed source, centralized data storage)

## Donations
If you want something, or want to say thanks by giving a monetary incentive, throw money at this Bitcoin address: `1E3nz6eF1474iNRZzJdsZyMT7BXo1y5b3n`
