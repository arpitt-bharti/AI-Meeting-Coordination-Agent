import gradio as gr
from langgraph.types import Command
from email_data.fetch_pending_approval_data import get_pending_approvals,delete_pending_approval
from graph_builders.fresh_email_graph_builder import build_fresh_email_graph
import traceback
from services.gmail_service import mark_email_as_read
import warnings

# Suppress the specific Starlette warning from cluttering the console
warnings.filterwarnings("ignore", category=DeprecationWarning, module="gradio")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="starlette")


pending = get_pending_approvals()
pending_map = {
    item["threadId"]: item
    for item in pending
}

current = pending[0] if pending else None
choices = [
    f"{item['recipient']} | {item['agenda']}"
    for item in pending
]
print(f'choices - {choices}') 

def approve_email(thread_id, edited_email):
    fresh_email_graph = build_fresh_email_graph()
    item = pending_map[thread_id]
    config = {
        "configurable": {
            "thread_id": f"mail_session{thread_id}"
        }
    }
    try:
        fresh_email_graph.invoke( 
            Command(
                resume={ 
                    "approved": True,
                    "edited_email": edited_email
                }
            ),
            config=config
        )
        delete_pending_approval(thread_id)
        mark_email_as_read(thread_id)
        print('Marked mail as read')
        return "Email sent successfully."
    
    except Exception as e:
        traceback.print_exc()
        return str(e)
    

def reject_email(thread_id):
    fresh_email_graph = build_fresh_email_graph()
    config = {
        "configurable": {
            "thread_id": f"mail_session{thread_id}"
        }
    }
    try:
        fresh_email_graph.invoke(
            Command(
                resume={
                    "approved": False,
                    "edited_email": ""
                }
            ),
            config=config
        )
        delete_pending_approval(thread_id)
        mark_email_as_read(thread_id)
        return "Request rejected."

    except Exception as e:
        traceback.print_exc()
        return str(e)
    
    
def load_pending_email(thread_id):
    item = pending_map[thread_id]
    return (
        item["recipient"],
        item["agenda"],
        item["draft_email"]
    )


with gr.Blocks(title="AI Meeting Coordinator") as demo:

    gr.Markdown("# 📅 AI Meeting Coordination Agent") 
    gr.Markdown("### Human Approval Dashboard")
    
    pending_dropdown = gr.Dropdown(
    choices=[
        (f"{item['recipient']} | {item['agenda']}", item["threadId"])
        for item in pending
    ], 
    label="Pending Approvals",
    interactive=True
    )

    with gr.Row():
        with gr.Column(scale=1):
            recipient = gr.Textbox(
                label="Recipient",
                value=current["recipient"] if current else "",
                interactive=False
            )
            agenda = gr.Textbox(
                label="Agenda",
                value=current["agenda"] if current else "",
                interactive=False
            )
        with gr.Column(scale=2):
            draft_email = gr.Textbox(
                label="Draft Email",
                value=current["draft_email"] if current else "",
                lines=15,
                interactive=True
            )
    with gr.Row():
        approve_btn = gr.Button(
            "✅ Approve",
            variant="primary"
        )

        reject_btn = gr.Button(
            "❌ Reject",
            variant="stop"
        )
    
    status = gr.Textbox(
    label="Status",
    interactive=False
    )

    approve_btn.click(
        fn=approve_email,
        inputs=[pending_dropdown,draft_email],
        outputs=[status]
    )
    
    reject_btn.click(
    fn=reject_email,
    inputs=[pending_dropdown],
    outputs=[status]
    )
    
    pending_dropdown.change(
    fn=load_pending_email,
    inputs=[pending_dropdown],
    outputs=[
        recipient,
        agenda,
        draft_email]
    )


demo.launch()