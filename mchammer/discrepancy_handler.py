## discrepancy_handler.py
class DiscrepancyHandler:
    def __init__(self, database, logger):
        self.database = database
        self.logger = logger

    def handle_discrepancies(self, discrepancies):
        for discrepancy in discrepancies:
            self.logger.log_discrepancy(f"Discrepancy detected: {discrepancy['type']} - {discrepancy['detail']}")
            if discrepancy['type'] == 'system_info':
                info_type, _, *info_value = discrepancy['detail'].split(' ')
                self.database.update_data('system_info', {'info_type': info_type, 'info_value': ' '.join(info_value)})
            elif discrepancy['type'] == 'file_info':
                if 'not found' in discrepancy['detail']:
                    file_path = discrepancy['detail'].split(' ')[1]
                    self.database.delete_data('file_info', {'file_path': file_path})
                else:
                    file_path, _, *file_hash = discrepancy['detail'].split(' ')
                    self.database.update_data('file_info', {'file_path': file_path, 'file_hash': ' '.join(file_hash)})
            elif discrepancy['type'] == 'user_info':
                user_name = discrepancy['detail'].split(' ')[1]
                self.database.delete_data('user_info', {'user_name': user_name})
            elif discrepancy['type'] == 'autorun_info':
                if 'not found' in discrepancy['detail']:
                    autorun_path = discrepancy['detail'].split(' ')[1]
                    self.database.delete_data('autorun_info', {'autorun_path': autorun_path})
                else:
                    autorun_path, _, *autorun_hash = discrepancy['detail'].split(' ')
                    self.database.update_data('autorun_info', {'autorun_path': autorun_path, 'autorun_hash': ' '.join(autorun_hash)})
            elif discrepancy['type'] == 'connection_info':
                local_address, _, remote_address, _, _ = discrepancy['detail'].split(' ')
                self.database.delete_data('connection_info', {'local_address': local_address, 'remote_address': remote_address})
