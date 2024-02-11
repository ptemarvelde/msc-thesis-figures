#! /bin/bash

find . -type f -name '*.drawio' -exec sh -c '
    drawio_file="$1"
    pdf_file="${drawio_file%.drawio}.pdf"
    echo "if $drawio_file and $pdf_file"
    if [ "$drawio_file" -nt "$pdf_file" ]; then
        echo "test"
    fi
' shell {} \;


# find . -type f -name '*.drawio' -exec sh -c 'file="$1"; echo Converting "$file"; drawio --export -r -f pdf --crop "$file"' shell {} \;
# echo "Converted all to PDF"