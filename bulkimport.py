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


def validate_map(base_comm: str, map_name: dict):
    """
    Check if the map exists. If not, import it.
    """

    mapname = get_map_name(map_name)

    command = f'{base_comm} write-importer-to-file --mapping {mapname} --file /home/dummymap.xlsx'
    execcommand = subprocess.run(command, shell=True)
    # get console output
    output = execcommand.stdout
    # check if 'Could not import mapping' is in the output
    if 'Could not import mapping' in output:
        # import the map
        command = f'{base_comm} load-import-mapping --file /home/dummymap.xlsx'
        execcommand = subprocess.run(command, shell=True)
        execcommand.check_returncode()
        return mapname
    else:
        return mapname

def create_command(map: dict, data: dict, installation_name: str,  sudo=True, **arguments):
    """
    Creates a command to run the bulk import utility.

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
    **arguments : dict
        Additional arguments to pass to the command.
        Arguments accepted are:
            dataset:           Dataset to import. For XLSX files this is equivalent to worksheets. Dataset indexes are zero-based. For example, in Excel to import the first worksheet set this option to zero (or omit it, as the defalt is zero).
            
            log:               Path to directory in which to log import details. If not set no logs will be recorded.

            log-level:         Logging threshold. Possible values are, in ascending order of importance: DEBUG, INFO, NOTICE, WARN, ERR, CRIT, ALERT. Default is INFO.

            limit-log-to:      Limit logging to specific event types when log level is set to INFO. Limit logging to specific event types for log level INFO. Valid values are: GENERAL (general status messages), EXISTING_RECORD_POLICY (messages relating to merging of existing records, SKIP (messages relating to conditional skipping of mappings, groups or records), RELATIONSHIPS (messages relating to creating of relationships. Seprate multiple types with commas or semicolors.

            import-all-datasets:    When importing an Excel .xslx file, if set import will be performed on all worksheets in the file. By default, only the first worksheet is imported. 

            add-to-set:        Optional identifier of set to add all imported items to.

            environment:       JSON-encoded key value pairs to add to import environment values.

            dryrun:                 If set import is performed without data actually being saved to the database. This is useful for previewing an import for errors.

            direct:                 If set import is performed without a transaction. This allows viewing of imported data during the import, which may be useful during debugging/development. It may also lead to data corruption and should only be used for testing.

            no-search-indexing:     If set indexing of changes made during import is not done. This may significantly reduce import time, but will neccessitate a reindex of the entire database after the import.

    """
    base_com = f'/var/www/html/{installation_name}/support/bin/caUtils'
    mapping = get_map_name(map)
    base_import = f'import-data --source {data["path"]} --mapping {mapping}'
    format = f'--format {data["filename"].split(".")[-1].upper()}'
    arguments = ' '.join([f'--{key} {value}' for key, value in arguments.items()])
    if sudo:
        base_com = f'sudo {base_com}'
    try:
        execcommand = subprocess.run(f'sudo mkdir -p -m00755 {arguments["log"]}', shell=True)
        execcommand.check_returncode()
    except TypeError:
       pass
    command = f'{base_com} {base_import} {format} {arguments}'

    return command


data_maps = {}

folder_path = os.path.join(os.getcwd(), 'installation_docs')

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


for id, data_map in data_maps.items():
    if 'map' in data_map.keys() and 'data' in data_map.keys():
        command = create_command(data_map['map'], data_map['data'], 'ifrepo-admin')
        execcommand = subprocess.run(command, shell=True)
        execcommand.check_returncode()
        print(f'Imported {data_map["data"]["filename"]} with {data_map["map"]["filename"]}')
    else:
        print(f'No map or data file found for {id}. Skipping...')
    