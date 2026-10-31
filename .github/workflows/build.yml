
name: Build HSEE Android APK

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            git zip unzip openjdk-17-jdk \
            python3.10 python3.10-dev python3.10-venv \
            autoconf libtool pkg-config \
            zlib1g-dev libncurses5-dev \
            libncursesw5-dev libtinfo5 \
            cmake libffi-dev libssl-dev

      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip
          python -m pip install buildozer==1.5.0 Cython==0.29.36

      - name: Show Python version
        run: python --version

      - name: Build APK
        run: |
          buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: HSEE-Mobile-APK
          path: bin/*.apk
          if-no-files-found: error
