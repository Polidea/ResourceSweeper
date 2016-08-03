---

__This repository is no longer maintained. Issue reports and pull requests will not be attended.__

---

ResourceSweeper
===============

Python tool that helps you to get rid off unused resources (images) in your Xcode project. It also can convert pngs that do not use alpha channel to jpgs (they are faster!).

Quick usage
----
1. Clone project.
2. Run script: `python sweep-resources.py /path/to/your/awesome/xcode/project/`.
3. If you want to convert pngs to images run also: `python optimize_pngs.py /path/to/your/awesome/xcode/project/` ( **WARNING** this part requires PIL, instructions will be added soon).
4. You can also check for unused class files which are still in the project, run: `python sweep-classes.py /path/to/your/awesome/xcode/project/ /path/to/your/awesome/xcode/project/main.m/file/directory/`
