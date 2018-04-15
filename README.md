# create-sql-state

> Write a create table statement based on data in a delimited file.

## Usage
This repository contains a simple command line script and GUI (requires appjar library) that parses a delimited data file, determines the max text length in each column, and then outputs a create table statement based on those lengths. The header row in the data file is used to create the column names. Additionally, fields from the first data row can be added as comments in the SQL statement with the optional -eg argument. 
