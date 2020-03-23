import urllib
import zipfile
import requests
import io


def read_file(path):

    def load_from_web():

        url = path
        data = urllib.request.urlopen(url)
        return unzip_file(data.read()).decode('utf8').split('\n')

    def unzip_file(zipped):
        filebytes = io.BytesIO(zipped)
        myzipfile = zipfile.ZipFile(filebytes)
        return myzipfile.read(myzipfile.namelist()[0])

    read_data = load_from_web()
    return read_data[0].replace('\n','').split(','), read_data[1:]


def format_data(data, header):

    def format_output(_dict):
        _as_output = {}
        series_id = '{}//{}//{}'.format(_dict['REF_AREA'], _dict['ENERGY_PRODUCT'], _dict['FLOW_BREAKDOWN'])
        points = [_dict['TIME_PERIOD']]
        fields = {
            'country': _dict['REF_AREA'],
            'concept': _dict['FLOW_BREAKDOWN'],
            'units': [_dict['UNIT_MEASURE']],
            'product': _dict['ENERGY_PRODUCT']
        }

        _as_output['series_id'] = series_id
        _as_output['points'] = points
        _as_output['fields'] = fields

        return _as_output

    def format_row(row):
        row = row.replace('\n', '').split(',')
        _current = {}
        for key in header:
            header_index = header.index(key)
            _current[key] = row[header_index]
        return format_output(_current)

    new_lines = []
    for row in data:
        if row == '':
            continue
        new_row = format_row(row)
        new_lines.append(new_row)
    
    return new_lines


def run():

    header, data = read_file('https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip')
    new_data = format_data(data, header)
    print(new_data)


run()