# Wari's Arcticons Checklist and Workflow
This is my general checklist and workflow for Arcticons's icon making process on Debian Linux. The process should be similar on other OSs too, though.
* If you use Windows or Mac, ensure that the linefeed character in all of your files is `LF`, not `CR` or `CRLF`. 
## Required Tools
1. Git - should be pre-installed on Linux
2. InkScape - [Download](https://inkscape.org/release/1.2.2/gnulinux/)
3. Geany - `sudo apt install geany`
4. Diffuse - `sudo apt install diffuse` to compare differences between files (optional)
5. SVGO - `sudo apt install svgo`
6. Compare two lists - [online tool](https://comparetwolists.com/)
## Directory Structure
```
(Your git folder)/
|_ Arcticons/ (Local repository of wwwwwwari/Arcticons)
|_ Arcticons-New-Icons/ (Local repository of wwwwwwari/Arcticons-New-Icons)
   |_ files/ (main workspace folder; also contains the randomizer script)
      |_ YYYY-MM-DD/ (workspace of each pull request)
      |  |_ svg/ (all SVG files are saved within here)
      |     |_ bkup/ (backups of /work/ SVG files I've made before applying the regex)
      |     |_ opti/ (final files to be copied to the main repository. shouldn't be edited directly)
      |     |_ work/ (main workspace for SVGs)
      |_ plans/ (icons I'm interested in doing in the future)
```
## Checklist
### While Making Icons
#### General Checks
1. Save the `<item component>` entries of the new icons in a new text file called `new_appfilter.txt`, this will be used to update `appfilter` after all icons are done.
2. No +-.,! in icon file names
3. If the name begins with a number, prefix it with an underscore, e.g. 1track.svg becomes \_1track.svg
4. Never use dots. They slow down the validation because of their differences from lines (i.e. fills instead of no fill; no stroke instead of strokes).  Use very small lines instead.
5. For Calendar apps, there are **TWO** appfilter entries to make per app: one with `drawable=calendar_31` (static icon) and the other with `drawable=calendar_` (dynamic icon).
### After Making Icons 
#### InkScape Checks
1. There are no hidden layers left.
2. Everything is ungrouped, including the layer. 
3. Combine everything.
4. All lines are 1px wide
5. All lines are ffffffff white
    1. Check the actual color code under the color slides, not the color slides themselves. InkScape loves to tell you that everything is pure white when the color code is like fffffffb).
7. All lines have round caps and round joins.
#### Geany Checks
1. Check that there is no `transform`, `evenodd` and `e-notation` mentioned in any svg files. If there is any, follow Arcticons' [guideline](https://ithub.com/Donnnno/Arcticons/blob/main/CONTRIBUTING.md#how-to-replace) on how to remove them.
    1. You can also remove `tranform` easily by making a dummy stroke nearby, combine it with the icon, save, then uncombine, remove the dummy stroke, and save again.
2. Back up the svg files above into a backup folder
3. Open the svg files in `geany` and CTRL+H the following using Regular Expressions and save all files:
    1. `stroke-width:\d*.?\d*;` -> `stroke-width:1;`
    2. `stroke:#[abcdef0-9]{3,6};` -> `stroke:#fff;`
    3. `stroke-linecap:[a-z]*;` -> `stroke-linecap:round;`
    4. `stroke-linejoin:[a-z]*;` -> `stroke-linejoin:round;`
    5. `stroke:rgba?.*?(?=[\"; ])` -> `stroke:#fff`
4. Re-check that everything still looks correct.
5. Using SVGO, re-save all the files as Optimized SVGs in a separate folder:
    1. `svgo -f ./work -i ./opti`
#### Final Checks & Making a Pull Request
1. Ensure that your GitHub repo is in sync with Donnnno's using the [web interface](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork) before proceeding.
2. Refresh the local PC's Arcticons repository folder with `git pull origin main`
3. Make sure icon file names aren't duplicate with any existing and newly added icons - check `Arcticons/icons/` and `Arcticons/other/`
4. Make sure no one has already submitted pull requests for any of the new icons yet (check new and recently merged PRs)
5. Update `Arcticons/other/appfilter.xml` following `new_appfilter.txt` and ensure the entries match the new icons, especially the value after `drawable=` (must match .svg file names).
    1. You don't need to insert each of the new entries to maintain the files' alphabetical sort order. Just insert all of your new entries somewhere - Arcticons' build process will automatically sort the lines afterwards.
    2. Also ensure your icon names don't already exist for other apps - use the **Compare two lists** tool to compare the list of your new icon names to the list of files in `icons/white` and `other/`
7. Update `Arcticons/other/requests.txt`. 
8. Copy icons from the `Arcticons-New-Icons/files/YYYY-MM-DD/opti/` to `Arcticons/other/`
9. Upload the changes with `git status` `git commit -m <comment>` and `git push origin main` to `wwwwwwari/Arcticons`
10. Make a pull request
## Other Notes
### Renaming Icon Files
If you want to change the icon file names, you need to rename the following files in addition to updating `appfilter.xml`:
1. `/app/src/light/res/drawable-nodpi/your-icon.png`
2. `/app/src/dark/res/drawable-nodpi/your-icon.png`
3. `/app/src/you/res/drawable-anydpi-v26/your-icon.xml`
4. `/icons/white/your-icon.svg`
5. `/icons/black/your-icon.svg`
