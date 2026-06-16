[app]
title = Volleyball Scoreboard
package.name = volleyballboard
package.domain = org.playxadomoy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Вказуємо Buildozer, що головний файл називається саме так:
source.main_py_name = volleybolll.py

version = 1.0
requirements = python3,kivy

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

