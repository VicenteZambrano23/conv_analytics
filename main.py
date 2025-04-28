from utils.groupchat import create_group_chat
from utils.get_sql_tables import get_sql_tables
from utils.update_counter import reset_counter
from utils.clean_graph import graph_clean

graph_clean()
reset_counter()
get_sql_tables()
create_group_chat()

