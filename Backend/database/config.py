import configparser
import os

# Load the environment or default to LOCAL
ENV = os.environ.get("ENV", "LOCAL").upper()

# Initialize configparser and read the file
config = configparser.ConfigParser()
config.read("Backend/database/config.ini")


# Check if the section exists
if ENV not in config:
    raise ValueError(f"Environment '{ENV}' not found in config.ini")

# Safely load configuration with error handling
try:
    DATABASE_CONFIG = {
        "host": config[ENV]["host"],
        "port": int(config[ENV]["port"]),
        "user": config[ENV]["user"],
        "password": config[ENV]["password"],
        "dbname": config[ENV]["database"]  # Changed to dbname for psycopg2
    }
except KeyError as e:
    raise KeyError(f"Missing required key in [{ENV}] section of config.ini: {e}")
except ValueError as ve:
    raise ValueError(f"Type conversion error in config.ini for environment [{ENV}]: {ve}")

print(DATABASE_CONFIG)  