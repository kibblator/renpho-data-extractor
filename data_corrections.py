import re
from injector import singleton, inject
from weight_data_repository import WeightDataRepository

class DataCorrectionService:
    @inject
    @singleton
    def __init__(self, weight_data_repository: WeightDataRepository):
        self.weight_data_repository = weight_data_repository

    def update_values(self, data_dict, correction_string):
        corrections = correction_string.split('\n')

        for correction in corrections:
            print(f'Correction string is: {correction}')
            match = re.match(r'^(\d+)[\s\-)\.]+([\d\.]+)$', correction)
            if match:
                try:
                    index = int(match.group(1)) - 1
                    value = float(match.group(2))
                    
                    if 0 <= index < len(data_dict):
                        key = list(data_dict.keys())[index]
                        data_dict[key] = value
                    else:
                        print(f"Ignoring correction {correction}: Index out of range")
                except ValueError:
                    print(f"Ignoring correction {correction}: Value is not a valid number")
            else:
                print(f"Ignoring correction {correction}: Not a valid correction format")
        
        self.weight_data_repository.store_weight_data(data_dict)

        return data_dict