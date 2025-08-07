#! /bin/python3

''' A function to build a table with informations , given one dict of columns and one of rows'''

# Import required modules for table construction 
from rich.table import Table
from rich.console import Console 

console=Console()

def builder(column: dict, rows : dict, end_s : bool, error=None, style=None,sr=None) -> console.print():  # The table build function
    table=Table()
    console=Console()
    for key, value in column.items():
        table.add_column(key,style=value)   
    for key, value in rows.items():
        if sr==None:
            if value==error:
                table.add_row(key,value,style='red',end_section=end_s)
            else:
                table.add_row(key,value,end_section=end_s)
        else:
            table.add_row(key,value,sr,end_section=end_s)
    console.print(table,soft_wrap=True,justify='full',style=style,highlight=True)
    

''' The sr variable is for the tool's version print in the banner purpose. It can also be 
used for Three(03) colummns and rows table printing but, if used in more than one rows line, the output will be ambiguous.
'''
'''The error variable should also be used carefully ...Check the network scan function in 
devices_utils code for an example of its usage'''

