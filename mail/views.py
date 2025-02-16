from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
from .forms import SendMailsForm
import openpyxl
from django.core.mail import EmailMessage, get_connection
from django.core.mail import send_mail
from django.conf import settings
import mimetypes


# @login_required
def home(request):
    return render(request, 'home.html')

# @login_required
def send_mails(request):
    if request.method == 'POST':
        form = SendMailsForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            excel_file = request.FILES['excel_file']
            
            # Process Excel file
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            emails = [cell.value for cell in sheet['A'][1:] if cell.value]  # Assuming emails are in column A
            
            # Prepare attachments
            attachment = request.FILES.getlist('attachments')

            # Send emails with attachments securely
            # Establish custom SMTP connection for the desired sender
            connection = get_connection(
                username=request.user.sender_email,
                password=request.user.key,
                fail_silently=False
            )

            # Send emails with attachments securely
            for email in emails:
                mail = EmailMessage(
                    subject,
                    message,
                    request.user.sender_email,
                    [email],
                    connection=connection,
                    headers={'X-Mailer': 'Django'}
                )

                # Attach files securely with proper MIME types
                if attachment:
                    mime_type, _ = mimetypes.guess_type(attachment.name)
                    if not mime_type:
                        mime_type = 'application/octet-stream'
                    mail.attach(attachment.name, attachment.read(), mime_type)

                mail.send(fail_silently=False)
            
            return redirect('home')
    else:
        form = SendMailsForm()
    return render(request, 'send_mails.html', {'form': form})