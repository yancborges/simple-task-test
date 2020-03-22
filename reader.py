import copy
import requests
import json
import urllib
import io
import zipfile


class Reader:

    def __init__(self, path):

        # Preparing util variables
        self.country_dict = {}
        self.VALID_FORMATS = ['csv', 'txt', 'zip']
        self.file_path = path
        self._extension = self.file_path[-3:]
        self._is_web = 'http://' in self.file_path or 'https://' in self.file_path
        self._is_zip = self._extension == 'zip'
        
        # Processing file
        self.keys, self.raw_data = self.read_csv()
        
        # Cleaning & formatting
        self.clean_data = self.format_data()
    

    def __str__(self):
        return print(self.clean_data)


    def check_ids(self):

        _checked = []
        for doc in self.clean_data:
            if doc['series_id'] in _checked:
                raise KeyError('Error! id duplicated: {}'.format(doc['series_id']))
            _checked.append(doc['series_id'])

        return True

    
    def read_csv(self):

        if not self._extension in self.VALID_FORMATS:
            raise TypeError('File format not supported')
        
        
        if self._is_web:
            read_data = self.load_from_web()
        
        else:
            try:
                if self._is_zip:
                    with open(self.file_path, 'r', encoding='utf8') as zipped:
                        read_data = self.unzip_file(zipped).readlines()
                else:
                    with open(self.file_path, 'r', encoding='utf8') as file:
                        read_data = file.readlines()
        
            except FileNotFoundError:
                raise FileNotFoundError('File not found, check if the path passed is correct')
        
        loaded_file = read_data[0].replace('\n','').split(','), read_data[1:]
        return loaded_file

    
    def format_data(self):
        clean_lines = []
        for line in self.raw_data:
            if line == '':
                continue
            current = {}
            line = line.replace('\n','')
            line_items = line.split(',')
            for key in self.keys:
                key_index = self.keys.index(key)
                current[key] = line_items[key_index]

            clean_lines.append(current)

        return self.setup_dict(clean_lines)


    def setup_dict(self, doc_list):

        _response = []
        for doc in doc_list:
            
            _current = {}

            series_id = 'jodi-data//{}//{}//{}//{}'.format(
                doc['REF_AREA'],
                doc['FLOW_BREAKDOWN'],
                doc['ENERGY_PRODUCT'],
                doc['TIME_PERIOD']
            )

            points = [doc['TIME_PERIOD']]
            fields = copy.deepcopy(doc)

            # Basic renaming
            fields['_REF_AREA'] = self.country_name(fields['REF_AREA'])
            fields['_ENERGY_PRODUCT'] = self.jodi_full_names('ENERGY_PRODUCT', fields['ENERGY_PRODUCT'])
            fields['_FLOW_BREAKDOWN'] = self.jodi_full_names('FLOW_BREAKDOWN', fields['FLOW_BREAKDOWN'])
            
            # Excluding duplicated fields
            fields.pop('TIME_PERIOD')

            _current['series_id'] = series_id
            _current['points'] = points
            _current['fields'] = fields

            _response.append(_current)

        return _response


    def country_name(self, code):

        # Avoiding a lot of unecessary request for data loaded previously
        if self.country_dict.get(code, None):
            return self.country_dict[code]

        else:
            url = 'https://restcountries.eu/rest/v2/alpha/' + code.lower()
            req = requests.get(url)

            if req.status_code != 200:
                raise ConnectionError('Unable to request url')

            value = json.loads(req.text)['name']

            self.country_dict[code] = value

            
        return self.country_dict[code]


    def jodi_full_names(self, key, value):

        values = {
            'ENERGY_PRODUCT': {
                'NATGAS': 'Natural Gas',
                'LNG': 'Liquefied Natural Gas'
            },
            'FLOW_BREAKDOWN': {
                'INSDPROD': 'Production',
                'INDPROD': 'Production',
                'OSOURCES': 'Receipts from Other Sources',
                'TOTIMPSB': 'Total Imports',
                'IMPLNG': 'Imported LNG',
                'IMPPIP': 'Imported through Pipeline LNG',
                'TOTEXPSB': 'Total Exports',
                'EXPLNG': 'Exported LNG',
                'EXPPIP': 'Exported through Pipeline',
                'STOCKCH': 'Stock Change',
                'TOTDEMC': 'Gross Inland Deliveries',
                'STATDIFF': 'Statistical Difference',
                'TOTDEMO': 'Gross Inland Deliveries',
                'MAINTOT': 'of which: Electricity and Heat Generation',
                'CLOSTLV': 'Closing Stocks',
                'CONVER': 'Conversion factor'
            }
        }

        return values[key][value]


    def load_from_web(self):

        url = self.file_path
        data = urllib.request.urlopen(url)
        if self._is_zip:
            return self.unzip_file(data.read()).decode('utf8').split('\n')
        return data.readlines()

    
    def unzip_file(self, zipped):
        filebytes = io.BytesIO(zipped)
        myzipfile = zipfile.ZipFile(filebytes)
        return myzipfile.read(myzipfile.namelist()[0])



