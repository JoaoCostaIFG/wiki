# Stopping Wine from creating filetype associations

By default, Wine creates associations to open some filetypes. I don't like this.

## Disabling it

Add `HKCU,"Software\Wine\FileOpenAssociations","Enable",2,"N"` to the `[Services]` section of `/usr/share/wine/wine.inf`

### Notes related to Arch

Install/upgrades to the Wine package will override this file. We can create a pacman hook to reapply this change for us:

```
[Trigger]
Operation = Install
Operation = Upgrade
Type = Path
Target = usr/share/wine/wine.inf

[Action]
Description = Stopping Wine from hijacking file associations...
When = PostTransaction
Exec = /bin/sh -c '/usr/bin/grep -q "HKCU,\"Software\\\Wine\\\FileOpenAssociations\",\"Enable\",2,\"N\"" /usr/share/wine/wine.inf || /usr/bin/sed -i "s/\[Services\]/\[Services\]\nHKCU,\"Software\\\Wine\\\FileOpenAssociations\",\"Enable\",2,\"N\"/g" /usr/share/wine/wine.inf'
```

## Source

[Arch wiki Wine page](https://wiki.archlinux.org/title/Wine#Prevent_Wine_from_creating_filetype_associations)