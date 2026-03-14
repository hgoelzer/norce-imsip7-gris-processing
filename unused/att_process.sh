# some processing on files

find Models/NORCE/CISM5-MAR364-ERA-t1/ -name *.nc | xargs -I xxx ./ncatt.sh xxx
