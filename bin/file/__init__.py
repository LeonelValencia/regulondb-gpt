import pandas as pd
from .reader import review_template_file

class File:
    def __init__(self, template_file_directory, output_file_name, error_skip):
        self.template_file_directory = template_file_directory
        self.output_file_name = output_file_name
        self.error_skip = error_skip

    def reader(self,):
        review_template_file(self.template_file_directory, self.error_skip)

    def phrases_result(self, phrases):
        # Guardar frases en un archivo CSV
        df = pd.DataFrame(phrases, columns=["phrases"])
        df.to_csv(self.output_file_name, index=False)