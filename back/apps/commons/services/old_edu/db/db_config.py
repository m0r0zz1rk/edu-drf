from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

from apps.commons.utils.django.settings import SettingsUtils

base_path = SettingsUtils().get_parameter_from_settings('SETTINGS_DIR')


class Settings(BaseSettings):
    """Класс настроек конфигурации для подключения к олдовой базе edu"""

    OLD_DB_HOST: str = '127.0.0.1'
    OLD_DB_PORT: int = 3306
    OLD_DB_USER: str = 'root'
    OLD_DB_PASSWORD: str = '<PASSWORD>'
    OLD_DB_NAME: str = 'edu'

    @property
    def database_url(self) -> str:
        """DSN для подключения к БД"""
        return (f"mssql+pyodbc://"
                f"{quote_plus(self.OLD_DB_USER)}:"
                f"{quote_plus(self.OLD_DB_PASSWORD)}@"
                f"{self.OLD_DB_HOST}/"
                f"{self.OLD_DB_NAME}?"
                f"driver=ODBC+Driver+17+for+SQL+Server")

    model_config = SettingsConfigDict(env_file=f'{base_path}/environment/.old.env')


old_edu_db_config = Settings()
