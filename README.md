This script will extract the coordinates of mapped reads from the SAM file. It will produce two files, one file for the coordinates of the reference tab-limited three-column file, chromosome, start, and end, and the other file will have more information about both the reads and the reference, it is a tab-limited eight-column file with a header. 
python get_coordinates.py SAM_file
