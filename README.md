# Mora Finder

A simple script to recognize different moral verses like hexameters, pentameters and so on.

## Running

It runs under Python 3.7. Start it like this:

```
python morafinder.py "my line to analyze"
```

Or you may start it without argument to get prompted for line after line until you type `exit`.

```
python morafinder.py
>>>
```

## Extending by additional feet

New type of feet could be added easily. `s` stands for short syllabes `l` for long ones. A comment shows where to add it.

```
anapest = "μμ-"
```

Then add a new line type where the comment says to.

```
double_anapest = [[anapest], [anapest]]
```

Multiple feet option could be also set. The following example shows how to mark, if the second anapest my be replaced by a dactyl.

```
double_anapest = [[anapest], [anapest, dactyl]]
```

## Language

Currently the Hungarian alphabet has been set to it, but you could reconfigure it by changing the vowel and consonant lines.


## License

Licensed under MIT license.
