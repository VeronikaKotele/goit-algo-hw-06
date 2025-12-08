from collections import UserDict

class TransactionStatistics:
    quantity: int = 0
    total_value: float = 0.0
    average_value: float = 0.0
    max_value: float = 0.0
    min_value: float = float('inf')

class TransactionStatisticsPerFlow(UserDict):
    '''A dictionary to hold TransactionStatistics indexed by flow_id'''
    def __setitem__(self, key: str, value: TransactionStatistics) -> None:
        super().__setitem__(key, value)

    def __getitem__(self, key: str) -> TransactionStatistics:
        return super().__getitem__(key)

class CompanyTransactionStatistics:
    exported: TransactionStatistics
    imported: TransactionStatistics
    
class TransactionStatisticsPerCompany(UserDict):
    '''A dictionary to hold TransactionStatistics indexed by company_id'''
    def __setitem__(self, key: str, value: CompanyTransactionStatistics) -> None:
        super().__setitem__(key, value)

    def __getitem__(self, key: str) -> CompanyTransactionStatistics:
        return super().__getitem__(key)

class GlobalTransactionStatistics:
    global_statistics: TransactionStatistics
    statistics_per_flow: TransactionStatisticsPerFlow
    statistics_per_company: TransactionStatisticsPerCompany
