from django.core.mail import EmailMessage
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from school_managment.mixin import RedirectAuthenticatedUserMixin
from django.views.generic import FormView, TemplateView, View, ListView, CreateView, UpdateView, DeleteView

from django.conf import settings
from .forms import UserRegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm,UpdateUserForm,ProfileUpdateForm, CreateUserForm,StudentForm
from .forms import UpdateLibraryHistoryForm, FeeHistoryUpdateForm, AddBookForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser, LibraryHistory,Profile, Student,FeesHistory,Library
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .token import custom_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class UserRegistrationView(RedirectAuthenticatedUserMixin,FormView):
    template_name = 'accounts/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy("accounts:home")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        
        # Perform Login Function
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            messages.success(
                self.request,
                f"Account created successfully for {user.first_name} {user.last_name}! You are now logged in.",
            )
            return redirect(self.success_url)
        else:
            messages.error(self.request, "Failed to log in after registration. Please try logging in manually.")
            return redirect("accounts:login")
        

class UserLoginView(RedirectAuthenticatedUserMixin, View):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("accounts:home")

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.first_name} {user.last_name}! You have successfully logged in.')
                next_url = request.GET.get('next', self.success_url)
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        return render(request, self.template_name, {'form': form})
    

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect(reverse('accounts:login'))
    


# Forgot Password
class ForgotPasswordView(RedirectAuthenticatedUserMixin, View):
    template_name = 'accounts/forgot_password.html'
    success_template_name = 'accounts/emailsendpage.html'
    form_class = ForgotPasswordForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = None
            
            if user is not None:
                current_site = get_current_site(request)
                mail_subject = 'Reset Your Password'
                message = render_to_string('accounts/reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': custom_token_generator.make_token(user),
                })

                send_email = EmailMessage(mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
                send_email.content_subtype = 'html'
                send_email.send()
                
                context = {
                    'email': email,
                }
                return render(request, self.success_template_name, context)
            else:
                messages.error(request, 'Account does not exist.')
                return redirect('accounts:forgot-password')
        else:
            return render(request, self.template_name, {'form': form})
        


# Reset Password   
class ResetPasswordView(RedirectAuthenticatedUserMixin, View):
    template_name = "accounts/reset_password.html"
    form_class = ResetPasswordForm
    
    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return None
    
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        
        if user is not None and custom_token_generator.check_token(user, token):
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('user:login')
    
    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        
        if user is not None and custom_token_generator.check_token(user, token):
            form = self.form_class(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']

                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password reset successful. Please login with your new password.')
                    return redirect('user:login')
                else:
                    messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('accounts:login')


# Profile View
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_view.html'

    def get_context_data(self, **kwargs):
        profile = Profile.objects.get_or_create(user=self.request.user)
        profile = Profile.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs) 
        context['profile'] = profile  
        return context


# Profile Update
class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'accounts/profile_update.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)


        user_form = UpdateUserForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse_lazy('accounts:profile_view'))  

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile
        }
        return render(request, self.template_name, context)



    



# Role-Based Dashboard View
# class DashboardView(LoginRequiredMixin, TemplateView):
#     template_name = 'dashboard/admin_dashboard.html'


class RoleRequiredMixn(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        user = self.request.user
        return user.is_superuser or (hasattr(user, 'role') and user.role in self.allowed_roles)
    
    def handle_no_permission(self):
        return redirect('accounts:login')
    

class StudentListView(RoleRequiredMixn ,LoginRequiredMixin, ListView):
    model = Student
    template_name = 'accounts/students_list.html'

    context_object_name = 'students'
    allowed_roles = ['admin', 'staff']

    def get_queryset(self):
        return Student.objects.all()
    

class AddStudentsView(RoleRequiredMixn, CreateView):
    model=Student
    form_class=StudentForm
    template_name='accounts/student/student_create.html'
    success_url=reverse_lazy('accounts:student_list')
    allowed_roles=['admin']
    


class UpdateStudentView(RoleRequiredMixn, UpdateView):
    model=Student
    form_class=StudentForm
    template_name='accounts/student/student_update.html'
    success_url=reverse_lazy('accounts:student_list')
    allowed_roles=['admin']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.get_object()  
        return context
    

class DeleteStudentsView(RoleRequiredMixn, DeleteView):
    model = Student
    template_name = 'accounts/student.html'  
    success_url = reverse_lazy('accounts:student_list')  
    allowed_roles=['admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_to_delete'] = self.object
        return context



class CreateUserView(RoleRequiredMixn, CreateView):
    model = CustomUser
    form_class = CreateUserForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('admin_dash')



class AdminDashboardView(RoleRequiredMixn, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'
    allowed_roles = ['admin']

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        context['students'] = Student.objects.all()
        return context
    

class UserProfileView(RoleRequiredMixn, TemplateView):
    template_name = 'accounts/user_profileview.html'
    allowed_roles = ['admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs['id'])
        profile = Profile.objects.get_or_create(user=user)
        context['user_profile'] = user
        context['profile'] = profile
        return context
    

class AddUserView(RoleRequiredMixn, CreateView):
    model = CustomUser
    form_class = CreateUserForm
    template_name ='accounts/usercreation.html'
    success_url = reverse_lazy('accounts:admin_dashboard')
    allowed_roles = ['admin']



class UpdateUserView(RoleRequiredMixn, UpdateView):
    model = CustomUser
    form_class = UpdateUserForm
    template_name = 'accounts/updateuser.html'
    success_url = reverse_lazy('accounts:admin_dashboard')
    context_object_name = 'user'
    allowed_roles = ['admin']

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context



class DeleteUserView(RoleRequiredMixn, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('accounts:admin_dashboard') 
    template_name = 'accounts/admin_dashboard.html'
    allowed_roles=['admin'] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_to_delete'] = self.object
        return context
    



class LibraryHistoryView(RoleRequiredMixn, TemplateView):
    template_name = "accounts/library/library_details.html"
    allowed_roles = ['admin','librarian']
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["library_data"] = LibraryHistory.objects.all() 
        return context



class AddLibraryRecord(RoleRequiredMixn, CreateView):
    model=LibraryHistory
    form_class=UpdateLibraryHistoryForm
    template_name='accounts/library/add_libraryhistory.html'
    success_url=reverse_lazy('accounts:libraryhistory')
    allowed_roles=['admin','librarian']



class UpdateLibraryHistory(RoleRequiredMixn, UpdateView):

    model=LibraryHistory
    form_class=UpdateLibraryHistoryForm
    template_name='accounts/library/update_libraryhistory.html'
    success_url=reverse_lazy('accounts:libraryhistory')
    allowed_roles=['admin','librarian']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["library_history"] = self.get_object()
        return context


class DeleteLibraryHistoryView(RoleRequiredMixn, DeleteView):
    model=LibraryHistory
    success_url=reverse_lazy('accounts:libraryhistory')
    template_name='library/deletehistory.html'
    allowed_roles=['admin','librarian']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["history_to_delete"] = self.object 
        return context
    



class FeeHistoryView(RoleRequiredMixn, TemplateView):
    template_name='accounts/fees/fees_details.html'
    allowed_roles=['staff','admin']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fee_history"] = FeesHistory.objects.all()
        return context


class AddNewFeeRecord(RoleRequiredMixn, CreateView):
    model=FeesHistory
    form_class=FeeHistoryUpdateForm
    template_name='accounts/fees/addfee_record.html'
    success_url=reverse_lazy('accounts:feehistory')
    allowed_roles=['staff','admin']



class UpdateFeeHistory(RoleRequiredMixn, UpdateView):
    model=FeesHistory
    form_class=FeeHistoryUpdateForm
    template_name='accounts/fees/update_fee.html'
    success_url=reverse_lazy('accounts:feehistory')
    allowed_roles=['staff','admin']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fee_history"] = self.get_object() 
        return context
    


class DeleteFeeHistory(RoleRequiredMixn, DeleteView):
    model=FeesHistory
    template_name='accounts/fees/fees_details.html'
    success_url=reverse_lazy('accounts:feehistory')
    allowed_roles=['staff','admin']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["history_to_delete"] = self.object
        return context
    


class StaffDashboardView(RoleRequiredMixn, TemplateView):
    template_name='dashboard/staff_dashboard.html'
    allowed_roles=['staff']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library'] = LibraryHistory.objects.all()  
        context['students'] = Student.objects.all()  
        return context
    

class StaffCreatStudentView(RoleRequiredMixn, CreateView):
    model=Student
    form_class=StudentForm
    template_name='accounts/student/student_create.html'
    success_url=reverse_lazy('accounts:staff_dashboard')
    allowed_roles=['staff']



class StaffStudentUpdateView(RoleRequiredMixn, UpdateView):
    model=Student
    form_class=StudentForm
    template_name='accounts/student/student_update.html'
    success_url=reverse_lazy('accounts:staff_dashboard')
    allowed_roles=['staff']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.get_object()  
        return context
    

class StaffStudentDeleteView(RoleRequiredMixn, DeleteView):
    model = Student
    template_name = 'students/DeleteStudent.html'  
    success_url = reverse_lazy('accounts:staff_dashboard')  
    allowed_roles=['staff']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_to_delete'] = self.object
        return context
    


class LibrarianDashboardView(RoleRequiredMixn, TemplateView):
    template_name='dashboard/librarian_dashboard.html'
    allowed_roles=['librarian']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_history'] = LibraryHistory.objects.all()
        context['fee_history'] = FeesHistory.objects.all()  
        context['students'] = Student.objects.all()  
        return context


class AddBooks(RoleRequiredMixn, CreateView):
    model=Library
    form_class=AddBookForm
    template_name='accounts/library/add_book.html'
    success_url=reverse_lazy('accounts:librarian_dashboard')
    allowed_roles=['admin','librarian']


class BookView(RoleRequiredMixn, TemplateView):
    template_name="accounts/library/books_lists.html"
    allowed_roles=['admin','librarian']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Library.objects.all()    
        return context
    

class UpdateBooksView(RoleRequiredMixn, UpdateView):
    model = Library
    form_class = AddBookForm
    template_name = "accounts/library/add_book.html"
    success_url = reverse_lazy('accounts:book_list')  
    allowed_roles=['admin','librarian']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = self.get_object()  # Fetch the current book object being edited
        return context
    

class DeleteBookView(RoleRequiredMixn, DeleteView):
    model=Library
    template_name="library/deletebook.html"
    success_url=reverse_lazy('accounts:book_list')
    allowed_roles=['admin','librarian']
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["book_to_delete"] = self.object
        return context