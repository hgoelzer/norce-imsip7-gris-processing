#!/bin/bash
# Add x,y to ISMIP GrIS file

if [ $# -lt 2 ]
  then
    echo "Not enough arguments supplied. Need file in 1 and res in 2"
    exit
fi

fout=$1
res=$2

if [ $res == "01" ]; then

    ncap2 -O -s 'x=(array(-720000.,1000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,1000.,$y))' ${fout} ${fout}
     
elif [ $res == "02" ]; then

    ncap2 -O -s 'x=(array(-720000.,2000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,2000.,$y))' ${fout} ${fout}
     
elif [ $res == "03" ]; then

    ncap2 -O -s 'x=(array(-720000.,3000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,3000.,$y))' ${fout} ${fout}
     
elif [ $res == "04" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,4000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,4000.,$y))' ${fout} ${fout}
    
elif [ $res == "05" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,5000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,5000.,$y))' ${fout} ${fout}
    
elif [ $res == "06" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,6000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,6000.,$y))' ${fout} ${fout}
    
elif [ $res == "08" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,8000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,8000.,$y))' ${fout} ${fout}
     
elif [ $res == "10" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,10000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,10000.,$y))' ${fout} ${fout}
     
elif [ $res == "12" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,12000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,12000.,$y))' ${fout} ${fout}
     
elif [ $res == "15" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,15000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,15000.,$y))' ${fout} ${fout}
     
elif [ $res == "16" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,16000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,16000.,$y))' ${fout} ${fout}
     
elif [ $res == "20" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,20000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,20000.,$y))' ${fout} ${fout}
     
elif [ $res == "24" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,24000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,24000.,$y))' ${fout} ${fout}
     
elif [ $res == "30" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,30000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,30000.,$y))' ${fout} ${fout}
     
elif [ $res == "40" ]; then
     
    ncap2 -O -s 'x=(array(-720000.,40000.,$x))' ${fout} ${fout}
    ncap2 -O -s 'y=(array(-3450000.,40000.,$y))' ${fout} ${fout}
     
fi

ncatted -a long_name,x,o,c,"x coordinate of projection" ${fout}
ncatted -a standard_name,x,o,c,"projection_x_coordinate" ${fout}
ncatted -a units,x,o,c,"m" ${fout}
ncatted -a axis,x,o,c,"X" ${fout}
ncatted -a long_name,x,o,c,"y coordinate of projection" ${fout}
ncatted -a standard_name,x,o,c,"projection_y_coordinate" ${fout}
ncatted -a units,y,o,c,"m" ${fout}
ncatted -a axis,y,o,c,"Y" ${fout}
