from typing import List
from system import Configurator
from db import CloudSql
from pandas import DataFrame
import numpy as np
import math
import json


class StoreFinder:

    SQL = '''
        SELECT ST_Distance_Sphere(POINT(lng, lat), POINT({current_lng:10.6f}, {current_lat:10.6f}) ) AS distance,
            store_id, lat, lng, name, address, lineOA, tel, AC, FM, FP, GP, KS, SP, VF, XT
            FROM `{database}`.`{table}`
            WHERE lat BETWEEN {min_lat:10.6f} AND {max_lat:10.6f}
            AND lng BETWEEN {min_lng:10.6f} AND {max_lng:10.6f}
            AND {product_type} = "1"
            HAVING distance <= {max_distance}
            ORDER BY distance
            LIMIT 10
    '''
    
    def __init__(self, configurator: Configurator):
        self.configurator = configurator
        self.database = self.configurator.get('cloud_sql.database')
        self.table = self.configurator.get('cloud_sql.table')

    def __get_border(self, lat: float, long: float, distance_meters: int):
        """ Calculate block of lat, long for defined `distance` """
        coef = distance_meters * 0.0000089
        min_lat = lat - coef
        max_lat = lat + coef
        min_long = long - (coef / math.cos(lat * 0.018))
        max_long = long + (coef / math.cos(lat * 0.018))
        return min_lat, max_lat, min_long, max_long

    def format_distance(self, data: DataFrame) -> DataFrame:
        if data.size > 0:
            data['distance'] = np.where(data['distance'].round(-2).astype(int) >= 1000,
                                        (data['distance'] / 1000).round(1).astype(str) + " กม.",
                                        data['distance'].round(-2).astype(int).astype(str) + " ม.")
            return data
        else:
            return data

    def find_shops(self, current_lat:float, current_long:float, max_distance:int, product_type:str) -> List:
        """Find top 10 shops, nearest first"""
        min_lat, max_lat, min_long, max_long = self.__get_border(current_lat, current_long, max_distance)
        db = CloudSql(self.configurator)
        query = self.SQL.format(database=self.database, table=self.table, 
                                current_lat=current_lat, current_lng=current_long, max_distance=max_distance,
                                min_lat=min_lat, max_lat=max_lat, min_lng=min_long, 
                                max_lng=max_long, product_type=product_type
                            )
        df = db.query_df(sql=query)
        df = self.format_distance(df)

        return json.loads(df.to_json(orient='records'))
