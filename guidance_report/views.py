from django.http import HttpResponse
from .utils import generate_gpt_response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from weasyprint import HTML
import os
from django.template.loader import render_to_string
from users.models import Student
from cv.models import Skills, Experience, Interests, CV, Qualities
from choices.models import Level5, Level6, Level8, Apprentice
from calculator.models import UserPoints, SubjectGrade
from goals.models import Goal
from psychometric.models import TestResult
from django.forms.models import model_to_dict
from django.db.models import QuerySet


def serialize_students_data(instance):
    return model_to_dict(instance)

class GuidanceReportModels(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            models = {
                "main_models": [
                    "predicted points and subjects",
                    "my studied goals",
                    "multiple intelligence score",
                    "values assessment",
                    "interest assessment"
                ],
                "cv_models": [
                    "address",
                    "personal statement",
                    "work experience",
                    "skills",
                    "qualities",
                    "interests",
                ],
                "education_models": [
                    "level 8",
                    "level 6/7",
                    "level 5(plc)",
                    "apprentices",
                ]
            }
            return Response({"success": True, "models": models}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GenerateGpt(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = self.request.user
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({"success": False, "message": "User does not exist or not a student"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            prompt = """Based on the student's data, create a guidance report for student on these topics 
            \nExecutive Summary
            \nSelf Assessment Results
            \nStudy Advice
            \nAcademic Record
            \nCareer Assessment
            \nGoal Setting
            \nEducational Options
            \nSuggested Resources 
            \nConclusion
            
            student data:
            \n"""



            # Main Models
            main_models = request.data.get('main_models', [])
            if "predicted points and subjects" in main_models:
                user_points = UserPoints.objects.filter(user=student).first()
                # subject = SubjectGrade.objects.filter(user=student).first()

                if user_points:
                    prompt += f"Predicted points and subjects: {user_points.total_points},\n"
                else:
                    prompt += "Predicted points and subjects: Not available\n"

            if "my studied goals" in main_models:
                goals = Goal.objects.filter(user=student).first()
                if goals:
                    prompt += f"My studied goals: {goals.goal}, {goals.description}\n"
                else:
                    prompt += "My studied goals: Not available\n"

            if "multiple intelligence score" in main_models:
                mi_score = TestResult.objects.filter(user=student, test__name='Multiple Intelligence').first()
                if mi_score:
                    prompt += f"Multiple intelligence score: {mi_score.score}\n"
                else:
                    prompt += "Multiple intelligence score: Not available\n"

            print("prompt: ", prompt)

            # CV Section
            cv = CV.objects.filter(user=student).first()
            if cv:
                prompt += f"Address: {cv.address}, {cv.city}, {cv.town}\n"
                prompt += f"Personal Statement: {cv.objective}\n"
            else:
                prompt += "CV data: Not available\n"

            work_experience = Experience.objects.filter(user=student)
            if work_experience.exists():
                experience_list = "\n".join([f"{exp.job_title} at {exp.company}" for exp in work_experience])
                prompt += f"Work Experience: {experience_list}\n"
            else:
                prompt += "Work Experience: Not available\n"

            skills = Skills.objects.filter(user=student)
            if skills.exists():
                skills_list = ", ".join([skill.skill_dropdown for skill in skills])
                prompt += f"Skills: {skills_list}\n"
            else:
                prompt += "Skills: Not available\n"

            qualities = Qualities.objects.filter(user=student)
            if qualities.exists():
                qualities_list = ", ".join([quality.quality_dropdown for quality in qualities])
                prompt += f"Qualities: {qualities_list}\n"
            else:
                prompt += "Qualities: Not available\n"

            interests = Interests.objects.filter(user=student)
            if interests.exists():
                interests_list = ", ".join([interest.interests for interest in interests])
                prompt += f"Interests: {interests_list}\n"
            else:
                prompt += "Interests: Not available\n"

            print("prompt: ", prompt)            # Education Options
            education_mappings = {
                "level 8": Level8.objects.filter(student=student).first(),
                "level 6/7": Level6.objects.filter(student=student).first(),
                "level 5(plc)": Level5.objects.filter(student=student).first(),
                "apprentices": Apprentice.objects.filter(student=student).first()
            }

            education_models = request.data.get('education_models', [])
            for key in education_models:
                if key in education_mappings:
                    label = education_mappings[key]
                    if label:
                        prompt += f"Education Option - {key.replace('_', ' ').title()}: {label}\n"
                    else:
                        prompt += f"Education Option - {key.replace('_', ' ').title()}: Not available\n"

            # gpt_response = generate_gpt_response(prompt)

            response = {"success": True, "message": "gpt report generated successfully", "prompt": prompt}
            return Response(response, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({"success": False, "message": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GeneratePDFReport(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            student = self.request.user
            user_obj = Student.objects.get(id=student.student.id)
            temp_name = "general/templates/"
            report_template = str(user_obj.first_name) + "-" + str(user_obj.last_name) + "-" + "guidance_report" + ".html"
            full_name = user_obj.full_name

            executive_summary = "A brief overview of the entire report, summarizing the key findings and recommendations based on your self-assessment and career goals. It highlights the main points that will be discussed in the following sections."
            self_assessment_result = "A brief overview of the entire report, summarizing the key findings and recommendations based on your self-assessment and career goals. It highlights the main points that will be discussed in the following sections."
            study_advice = "Tailored recommendations on study <b>habits, strategies, and academic</b> planning based on your self-assessment results. This may include advice on study techniques, time management, and areas to focus on."
            academic_record = "A summary of your academic history, including grades, courses taken, and any relevant academic achievements. It may also include an analysis of your performance trends over time."
            career_assessment = "An evaluation of potential career paths based on your self-assessment results, interests, and academic record. It may include suggested careers, job roles, and industries that align with your profile."

            context = {
                "first_name": user_obj.first_name,
                "last_name": user_obj.last_name,
                "executive_summary": executive_summary,
                "self_assessment_result": self_assessment_result,
                "study_advice": study_advice,
                "academic_record": academic_record,
                "career_assessment": career_assessment,

            }
            rendered_template = render_to_string('guidance_report.html', context)
            open(temp_name + report_template, "w").write(rendered_template)
            HTML(temp_name + report_template).write_pdf(str("guidance_report") + '.pdf')
            file_location = f'{"guidance_report"}.pdf'
            with open(file_location, 'rb') as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{full_name} Guidance Report.pdf"'
            os.remove(temp_name + report_template)
            os.remove("guidance_report.pdf")
            return response

        except Exception as e:
            return Response({'message': "All steps of Guidance Report should be completed . " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GenerateGuidanceReportGPT(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = self.request.user
            try:
                student = Student.objects.get(user=user)
                print("student: ", student)
            except Student.DoesNotExist:
                return Response({"success": False, "message": "User does not exist or is not a student"},
                                status=status.HTTP_400_BAD_REQUEST)

            prompt = (
                "You are an educational counselor tasked with creating a career guidance report for a second-level student in Ireland. "
                "The report must follow this structured format:\n\n"
                "<h1>Career Guidance Report</h1>\n\n"
                "<h2>Introduction</h2>\n"
                "<p>Provide a brief introduction with personal details, including name, age, and educational stage.</p>\n\n"
                "<h2>Self-Assessment Results</h2>\n"
                "<p>Summarize the student's results from the Multiple Intelligences Test, Occupational Values Assessment, and Occupational Interest Assessment.</p>\n"
                "<ul>\n"
                "  <li><strong>Multiple Intelligences:</strong> List top three intelligences with descriptions.</li>\n"
                "  <li><strong>Occupational Interests:</strong> Highlight top three interests and their implications.</li>\n"
                "  <li><strong>Occupational Values:</strong> Outline top three values with explanations.</li>\n"
                "</ul>\n"
                "<p>Explain what these results mean for the student's strengths and potential career paths. Suggest five compatible careers with brief descriptions.</p>\n\n"
                "<h2>Suggested Study Techniques and Advice</h2>\n"
                "<p>Provide study techniques tailored to the student's strengths based on the Multiple Intelligences scores.</p>\n\n"
                "<h2>Academic Achievement</h2>\n"
                "<p>Summarize the CAO points and highlight strong subjects. Suggest relevant courses based on academic performance.</p>\n\n"
                "<h2>Career Exploration</h2>\n"
                "<p>Offer practical advice for exploring careers further, such as shadowing, volunteering, and attending open days.</p>\n\n"
                "<h2>Goals of Student</h2>\n"
                "<p>Outline short-term (next three months) and long-term (next year) goals with actionable steps.</p>\n\n"
                "<h2>Compatible Courses</h2>\n"
                "<ul>\n"
                "  <li>10 Level 8 Courses</li>\n"
                "  <li>10 Level 6/7 Courses</li>\n"
                "  <li>5 Apprenticeships</li>\n"
                "  <li>3 QQI Level 5 Courses</li>\n"
                "  <li>Other non-education-based ideas</li>\n"
                "</ul>\n\n"
                "<h2>Conclusion</h2>\n"
                "<p>Provide an encouraging summary highlighting the student's strengths and the alignment of their goals with their potential career paths.</p>\n\n"
                "**Output Requirements:**\n"
                "- Use proper HTML tags for headings, paragraphs, and lists.\n"
                "- Format data into readable sections with lists, tables, or structured paragraphs.\n"
                "- Ensure the language is professional, encouraging, and tailored to the student's strengths.\n"
                "- Do not include placeholder text or any explanations outside the report structure.\n"
            )

            # Retrieve the request data
            request_data = request.data

            student_data = serialize_students_data(student)
            prompt += f"Student's Data: {student_data}\n"

            # Check if this is a feedback-driven request
            feedback = request_data.get("feedback", None)
            previous_response = request_data.get("previous_response", None)

            if feedback and previous_response:
                # Append the previous report and feedback to the prompt
                prompt += (
                    "This is a revision request. Below is the previously generated report and the feedback provided by the user.\n\n"
                    "Previously generated report:\n"
                    "--------------------------------\n"
                    f"{previous_response}\n\n"
                    "Feedback from the user:\n"
                    f"- {feedback}\n\n"
                    "Please revise the report based on this feedback while retaining the original structure and addressing all feedback."
                )
            else:
                # Generate the initial report
                prompt += (
                    "This is an initial report generation request. Use the provided student data to generate a detailed and personalized report.\n\n"
                )

            # Predicted Points and Subjects
            if request_data.get('predicted_points_and_subjects') == 'Yes':
                # Fetch UserPoints for the student
                user_points = UserPoints.objects.filter(user=student).first()
                if user_points:
                    prompt += f"- Predicted Points: {user_points.total_points}\n"

                    # Fetch related grades through the grades ManyToManyField
                    subjects = user_points.grades.all()
                    if subjects.exists():
                        subject_list = "\n".join([
                            f"  - Subject: {subject.subject.name}, Grade: {subject.grade}, Points: {subject.point}, Level: {subject.level.subjectlevel}"
                            for subject in subjects
                        ])
                        prompt += f"- Subjects:\n{subject_list}\n"
                    else:
                        prompt += "- Subjects: Not available\n"
                else:
                    prompt += "- Predicted Points and Subjects: Not available\n"

            # My Stated Goals
            if request_data.get('my_stated_goals') == 'Yes':
                # Fetch goals for the student
                goals = Goal.objects.filter(user=student)
                if goals.exists():
                    goal_list = "\n".join([f"  - {goal.goal}: {goal.description}" for goal in goals])
                    prompt += f"- Goals:\n{goal_list}\n"
                else:
                    prompt += "- Goals: Not available\n"

            # Multiple Intelligence Score
            if request_data.get('mis') == 'Yes':
                mi_score = TestResult.objects.filter(user=student, test__name='Multiple Intelligence').first()
                if mi_score:
                    prompt += f"- Multiple Intelligence Score: {mi_score.score}\n"
                else:
                    prompt += "- Multiple Intelligence Score: Not available\n"

            # Address
            if request_data.get('address') == 'Yes':
                cv = CV.objects.filter(user=student).first()
                if cv and cv.address and cv.city and cv.town:
                    prompt += f"- Address: {cv.address}, {cv.city}, {cv.town}\n"
                else:
                    prompt += "- Address: Not available\n"

            # Personal Statement
            if request_data.get('personal_statement') == 'Yes':
                cv = CV.objects.filter(user=student).first()
                if cv and cv.objective:
                    prompt += f"- Personal Statement: {cv.objective}\n"
                else:
                    prompt += "- Personal Statement: Not available\n"

            # Work Experience
            if request_data.get('work_experience') == 'Yes':
                work_experience = Experience.objects.filter(user=student)
                if work_experience.exists():
                    experience_list = "\n".join([
                        f"  - Job Title: {exp.job_title}, Company: {exp.company}, City: {exp.city}, Country: {exp.country}, Description: {exp.description}"
                        for exp in work_experience
                    ])
                    prompt += f"- Work Experience:\n{experience_list}\n"
                else:
                    prompt += "- Work Experience: Not available\n"

            # Skills
            if request_data.get('skills') == 'Yes':
                skills = Skills.objects.filter(user=student)
                if skills.exists():
                    skills_list = "\n".join([f"  - {skill.skill_dropdown}: {skill.description}" for skill in skills])
                    prompt += f"- Skills:\n{skills_list}\n"
                else:
                    prompt += "- Skills: Not available\n"

            # Qualities
            if request_data.get('qualities') == 'Yes':
                qualities = Qualities.objects.filter(user=student)
                if qualities.exists():
                    qualities_list = ", ".join([quality.quality_dropdown for quality in qualities])
                    prompt += f"- Qualities: {qualities_list}\n"
                else:
                    prompt += "- Qualities: Not available\n"

            # Interests
            if request_data.get('interest') == 'Yes':
                interests = Interests.objects.filter(user=student)
                if interests.exists():
                    interests_list = ", ".join([interest.interests for interest in interests])
                    prompt += f"- Interests: {interests_list}\n"
                else:
                    prompt += "- Interests: Not available\n"

            # Values Assessment
            if request_data.get('values_assessment') == 'Yes':
                values_assessment = TestResult.objects.filter(user=student, test__name='Values Assessment').first()
                if values_assessment:
                    prompt += f"- Values Assessment Score: {values_assessment.score}\n"
                else:
                    prompt += "- Values Assessment: Not available\n"

            # Interest Assessment
            if request_data.get('interest_assessment') == 'Yes':
                interest_assessment = TestResult.objects.filter(user=student, test__name='Interest Assessment').first()
                if interest_assessment:
                    prompt += f"- Interest Assessment Score: {interest_assessment.score}\n"
                else:
                    prompt += "- Interest Assessment: Not available\n"

            # Education Options
            education_options = request_data.get('education_options', [])
            if education_options:
                # Prepare the education mappings
                education_mappings = {
                    "level 8": Level8,
                    "level 6/7": Level6,
                    "level 5(plc)": Level5,
                    "apprentices": Apprentice
                }
                for key in education_options:
                    if key in education_mappings:
                        entries = education_mappings[key].objects.filter(choice__user=student)
                        if entries.exists():
                            # Build the education list with detailed information
                            education_list = "\n".join([
                                f"  - Code: {entry.code}, Title: {entry.title}, College: {entry.college}, Points: {getattr(entry, 'point', 'N/A')}, Info: {entry.course_information}"
                                for entry in entries
                            ])
                            prompt += f"- Education Option - {key.title()}:\n{education_list}\n"
                        else:
                            prompt += f"- Education Option - {key.title()}: Not available\n"

            # Add additional instructions to the prompt
            prompt += "\n\nPlease write the report in a formal and professional tone, using clear and concise language. Make sure to reference the student's specific data throughout the report, providing personalized advice and recommendations."

            # Generate the GPT response
            gpt_response = generate_gpt_response(prompt)

            response = {"success": True, "message": "GPT report generated successfully", "gpt_response": gpt_response}

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

