from langgraph.graph import StateGraph, START
from states.confirmation_state import ConfirmationState
from langgraph.checkpoint.sqlite import SqliteSaver
from nodes.confirmation_email_nodes.approve_meeting_node import approve_meeting_node
from nodes.confirmation_email_nodes.create_event_node import create_event_node
from nodes.confirmation_email_nodes.dont_schedule_node import dont_schedule_node
from nodes.confirmation_email_nodes.extractReplyEmailData import extractReplyEmailData
from nodes.confirmation_email_nodes.update_email_data_in_db import update_email_data_in_db
from nodes.confirmation_email_nodes.approve_meeting_node import schedule_routing
from email_data.checkpoint import checkpointer

def build_confirmation_graph() :
    graph_builder = StateGraph(ConfirmationState) 

    graph_builder.add_node('extractReplyEmailData', extractReplyEmailData)
    graph_builder.add_node('approve_meeting', approve_meeting_node) 
    graph_builder.add_node('create_event_node', create_event_node) 
    graph_builder.add_node('dont_schedule_node', dont_schedule_node)
    graph_builder.add_node('update_email_data_in_db', update_email_data_in_db)

    graph_builder.add_edge(START, 'extractReplyEmailData')
    graph_builder.add_edge('extractReplyEmailData', 'approve_meeting') 
    graph_builder.add_conditional_edges('approve_meeting', schedule_routing, {'create_event' : 'create_event_node', 'dont_schedule':'dont_schedule_node'})
    graph_builder.add_edge('create_event_node', 'update_email_data_in_db')

    confirmation_Graph = graph_builder.compile(checkpointer=checkpointer)
    return confirmation_Graph

