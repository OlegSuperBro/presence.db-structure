# About this file

Presence.db is file used by game called osu!.

osu! also contain [other .db files](https://github.com/ppy/osu/wiki/Legacy-database-file-structure), but there is no documentation for presence.db

Presence.db contains user info displayed in F9 menu

## Known information

First of all, you should check [data types](https://github.com/ppy/osu/wiki/Legacy-database-file-structure#data-types) osu! uses.

### Structure of Presence.db

|Data type|Description|
|-|-|
|Int|Game version when this file created (e.g. 20230319)|
|Int|Users count|
|Users*|Aforementioned Users|

### Users information

|Data type|Description|
|-|-|
|Int|Online user id|
|String|Player name|
|???|???|
|???|???|
|Byte|Player status. It is split into 4 bits. First 4 bits is booleans for "is player", "is global moderator", "is supporter". One bit not used. Second 4 bits used for displaying gamemode player curently playing (not main gamemode) "0000" - std, "0010" - taiko, "0100" - ctb, "0110" - mania|
|Float|Longitude of player|
|Float|Latitude of player|
|Int|Player rank in current gamemode|
|Long|Timestamp (when last time player was checked?)|

## If you want help

I already put here my **presence.db** file and it sql version (**data.db**). You can view it in an sqllite viewer (i use [this](https://inloop.github.io/sqlite-viewer/) one).
If you find out about some data, you can create [issue](https://github.com/OlegSuperBro/presence.db-structure/issues) or create [pull request](https://github.com/OlegSuperBro/presence.db-structure/pulls)

You can use your own **presence.db** file. Just copy it in this directory and run **export_presence_to_sql.py**.
**data.db** file should appear (or changed if it already exist) in this directory
