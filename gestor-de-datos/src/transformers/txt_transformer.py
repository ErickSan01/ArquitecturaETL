from src.extractors.txt_extractor import TXTExtractor
from os.path import join
import luigi, os, csv, json, re

class TXTTransformer(luigi.Task):

    def requires(self):
        return TXTExtractor()
    
    def run(self):
        result = []
        for file in self.input():
            with file.open() as txt_file:
                header = []
                regex = re.compile('[^a-zA-Z]')
                header = [regex.sub('', column) for column in txt_file.readline().strip().lower().split(',')]
                #next(txt_file)
                
                txt_reader = txt_file.read()
                for row in txt_reader.split(';'):
                    datarow = row.split(',')
                    entry = dict(zip(header, datarow))
                    # print("ENTRY ",entry)
                    # print(entry['descricao'])
                    if not entry['descricao']:
                        continue

                    result.append(
                        {
                            "description": entry['descricao'],
                            "quantity": entry['montante'],
                            "price": entry['precounitario'],
                            "total": float(entry['montante']) * float(entry['precounitario']),
                            "invoice_date": entry['datadafatura'],
                            "invoice": entry['numerodafatura'],
                            "provider": entry['iddocliente'],
                            "country": entry['pais']
                        }
                    )

        with self.output().open('w') as out:
            out.write(json.dumps(result, indent=4))


    def output(self):
        project_dir = os.path.dirname(os.path.abspath("loader.py"))
        result_dir = join(project_dir, "result")
        return luigi.LocalTarget(join(result_dir, "txt.json"))