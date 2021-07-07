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
        fileFound=0
        numberOfFiles=1
        for file in $files
        do
            if [ "$file" != "$WORKING_DIR/currentCopy.txt" ];
            then
                numberOfFiles=$(($numberOfFiles + 1))
                echo $file
                echo $numberOfFiles
                difference=$(diff -s currentCopy.txt $file | grep "\-\-\-")
                if [ "$difference" != "---" ];
                then
                    fileFound=1
                fi
            fi
        done
        echo $numberOfFiles
        if [[ $fileFound -eq 0 ]]
        then
            echo "new copy"
            echo $currentSelection > "$WORKING_DIR/clip$numberOfFiles.txt"
        fi
        # if [ "$existingFile" == "" ];
        # then
        #     numClips=$(ls | grep -ce "clip[0-9]*.txt")
        #     echo $numClips
        #     echo $currentSelection >> "clip$numClips.txt"
        # fi
    fi
    prevSelection=$currentSelection    
done