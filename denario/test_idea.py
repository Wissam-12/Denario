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
    We have conducted an experiment where a group of 40 participants performed 3 different types of intellectual tasks (numerical, sequential, and verbal) while at the same time they drew circles with their dominant hand on a tablet during two minutes. For each task type there was an easy and a difficult variant -- which leads to a total of 6 tasks per participant. After each of the 6 tasks, the participants answered a questionnaire about the effort and the perceived difficulty of the different tasks. The data containing the answers to the questionnaire is in the file data-from-trials.csv, which contains as columns:
the identifier of the participant (Participant ID), the type of task (Task), the actual experimental difficulty of the task (Task Difficulty), the order in which the participant executed the task (the order was randomized across different participants), the progress of the participant in the task at the end of the 2-minute timeout (Participant Progress) in number of accomplished subtasks, the number of correctly accomplished subtasks (Correct Progress), the number of mistakes by the end of the task (Total Mistakes), the difficulty reported by the participant (0 = Easy, 1 = Difficult), the participant's perceived mental load (Task Perceived Mental Demand) in a 7-point Likert scale, the participant's task perceived physical effort (Task Perceived Physical Effort) in a 7-point Likert scale, and the participant's task perceived difficulty in a 7-point Likert scale (Task Perceived Difficulty Likert). 

For each task we stored the traces of the drawn circles in CSV files as time series containing 3 columns: the timestamp, the x-coordinate, and the y-coordinate. We provide as example the file P1-NumericalDifficult-02-08-2024-T11-47-20.498.txt, which corresponds to the difficult numerical task conducted by participant 1 (P1). We do have the traces of all the participants and tasks (240 in total).

Which research questions could you answer with this data?
    """
    denario.set_data_description(data_description_content)


    # --- Run idea generation (FAST MODE) ---
    denario.get_idea(
        mode="cmbagent",
        llm=models["mistral-small-latest"], 
        idea_maker_model=models["mistral-small-latest"], 
        idea_hater_model = models["mistral-small-latest"], 
        planner_model = models["mistral-small-latest"], 
        plan_reviewer_model = models["mistral-small-latest"], 
        orchestration_model = models["mistral-small-latest"], 
        formatter_model = models["mistral-small-latest"], 
    )

    # --- Basic assertions ---
    input_dir = os.path.join(project_dir, "input_files")
    assert os.path.exists(input_dir), "input_files folder not created"

    print("\nIdea module (fast mode) executed successfully")


if __name__ == "__main__":
    test_idea_fast()
