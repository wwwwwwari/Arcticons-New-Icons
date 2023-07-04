# My Arcticons Checklist and Workflow
This is my general checklist and workflow for Arcticons development on Debian Linux.
## Required Tools
1. Git - should be pre-installed on Linux
2. InkScape - [Download](https://inkscape.org/release/1.2.2/gnulinux/)
3. Geany - `sudo apt install geany`
4. Diffuse - `sudo apt install diffuse`
## My Directory Structure
```
(My git folder)/
|_ Arcticons/ (Local repository of wwwwwwari/Arcticons)
|_ Arcticons-New-Icons/ (Local repository of wwwwwwari/Arcticons-New-Icons)
   |_ files/ (main workspace folder; also contains the randomizer script)
      |_ YYYY-MM-DD/ (workspace of each pull request)
      |  |_ svg/ (all SVG files are saved within here)
      |     |_ bkup/ (backups of /work/ SVG files I've made before applying the regex)
      |     |_ opti/ (final files to be copied to the main repository. you shouldn't edit these directly)
      |     |_ work/ (main workspace for SVGs)
      |_ plans/ (icons I'm interested in doing in the future)
```
## Checklist
### While Making Icons
#### General Checks
1. Save the `<item component>` entries of the new icons in a new text file called `new_appfilter.txt`, this will be used to update `appfilter` after all icons are done.
2. No +1-.,! in icon file names
3. If the name begins with a number, prefix it with an underscore, e.g. 1track.svg becomes \_1track.svg
4. Never use dots. Dots slow down the validation because of their differences from lines (i.e. fills instead of no fill; no stroke instead of strokes).  Use very small lines instead.
### After Making Icons 
#### InkScape Checks
1. There are no hidden layers left.
2. Everything is ungrouped, including the layer. 
3. Combine everything.
4. All lines are 1px wide
5. All lines are ffffffff white (check the actual color code, not the color slide).
6. All lines have round caps and round joins.
#### Geany Checks
##### SVG Validation
1. Check that there is no `transform`, `evenodd` and `e-notation` mentioned in any svg files. If there is any, follow Arcticons' [guideline](https://ithub.com/Donnnno/Arcticons/blob/main/CONTRIBUTING.md#how-to-replace) on how to remove them.
    1. You can also remove `tranform` easily by making a dummy stroke nearby, combine it with the icon, save, then uncombine, remove the dummy stroke, and save again.
2. Back up the svg files above into a backup folder
3. Open the svg files in `geany` and CTRL+H the following using Regular Expressions and save all files:
    1. `stroke-width:\d*.?\d*;` -> `stroke-width:1;`
    2. `stroke:#[abcdef0-9]{3,6};` -> `stroke:#fff;`
    3. `stroke-linecap:[a-z]*;` -> `stroke-linecap:round;`
    4. `stroke-linejoin:[a-z]*;` -> `stroke-linejoin:round;`
4. Re-check that everything still looks correct.
5. Using SVGO, re-save all the files as Optimized SVGs in a separate folder:
    1. `svgo -f ./work -i ./opti`
##### File Updates and Pull Request
1. Ensure wwwwwwari's GitHub repo is in sync with Donnnno's using the web interface.
2. Refresh the local PC's Arcticons repository folder with `git pull origin main`
3. Make sure icon file names aren't duplicate with any newly added icons - check `Arcticons/other/`
4. Make sure no one has already submitted pull requests for any of the new icons yet - check open pull requests
5. Update `Arcticons/other/appfilter.xml` following `new_appfilter.txt` and ensure the entries match the new icons
6. Update `Arcticons/other/requests.xml`. 
7. Copy icons from the `Arcticons-New-Icons/files/YYYY-MM-DD/opti/` to `Arcticons/other/`
8. Upload the changes with `git push origin main` to wwwwwwari/Arcticons
9. Make a pull request
