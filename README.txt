Touch-Sequencer A Midi sequencer for use with touch tablets
-----------------------------------------------------------

Website: http://www.notesandvolts.com/


About
-----

A Python and Pure Data Midi Sequencer for touch screens

For questions you can check out the blog or email me at guy@notesandvolts.com

I also hang around in IRC, #doomcentral on irc.freenode.net

I'm now feeling that this is ready enough to start mentioning it to people so this is Version 1.0 Beta



Intro
-----

This is essentially a rewrite of a Midi sequencer I wrote for
the Nintendo DS. I wanted more screen space and something a litle
more developer friendly so this is currently being aimed at the
Always Innovating Touchbook I use.

The idea is to have a Python/pyGame client that runs on the Touchbook
and communicates via OSC with a Pure Data patch that does the grunt work.


Setup
-----

There are two parts to the sequencer, the Python GUI client and the Pure Data
patch. Run both, make sure they,re communicating over OSC, send the Midi
output to all the gear you want, then rock out.


Dependencies
------------

This was written for python 2.6
The python UI is written using pyGame for all the graphics/interface so
pyGame needs to be installed and working
The Pure Data patch uses some OSC externals from mrPeach. Will run fine
with PDExtended, otherwise make sure that the correct externals are available.


Still to do
-----------
There are plans to add in a swing setting for the grids to allow swing to
be added to 8th or 16th notes
The UI is pretty poor and could do with some improvements
Follow mode needs to be added so grids can be edited and seen changing in real time
A step number indicator is needed as well
Track info on the main screen would be good
A 16 * 32 grid would be useful to add
Eventually a more freeform grid more like a midi matrix would be nice to have



Useful things
-------------

http://puredata.hurleur.com/

The Pure Data forum (currently seems to be down)
Full of people who know what they're talking about and are very willing to help.




