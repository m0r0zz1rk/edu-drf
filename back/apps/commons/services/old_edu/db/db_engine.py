from sqlalchemy import create_engine

from apps.commons.services.old_edu.db.db_config import old_edu_db_config

# Создание движка для работы с олдовой базой edu
old_edu_connect_engine = create_engine(
    url=old_edu_db_config.database_url,
    echo=False,
    pool_size=10,
    max_overflow=5
)
