#!/bin/bash
while read -d $'\0' file; do
    echo "Creating image file... :${file}"
    IMAGE_TITLE=`basename "${file}" | sed 's/\.[^\.]*$//'`
    OUTPUT_IMAGE_DIR="`dirname "${file}"`/../"
    ./node_modules/.bin/mmdc -i ${file} -o ${OUTPUT_IMAGE_DIR}${IMAGE_TITLE}.png
done < <(find ./images -name '*.mmd' -print0)
