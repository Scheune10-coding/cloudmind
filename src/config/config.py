import os
import yaml
import sys

class Config:
  _instance = None

  def __init__(self, data: dict):
    yaml_port = data['server']['port']
    yaml_host = data['server']['host']

    self.port = int(os.environ.get('SERVER_PORT', yaml_port))
    self.host = os.environ.get('SERVER_HOST', yaml_host)
    self.database_path = os.environ.get('DATABASE_PATH', data['database']['path'])
    self.logging_level = os.environ.get('LOGGING_LEVEL', data['logging']['level'])
    self.logging_file = os.environ.get('LOGGING_FILE', data['logging']['file'])
    self.llm_model = os.environ.get('LLM_MODEL_NAME', data['llm']['model'])
    self.llm_max_tokens = int(os.environ.get('LLM_MAX_TOKENS', data['llm']['max_tokens']))
    self.llm_temperature = float(os.environ.get('LLM_TEMPERATURE', data['llm']['temperature']))

  @classmethod
  def load(cls, path: str):
    try:
      with open(path, 'r') as f:
        data = yaml.safe_load(f)
    except FileNotFoundError:
      logger.error(f"Config file '{path}' not found.")
      sys.exit(1)
    except yaml.YAMLError as e:
      logger.error(f"Error parsing config file: {e}")
      sys.exit(1)
    cls._instance = cls(data)
    return cls._instance

  @classmethod
  def get_instance(cls):
    if cls._instance is None:
      raise RuntimeError("Zuerst Config.load() aufrufen!")
    return cls._instance