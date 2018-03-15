if [ $# -eq 0 ]
then
    echo "you have to specify the main file path";
    exit
fi

USDIR="dir/"
TMPFILE="tmp.tsv"
OUTFILE="output_point_1.tsv"
TIMES=19

# init
mkdir $USDIR

function cadd {
 if [[ -n $1 && -n $2 && -n $3 && $1 -gt $TIMES ]]
 then
  echo $3 >> $USDIR/$2
 fi
}

cut -f 1,2,5 $1 | uniq | cut -f 1,3 | sort | uniq -c > $TMPFILE

while read -r line
do
 cadd $line &
done < $TMPFILE
wait

# refactor output
echo "Refactoring data"
for f in $USDIR*
do
    if [[ -f $f ]]
    then
        echo "File "$f
        outline=`(basename $f)`
        while read -r line
        do
                outline=$outline'\t'$line
        done < $f
        echo -e $outline >> $OUTFILE
    fi
done

# clean
rm -r -f $USDIR
rm -f $TMPFILE