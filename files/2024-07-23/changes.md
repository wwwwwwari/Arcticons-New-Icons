5 new commits (had to separate them because my elderly eyes are in pain trying to count and make sure nothing is missing 😵‍💫):
* **f23cec1 4 new icons for websites (no appfilter entries):** mangadex.svg, nintendo.svg (+1 alt), tryhackme.svg
* **5ed6100 5 new apps using existing icons:** wetter.com (weather.svg), duet (duet.svg)<sup>[note 1]</sup>, snaptik (downloads.svg), cross dj (cross_dj.svg), dailyal (dailyal.svg)
* **d95737e 2 new generic icons:** android_alt_1.svg, power.svg
* **da20926 2 changed icons for existing apps:** antutu benchmark (from citra.svg)<sup>[note 2]</sup>, hitv (new logo)
* **d375ed1 92 new icons for new apps**

**Notes**
1. Duet already has an existing icon but it's not assigned to anything in the appfilter.xml. 5ed6100 adds the missing line.
2. It seems that Citra for Android uses AnTuTu Benchmark's package name (com.antutu.ABenchMark) as a camouflage to make their apps run faster (see [the release page](https://github.com/weihuoya/citra/releases/tag/20240520)). I downloaded the Citra AnTuTu APKs from that release page and checked their activity names. There doesn't seem to be an acitivity named "com.android.module.app.ui.start.ABenchMarkStart" in the camouflaged Citra, so I think that activity only belongs to the real AnTuTu Benchmark app. 
