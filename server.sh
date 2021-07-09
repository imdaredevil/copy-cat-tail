#!/bin/bash

CONFIG_DIR="/home/imdaredevil/.copy-cat-tail/config"
. "$CONFIG_DIR/config"
cd $WORKING_DIR
prevSelection='5'
currentSelection='5'
while :
do
    sleep 0.5
    currentSelection=$(xclip -o -selection clipboard)
    if [ "$currentSelection" != "$prevSelection" ]
    then
        files=$(find $WORKING_DIR/copies -maxdepth 1 -type f)
        if [ "$files" != "" ];
        then
            echo -n $currentSelection > "$WORKING_DIR/currentCopy.txt"
        fi
        fileFound=$((-1))
        numberOfFiles=0
        for file in $files
        do
                difference=$(diff -s currentCopy.txt copies/clip$numberOfFiles.txt | grep "\-\-\-")
                if [ "$difference" != "---" ];
                then
                    fileFound=$(($numberOfFiles))
                fi
                numberOfFiles=$(($numberOfFiles + 1))
        done
        if [[ $fileFound -eq -1 ]]
        then
            currentWriteIdxFile=$(ls | grep "currentWriteIdx.txt")
            currentWriteIdx=$(($numberOfFiles))
            if [ "$currentWriteIdxFile" != "" ];
            then
                currentWriteIdx=$(cat currentWriteIdx.txt)
            fi
            echo -n $currentSelection > "$WORKING_DIR/copies/clip$currentWriteIdx.txt"
            fileFound=$(($numberOfFiles))
            currentWriteIdx=$((($currentWriteIdx + 1) % $MAX_COPY_LIMIT))
            echo -n $currentWriteIdx > "currentWriteIdx.txt"
        fi
        echo -n $fileFound > "$WORKING_DIR/currentIdx.txt"
    fi
    prevSelection=$currentSelection    
done