from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
import base64
from io import BytesIO
import seaborn as sns

import matplotlib.pyplot as plt
from django.http import JsonResponse

from django.shortcuts import render
import numpy as np




def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='users-register')


def index(request):
    return render(request, 'app/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

from .models import Profile

def profile(request):
    user = request.user
    # Ensure the user has a profile
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})







               

def Model_db(request):
    records = UserAssessment.objects.all().order_by('-created_at')
    return render(request, 'app/database.html', {'records': records})



def Basic_report(request):
    return render(request, 'app/Basic_report.html')


def Metircs_report(request):
    return render(request, 'app/Metrics_report.html')






from django.shortcuts import render
from django.http import JsonResponse
# import random
# import json
import numpy as np
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
#from .models import Response, models
from Chatbot.processor import chatbot_response
# Remove the comments to download additional nltk packages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def chatbot_response_view(request):
    if request.method == 'POST':
        the_question = request.POST.get('question', '')

        response = chatbot_response(the_question)
        print(response)

        return JsonResponse({"response": response})
    else:
        
        return JsonResponse({"message": "This endpoint only accepts POST requests."})
 



def logout_view(request):  
    auth_logout(request)
    return redirect('/')

import numpy as np
import joblib
from django.shortcuts import render
from .forms import SystemMonitorForm

# =========================
# LOAD MODEL & ENCODER
# =========================
ml_model = joblib.load('App/Model.pkl')
label_encoder = joblib.load('App/label_encoder.pkl')


def fault_prediction(request):

    if request.method == 'POST':
        form = SystemMonitorForm(request.POST)

        if form.is_valid():


            cpu_usage = form.cleaned_data['cpu_usage']
            cpu_load = form.cleaned_data['cpu_load_1min']
            memory_usage = form.cleaned_data['memory_usage']
            disk_usage = form.cleaned_data['disk_usage']
            disk_io = form.cleaned_data['disk_io']
            network_latency = form.cleaned_data['network_latency']
            packet_loss = form.cleaned_data['packet_loss']
            bandwidth_usage = form.cleaned_data['bandwidth_usage']
            response_time = form.cleaned_data['response_time']
            error_log_count = form.cleaned_data['error_log_count']
            warning_log_count = form.cleaned_data['warning_log_count']
            process_count = form.cleaned_data['process_count']
            system_temperature = form.cleaned_data['system_temperature']
            auth_failure_count = form.cleaned_data['auth_failure_count']
            service_restart_count = form.cleaned_data['service_restart_count']

            # =========================
            # PREPROCESS (VERY IMPORTANT)
            # =========================
            disk_io = np.log1p(disk_io)
            bandwidth_usage = np.log1p(bandwidth_usage)

            # =========================
            # FEATURE VECTOR
            # =========================
            features = np.array([[ 
                cpu_usage,
                cpu_load,
                memory_usage,
                disk_usage,
                disk_io,
                network_latency,
                packet_loss,
                bandwidth_usage,
                response_time,
                error_log_count,
                warning_log_count,
                process_count,
                system_temperature,
                auth_failure_count,
                service_restart_count
            ]])

            # =========================
            # PREDICTION
            # =========================
            pred_class = ml_model.predict(features)[0]

            # ✅ CORRECT DECODING
            failure_label = label_encoder.inverse_transform([pred_class])[0]

            # =========================
            # RECOMMENDATIONS
            # =========================
            recommendations = {

                "Normal": [
                    "The system is operating within acceptable performance limits with stable CPU, memory, and disk usage. "
                    "No abnormal patterns are detected in logs or response time. "
                    "Continue regular monitoring to ensure consistent system health.",

                    "All critical services are running without interruptions and network latency is minimal. "
                    "There are no signs of congestion, packet loss, or resource exhaustion. "
                    "Maintain current configurations and periodic system checks.",

                    "System temperature and hardware metrics remain within safe operating thresholds. "
                    "There are no warning indicators related to hardware or software instability. "
                    "Preventive maintenance schedules should be followed as planned.",

                    "Authentication attempts and security logs show normal behavior with no suspicious activity. "
                    "Access control policies are functioning correctly. "
                    "Continue enforcing standard security practices.",

                    "Overall system stability indicates optimal operational performance. "
                    "No immediate corrective actions are required at this time. "
                    "Historical data can be archived for trend analysis and future prediction improvements."
                ],

                "Network": [
                    "High network latency and packet loss indicate potential network congestion or routing issues. "
                    "Inspect network interfaces, switches, and routers for faults or misconfigurations. "
                    "Verify bandwidth allocation and traffic distribution.",

                    "Check for abnormal traffic patterns or sudden spikes in bandwidth usage. "
                    "Such behavior may be caused by misconfigured services or external network load. "
                    "Apply traffic shaping or quality-of-service (QoS) policies if necessary.",

                    "Review firewall rules and network security policies to ensure they are not blocking legitimate traffic. "
                    "Improper firewall configurations can significantly affect connectivity. "
                    "Update network rules where required.",

                    "Monitor DNS resolution time and gateway responsiveness for delays. "
                    "Slow name resolution or gateway failures can increase response times. "
                    "Ensure redundancy and failover mechanisms are properly configured.",

                    "Persistent network issues may lead to service outages and user dissatisfaction. "
                    "Proactive network diagnostics and continuous monitoring are recommended. "
                    "Escalate the issue to network administrators if the problem persists."
                ],

                "Hardware": [
                    "Elevated CPU usage and high system temperature suggest possible hardware stress or overload. "
                    "Inspect cooling systems such as fans and heat sinks for proper functioning. "
                    "Ensure adequate airflow in the system environment.",

                    "High disk usage or excessive disk I/O activity may indicate disk wear or storage bottlenecks. "
                    "Check disk health using SMART tools and monitor read/write performance. "
                    "Consider disk replacement or storage expansion if required.",

                    "Memory utilization near maximum limits can cause system instability and slowdowns. "
                    "Analyze running processes for memory leaks or inefficient resource usage. "
                    "Upgrade system memory if workload demands increase.",

                    "Frequent hardware warnings and restarts may signal impending hardware failure. "
                    "Backup critical data immediately to prevent data loss. "
                    "Schedule preventive hardware maintenance or component replacement.",

                    "Ignoring hardware issues can lead to unexpected system crashes and prolonged downtime. "
                    "Early detection allows timely corrective action and cost reduction. "
                    "Regular hardware health audits are strongly recommended."
                ],

                "Software": [
                    "Increased response time and frequent service restarts indicate software instability. "
                    "Review application logs to identify errors or unhandled exceptions. "
                    "Debug and patch faulty modules promptly.",

                    "A high number of error and warning logs suggest misconfigured or outdated software components. "
                    "Ensure that all applications and dependencies are updated to stable versions. "
                    "Perform regression testing after updates.",

                    "Memory leaks or inefficient resource usage can degrade application performance over time. "
                    "Profile running applications to identify performance bottlenecks. "
                    "Optimize code and resource handling mechanisms.",

                    "Service crashes may be caused by improper configuration files or incompatible library versions. "
                    "Validate configuration settings and environment variables. "
                    "Restore services using verified backup configurations.",

                    "Unresolved software issues can severely impact system reliability and user experience. "
                    "Adopt continuous integration and testing practices to minimize failures. "
                    "Maintain version control and rollback strategies."
                ],

                "Security": [
                    "A high number of authentication failures may indicate unauthorized access attempts. "
                    "Review authentication logs and identify suspicious IP addresses or user accounts. "
                    "Apply account lockout or CAPTCHA mechanisms if required.",

                    "Repeated security alerts suggest potential brute-force attacks or credential misuse. "
                    "Enforce strong password policies and multi-factor authentication (MFA). "
                    "Regularly update access credentials.",

                    "Analyze system access logs to detect unusual login patterns or privilege escalation attempts. "
                    "Ensure role-based access control is correctly enforced. "
                    "Remove unused or inactive user accounts.",

                    "Outdated software or unpatched systems may expose security vulnerabilities. "
                    "Apply security patches and updates without delay. "
                    "Conduct vulnerability assessments and penetration testing.",

                    "Security breaches can compromise sensitive data and system integrity. "
                    "Immediate investigation and incident response procedures should be initiated. "
                    "Maintain continuous security monitoring and audit trails."
                ]
                }


            recommendation_text = recommendations.get(
                failure_label, "No recommendation available."
            )

            # =========================
            # SAVE TO DATABASE
            # =========================
            instance = form.save(commit=False)
            instance.failure_type = failure_label
            instance.save()

            return render(request, 'app/output.html', {
            'result': failure_label,
            'recommendation_text': recommendation_text,  # LIST
            'system_id': instance.id                     # REQUIRED FOR TICKET
            })

    else:
        form = SystemMonitorForm()

    return render(request, 'app/deploy_fault.html', {'form': form})

import numpy as np
import joblib
import psutil
from django.shortcuts import render
from .models import SystemMonitor

# Load model and encoder
ml_model = joblib.load('App/Model.pkl')
label_encoder = joblib.load('App/label_encoder.pkl')


def real_time_fault_prediction(request):

    context = {}

    # =========================
    # STEP 1: LOAD REAL DATA
    # =========================
    if request.method == 'POST' and 'load_data' in request.POST:

        cpu_usage = psutil.cpu_percent(interval=1)

        try:
            cpu_load = psutil.getloadavg()[0]
        except:
            cpu_load = 0.5

        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        disk_io = psutil.disk_io_counters().read_bytes + \
                  psutil.disk_io_counters().write_bytes

        net = psutil.net_io_counters()
        bandwidth_usage = net.bytes_sent + net.bytes_recv

        data = {
            'cpu_usage': round(cpu_usage, 2),
            'cpu_load_1min': round(cpu_load, 2),
            'memory_usage': round(memory_usage, 2),
            'disk_usage': round(disk_usage, 2),
            'disk_io': round(np.log1p(disk_io), 2),
            'network_latency': 10,
            'packet_loss': 0.0,
            'bandwidth_usage': round(np.log1p(bandwidth_usage), 2),
            'response_time': 50,
            'error_log_count': 0,
            'warning_log_count': 0,
            'process_count': len(psutil.pids()),
            'system_temperature': 40,
            'auth_failure_count': 0,
            'service_restart_count': 0
        }

        context['loaded'] = True
        context['data'] = data

        return render(request, 'app/real_time_form.html', context)

    # =========================
    # STEP 2: PREDICT
    # =========================
    if request.method == 'POST' and 'predict' in request.POST:

        # Read USER-EDITED values
        data = {
            key: float(request.POST.get(key))
            for key in [
                'cpu_usage', 'cpu_load_1min', 'memory_usage',
                'disk_usage', 'disk_io', 'network_latency',
                'packet_loss', 'bandwidth_usage', 'response_time',
                'error_log_count', 'warning_log_count', 'process_count',
                'system_temperature', 'auth_failure_count',
                'service_restart_count'
            ]
        }

        features = np.array([list(data.values())])

        pred = ml_model.predict(features)[0]
        failure_label = label_encoder.inverse_transform([pred])[0]

        recommendations = {

                "Normal": [
                    "The system is operating within acceptable performance limits with stable CPU, memory, and disk usage. "
                    "No abnormal patterns are detected in logs or response time. "
                    "Continue regular monitoring to ensure consistent system health.",

                    "All critical services are running without interruptions and network latency is minimal. "
                    "There are no signs of congestion, packet loss, or resource exhaustion. "
                    "Maintain current configurations and periodic system checks.",

                    "System temperature and hardware metrics remain within safe operating thresholds. "
                    "There are no warning indicators related to hardware or software instability. "
                    "Preventive maintenance schedules should be followed as planned.",

                    "Authentication attempts and security logs show normal behavior with no suspicious activity. "
                    "Access control policies are functioning correctly. "
                    "Continue enforcing standard security practices.",

                    "Overall system stability indicates optimal operational performance. "
                    "No immediate corrective actions are required at this time. "
                    "Historical data can be archived for trend analysis and future prediction improvements."
                ],

                "Network": [
                    "High network latency and packet loss indicate potential network congestion or routing issues. "
                    "Inspect network interfaces, switches, and routers for faults or misconfigurations. "
                    "Verify bandwidth allocation and traffic distribution.",

                    "Check for abnormal traffic patterns or sudden spikes in bandwidth usage. "
                    "Such behavior may be caused by misconfigured services or external network load. "
                    "Apply traffic shaping or quality-of-service (QoS) policies if necessary.",

                    "Review firewall rules and network security policies to ensure they are not blocking legitimate traffic. "
                    "Improper firewall configurations can significantly affect connectivity. "
                    "Update network rules where required.",

                    "Monitor DNS resolution time and gateway responsiveness for delays. "
                    "Slow name resolution or gateway failures can increase response times. "
                    "Ensure redundancy and failover mechanisms are properly configured.",

                    "Persistent network issues may lead to service outages and user dissatisfaction. "
                    "Proactive network diagnostics and continuous monitoring are recommended. "
                    "Escalate the issue to network administrators if the problem persists."
                ],

                "Hardware": [
                    "Elevated CPU usage and high system temperature suggest possible hardware stress or overload. "
                    "Inspect cooling systems such as fans and heat sinks for proper functioning. "
                    "Ensure adequate airflow in the system environment.",

                    "High disk usage or excessive disk I/O activity may indicate disk wear or storage bottlenecks. "
                    "Check disk health using SMART tools and monitor read/write performance. "
                    "Consider disk replacement or storage expansion if required.",

                    "Memory utilization near maximum limits can cause system instability and slowdowns. "
                    "Analyze running processes for memory leaks or inefficient resource usage. "
                    "Upgrade system memory if workload demands increase.",

                    "Frequent hardware warnings and restarts may signal impending hardware failure. "
                    "Backup critical data immediately to prevent data loss. "
                    "Schedule preventive hardware maintenance or component replacement.",

                    "Ignoring hardware issues can lead to unexpected system crashes and prolonged downtime. "
                    "Early detection allows timely corrective action and cost reduction. "
                    "Regular hardware health audits are strongly recommended."
                ],

                "Software": [
                    "Increased response time and frequent service restarts indicate software instability. "
                    "Review application logs to identify errors or unhandled exceptions. "
                    "Debug and patch faulty modules promptly.",

                    "A high number of error and warning logs suggest misconfigured or outdated software components. "
                    "Ensure that all applications and dependencies are updated to stable versions. "
                    "Perform regression testing after updates.",

                    "Memory leaks or inefficient resource usage can degrade application performance over time. "
                    "Profile running applications to identify performance bottlenecks. "
                    "Optimize code and resource handling mechanisms.",

                    "Service crashes may be caused by improper configuration files or incompatible library versions. "
                    "Validate configuration settings and environment variables. "
                    "Restore services using verified backup configurations.",

                    "Unresolved software issues can severely impact system reliability and user experience. "
                    "Adopt continuous integration and testing practices to minimize failures. "
                    "Maintain version control and rollback strategies."
                ],

                "Security": [
                    "A high number of authentication failures may indicate unauthorized access attempts. "
                    "Review authentication logs and identify suspicious IP addresses or user accounts. "
                    "Apply account lockout or CAPTCHA mechanisms if required.",

                    "Repeated security alerts suggest potential brute-force attacks or credential misuse. "
                    "Enforce strong password policies and multi-factor authentication (MFA). "
                    "Regularly update access credentials.",

                    "Analyze system access logs to detect unusual login patterns or privilege escalation attempts. "
                    "Ensure role-based access control is correctly enforced. "
                    "Remove unused or inactive user accounts.",

                    "Outdated software or unpatched systems may expose security vulnerabilities. "
                    "Apply security patches and updates without delay. "
                    "Conduct vulnerability assessments and penetration testing.",

                    "Security breaches can compromise sensitive data and system integrity. "
                    "Immediate investigation and incident response procedures should be initiated. "
                    "Maintain continuous security monitoring and audit trails."
                ]
                }

        instance = SystemMonitor.objects.create(**data, failure_type=failure_label)

        return render(request, 'app/output.html', {
            'result': failure_label,
            'recommendation_text': recommendations.get(failure_label),
            'system_id': instance.id
        })
    return render(request, 'app/real_time_form.html')


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ticket, SystemMonitor

@login_required
def raise_ticket(request, system_id):
    system_monitor = get_object_or_404(SystemMonitor, id=system_id)

    if request.method == 'POST':
        Ticket.objects.create(
            system_monitor=system_monitor,
            raised_by=request.user,   # ✅ FIXED

            cpu_usage=system_monitor.cpu_usage,
            cpu_load_1min=system_monitor.cpu_load_1min,
            memory_usage=system_monitor.memory_usage,
            disk_usage=system_monitor.disk_usage,
            disk_io=system_monitor.disk_io,
            network_latency=system_monitor.network_latency,
            packet_loss=system_monitor.packet_loss,
            bandwidth_usage=system_monitor.bandwidth_usage,
            response_time=system_monitor.response_time,
            error_log_count=system_monitor.error_log_count,
            warning_log_count=system_monitor.warning_log_count,
            process_count=system_monitor.process_count,
            system_temperature=system_monitor.system_temperature,
            auth_failure_count=system_monitor.auth_failure_count,
            service_restart_count=system_monitor.service_restart_count,
            failure_type=system_monitor.failure_type
        )

        messages.success(request, "Ticket raised successfully!")
        return redirect('user-tickets')

    return render(request, 'app/raise_ticket.html', {'system': system_monitor})



# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket

from django.shortcuts import render, get_object_or_404
from .models import Ticket

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    return render(request, 'app/ticket_detail.html', {
        'ticket': ticket
    })






# views.py
# views.py
from django.contrib.auth.decorators import login_required

@login_required
def user_tickets(request):
    tickets = Ticket.objects.filter(
        raised_by=request.user
    ).order_by('-created_at')

    return render(request, 'app/user_tickets.html', {
        'tickets': tickets
    })























































from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminUser
from .forms import AdminRegisterForm, AdminLoginForm

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            # Save new admin
            admin_user = form.save(commit=False)
            admin_user.password = form.cleaned_data['password']
            admin_user.save()
            messages.success(request, "Admin account created successfully.")
            return redirect('admin-login')
    else:
        form = AdminRegisterForm()
    return render(request, 'admin_templates/admin_register.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                admin_user = AdminUser.objects.get(username=username, password=password)
                request.session['admin_user_id'] = admin_user.id
                
                return redirect('admin-dashboard')
            except AdminUser.DoesNotExist:
                messages.error(request, "Invalid username or password.")
    else:
        form = AdminLoginForm()
    return render(request, 'admin_templates/admin_login.html', {'form': form})


def admin_logout(request):
    if 'admin_user_id' in request.session:
        del request.session['admin_user_id']
    messages.success(request, "Admin logged out successfully.")
    return redirect('admin-login')




from .models import Ticket

def admin_dashboard(request):
    if 'admin_user_id' not in request.session:
        return redirect('admin-login')

    tickets = Ticket.objects.all().order_by('-created_at')
    return render(request, 'admin_templates/admin_dashboard.html', {
        'tickets': tickets
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Ticket
from .utils.gemini import generate_gemini_analysis


def admin_analyze_ticket(request, ticket_id):
    """
    Admin-only page to run Gemini analysis on a ticket.
    Uses custom admin login via session.
    """

    # 🔐 Check admin session
    if not request.session.get('admin_user_id'):
        messages.error(request, "Admin login required")
        return redirect('admin-login')

    ticket = get_object_or_404(Ticket, id=ticket_id)

    # 🧠 Run Gemini only when admin clicks button
    if request.method == 'POST':
        if not ticket.ai_analysis:
            try:
                messages.info(request, "Running Gemini AI analysis...")
                ticket.ai_analysis = generate_gemini_analysis(ticket)
                ticket.save()
                messages.success(request, "AI analysis completed successfully.")
            except Exception as e:
                messages.error(request, f"Gemini failed: {str(e)}")
        else:
            messages.info(request, "AI analysis already exists.")

        return redirect('admin-analyze-ticket', ticket_id=ticket.id)

    return render(request, 'admin_templates/admin_ticket_detail.html', {
        'ticket': ticket
    })




def admin_developer_list(request):
    if not request.session.get('admin_user_id'):
        return redirect('admin-login')
    developers = SeniorDeveloper.objects.all()
    return render(request, 'admin_templates/admin_developer_list.html', {'developers': developers})



from .models import SeniorDeveloper, DeveloperDocument
from django.shortcuts import render, redirect
from django.contrib import messages
def admin_add_developer(request):
    if not request.session.get('admin_user_id'):
        return redirect('admin-login')

    if request.method == 'POST':
        SeniorDeveloper.objects.create(
            name=request.POST['name'],
            experience_years=request.POST['experience'],
            expertise=request.POST['expertise']
        )
        messages.success(request, "Senior Developer added")
        return redirect('admin-dashboard')

    return render(request, 'admin_templates/add_developer.html')
def admin_upload_document(request, dev_id):
    if not request.session.get('admin_user_id'):
        return redirect('admin-login')

    developer = SeniorDeveloper.objects.get(id=dev_id)

    if request.method == 'POST':
        DeveloperDocument.objects.create(
            developer=developer,
            title=request.POST['title'],
            document=request.FILES['document']
        )
        messages.success(request, "Document uploaded")
        return redirect('admin-dashboard')

    return render(request, 'admin_templates/upload_document.html', {
        'developer': developer
    })




def senior_developers(request):
    developers = SeniorDeveloper.objects.all()
    return render(request, 'app/senior_developers.html', {
        'developers': developers
    })
def developer_documents(request, dev_id):
    developer = SeniorDeveloper.objects.get(id=dev_id)
    return render(request, 'app/developer_documents.html', {
        'developer': developer
    })
from .models import DeveloperDocument, DocumentQuestion
from .utils.gemini_doc import ask_gemini_from_doc

def ask_document_question(request, doc_id):
    document = DeveloperDocument.objects.get(id=doc_id)

    if request.method == 'POST':
        question = request.POST['question']

        answer = ask_gemini_from_doc(
            document.document.path,
            question
        )

        DocumentQuestion.objects.create(
            document=document,
            question=question,
            answer=answer
        )

        return render(request, 'app/document_qa.html', {
            'document': document,
            'question': question,
            'answer': answer
        })

    return render(request, 'app/document_qa.html', {
        'document': document
    })

















