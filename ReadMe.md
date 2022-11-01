Installation approach
1. python -m venv xrtrading (create a virutal environment)
2. source /path/to/xrtrading/bin/activate
3. pip install -r requirements.txt
4. python report.py -t TeamMap.csv -p ProductMaster.csv -s Sales.csv --team-report=TeamReport.csv --product-report=ProductReport.csv (must use the same flags however name of input files may change)
5. Two report files in the same directory will be generated

Notes
1. May need to use python3 instead of python in certain installations and path configurations