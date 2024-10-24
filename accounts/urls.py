from django.urls import path
from . import views
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path("", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path("logout/", UserLogoutView.as_view(), name="logout"),

    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/validate/<uidb64>/<token>/", ResetPasswordView.as_view(), name="reset_password_validate"),


    # Profile
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),


    path('students/', StudentListView.as_view(), name='student_list'),
    path('addstudent/', AddStudentsView.as_view(), name='add_student'),
    path('student/edit/<pk>/', UpdateStudentView.as_view(), name='update_student'),
    path('student/delete/<pk>/', DeleteStudentsView.as_view(), name='delete_student'),


    path('add_libraryhistory/',AddLibraryRecord.as_view(),name='add_library'),
    path('libraryhistory',LibraryHistoryView.as_view(),name='libraryhistory'),
    path('update_libraryhistory/<pk>/', UpdateLibraryHistory.as_view(), name='update_history'),
    path('delete_libraryhistory/<pk>/', DeleteLibraryHistoryView.as_view(), name='delete_history'),



    path('addfeehistory', AddNewFeeRecord.as_view(), name='add_feehistory'),
    path('feehistory', FeeHistoryView.as_view(), name='feehistory'),
    path('update_feehistory/<pk>/', UpdateFeeHistory.as_view(), name='update_fee'),
    path('delete_feehistory/<pk>/', DeleteFeeHistory.as_view(), name='delete_fee'),


    # Role-based dashboards
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('profile/<id>/', UserProfileView.as_view(), name='user_profile'),
    path('adduser',AddUserView.as_view(),name='adduser'),
    path('users/edit/<pk>/', UpdateUserView.as_view(), name='updateuser'),
    path('users/delete/<pk>/', DeleteUserView.as_view(), name='deleteuser'),


    path('staff_dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('staff_addstudent/', StaffCreatStudentView.as_view(), name='staff_addstudent'),
    path('staff_student/Update/<pk>/', StaffStudentUpdateView.as_view(), name='staff_updatestudent'),
    path('Staff_student/delete/<pk>/', StaffStudentDeleteView.as_view(), name='staff_deletestudent'),


    path('librarian_dashboard/', LibrarianDashboardView.as_view(), name='librarian_dashboard'),


    path('books',BookView.as_view(),name='book_list'),
    path('addbook',AddBooks.as_view(),name='addbook'),
    path('editbook/<pk>/',UpdateBooksView.as_view(),name='editbook'),
    path('deletebook/<pk>/',DeleteBookView.as_view(),name='deletebook'),
]