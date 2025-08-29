import streamlit as st
from datetime import datetime
import warnings
from my_crew.crew import MyCrew


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


st.title("Searching Data and Analysing it and Producing final report")


def run():
    """
    Run the crew.
    """
    inputs = {
        "topic": "Premier League",
         "current_year": str(datetime.now().year)
    }
    
    try:

        result = MyCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    for task in result.tasks_output:

        for line in task.raw.split("\n"):

            st.markdown(line.strip())
    
        st.markdown("*"*26 + " Task End " + "*"*26)


run()




