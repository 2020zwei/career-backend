import os

from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML

from calculator.models import UserPoints
from choices.models import Level5, Level6, Level8, Apprentice
from cv.models import Skills, Experience, Interests, CV, Qualities
from goals.models import Goal
from psychometric.models import TestResult, TestResultDetail, PsychometricTest
from users.models import Student
from .utils import generate_gpt_response


def serialize_students_data(instance):
	return model_to_dict(instance)


class GuidanceReportModels(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		try:
			models = {
				"main_models": ["predicted points and subjects", "my studied goals", "multiple intelligence score",
								"values assessment", "interest assessment"],
				"cv_models": ["address", "personal statement", "work experience", "skills", "qualities",
							  "interests", ],
				"education_models": ["level 8", "level 6/7", "level 5(plc)", "apprentices", ]}
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

			print("prompt: ", prompt)  # Education Options
			education_mappings = {"level 8": Level8.objects.filter(student=student).first(),
								  "level 6/7": Level6.objects.filter(student=student).first(),
								  "level 5(plc)": Level5.objects.filter(student=student).first(),
								  "apprentices": Apprentice.objects.filter(student=student).first()}

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
			report_template = str(user_obj.first_name) + "-" + str(
				user_obj.last_name) + "-" + "guidance_report" + ".html"
			full_name = user_obj.full_name

			executive_summary = ("A brief overview of the entire report, summarizing the key findings and "
								 "recommendations based on your self-assessment and career goals. It highlights the "
								 "main points that will be discussed in the following sections.")
			self_assessment_result = ("A brief overview of the entire report, summarizing the key findings and "
									  "recommendations based on your self-assessment and career goals. It highlights "
									  "the main points that will be discussed in the following sections.")
			study_advice = ("Tailored recommendations on study <b>habits, strategies, and academic</b> planning based "
							"on your self-assessment results. This may include advice on study techniques, "
							"time management, and areas to focus on.")
			academic_record = ("A summary of your academic history, including grades, courses taken, and any relevant "
							   "academic achievements. It may also include an analysis of your performance trends "
							   "over time.")
			career_assessment = ("An evaluation of potential career paths based on your self-assessment results, "
								 "interests, and academic record. It may include suggested careers, job roles, "
								 "and industries that align with your profile.")

			context = {"first_name": user_obj.first_name, "last_name": user_obj.last_name,
					   "executive_summary": executive_summary, "self_assessment_result": self_assessment_result,
					   "study_advice": study_advice, "academic_record": academic_record,
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
			return Response({'message': "All steps of Guidance Report should be completed . " + str(e)},
							status=status.HTTP_400_BAD_REQUEST)


class GenerateGuidanceReportGPT(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		user = request.user
		try:
			# Fetch the student record
			try:
				student = Student.objects.get(user=user)
			except Student.DoesNotExist:
				return Response({"success": False, "message": "Student record not found."}, status=404)

			# Fetch the CV record for the student
			try:
				cv = CV.objects.get(user=student)
			except CV.DoesNotExist:
				cv = None

			# Gather Personal Information
			personal_info = {"first_name": student.first_name or "Not provided",
							 "last_name": student.last_name or "Not provided",
							 "full_name": student.full_name or "Not provided",
							 "city": cv.city if cv else "Not provided", "county": cv.town if cv else "Not provided",
							 "eircode": cv.eircode if cv else "Not provided",
							 "school": student.school or "Not provided", }

			# Parse request body
			data = request.data
			feedback = data.get("feedback", None)
			previous_response = data.get("previous_response", None)

			# Helper function to structure test results
			def structure_test_results(test_name):
				test_obj = PsychometricTest.objects.filter(name__iexact=test_name).first()
				if not test_obj:
					return None
				test_result = TestResult.objects.filter(user=student, test=test_obj).first()
				if not test_result:
					return None
				question_scores = TestResultDetail.objects.filter(result=test_result).values("question__type__type",
																							 "answer__weightage")
				breakdown = {}
				for detail in question_scores:
					question_type = detail["question__type__type"]
					weightage = detail["answer__weightage"]
					breakdown[question_type] = breakdown.get(question_type, 0) + weightage
				return {"score": test_result.score, "total_score": sum(breakdown.values()),
						"details": [{"category": question_type, "score": score} for question_type, score in
									breakdown.items()], }

			# Gather Self-Assessment Results
			assessment_results = {}
			if data.get("mis") == "Yes":
				assessment_results["multiple_intelligence"] = structure_test_results("Multiple Intelligence")
			if data.get("values_assessment") == "Yes":
				assessment_results["values"] = structure_test_results("Occupational Values Assesment")
			if data.get("interest_assessment") == "Yes":
				assessment_results["interest"] = structure_test_results("Occupational Interest Assesment")

			# Gather CV Data
			cv_data = {}
			if cv:
				if data.get("personal_statement") == "Yes":
					cv_data["personal_statement"] = cv.objective or "Not provided"
				if data.get("work_experience") == "Yes":
					cv_data["work_experience"] = list(
						Experience.objects.filter(user=student).values("job_title", "company", "city", "country",
																	   "description", "startdate", "enddate",
																	   "is_current_work"))
				if data.get("skills") == "Yes":
					cv_data["skills"] = list(Skills.objects.filter(user=student).values_list("description", flat=True))
				if data.get("interest") == "Yes":
					cv_data["interests"] = list(
						Interests.objects.filter(user=student).values_list("interests", flat=True))
					cv_data["qualities"] = list(
						Qualities.objects.filter(user=student).values_list("description", flat=True))

			# Gather Predicted Points and Subjects
			predicted_points = None
			if data.get("predicted_points_and_subjects") == "Yes":
				user_points = UserPoints.objects.filter(user=student).first()
				if user_points:
					predicted_points = {"total_points": user_points.total_points,
										"grades": list(user_points.grades.values("subject__name", "grade", "point")), }

			# Gather Goals
			goals = None
			if data.get("my_stated_goals") == "Yes":
				goals = list(Goal.objects.filter(user=student).values("proffession", "goal", "description",
																	  "realistic",
																	  "countdown"))

			# Gather Education Options
			education_options = {}
			if data.get("education_options"):
				options = data.get("education_options")
				if "level 5(plc)" in options:
					education_options["level_5"] = list(Level5.objects.filter(choice__user=student).values())
				if "level 6/7" in options:
					education_options["level_6_7"] = list(Level6.objects.filter(choice__user=student).values())
				if "level 8" in options:
					education_options["level_8"] = list(Level8.objects.filter(choice__user=student).values())
				if "apprenticeship" in options:
					education_options["apprenticeship"] = list(Apprentice.objects.filter(
						choice__user=student).values())

			# Example arrays of scores and their ranges (adjust these arrays to reflect actual data you have)
			multiple_intelligence_scores = [{"category": "Interpersonal", "score": 32, "out_of": 40},
											{"category": "Visual/Spatial", "score": 30, "out_of": 40},
											{"category": "Body/Kinesthetic", "score": 28, "out_of": 40},
											{"category": "Intrapersonal", "score": 27, "out_of": 40},
											{"category": "Logical/Mathematical", "score": 27, "out_of": 40},
											{"category": "Musical", "score": 24, "out_of": 40},
											{"category": "Existential", "score": 22, "out_of": 40},
											{"category": "Verbal/Linguistic", "score": 22, "out_of": 40},
											{"category": "Naturalistic", "score": 16, "out_of": 40}, ]

			occupational_interest_scores = [{"category": "Artistic/Creative", "score": 35, "out_of": 70},
											{"category": "Social", "score": 34, "out_of": 70},
											{"category": "Understanding/Investigative", "score": 32, "out_of": 70},
											{"category": "Clerical/Organisational", "score": 31, "out_of": 70},
											{"category": "Manual/Practical", "score": 21, "out_of": 70},
											{"category": "Influencing/Persuasive", "score": 18, "out_of": 70}, ]

			occupational_values_scores = [{"category": "Status", "score": 20, "out_of": 28},
										  {"category": "Security", "score": 18, "out_of": 28},
										  {"category": "Creativity", "score": 16, "out_of": 28},
										  {"category": "Autonomy", "score": 12, "out_of": 28},
										  {"category": "People", "score": 12, "out_of": 28},
										  {"category": "Variety", "score": 9, "out_of": 28}, ]

			# Example CAO or grading data
			# English H1, Accounting H2, Biology H1, Chemistry H2, Irish O3, Maths H2
			# H1=90-100%, H2=80-89%, O3=70-79% (Easier level)
			subject_grades = [{"subject": "English", "grade": "H1", "range": "90%-100%"},
							  {"subject": "Accounting", "grade": "H2", "range": "80%-89%"},
							  {"subject": "Biology", "grade": "H1", "range": "90%-100%"},
							  {"subject": "Chemistry", "grade": "H2", "range": "80%-89%"},
							  {"subject": "Irish", "grade": "O3", "range": "70%-79% (Ordinary Level)"},
							  {"subject": "Maths", "grade": "H2", "range": "80%-89%"}, ]

			# Combine all gathered data
			response_data = {"personal_info": personal_info, "self_assessment_results": assessment_results,
							 "cv_data": cv_data, "predicted_points": predicted_points, "goals": goals,
							 "education_options": education_options, }

			# Construct an enhanced prompt
			# We instruct GPT to improve upon the previous_response if provided, and incorporate user feedback if
			# given.
			# We also provide the arrays and ask GPT to use them creatively to build a better final HTML report.
			prompt = f"""
			You are an expert career guidance counselor and professional HTML designer. You have access to the user's data, previous report version, and feedback. Your task is to produce a final HTML report following a strict predefined structure.

			DO NOT:
			- Use Markdown formatting or code fences (no ```).
			- Include triple backticks anywhere in the output.

			Your final output must ONLY be valid HTML as described below.

			***********************
			REPORT FORMAT AND REQUIREMENTS
			***********************
			The final output MUST be a valid, standalone HTML document, structured as follows:

			<html>
			  <head>
			    <title>Career Guidance Report</title>
			    <style>
			      /* Include styling here, such as fonts, colors, layout.
			         Use clean, readable fonts.
			         Include headings, subtle color accents, and spacing for readability.
			         Use CSS selectors to style tables, headings, and lists.
			      */
			    </style>
			  </head>
			  <body>
			    <header>
			      <h1>Career Guidance Report</h1>
			      <h2>Student Name: [Replace with Student's Full Name]</h2>
			    </header>

			    <section id="introduction">
			      <h3>1. Introduction</h3>
			      <p>[Provide a brief introduction, referencing the student's approximate age or educational stage and the purpose of the report.]</p>
			    </section>

			    <section id="self-assessment">
			      <h3>2. Self-Assessment Results</h3>
			      <h4>2.1 Multiple Intelligence Scores</h4>
			      <table>
			        <!-- Display multiple intelligence scores in a table -->
			      </table>
			      <h4>2.2 Occupational Interest Scores</h4>
			      <table>
			        <!-- Display occupational interest scores here -->
			      </table>
			      <h4>2.3 Occupational Values Scores</h4>
			      <table>
			        <!-- Display occupational values scores here -->
			      </table>
			      <h4>2.4 Top Skills & Qualities</h4>
			      <ul>
			        <!-- Highlight top three skills & qualities from CV data -->
			      </ul>
			      <p>[Discuss what these scores mean, interpret them meaningfully, and suggest 5 possible careers compatible with these results.]</p>
			    </section>

			    <section id="study-advice">
			      <h3>3. Suggested Study Techniques and Advice</h3>
			      <p>[Tailor advice based on the multiple intelligence strengths. Provide practical, actionable study tips.]</p>
			    </section>

			    <section id="academic-achievement">
			      <h3>4. Academic Achievement</h3>
			      <table>
			        <!-- Show subject grades and corresponding percentages -->
			      </table>
			      <p>[Discuss the student's strongest subjects and suggest areas of study or courses that align with them.]</p>
			    </section>

			    <section id="career-exploration">
			      <h3>5. Career Exploration</h3>
			      <p>[Provide practical steps for exploring suggested careers: shadowing, volunteering, online research, etc.]</p>
			    </section>

			    <section id="goals">
			      <h3>6. Student's Goals</h3>
			      <h4>6.1 Short-Term Goals (3 months)</h4>
			      <ul>
			        <!-- List short-term goals and suggestions to achieve them -->
			      </ul>
			      <h4>6.2 Long-Term Goals (1 year)</h4>
			      <ul>
			        <!-- List long-term goals and suggestions to achieve them -->
			      </ul>
			    </section>

			    <section id="education-options">
			      <h3>7. Compatible Courses and Opportunities</h3>
			      <h4>7.1 QQI Level 5 (PLC) Options</h4>
			      <ul>
			        <!-- List relevant Level 5 courses if available -->
			      </ul>
			      <h4>7.2 Level 6/7 Courses</h4>
			      <ul>
			        <!-- List relevant Level 6/7 courses if available -->
			      </ul>
			      <h4>7.3 Level 8 Courses</h4>
			      <ul>
			        <!-- List relevant Level 8 courses if available -->
			      </ul>
			      <h4>7.4 Apprenticeships</h4>
			      <ul>
			        <!-- List apprenticeships if available -->
			      </ul>
			      <p>[Suggest non-education activities as well if data is sparse.]</p>
			    </section>

			    <section id="conclusion">
			      <h3>8. Conclusion</h3>
			      <p>[Summarize the student's strengths, reassure them, and encourage next steps. Reference any feedback or improvements from the previous response and user feedback. The conclusion should be positive and forward-looking.]</p>
			    </section>

			  </body>
			</html>

			***********************
			ADDITIONAL INSTRUCTIONS
			***********************
			- Incorporate the user's feedback: "{feedback}" and improve upon the "previous_response" by enhancing layout, color usage, and adding more depth and clarity.
			- Use the arrays of scores and grading data provided to populate the tables and interpretations.
			- The data you have available:
			  Personal Info: {response_data['personal_info']}
			  Self-Assessment Results: {response_data['self_assessment_results']}
			  CV Data: {response_data['cv_data']}
			  Goals: {response_data['goals']}
			  Predicted Points: {response_data['predicted_points']}
			  Education Options: {response_data['education_options']}

			Scoring & Grading Data:
			Multiple Intelligence Scores:
			{multiple_intelligence_scores}

			Occupational Interest Scores:
			{occupational_interest_scores}

			Occupational Values Scores:
			{occupational_values_scores}

			Subject Grades (with percentage ranges):
			{subject_grades}

			- DO NOT include triple backticks.
			- DO NOT use Markdown code fences.
			- Only produce the final HTML as the output.
			- Do not add any styling or CSS to the HTML. Only include the structure and content.
			"""

			# Generate the GPT response using your existing GPT configuration
			gpt_response = generate_gpt_response(prompt)

			return Response({"success": True, "message": gpt_response}, status=200)

		except Exception as e:
			return Response({"success": False, "message": str(e)}, status=400)
