#!/bin/bash

CONFIG_DIR="$HOME/.copy-cat-tail/config"
. "$CONFIG_DIR/config"
cd $WORKING_DIR
prevSelection=""
currentSelection=''
echo "server listening to copies texts"
while :
do
    sleep 0.5
    currentSelection=$(xclip -o -selection clipboard)
    if [ "$currentSelection" != "$prevSelection" ];
    then
        files=$(find $WORKING_DIR/copies -maxdepth 1 -type f)
        echo -n "$currentSelection" > "$WORKING_DIR/currentCopy.txt"
        fileFound=$((-1))
        numberOfFiles=0
        for file in $files
        do
                difference=$(diff -s currentCopy.txt copies/clip$numberOfFiles.txt | grep "identical")
                if [ "$difference" == "Files currentCopy.txt and copies/clip$numberOfFiles.txt are identical" ];
                then
                    fileFound=$(($numberOfFiles % $MAX_COPY_LIMIT))
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
            echo -n "$currentSelection" > "$WORKING_DIR/copies/clip$currentWriteIdx.txt"
            fileFound=$(($currentWriteIdx))
            currentWriteIdx=$((($currentWriteIdx + 1) % $MAX_COPY_LIMIT))
            echo -n $currentWriteIdx > "currentWriteIdx.txt"
        fi
        echo -n $fileFound > "$WORKING_DIR/currentIdx.txt"
    fi
    prevSelection=$currentSelection    
done