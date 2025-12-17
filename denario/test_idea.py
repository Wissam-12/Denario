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
        topic="Motor and cognitive task analysis using circle drawing data",
        domain="Cognitive Science / Human-Computer Interaction",
        objectives=[
            "Analyze the relation between cognitive task type and motor behavior",
            "Investigate perceived difficulty vs actual performance",
            "Correlate trace patterns with task difficulty and effort"
        ]
    )

    # --- Initialize Denario ---
    denario = Denario(
        research=research,
        project_dir=project_dir,
        clear_project_dir=True
    )


    data_description_content = """
    We have conducted an experiment where a group of 40 participants performed
    3 different types of intellectual tasks (numerical, sequential, and verbal)
    while drawing circles with their dominant hand on a tablet during two minutes.
    For each task type there was an easy and a difficult variant, giving a total
    of 6 tasks per participant. Participants answered a questionnaire about effort
    and perceived difficulty. The data is in data-from-trials.xlsx, and the
    circle traces are in CSV files in input_files/.

    Which research questions could you answer with this data?
    """
    denario.set_data_description(data_description_content)


    # --- Run idea generation (FAST MODE) ---
    denario.get_idea(
        mode="fast",
        llm=models["mistral-small-latest"], 
    )

    # --- Basic assertions ---
    input_dir = os.path.join(project_dir, "input_files")
    assert os.path.exists(input_dir), "input_files folder not created"

    print("\nIdea module (fast mode) executed successfully")


if __name__ == "__main__":
    test_idea_fast()
