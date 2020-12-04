from pandas import DataFrame
from avro.schema import parse
import json
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter


class AvroWriter:
    def __init__(self, avro_schema_file, avro_data_file):
        self.avro_data_file = avro_data_file
        self.schema = parse(open(avro_schema_file, "rb").read())

    def write_sample(self):
        with DataFileWriter(open(self.avro_data_file, "wb"),
                            DatumWriter(),
                            self.schema) as writer:
            writer.append({'name': 'Prague',
                           "year": 2020,
                           "population": 1324277,
                           "area": 496})
            writer.append({'name': 'Berlin',
                           "year": 2019,
                           "population": 3769495,
                           "area": 891})
            writer.append({'name': 'Vienna',
                           "year": 2018,
                           "population": 1888776,
                           "area": 414})


class AvroReader:
    def __init__(self, avro_data_file):
        self.avro_reader = DataFileReader(open(avro_data_file, "rb"), DatumReader())

    def print(self):
        # There is schema available in meta field
        print("---- SCHEMA ----")
        # Print schema as dict
        print(self.avro_reader.meta)
        # Or load it into json
        schema_json = json.loads(self.avro_reader.meta.get('avro.schema').decode('utf-8'))
        print('Avro schema [{}]: {}.{}'.format(schema_json['type'], schema_json['namespace'], schema_json['name']))
        for field in schema_json['fields']:
            print('Field {}:{}'.format(field['name'], field['type']))
        records = [record for record in self.avro_reader]
        print("---- AVRO RECORDS ----")
        print(records)
        print("---- PANDAS DATAFRAME ----")
        print(DataFrame.from_records(records))


if __name__ == '__main__':
    schema_path = './sample.avsc'
    data_path = './sample.avro'
    avro_writer = AvroWriter(schema_path, data_path)
    avro_writer.write_sample()
    avro_reader_embedded = AvroReader(data_path)
    avro_reader_embedded.print()
