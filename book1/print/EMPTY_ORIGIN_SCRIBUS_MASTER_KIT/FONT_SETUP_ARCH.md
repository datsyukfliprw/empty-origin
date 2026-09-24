# Arch Linux setup

```bash
sudo pacman -S scribus noto-fonts hyphen-en ghostscript
yay -S ebgaramond-otf
```

Verify:
```bash
fc-match "EB Garamond"
fc-match "Noto Sans Condensed"
fc-match "Noto Serif"
```

Restart Scribus after installing fonts.
