from datetime import date
from eurusdyfinance import *
from flask import Flask, request

fromdate = date(2006, 1, 1)
todate = date(2007, 1, 1)

execute(fromdate, todate)

# generate a simple python rest api
