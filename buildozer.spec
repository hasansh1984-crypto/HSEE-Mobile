[app]

title = HSEE Mobile
package.name = hseemobile
package.domain = org.lorestan
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1

[app:android]

android.permissions = INTERNET
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True
p4a.branch = develop
