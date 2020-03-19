class Reader:

    def __init__(self, path):

        self.file_path = path
        self.keys, self.raw_data = self.read_csv()
        self.clean_data = self.format_data()

    
    def read_csv(self):

        with open(self.file_path, 'r', encoding='utf8') as file:
            read_data = file.readlines()
            return read_data[0].replace('\n','').split(','), read_data[1:]


    def format_data(self):
        clean_lines = []
        for line in self.raw_data:
            current = {}
            line = line.replace('\n','')
            line_items = line.split(',')
            for key in self.keys:
                key_index = self.keys.index(key)
                current[key] = line_items[key_index]

            clean_lines.append(current)

        return clean_lines


