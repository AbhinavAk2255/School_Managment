from django.db import models
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Office Staff'),
        ('librarian', 'Librarian'),
    )

    email = models.EmailField(max_length=254, verbose_name='email address')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Add related_name to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    
    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)




class Student(models.Model):
    class_section = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)

    # Contact Information
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()

    # Enrollment Information
    admission_number = models.CharField(max_length=4, unique=True, editable=False)
    date_of_enrollment = models.DateField(auto_now_add=True)
    current_class = models.CharField(max_length=50)
    section = models.CharField(max_length=10, choices=class_section)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.admission_number}"

    def save(self, *args, **kwargs):
        if not self.admission_number:
            self.admission_number = str(random.randint(1000, 9999))  # Generate random 4-digit number
        super(Student, self).save(*args, **kwargs)


class Library(models.Model):

    Avilable_Chances = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    book_title = models.CharField(max_length=225)
    book_author = models.CharField(max_length=200)
    book_avilability = models.CharField(max_length=10, choices=Avilable_Chances)

    def __str__(self):
        return self.book_title
    

class LibraryHistory(models.Model):

    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),


    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book_name = models.ForeignKey(Library, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.book_name} borrowed by {self.student.first_name} {self.student.last_name}"



class FeesHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_date = models.DateField()
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Fees history for {self.student} on {self.payment_date}"
    

    def save(self, *args, **kwargs):
        self.outstanding_fees = self.total_fees - self.fees_paid
        super().save(*args, **kwargs)


    

