# modify calendar attribute
echo $1
#ncatted -a calendar,time,d,, $1
ncatted -a calendar,time,o,c,standard $1

