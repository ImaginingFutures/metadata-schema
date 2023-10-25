import os
import subprocess
import pylightxl as xl


def get_map_name(map_name: dict) -> str:
    """
    Extract the mapping code name from the map file.
    """
    # Check if the map file is an Excel file
    if map_name["filename"].split(".")[-1].lower() != "xlsx":
        return None

    map_path = map_name["path"]
    xls = xl.readxl(map_path)
    
    # Specify the sheet name you want to work with
    sheet_name = xls.ws_names[0]
    
    # Get the data from the sheet
    data = xls.ws(sheet_name).range('A1:C100')
    
    # Find the value based on your criteria
    for row in data:
        if row[0] == 'Setting' and row[1] == 'code':
            mapname = row[2]
            return mapname

    # Return a default value or raise an exception if the value is not found
    return None


def validate_map(base_comm: str, map_name: dict) -> str:
    """
    Check if the map exists. If not, import it.
    """
    mapname = get_map_name(map_name)
    map_path = map_name['path']
    command = f'{base_comm} load-import-mapping --file "{map_path}"'
    try:
        execcommand = subprocess.run(command, shell=True, capture_output=True, text=True)
        execcommand.check_returncode()
        return mapname
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error during map validation: {e.stderr}")


def create_command(map: dict, data: dict, installation_name: str,  sudo=False, import_all_datasets=False, dryrun=False, direct=False, no_search_indexing=False, **arguments) -> str:
    """
    Creates a command to prepare the run
    """
    
    # prepare the command

    base_command = f'/var/www/html/{installation_name}/support/bin/caUtils'
    mapping = validate_map(base_command, map)
    base_import = f'import-data --source "{data["path"]}" --mapping "{mapping}"'
    format = f'--format {data["filename"].split(".")[-1].upper()}'
    arguments = ' '.join([f'--{key.replace("_", "-")} {value}' for key, value in arguments.items()])
    
    # add sudo to execute the command
    if sudo:
        base_command = f'sudo {base_command}'


    # create a list of flags based on the boolean variables
    flags = [
        "--import-all-dataset" if import_all_datasets else "",
        "--dryrun" if dryrun else "",
        "--direct" if direct else "",
        "--no-search-indexing" if no_search_indexing else ""
    ]
    
    # join the flags with a space to include in the command
    flag_string = " ".join(flags)

    # ensure the path to log is created in case it's declared
    log_path = arguments.get('log')
    
    if log_path is not None:
        try:
            execcommand = subprocess.run(f'sudo mkdir -p -m00755 {log_path}', shell=True)
            print(execcommand.stdout)
            execcommand.check_returncode()
        except subprocess.CalledProcessError as e:
            print(f"Error while creating log directory: {e}")
    
    # Create command to run
    
    command = f'{base_command} {base_import} {format} {flag_string} {arguments}'

    return command

def map_data_pair(folder_path: str) -> dict:
    """
    Receive a path or pathlike string and creates a dictionary with the filenames and paths of each pair of maps and data spreadsheets. 

    Spreadsheets must be in xlsx to work. 

    Both data and maps must be in the same directory and share the id.

    Namefiles must be like

    01.map.xlsx
    01.data.xlsx

    """

    data_maps = {}

    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            id = filename.split('.')[0]
            
            type = 'map' if 'map' in filename.lower() else 'data'

            try:
                data_maps[id][type] = {'filename': filename,
                                    'path': os.path.join(folder_path, filename)}
            except KeyError:
                data_maps[id] = {}
                data_maps[id][type] = {'filename': filename,
                                    'path': os.path.join(folder_path, filename)}

    return data_maps

def bulk_install(files_path: str, installation_name: str, sudo=False, import_all_datasets=False, dryrun=False, direct=False, no_search_indexing=False, **arguments):
    """
    Run the bulk import utility.

    Parameters
    ----------
    map : dict
        Dictionary containing the map file's filename and path.
        Correspond to "Mapping to import data with."
        If the map is not previously imported into the system, the command 'load-import-mapping' will be used to import the map.
    data : dict
        Dictionary containing the data file's filename and path.
        Correspond to "Data to import. For files provide the path; for database, OAI and other non-file sources provide a URL."
    installation_name : str
        Name of the installation. It must correspond to the name of the installation's folder in /var/www/html.
    sudo : bool, optional
        Whether or not to use sudo in the command. The default is True.
    import_all_datasets: bool, optional
        When importing an Excel .xslx file, if set import will be performed on all worksheets in the file. By default, only the first worksheet is imported.
    dryrun: bool, optional
        If set import is performed without data actually being saved to the database. This is useful for previewing an import for errors.
    direct: bool, optional
        If set import is performed without a transaction. This allows viewing of imported data during the import, which may be useful during debugging/development. It may also lead to data corruption and should only be used for testing.
    no_search_indexing: bool, optional
        If set indexing of changes made during import is not done. This may significantly reduce import time, but will neccessitate a reindex of the entire database after the import.

    **arguments : dict
        Additional arguments to pass to the command.
        Arguments accepted are:
        dataset:           
            Dataset to import. For XLSX files this is equivalent to worksheets. Dataset indexes are zero-based. For example, in Excel to import the first worksheet set this option to zero (or omit it, as the defalt is zero).
            
        log:               
            Path to directory in which to log import details. If not set no logs will be recorded.

        loglevel:         
            Logging threshold. Possible values are, in ascending order of importance: DEBUG, INFO, NOTICE, WARN, ERR, CRIT, ALERT. Default is INFO.

        limit_log_to:      
            Limit logging to specific event types when log level is set to INFO. Limit logging to specific event types for log level INFO. Valid values are: GENERAL (general status messages), EXISTING_RECORD_POLICY (messages relating to merging of existing records, SKIP (messages relating to conditional skipping of mappings, groups or records), RELATIONSHIPS (messages relating to creating of relationships. Seprate multiple types with commas or semicolors. 

        add_to_set:        
            Optional identifier of set to add all imported items to.

        environment:       
            JSON-encoded key value pairs to add to import environment values.

    """
    data_maps = map_data_pair(files_path)
    
    for id, data_map in data_maps.items():
        if 'map' in data_map.keys() and 'data' in data_map.keys():
            command = create_command(data_map['map'], data_map['data'], installation_name, sudo, import_all_datasets, dryrun, direct, no_search_indexing, **arguments)
            execcommand = subprocess.run(command, shell=True, capture_output=True, text=True)
            execcommand.check_returncode()
            print(execcommand.stdout)
            print(f'Imported {data_map["data"]["filename"]} with {data_map["map"]["filename"]}')
        else:
            print(f'No map or data file found for {id}. Skipping...')
    

if __name__ == '__main__':
    folder_path = os.path.join(os.getcwd(), 'installation_docs')
    bulk_install(folder_path, 'ifrepo-admin', log='/var/log/caImport', log_level="DEBUG")