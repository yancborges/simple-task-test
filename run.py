from reader import Reader

# r = Reader('jodi_gas_csv_beta/jodi_gas_beta.csv')
r = Reader('https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip')

print(r.check_ids())
print(r)