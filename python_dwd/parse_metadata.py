""" Meta data handling """
from typing import Union
import pandas as pd

from python_dwd.enumerations.column_names_enumeration import DWDMetaColumns
from python_dwd.enumerations.parameter_enumeration import Parameter
from python_dwd.enumerations.period_type_enumeration import PeriodType
from python_dwd.enumerations.time_resolution_enumeration import TimeResolution
from python_dwd.indexing.file_index_creation import create_file_index_for_dwd_server, \
    reset_file_index_cache
from python_dwd.indexing.meta_index_creation import create_meta_index_for_dwd_data, \
    reset_meta_index_cache


def metadata_for_dwd_data(parameter: Union[Parameter, str],
                          time_resolution: Union[TimeResolution, str],
                          period_type: Union[PeriodType, str],
                          create_new_meta_index: bool = False,
                          create_new_file_index: bool = False) -> pd.DataFrame:
    """
    A main function to retrieve metadata for a set of parameters that creates a
        corresponding csv.
    STATE information is added to metadata for cases where there's no such named
    column (e.g. STATE) in the pandas.DataFrame.
    For this purpose we use daily precipitation data. That has two reasons:
     - daily precipitation data has a STATE information combined with a city
     - daily precipitation data is the most common data served by the DWD
    Args:
        parameter: observation measure
        time_resolution: frequency/granularity of measurement interval
        period_type: recent or historical files
        create_new_meta_index: if true: a new meta index for metadata will
         be created
        create_new_file_index: if true: a new file index for metadata will
         be created
    Returns:
        pandas.DataFrame with metadata for selected parameters
    """
    if create_new_meta_index:
        reset_meta_index_cache()

    if create_new_file_index:
        reset_file_index_cache()

    parameter = Parameter(parameter)
    time_resolution = TimeResolution(time_resolution)
    period_type = PeriodType(period_type)

    meta_index = create_meta_index_for_dwd_data(
        parameter, time_resolution, period_type)

    # If no state column available, take state information from daily historical precipitation
    if DWDMetaColumns.STATE.value not in meta_index:
        mdp = create_meta_index_for_dwd_data(
            Parameter.PRECIPITATION_MORE, TimeResolution.DAILY, PeriodType.HISTORICAL)

        meta_index = pd.merge(
            left=meta_index,
            right=mdp.loc[:, [DWDMetaColumns.STATION_ID.value, DWDMetaColumns.STATE.value]],
            how="left"
        )

    meta_index[DWDMetaColumns.HAS_FILE.value] = False

    file_index = create_file_index_for_dwd_server(
        parameter, time_resolution, period_type)

    meta_index.loc[meta_index.iloc[:, 0].isin(
        file_index[DWDMetaColumns.STATION_ID.value]), DWDMetaColumns.HAS_FILE.value] = True

    return meta_index