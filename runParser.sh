
files="$(ls ebay_data)"
args=""
for file in $files
do
    args="${args} ebay_data/${file}"
done

python skeleton_parser.py $args

#sort and eliminate duplicate lines in .dat files
sort usersTable.dat >| temp.dat
uniq temp.dat >| usersTable.dat

sort categoryTable.dat >| temp.dat
uniq temp.dat >| categoryTable.dat

sort bidsTable.dat >| temp.dat
uniq temp.dat >| bidsTable.dat

sort itemsTable.dat >| temp.dat
uniq temp.dat >| itemsTable.dat

rm -f temp.dat #remove temporary file

sqlite3 dataset.db < create.sql
sqlite3 dataset.db < load.txt
