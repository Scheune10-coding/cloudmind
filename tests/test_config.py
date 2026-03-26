import pytest
from src.config.config import Config

@pytest.fixture(autouse=True)
def reset_config():
    Config._instance = None
    yield
    Config._instance = None

def test_config_loading():
  config = Config.load("config.yaml")
  assert config is not None

def test_config_env_override(monkeypatch):
  ENV_PORT = 9090
  monkeypatch.setenv('SERVER_PORT', str(ENV_PORT))
  config = Config.load("config.yaml")
  assert config.port == ENV_PORT

def test_singleton_behavior():
  config1 = Config.load("config.yaml")
  config2 = Config.get_instance()
  assert config1 is config2