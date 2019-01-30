plugin.audio.deejayIt.reloaded
==============================

[![Build Status](https://travis-ci.com/karrukola/plugin.audio.deejayIt.reloaded.svg?branch=v2)](https://travis-ci.com/karrukola/plugin.audio.deejayIt.reloaded)

[IT]
I reloaded di Radio DeeJay su Kodi. Da Deejay Chiama Italia a Tropical Pizza, da Asganaway al Deejay Time, i programmi di Radio Deejay da riascoltare quando e dove vuoi.

[EN]
A Kodi plugin that lets you access Radio Deejay's reloaded section.

Radio DeeJay is an Italian radio station. It was founded on 1 February 1982 by the Italian radio and television personality Claudio Cecchetto and was acquired by the Gruppo Editoriale L'Espresso in 1989 (which also owns DeeJay TV, Repubblica Radio TV, m2o and Radio Capital). [source: Wikipedia]

# Technical details

Version 2 of this plugin relies on the API used by the official mobile apps. The JSON output is then parsed and used to present data on screen.

## APIs

### Get list of Reloaded
http://www.deejay.it/api/pub/v1/programs_ondemand?section=radio

### Get latest episode(s)
http://www.deejay.it/api/pub/v1/archive_ondemand?last_day=1&pid=225196&rid=225228


# TODO

- [x] Come cazzo si vedono i podcast di 30 songs?
- [ ] Cordialemente da un errore (reloaded=Null) - usa JSON
- [ ] DeeGiallo da un errore (titolo puntata in unicode) - usa JSON
- [ ] DJs from Mars dopo 15-9-2018  http://www.deejay.it/api/pub/v1/archive_ondemand?date_end=2018-08-31&date_start=2018-08-01&pid=None&rid=527359
- [ ] Vic e Valentina Ricci  http://www.deejay.it/api/pub/v1/archive_ondemand?date_end=2018-08-31&date_start=2018-08-01&pid=None&rid=526841
