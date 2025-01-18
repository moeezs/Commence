Project Overview:

Commence is an innovative web application designed to simplify the management of academic courses. It allows users to seamlessly add and organize their courses, with a particular focus on extracting key information from course syllabi and streamlining access to essential course details. The platform is equipped with intuitive features that help students stay organized and informed throughout the semester.

Core Features and Functionality:

1. Add a Course:

The process begins with the "Add a Class" button, which opens a popup menu. This intuitive interface allows users to input the course name and upload the course syllabus file (in PDF format).
Once the user clicks "Add," the course is added to a centralized grid at the bottom of the screen. This grid visually organizes all added courses, displaying the course name and instructor's name for easy identification.
The instructor's name, along with the course name, is automatically extracted from the syllabus file using PyPDF, ensuring the process is automated and efficient.

2. Course Details Grid:

After a course is added, it appears in a grid view where each row represents a distinct course.
Each course listing includes essential details: the course name and the instructor's name.
The grid provides an easy-to-navigate overview of all courses added by the user.

3. Detailed Course Information:

When the user clicks on a specific course in the grid, a new popup menu opens, offering additional features and information.
One key feature is the "Download Calendar" button, which generates and downloads a calendar file containing important dates from the syllabus. This file can be imported into any major calendar application (e.g., Google Calendar, Apple Calendar), allowing users to keep track of deadlines for assignments, quizzes, exams, and other key course milestones.

4. Course Component Weightings:

In the same course popup, a detailed table displays the weightings for various course components, such as:
Final exam: 30%
Midterms: 20%
Assignments: 10%, etc.
This breakdown, which is also extracted from the syllabus, provides students with a clear understanding of how their grade will be determined throughout the semester.

Technical Implementation:

1. Syllabus Parsing: The backbone of Commence’s ability to automatically extract course details lies in the use of PyPDF. This Python library allows the application to parse the uploaded syllabus PDF, extracting important textual information such as the course name, instructor, and key dates.

2. Data Storage: All extracted data, including course details, instructor names, and calendar dates, is stored in a JSON file format. This structure makes it easy to access and update the data as the user adds or edits courses.

3. Calendar Integration: The "Download Calendar" feature relies on the extracted dates and formats them into a downloadable calendar file. This functionality leverages calendar APIs or formatting libraries to create a file compatible with a variety of calendar applications.

User Experience:

Commence is designed with simplicity and efficiency in mind. The interface is user-friendly, with minimal input required from the user beyond uploading the syllabus file and naming the course. This allows users to quickly add and organize their courses, while the automated extraction of relevant information minimizes the time spent manually inputting details.

The integration of calendar downloads ensures that users are always aware of upcoming deadlines, and the course component weighting table provides transparency about how their performance will be evaluated.

Conclusion:

Commence is a powerful tool for students looking to streamline their course management process. By automating the extraction of syllabus information and providing essential features like calendar integration and grade component breakdowns, Commence empowers users to stay organized and focused throughout the academic term.
