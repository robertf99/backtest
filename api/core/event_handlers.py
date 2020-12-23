from typing import Callable
from fastapi import FastAPI
from core.config import app_config
import pandas as pd


def _startup_mode(app: FastAPI) -> None:
    path = app_config.RAW_DATA_PATH
    try:
        df_source = (
            pd.read_csv(
                path,
                header=0,
                encoding="gb2312",
                parse_dates=True,
                infer_datetime_format=True,
                nrows=100,
            )
            .rename(columns={"证券代码": "Tick.Exchange", "证券简称": "Name"})
            # wide Date columns to long
            .melt(
                id_vars=["Tick.Exchange", "Name"], var_name="Date", value_name="Close"
            )
            # del empty rows
            .query("Close != 0")
            # reformat date
            .assign(Date=lambda df: pd.to_datetime(df.Date))
            # seperate tick and exchange, ie, 110030.SH -> [110030, SH]
            .assign(
                Tick=lambda df: df["Tick.Exchange"].str.split(".", expand=True)[0],
                Exchange=lambda df: df["Tick.Exchange"].str.split(".", expand=True)[1],
            )
            .drop("Tick.Exchange", axis=1)
        )
        app.state.df_source = df_source
    except Exception as e:
        raise e


def startup_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        print("Running APP startup handler")
        _startup_mode(app)

    return startup
