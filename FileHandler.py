import shutil
import os
import logging


class FileHandler:
    def __init__(self, input_folder, incorrect_folder, processed_folder):
        self.input_folder = input_folder
        self.incorrect_folder = incorrect_folder
        self.processed_folder = processed_folder
        logging.info("Filehandler initialized")

    def get_fb2_file(self):
        return os.listdir(self.input_folder)[0]

    def remove_invalid_files_from_folder(self):
        os.chdir(self.input_folder)
        for input_file in os.listdir(self.input_folder):
            if not input_file.endswith(".fb2"):
                shutil.move(input_file, self.incorrect_folder)
            else:
                continue
        logging.info("All invalid files were removed to incorrect folder")

    def remove_processed_files_from_input_folder(self):
        os.chdir(self.input_folder)
        shutil.move(self.get_fb2_file(), self.processed_folder)
        logging.info("Processed fb2 file was moved to processed folder")
