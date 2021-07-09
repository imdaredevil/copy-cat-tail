#!/bin/bash

. config.sh
mkdir -p $WORKING_DIR
cd $WORKING_DIR
prevSelection='5'
currentSelection='5'
while :
do
    sleep 0.5
    currentSelection=$(xclip -o -selection clipboard)
    if [ "$currentSelection" != "$prevSelection" ]
    then
        files=$(find $WORKING_DIR -maxdepth 1 -type f)
        if [ "$files" != "" ];
        then
            echo $currentSelection > "$WORKING_DIR/currentCopy.txt"
        fi
        fileFound=$((-1))
        numberOfFiles=0
        for file in $files
        do
            if [ "$file" != "$WORKING_DIR/currentCopy.txt" ] && [ "$file" != "$WORKING_DIR/currentIdx.txt" ];
            then
                difference=$(diff -s currentCopy.txt clip$numberOfFiles.txt | grep "\-\-\-")
                if [ "$difference" != "---" ];
                then
                    fileFound=$(($numberOfFiles))
                fi
                numberOfFiles=$(($numberOfFiles + 1))
            fi
        done
        if [[ $fileFound -eq -1 ]]
        then
            echo $currentSelection > "$WORKING_DIR/clip$numberOfFiles.txt"
            fileFound=$(($numberOfFiles))
        fi
        echo $fileFound > "$WORKING_DIR/currentIdx.txt"
    fi
    prevSelection=$currentSelection    
done