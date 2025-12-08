from collections import UserDict
from dataclasses import dataclass, field

@dataclass
class TransactionStatistics:
    quantity: int = 0
    total_value: float = 0.0
    average_value: float = 0.0
    max_value: float = 0.0
    min_value: float = field(default_factory=lambda: float('inf'))
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)

class TransactionStatisticsPerFlow(UserDict):
    '''A dictionary to hold TransactionStatistics indexed by flow_id'''
    def __setitem__(self, key: str, value: TransactionStatistics) -> None:
        super().__setitem__(key, value)

    def __getitem__(self, key: str) -> TransactionStatistics:
        return super().__getitem__(key)

@dataclass
class CompanyTransactionStatistics:
    exported: TransactionStatistics = field(default_factory=TransactionStatistics)
    imported: TransactionStatistics = field(default_factory=TransactionStatistics)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
    
class TransactionStatisticsPerCompany(UserDict):
    '''A dictionary to hold TransactionStatistics indexed by company_id'''
    def __setitem__(self, key: str, value: CompanyTransactionStatistics) -> None:
        super().__setitem__(key, value)

    def __getitem__(self, key: str) -> CompanyTransactionStatistics:
        return super().__getitem__(key)

@dataclass
class GlobalTransactionStatistics:
    global_statistics: TransactionStatistics = field(default_factory=TransactionStatistics)
    statistics_per_flow: TransactionStatisticsPerFlow = field(default_factory=TransactionStatisticsPerFlow)
    statistics_per_company: TransactionStatisticsPerCompany = field(default_factory=TransactionStatisticsPerCompany)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
