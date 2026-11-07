# Unpack-Channels

Раскладывает запакованную по каналам текстуру (ORM, `MT_R_AO` и т. п.) на отдельные чёрно-белые PNG — одной кнопкой из Проводника, без Photoshop.

```
T_big_rock_01_MT_R_AO.png   →   T_big_rock_01_MT.png   (R)
                                T_big_rock_01_R.png    (G)
                                T_big_rock_01_AO.png   (B)
```

## Установка (Windows)

1. Установите [Python 3.9+](https://www.python.org/downloads/). В установщике отметьте **Add python.exe to PATH**.
2. Скачайте репозиторий (**Code → Download ZIP** или `git clone`) и положите папку туда, где она будет жить постоянно — ярлык ссылается на неё.
3. Запустите **`install.bat`**. Он:
   - ставит зависимости (`numpy`, `opencv-python-headless`);
   - добавляет пункт **Unpack channels** в меню ПКМ → **Отправить**;
   - прогоняет самопроверку — в конце должно быть `selftest ok`.

Перенесли папку — запустите `install.bat` ещё раз.

## Использование

Выделите одну или несколько текстур → ПКМ → **Отправить → Unpack channels**. Файлы появятся рядом с исходником. Окно консоли остаётся открытым только при ошибке.

Из командной строки:

```
python unpack_channels.py T_rock_MT_R_AO.png T_wood_ORM.tga
```

## Как выбираются имена

- Последние части имени через `_` — это каналы по порядку **R, G, B, A**.
- Канал, залитый одним значением (например, пустая альфа), пропускается и имени не занимает.
- Частей в имени должно быть хотя бы на одну больше, чем каналов: что-то должно остаться базовым именем. Иначе (`T_rock_ORM.png` — три части на три канала) файлы получат суффиксы `_R`, `_G`, `_B`, `_A`.
- Одноимённые файлы рядом перезаписываются.

## Форматы

PNG, TGA, TIFF, JPG, BMP — всё, что читает OpenCV. Битность сохраняется: 8-битный исходник даёт 8-битные PNG, 16-битный — 16-битные.

## Удаление

Удалите ярлык `Unpack channels` из папки «Отправить» (Win+R → `shell:sendto`) и саму папку.

---

# English

Splits a channel-packed texture (ORM, `MT_R_AO` and so on) into separate greyscale PNGs, with one click from Explorer and no Photoshop.

```
T_big_rock_01_MT_R_AO.png   →   T_big_rock_01_MT.png   (R)
                                T_big_rock_01_R.png    (G)
                                T_big_rock_01_AO.png   (B)
```

## Installation (Windows)

1. Install [Python 3.9+](https://www.python.org/downloads/). In the installer, tick **Add python.exe to PATH**.
2. Download the repository (**Code → Download ZIP** or `git clone`) and put the folder where it will stay. The shortcut points to it.
3. Run **`install.bat`**. It:
   - installs the dependencies (`numpy`, `opencv-python-headless`);
   - adds **Unpack channels** to the right-click → **Send to** menu;
   - runs the self-test, which should end with `selftest ok`.

If you move the folder, run `install.bat` again.

## Usage

Select one or more textures, then right-click → **Send to → Unpack channels**. The files appear next to the source. The console window stays open only if something went wrong.

From the command line:

```
python unpack_channels.py T_rock_MT_R_AO.png T_wood_ORM.tga
```

## How the names are chosen

- The last `_`-separated parts of the file name are the channels, in **R, G, B, A** order.
- A channel filled with a single value (an unused alpha, for example) is skipped and takes no name.
- The name needs at least one more part than there are channels, so that something is left as the base name. Otherwise the files get `_R`, `_G`, `_B` and `_A` suffixes. `T_rock_ORM.png` is an example: three parts for three channels.
- Files with the same name next to the source are overwritten.

## Formats

PNG, TGA, TIFF, JPG and BMP, or anything else OpenCV reads. The bit depth is preserved: an 8-bit source gives 8-bit PNGs, a 16-bit source gives 16-bit ones.

## Uninstall

Delete the `Unpack channels` shortcut from the Send To folder (Win+R → `shell:sendto`), then delete the folder itself.
