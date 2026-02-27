"""Node: pause graph and ask a human to approve/edit the draft answer.

In CLI mode this prints the draft and reads stdin.
In Streamlit mode the graph is interrupted here and the UI handles approval.
"""
from __future__ import annotations

from agent.state import EmailState


def human_approval_node(state: EmailState) -> dict:
    """
    CLI implementation: print the draft and prompt for approval.

    In Streamlit, this node is declared as an interrupt point in the graph
    and the UI resumes the graph after collecting human input.
    """
    if state.error:
        return {}

    print("\n" + "=" * 60)
    print(f"📧  Email file : {state.file_path}")
    print(f"🏷️   Topic      : {state.topic}")
    print(f"👤  Sender     : {state.sender_name}")
    print("-" * 60)
    print("DRAFT ANSWER:\n")
    print(state.draft_answer)
    print("=" * 60)

    while True:
        choice = input("\n[A]pprove / [E]dit / [R]eject ? ").strip().lower()
        if choice in ("a", "approve"):
            return {"approved": True, "final_answer": state.draft_answer}
        elif choice in ("e", "edit"):
            print("Paste your edited answer (end with a line containing only '---'):")
            lines = []
            while True:
                line = input()
                if line.strip() == "---":
                    break
                lines.append(line)
            edited = "\n".join(lines)
            return {"approved": True, "final_answer": edited, "human_feedback": edited}
        elif choice in ("r", "reject"):
            return {"approved": False, "final_answer": ""}
        else:
            print("Please type 'a', 'e', or 'r'.")