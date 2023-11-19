# rfd
Request for discussion - comprehensive discussions that integrate with GIT environments for CI | CD 

# Class Structure:
The script defines a class RFDGenerator to encapsulate the functionality.
Class variables are used for constants like the CSV file name, title choices, section choices, and state mapping.
# Initialization:
The __init__ method initializes instance variables for the RFD title, authors, state, and sections.
# User Input:
The get_metadata method collects information from the user, such as the RFD title, authors, and state. Authors are entered in a comma-separated format.
The get_state_choice method prompts the user for the state of the RFD, mapping full state names to abbreviated ones.
# Authors Parsing:
The parse_authors method takes the comma-separated authors' input and creates a list of dictionaries with first name, last name, and email.
Section Selection:
The get_sections method guides the user through selecting RFD title and section choices. It uses a loop until the user decides to exit.
# Section Input:
The get_section_input method prompts the user to input content for each selected section under a given title.
# RFD Generation:
The generate_rfd method generates a timestamped Markdown file with the RFD content, including metadata and sections. The file is also opened in the default text editor.
# CSV Update:
The update_csv method appends a new row to a CSV file with information about the generated RFD, including title, filename, state, and a placeholder for the link to the PR or discussion.
# Opening RFD:
The open_rfd method attempts to open the generated RFD file in the user's default text editor using the EDITOR environment variable. If unsuccessful, it catches and prints an error.
# Main Execution:
The __main__ block creates an instance of the RFDGenerator class and executes the run method to start the RFD generation process.