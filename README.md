Brid.gy ![Brid.gy](https://raw.github.com/snarfed/bridgy/master/static/bridgy_logo_128.jpg)
===

Got a web site? Post links to it on social networks? Wish comments showed up on
your site too? Brid.gy copies them back for you.

http://brid.gy/

Brid.gy uses [webmentions](http://www.webmention.org/), which are a part of the
[IndieWeb](http://indiewebcamp.com/) ecosystem, so your site will need to accept
webmentions for Brid.gy to work with it. Check out some of the
[existing implementations](http://indiewebcamp.com/webmention#Implementations)!

License: This project is placed in the public domain.


Development
---
All dependencies are in git submodules. Be sure to run
`git submodule init; git submodule update` after you clone the repo.

The tests require the App Engine SDK and python-mox.


Related work
---
* http://webmention.io/
* https://github.com/vrypan/webmention-tools
* http://indiewebcamp.com/original-post-discovery
* http://indiewebcamp.com/permashortcitation
* http://indiewebcamp.com/Twitter#Why_permashortcitation_instead_of_a_link


TODO
---

* clear source error status on successful poll
* link to targets in recent comments?
* use app engine's app stats tracing to check that comments queries are parallelized
* make front page sort case-independent
* likes/favorites. based on http://indiewebcamp.com/like and
  http://indiewebcamp.com/responses, it looks like it's just u-like and a
  webmention, similar to a reply and may not even need a u-in-reply-to.
  http://indiewebcamp.com/irc/2013-11-11 , http://indiewebcamp.com/repost .
  test against sandeep.io! http://www.sandeep.io/39
* reshares/reposts, e.g. retweets. http://indiewebcamp.com/repost .
  looks like it's just a link with u-repost, e.g.
      <a class="u-repost" href="http://www.sandeep.io/39">
  e.g. http://sandeep.shetty.in/2013/06/indieweb-repost-test.html,
  http://www.sandeep.io/35
  also maybe test against http://barryfrost.com/how-to-comment

lower priority:

* detect updated comments and send new webmentions for them
* only handle public posts? (need to add privacy/audience detection to
  activitystreams-unofficial)
* cache some API calls with a short expiration, e.g. twitter mentions
* cache webmention discovery
* cache served MF2 HTML and JSON with a short expiration. ideally include the
  cache expiration in the content.
* clear toast messages?
