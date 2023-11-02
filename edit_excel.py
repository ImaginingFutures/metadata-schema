import pandas as pd

class EditExcel:

    def __init__(self, file):
        self.file = file

    def bulk_replace_values(self, old, new, column):
        df = pd.read_excel(self.file)
        try:
            df[column] = df[column].str.replace(old, new)
        except KeyError:
            print('Column name not found!')
            authorization = input('Do you want to search for the old value in all columns? (y/n): ')
            if authorization == 'y':
                # search for old value in all columns
                for col in df.columns:
                    try:
                        df[col] = df[col].str.replace(old, new)
                    except AttributeError:
                        pass
            else:
                columns_names = df.columns
                print('Column names: ', columns_names)
                print('Exiting...')
                exit()
        df.to_excel(self.file, index=False)
        print('Done!')



if __name__ == '__main__':
    file2edit = input('Enter the file path to edit (abs path is preferred): ')
    old_value = input('Enter the value to replace: ')
    new_value = input('Enter the new value: ')
    column_name = input('Enter the column name: ')
    edit = EditExcel(file2edit)
    edit.bulk_replace_values(old_value, new_value, column_name)


