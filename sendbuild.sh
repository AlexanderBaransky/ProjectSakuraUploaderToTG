#!/bin/bash

FILEPATH=$(ls $OUT/ProjectSakura*.zip)
FILENAME=$(basename $(ls $OUT/ProjectSakura*.zip))
MD5_CHKSUM=$(ls $OUT/ProjectSakura*.zip.md5sum)

python3 vendor/lineage/build/tools/uploader/send.py $FILEPATH $FILENAME $MD5_CHKSUM