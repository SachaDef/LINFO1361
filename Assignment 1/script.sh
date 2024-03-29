echo "Test&Log of Rubik2D.py problem solver" >> log.txt
echo "=====================================" >> log.txt
echo "=====================================" >> log.txt
echo >> log.txt

for search in bfst bfsg dfst dfsg
    do
    echo "With search function $search" >> log.txt
    echo "=====================================" >> log.txt
    echo >> log.txt

    for instance in a01 a02 a03 a04 a05 b01 b02 b03 b04 b05
    do
        echo "Instance $instance" >> log.txt
        echo >> log.txt
        python3 rubik2D.py instances/$instance $search >> log.txt
    done

done