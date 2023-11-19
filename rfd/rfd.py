import os
import csv
from datetime import datetime

class RFDGenerator:
    CSV_FILE = "rfd_records.csv"
    TITLE_CHOICES = {
        '1': "Add or change a company process",
        '2': "An architectural or design decision for hardware or software",
        '3': "Change to an API or command-line tool used by customers",
        '4': "Change to an internal API or tool",
        '5': "Change to an internal process",
        '6': "A design for testing",
    }

    SECTION_CHOICES = {
        '1': "Step 1: Assessing Problems and Resources",
        '2': "Step 2: Setting Goals and Desired Outcomes",
        '3': "Step 3: Evidence-Based and Promising Practices",
        '4': "Step 4: Assessing Fit for a Prevention Activity",
        '5': "Step 5: Determining Capacity",
        '6': "Step 6: Planning to Implement and Evaluate",
        '7': "Step 7: Process Evaluation",
        '8': "Step 8: Outcome Evaluation",
        '9': "Step 9: Continuous Quality Improvement (CQI)",
        '10': "Step 10: Sustainability for a Prevention Activity",
    }

    STATE_MAPPING = {
        'p': 'prediscussion',
        'i': 'ideation',
        'd': 'discussion',
        'pub': 'published',
        'c': 'committed',
        'a': 'abandoned',
    }

    def __init__(self):
        self.title = None
        self.authors = []
        self.state = 'prediscussion'
        self.sections = []

    def run(self):
        self.get_metadata()
        self.get_sections()
        self.generate_rfd()

    def get_metadata(self):
        self.title = input("Enter the title of the RFD: ")
        authors_input = input("Enter the authors (comma-separated, format: first name, last name, email): ")
        self.parse_authors(authors_input)
        self.get_state_choice()  # Call the method to get the state choice

    def get_state_choice(self):
        full_state_names = ', '.join(['Prediscussion', 'Ideation', 'Discussion', 'Published', 'Committed', 'Abandoned'])
        state_choice = input(f"Enter the full name of the state ({full_state_names}): ").title()
        state_mapping = {state.lower()[0]: state.lower() for state in self.STATE_MAPPING.values()}
        self.state = state_mapping.get(state_choice[0], 'prediscussion')

    def parse_authors(self, authors_input):
        author_list = [author.strip() for author in authors_input.split(',')]
        
        for i in range(0, len(author_list), 3):
            if i + 2 < len(author_list):
                self.authors.append({
                    'first_name': author_list[i],
                    'last_name': author_list[i + 1],
                    'email': author_list[i + 2]
                })

    def get_sections(self):
        while True:
            self.show_title_choices()
            title_choice = input("Enter the corresponding number for the title (or 'exit' to finish): ")
            
            if title_choice.lower() == 'exit':
                return
            elif title_choice in self.TITLE_CHOICES:
                self.title = title_choice
                self.show_section_choices()
                self.get_section_input()

    def show_title_choices(self):
        print("\nChoose a title for the section:")
        for key, value in self.TITLE_CHOICES.items():
            print(f"{key}. {value}")

    def show_section_choices(self):
        print(f"\nChoose a section for the title '{self.TITLE_CHOICES[self.title]}':")
        for key, value in self.SECTION_CHOICES.items():
            print(f"{key}. {value}")

    def get_section_input(self):
        while True:
            choice = input("Enter the corresponding number for the section (or 'exit' to finish): ")
            
            if choice.lower() == 'exit':
                return
            elif choice in self.SECTION_CHOICES:
                section_title = self.SECTION_CHOICES[choice]
                content = input(f"Enter content for {section_title}: ")
                self.add_section(section_title, content)
                self.show_section_choices()  # Show the choices again for the next section
            else:
                print("Invalid choice. Please choose a valid number.")

    def add_section(self, section_title, content):
        self.sections.append({'title': section_title, 'content': content})

    def generate_metadata(self):
        authors_formatted = [f"{author['first_name']} {author['last_name']} <{author['email']}>" for author in self.authors]
        metadata = f"---\nauthors: {', '.join(authors_formatted)}\nstate: {self.state}\n---\n"
        return metadata

    def generate_rfd(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{self.title.lower().replace(' ', '_')}_rfd.md"
        with open(filename, 'w') as file:
            file.write(self.generate_metadata())
            file.write(f"# {self.title}\n\n")
            for section in self.sections:
                file.write(f"## {section['title']}\n\n{section['content']}\n\n")

        print(f"RFD generated successfully: {filename}")
        self.update_csv(filename)
        self.open_rfd(filename)

    def update_csv(self, filename):
        with open(self.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.title, filename, self.state, 'Link to PR or discussion'])  # Update with the actual link

    def open_rfd(self, filename):
        try:
            os.system(f"{os.getenv('EDITOR', 'nano')} {filename}")
        except Exception as e:
            print(f"Error opening the file: {e}")

if __name__ == "__main__":
    rfd_generator = RFDGenerator()
    rfd_generator.run()
