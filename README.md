ResourceSweeper
===============

Python tool that helps you to get rid off unused resources (images) in your Xcode project. It also can convert pngs that do not use alpha channel to jpgs (they are faster!).

Quick usage
----
1. Clone project.
2. Run script: `python sweep-resources.py /path/to/your/awesome/xcode/project/`.
3. If you want to convert pngs to images run also: `python optimize_pngs.py /path/to/your/awesome/xcode/project/` ( **WARNING** this part requires PIL, instructions will be added soon).
