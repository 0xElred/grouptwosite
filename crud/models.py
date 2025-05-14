from django.db import models

# Create your models here.

class Gender(models.Model):
    class Meta:
        db_table = 'tbl_genders' # crud_gender = tbl_genders

    gender_id = models.BigAutoField(primary_key=True, blank=False) # gender_id = BIGINT NOT NULL AUTO_INCREMENT
    gender = models.CharField(max_length=50, blank=False) # gender = VARCHAR(50) NOT NULL
    created_at = models.DateTimeField(auto_now_add=True) # created_at = TIMESTAMP  DEFAULT CURRENT_TIMESTAMP
    updated_at = models.DateTimeField(auto_now=True) # updated_at = TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

class Users(models.Model):
    class Meta:
        db_table = 'tbl_users' # crud_users = tbl_users

    user_id = models.BigAutoField(primary_key=True, blank=False) # user_id = BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY
    full_name = models.CharField(max_length=55, blank=False) # full_name = VARCHAR(555) NOT NULL
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE) # gender_id = NOT NULL // FOREIGN KEY(gender_id) REFERENCES tbl_genders(gender_id) ON DELETE CASCADE
    birth_date = models.DateField(blank=False) # birth_date = DATE NOT NULL
    address = models.CharField(max_length=255, blank=False) # address = VARCHAR(255) NOT NULL
    contact_number = models.CharField(max_length=55, blank=False) # contact_number = VARCHAR(55) NOT NULL 
    other_phone_number = models.CharField(max_length=55, blank=True) # other_phone_number = VARCHAR(55) DEFAULT NULL
    email = models.EmailField(max_length=55, blank=True) # email = VARCHAR(55) DEFAULT NULL
    username = models.CharField(max_length=55, blank=False, unique=True) # username = VARCHAR(55) NOT NULL // UNIQUE
    password = models.CharField(max_length=255, blank=False) # password = VARCHAR(255) NOT NULL
    created_at = models.DateTimeField(auto_now_add=True) # created_at = TIMESTAMP  DEFAULT CURRENT_TIMESTAMP
    updated_at = models.DateTimeField(auto_now=True) # updated_at = TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP