"""
Module providing the ability to save a new file to a specified path with a string input.
"""
import os
import logging

# Use External Library that already does path and file name validation
# cross platform.
from pathvalidate import ValidationError, validate_filepath, validate_filename

# Use External Library that allows ANSI color in the output
from colorama import just_fix_windows_console, Fore, Style

# Start Fixes for Console ANSI color support. (Not just windows.)
just_fix_windows_console()

# Setup Logging output
LOGGER_OUTPUT_FORMAT = [
    '------------------------------------',
    Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW + '   Logging Level:' + Fore.RED + ' %(levelname)s',
    Style.RESET_ALL + Style.BRIGHT + ' - Time:          ' + Style.RESET_ALL + '%(asctime)s',
    Style.BRIGHT + ' - File:          ' + Style.RESET_ALL + '%(pathname)s',
    Style.BRIGHT + ' - Function:      ' + Style.RESET_ALL + '%(funcName)s',
    Style.BRIGHT + ' - Line Number:   ' + Style.RESET_ALL + '%(lineno)d',
    '------------------ [ Begin Message ] ------------------',
    '%(message)s']
# Configure Logging
logging.basicConfig(level=logging.DEBUG, format='\n'.join(LOGGER_OUTPUT_FORMAT), 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def save_file(path:str, file_name:str, data:str, auto_create_dir:bool = True) -> bool:
    """
    Saves the specified data to a file in the given path.

    Parameters:
    - path (str): The directory path where the file should be saved.
    - filename (str): The name of the file to be created.
    - data (str): The data to be written to the file.
    - create_path_if_not_exists (bool): Whether to create the directory if it does not exist.

    Returns:
    - bool: True if the file is successfully saved, False otherwise.

    Raises:
    - ValueError: If any of the parameters are invalid (e.g., empty path or filename).
    - ValidationError: If the path or filename are invalide.
    - FileExistsError: If a file with the specified name already exists in the directory.
    - FileNotFoundError: If the path does not exist AND auto_create_dir is not TRUE.
    - PermissionError: If the script does not have permission to write to the path
    - Exception: If any unknown/or unexpected errors arise.
    """
    logger.debug({
        'path': path,
        'filename': file_name,
        'data': data,
        'auto_create_dir': auto_create_dir,
        'os.path.exists(path)': os.path.exists(path)
    })
    try:
        # Validate path
        if not isinstance(path, str):
            raise ValueError("Path must be a string.")
        validate_filepath(path, platform='auto', max_len=None)

        # Validate filename
        if not file_name or not isinstance(file_name, str):
            raise ValueError("Filename must be a non-empty string.")
        validate_filename(file_name, platform='auto')

        # Validate auto_create_dir
        if not isinstance(auto_create_dir, bool):
            raise ValueError("auto_create_dir must be a boolean value.")

        # Verify and create the directory path if it does not exist
        if not os.path.exists(path):
            logger.debug('Path "%s" does not exist', path)
            if auto_create_dir:
                logger.debug('Attempting to create path "%s".', path)
                os.makedirs(path)
            else:
                raise FileNotFoundError(f"The specified path '{path}' does not exist and is not being created.")

        # Construct the full file path
        file_path = os.path.join(path, file_name)
        logger.debug('Combined file_path is "%s".', file_path)

        # Check if the file already exists
        if os.path.exists(file_path):
            raise FileExistsError(f"A file with the name '{file_name}' already exists in the directory '{path}'.")

        # Write data to the file
        logger.debug('Attempting to write file.')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)

        logger.debug('All is well. Returning True.')
        return True

    except ValidationError as ve:
        logger.exception(str(ve))
        print(f"ValidationError:\n {ve}")

    except ValueError as ve:
        logger.exception(str(ve))
        print(f"ValueError:\n {ve}")

    except FileNotFoundError as fnf:
        logger.exception(str(fnf))
        print(f"FileNotFoundError:\n {fnf}")

    except FileExistsError as fee:
        logger.exception(str(fee))
        print(f"FileExistsError:\n {fee}")

    except PermissionError as pe:
        logger.exception(str(pe))
        print(f"PermissionError:\n {pe}")

    except Exception as e:
        logger.exception(str(e))
        print(f"An error occurred:\n {e}")

    return False

# Once Unit Test are created this will be activated.
# if __name__ == "__main__":
#     pytest.main([__file__])
