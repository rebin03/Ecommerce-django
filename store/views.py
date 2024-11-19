from django.shortcuts import render
from django.views.generic import View
from store.forms import SignUpForm
from django.core.mail import send_mail

# Create your views here.

def send_otp_email(user):
    
    user.generate_otp()
    subject = 'Verify your email'
    message = f'OTP for account verification is {user.otp}'
    from_email = 'iamrbn03@gmail.com'
    to_email = [user.email]
    
    send_mail(subject, message, from_email, to_email)
    

class SignUpView(View):
    
    template_name = 'register.html'
    form_class = SignUpForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            user_obj = form.save(commit=False)
            user_obj.is_active = False
            
            user_obj.save()
            
            send_otp_email(user_obj)

            pass