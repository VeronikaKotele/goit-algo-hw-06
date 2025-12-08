from .models import Transaction, TransactionStatistics, GlobalTransactionStatistics, CompanyTransactionStatistics

def calculate_statistics(transactions: list[Transaction]) -> GlobalTransactionStatistics:
    """Calculates transaction statistics from a list of transactions"""
    results = GlobalTransactionStatistics()

    for t in transactions:
        value = t.order_value
        flow_id_supplier = t.flow_id_supplier
        flow_id_internal = t.flow_id_internal
        flow_id_customer = t.flow_id_customer
        flow_ids = [flow_id_supplier, flow_id_internal, flow_id_customer]
        company_ids = [flow_id_to_company_ids(flow_id) for flow_id in flow_ids]
        exporting_companies = [id['sender'] for id in company_ids]
        importing_companies = [id['receiver'] for id in company_ids]

        # Update global statistics
        update_statistics(results['global_statistics'], value)

        # Update per-flow statistics
        for flow_id in flow_ids:
            if flow_id not in results['statistics_per_flow']:
                results['statistics_per_flow'][flow_id] = TransactionStatistics()
            update_statistics(results['statistics_per_flow'][flow_id], value)

        # Update per-company statistics
        for company_id in exporting_companies + importing_companies:
            if company_id not in results['statistics_per_company']:
                results['statistics_per_company'][company_id] = CompanyTransactionStatistics()
        for company_id in exporting_companies:
            update_statistics(results['statistics_per_company'][company_id]['exported'], value)
        for company_id in importing_companies:
            update_statistics(results['statistics_per_company'][company_id]['imported'], value)

    return results

def flow_id_to_company_ids(flow_id: str) -> dict[str, str]:
    """Extracts company ID from flow ID by removing the last 4 characters"""
    company_ids = flow_id.split('_')
    if len(company_ids) < 2:
        raise ValueError(f'Invalid flow_id format: {flow_id}: should contain _ separator')

    return { 'sender': company_ids[0], 'receiver': company_ids[1] }

def update_statistics(stats: TransactionStatistics, value: float) -> None:
    """Updates average statistics in-place"""
    stats['quantity'] += 1
    stats['total_value'] += value
    stats['max_value'] = max(stats['max_value'], value)
    stats['min_value'] = min(stats['min_value'], value)
    stats['average_value'] = stats['total_value'] / stats['quantity'] if stats['quantity'] > 0 else 0.0