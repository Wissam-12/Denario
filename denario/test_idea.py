import os
from denario.denario import Denario
from denario.research import Research
from denario.llm import models

def test_idea_fast():
    # --- Setup project directory ---
    project_dir = os.path.join(os.getcwd(), "test_project_idea")

    # Clean old run
    if os.path.exists(project_dir):
        import shutil
        shutil.rmtree(project_dir)

    # --- Initialize research object ---
    research = Research(
        topic="Graph neural networks for molecular property prediction",
        domain="Machine Learning / Drug Discovery",
        objectives=[
            "Propose a novel GNN architecture",
            "Improve performance on molecular benchmarks"
        ]
    )

    # --- Initialize Denario ---
    denario = Denario(
        research=research,
        project_dir=project_dir,
        clear_project_dir=True
    )


    data_description_content = """
    # Data Description

    This project uses molecular datasets to train and evaluate graph neural networks.

    ## Tools
    - PyTorch Geometric
    - RDKit
    """
    denario.set_data_description(data_description_content)


    # --- Run idea generation (FAST MODE) ---
    denario.get_idea(
        mode="fast",
        llm=models["gemini-2.5-flash"],
    )

    # --- Basic assertions ---
    input_dir = os.path.join(project_dir, "input_files")
    assert os.path.exists(input_dir), "input_files folder not created"

    print("\n Idea module (fast mode) executed successfully")


if __name__ == "__main__":
    test_idea_fast()
