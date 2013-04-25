Khan Video Search
-----------------
  
  A webapp based on gae-init (see below for links) that allows users to search for 
  Dutch educational youtube videos...  

TODO:

  - Bring design in line with KhanAcademie
  - Allow for data to be collected and stored
  - Implement a voting system for videos returned by search
  - Implement a system that allows users to tag videos
  
Running the build.py script (first time)
----------------------------------------

    $ cd /path/to/project-name/main
    $ ./build.py -c
    $ dev_appserver.py .

To test it visit `http://localhost:8080/` in your browser.

Running the Development Environment
-----------------------------------

To watch for changes of your `*.less` and `*.coffee` files and compile them
automatically to `*.css` and `*.js` respectively:

    $ cd /path/to/project-name/main
    $ ./build.py -w

To run the actual server (in another bash):

    $ dev_appserver.py /path/to/project-name/main

To test it visit `http://localhost:8080/` in your browser.

Deploying on Google App Engine
------------------------------

Before deploying make sure that the `app.yaml` and `config.py` are up to date.

    $ cd /path/to/project/main
    $ ./build.py -m
    $ appcfg.py update .

Tech Stack
----------

  - [Google App Engine][gae]
  - [Python 2.7][gaepython]
  - [NDB][]
  - [Jinja2][]
  - [Flask][]
  - [jQuery][]
  - [CoffeeScript][]
  - [LessCSS][]
  - [Bootstrap][]
  - [Font Awesome][fontawesome]

Requirements
------------

  - [Google App Engine SDK for Python][gaesdk]
  - [node.js][nodejs]
  - [OSX][] or [Linux][] or [Windows][]
  - [Mercurial][]
  - [Sublime][] (If you are a developer, you need that)

Contributions and Ideas
-----------------------

  - [tzador][]
  - [chris][]
  - [ksymeon][]
  - [gmist][]
  - [stefanlindmark][]

Author
------

[![Lipis flair on stackoverflow.com][lipisflair]][lipis]

[gaeinit]: http://gae-init.appspot.com
[docs]: http://docs.gae-init.appspot.com
[tutorial]: http://docs.gae-init.appspot.com/tutorial/
[gae]: https://developers.google.com/appengine/
[gaepython]: https://developers.google.com/appengine/docs/python/python27/using27
[ndb]: https://developers.google.com/appengine/docs/python/ndb/
[jinja2]: http://jinja.pocoo.org/docs/
[flask]: http://flask.pocoo.org/
[jquery]: http://jquery.com/
[coffeescript]: http://coffeescript.org/
[lesscss]: http://lesscss.org/
[bootstrap]: http://twitter.github.com/bootstrap/
[fontawesome]: http://fortawesome.github.com/Font-Awesome/

[gaesdk]: https://developers.google.com/appengine/downloads
[nodejs]: http://nodejs.org/
[osx]: http://www.apple.com/osx/
[linux]: http://www.ubuntu.com
[windows]: http://windows.microsoft.com/
[mercurial]: http://mercurial.selenic.com/
[sublime]: http://www.sublimetext.com/

[tzador]: http://stackoverflow.com/users/165697/tzador
[chris]: http://stackoverflow.com/users/226394/chris-top
[ksymeon]: https://plus.google.com/102598378133436784997
[gmist]: https://github.com/gmist
[stefanlindmark]: http://www.linkedin.com/in/stefanlindmark

[lipisflair]: http://stackexchange.com/users/flair/5282.png
[lipis]: http://stackoverflow.com/users/8418/lipis
