# compare_internet_packages

## General info
> Comparison of internet packages from different internet service provider in Iran

---

## Requirements
- python3
- use virtual environments & install requirements packages ([gist](https://gist.github.com/mheidari98/8ae29b88bd98f8f59828b0ec112811e7)) 
- Chrome web driver : Download it from the address below and Put it next to the main.py in the base folder 
  ```
  Chrome:    https://sites.google.com/a/chromium.org/chromedriver/downloads
  ```

 ---

## Usage
  Get the best package offered with **100000** toman budget from **mci** and **mtn** :
  ```bash
  python main.py -b 100000 -p mci mtn
  ```
  for more options :
  ```bash
  python main.py -h
  ```

---
## Task-Lists
- [x] support Hamrahe Aval (MCI)
- [x] support Irancell (MTN)
- [ ] support RighTel 
