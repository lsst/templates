#After scons several latex templates are instantiated
#This just makes sure the 'make' works in them

DOCS="/latex_lsstdoc/EXAMPLE-0/  
/technote_aastex/testn-000/ 
/technote_adasstex/testn-000/ 
/technote_spietex/testn-000/ 
/technote_latex/testn-000/ 
/test_report/TESTTR-0/ 
"

here=`pwd`

for d in $DOCS; do
	cd $here
	cd "project_templates$d"
	make
done

