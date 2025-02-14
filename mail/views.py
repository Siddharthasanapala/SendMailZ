from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
from .forms import SendMailsForm
import openpyxl
from django.core.mail import send_mail
from django.conf import settings

# @login_required
def home(request):
    return render(request, 'home.html')

# @login_required
def send_mails(request):
    if request.method == 'POST':
        form = SendMailsForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.cleaned_data['message']
            excel_file = request.FILES['excel_file']
            
            # Process Excel file
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            emails = [cell.value for cell in sheet['A'][1:] if cell.value]  # Assuming emails are in column A
            
            # Send emails
            for email in emails:
                send_mail(
                    'Subject',
                    message,
                    request.user.sender_email,
                    [email],
                    auth_user=request.user.sender_email,
                    auth_password=request.user.key,
                    fail_silently=False,
                )
            
            return redirect('home')
    else:
        form = SendMailsForm()
    return render(request, 'send_mails.html', {'form': form})