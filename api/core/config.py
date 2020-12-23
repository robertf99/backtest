from pydantic import BaseSettings


class Config(BaseSettings):
    """
    docstring
    """

    RAW_DATA_PATH = "raw_data/source.csv"
    COMMISSION = 0.0002

    class Config:
        case_sensitive = True
        env_prefix = "BACKTEST_"


app_config = Config()
