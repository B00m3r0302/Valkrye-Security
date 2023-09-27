## console_interface.py
import cmd
from database import Database
from logger import Logger

class ConsoleInterface(cmd.Cmd):
    def __init__(self, database: Database, logger: Logger):
        super().__init__()
        self.database = database
        self.logger = logger
        self.prompt = '> '

    def do_exit(self, inp):
        '''Exit the console interface.'''
        print('Exiting...')
        return True

    def do_view_tables(self, inp):
        '''View all tables in the database.'''
        tables = ['system_info', 'file_info', 'user_info', 'autorun_info', 'connection_info']
        for table in tables:
            print(f"Table: {table}")
            data = self.database.get_data(table)
            for row in data:
                print(row)

    def do_manage_trusted_ips(self, inp):
        '''Manage trusted IP addresses.'''
        print('This feature is not implemented yet.')

    def do_view_discrepancies(self, inp):
        '''View all discrepancies.'''
        print('This feature is not implemented yet.')

    def run_menu(self):
        self.cmdloop('MCHammer Console Interface. Type help or ? to list commands.\n')

if __name__ == '__main__':
    database = Database('mchammer.db')
    logger = Logger('mchammer.log')
    console_interface = ConsoleInterface(database, logger)
    console_interface.run_menu()
