from states.fresh_graph_state import Fresh_Email_State

def email_not_approved_node(state: Fresh_Email_State):
    print("Draft email rejected by human.")
    return {
        "messages": [
            "Draft email rejected by human."
        ]
    }