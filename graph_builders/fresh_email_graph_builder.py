from langgraph.graph import START, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from nodes.freshh_email_nodes.store_email_data_db_node import store_email_data_db_node
from states.fresh_graph_state import Fresh_Email_State
from nodes.freshh_email_nodes.classify_email_agent import classify_email_agent
from nodes.freshh_email_nodes.draft_reply import draft_reply
from nodes.freshh_email_nodes.email_not_approved_node import email_not_approved_node
from nodes.freshh_email_nodes.get_available_slots import get_available_slots
from nodes.freshh_email_nodes.handle_meeting_requests import handle_meeting_requests
from nodes.freshh_email_nodes.hITL_node import hITL_node
from nodes.freshh_email_nodes.no_meeting_node import no_meeting_node
from nodes.freshh_email_nodes.select_best_slots_node import select_best_slots_node
from nodes.freshh_email_nodes.send_email_node import send_email_node
from nodes.freshh_email_nodes.classify_email_agent import post_classication_routing
from nodes.freshh_email_nodes.hITL_node import approval_node_routing
from email_data.checkpoint import checkpointer

def build_fresh_email_graph() : 
    graph_builder = StateGraph(Fresh_Email_State)

    graph_builder.add_node('classify_email_agent', classify_email_agent) 
    graph_builder.add_node('no_meeting_node', no_meeting_node)
    graph_builder.add_node('handle_meeting_requests', handle_meeting_requests) 
    graph_builder.add_node('get_available_slot',get_available_slots)
    graph_builder.add_node('select_best_slots_node',select_best_slots_node) 
    graph_builder.add_node('draft_reply',draft_reply) 
    graph_builder.add_node('approval_node',hITL_node) 
    graph_builder.add_node('send_email_node',send_email_node)
    graph_builder.add_node('email_not_approved_node',email_not_approved_node) 
    graph_builder.add_node('store_email_data_db_node',store_email_data_db_node)

    graph_builder.add_conditional_edges('classify_email_agent', post_classication_routing, {'Not_Meeting_Email':'no_meeting_node', 'handle_meeting_requests':'handle_meeting_requests'})
    graph_builder.add_edge(START, 'classify_email_agent')
    graph_builder.add_edge('handle_meeting_requests', 'get_available_slot')
    graph_builder.add_edge('get_available_slot', 'select_best_slots_node')
    graph_builder.add_edge('select_best_slots_node', 'draft_reply')
    graph_builder.add_edge('draft_reply', 'approval_node')
    graph_builder.add_conditional_edges('approval_node', approval_node_routing, {'send_email_action' : 'send_email_node', 'email_not_approved_action' : 'email_not_approved_node'})
    graph_builder.add_edge('send_email_node', 'store_email_data_db_node')

    fresh_email_graph = graph_builder.compile(checkpointer=checkpointer)
    return fresh_email_graph
