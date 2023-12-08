import csv
from PyQt6 import QtWidgets

def assign_grades(scores):
    grades = []
    for score in scores:
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"

        grades.append(grade)

    return grades

class GradesTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grades Tab")

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.num_students_label = QtWidgets.QLabel("Total number of students:")
        layout.addWidget(self.num_students_label)

        self.num_students_input = QtWidgets.QLineEdit()
        layout.addWidget(self.num_students_input)

        self.proceed_button = QtWidgets.QPushButton("Proceed")
        self.proceed_button.clicked.connect(self.show_grades_input)
        layout.addWidget(self.proceed_button)

        self.output_label = QtWidgets.QLabel()
        layout.addWidget(self.output_label)

        self.scores_labels = []
        self.scores_inputs = []

        self.calculate_button = QtWidgets.QPushButton("Calculate Grades")
        self.calculate_button.clicked.connect(self.calculate_grades)
        self.calculate_button.setHidden(True)
        layout.addWidget(self.calculate_button)

    def show_grades_input(self):
        try:
            num_students = int(self.num_students_input.text())
        except ValueError:
            self.output_label.setText("Invalid input. Please enter a valid number of students.")
            return

        for label, input_field in zip(self.scores_labels, self.scores_inputs):
            label.setParent(None)
            input_field.setParent(None)

        self.scores_labels = []
        self.scores_inputs = []

        for i in range(num_students):
            label = QtWidgets.QLabel(f"Enter score for Student {i + 1}:")
            self.scores_labels.append(label)
            self.layout().addWidget(label)

            scores_input = QtWidgets.QLineEdit()
            scores_input.setPlaceholderText("Enter score")
            self.scores_inputs.append(scores_input)
            self.layout().addWidget(scores_input)

        self.calculate_button.setHidden(False)

        self.proceed_button.setHidden(True)

    def calculate_grades(self):
        try:
            num_students = int(self.num_students_input.text())
            scores = [int(input_field.text()) for input_field in self.scores_inputs]
        except ValueError:
            self.output_label.setText("Invalid input. Please enter valid scores.")
            return

        student_grades = assign_grades(scores)

        csv_filename = "grades_output.csv"
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Student", "Score", "Grade"])
            for i in range(num_students):
                writer.writerow([f"Student {i + 1}", scores[i], student_grades[i]])

        output_text = f"Grades saved to {csv_filename}"
        for i in range(num_students):
            output_text += f"\nStudent {i + 1} score is {scores[i]} and their grade is {student_grades[i]}"

        self.output_label.setText(output_text)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = GradesTab()
    window.show()
    app.exec()
