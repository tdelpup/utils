from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Type

class TransformationStrategy(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame, context: dict) -> pd.DataFrame:
        pass

class StrategyFactory:
    _strategies: Dict[str, Type[TransformationStrategy]] = {}
    
    @classmethod
    def register(cls, name: str):
        def decorator(strategy_class: Type[TransformationStrategy]):
            cls._strategies[name] = strategy_class
            return strategy_class
        return decorator
    
    @classmethod
    def create(cls, name: str, *args, **kwargs) -> TransformationStrategy:
        if name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {name}")
        return cls._strategies[name](*args, **kwargs)

# Register strategies
@StrategyFactory.register("first")
class HolidayMergeStrategy(TransformationStrategy):
    def transform(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return df

@StrategyFactory.register("group_by")
class GroupByStrategy(TransformationStrategy):
    def __init__(self, group_columns, agg_functions):
        self.group_columns = group_columns
        self.agg_functions = agg_functions

    def transform(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return df.groupby(self.group_columns).agg(self.agg_functions)

class DataFrameETL:
    def __init__(self):
        self.strategies = []
        
    def add_strategy(self, strategy_name: str, *args, **kwargs):
        strategy = StrategyFactory.create(strategy_name, *args, **kwargs)
        self.strategies.append(strategy)
        return self
        
    def process(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        for strategy in self.strategies:
            df = strategy.transform(df, **kwargs)
        return df
    

import pandas as pd
from io import StringIO

data_today = """date,category,sales,profit
2023-01-02,A,100,10
2023-01-03,A,300,10
2023-01-02,B,200,20"""


today_df = pd.read_csv(StringIO(data_today))

etl = DataFrameETL() \
   .add_strategy("first") \
   .add_strategy("group_by", group_columns=['category'], agg_functions={'sales': 'sum'})

result = etl.process(today_df)

print(result)
