import os
import dotenv

from dotenv import dotenv_values


env = dotenv_values()

OS_TYPE = env["OS_TYPE"].strip()

# sharepoint
SHAREPOINT_SITE_URL = env["SHAREPOINT_SITE_URL"]
SHAREPOINT_DOC_URL = env["SHAREPOINT_DOC_URL"]
SHAREPOINT_USERNAME = env["SHAREPOINT_USERNAME"]
SHAREPOINT_PASSWORD = env["SHAREPOINT_PASSWORD"]


def set_env_variable(key, value):
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    os.environ[key] = value.rstrip()
    dotenv.set_key(dotenv_file, key, os.environ[key])
