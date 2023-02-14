from django.db import models
import bcrypt


class User(models.Model):
    GENDER_STATUS_MALE = 'Male'
    GENDER_STATUS_FEMALE = 'Female'

    GENDER_STATUS_CHOICE = [
        (GENDER_STATUS_FEMALE, 'Female'),
        (GENDER_STATUS_MALE, 'Male'),
    ]

    MARITAL_STATUS_SINGLE = 'Single'
    MARITAL_STATUS_MARRIED = 'MARRIED'
    MARITAL_STATUS_SINGLE_MOM = 'Single Mom'
    MARITAL_STATUS_DIVORCED = 'Divorced'
    MARITAL_STATUS_WIDOW = 'Widow'

    MARITAL_STATUS_CHOICE = [
        (MARITAL_STATUS_SINGLE, 'Single'),
        (MARITAL_STATUS_MARRIED, 'Married'),
        (MARITAL_STATUS_DIVORCED, 'Divorced'),
        (MARITAL_STATUS_WIDOW, 'Widow'),
        (MARITAL_STATUS_SINGLE_MOM, 'Single Mom'),
    ]

    OCCUPATION_STATUS_EMPLOYED = 'Employed'
    OCCUPATION_STATUS_BUSINESS_OWNER = 'Business Owner'
    OCCUPATION_STATUS_UNEMPLOYED = 'Unemployed'

    OCCUPATION_STATUS_CHOICE = [
        (OCCUPATION_STATUS_EMPLOYED, 'Employed'),
        (OCCUPATION_STATUS_BUSINESS_OWNER, 'Business Owner'),
        (OCCUPATION_STATUS_UNEMPLOYED, 'Unemployed')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=14,
        choices=GENDER_STATUS_CHOICE,
        default=GENDER_STATUS_MALE)

    marital_status = models.CharField(
        max_length=14,
        choices=MARITAL_STATUS_CHOICE,
        default=MARITAL_STATUS_SINGLE)
    address = models.CharField(max_length=150)
    password = models.BinaryField(max_length=16)
    email = models.CharField(unique=True, max_length=150)
    phone_number = models.CharField(max_length=15)
    username = models.CharField(max_length=100, unique=True)
    state_of_origin = models.CharField(max_length=100)
    state_of_residence = models.CharField(max_length=100)
    occupation = models.CharField(
        max_length=14,
        choices=OCCUPATION_STATUS_CHOICE,
        default=OCCUPATION_STATUS_UNEMPLOYED)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_admin')
    members = models.ManyToManyField(User, related_name='group_members')
    max_capacity = models.PositiveIntegerField()
    is_public = models.BooleanField(default=True)
    is_searchable = models.BooleanField()

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SavingsPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    periodic_amount = models.PositiveIntegerField()

    def __str__(self):
        return self.user


class Collection(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class CollectTable(models.Model):
    CONTRIBUTION_INTERVAL_DAILY = 'Daily'
    CONTRIBUTION_INTERVAL_WEEKLY = 'Weekly'
    CONTRIBUTION_INTERVAL_MONTHLY = 'Monthly'

    CONTRIBUTION_INTERVAL_CHOICE = [
        (CONTRIBUTION_INTERVAL_DAILY, 'Daily'),
        (CONTRIBUTION_INTERVAL_WEEKLY, 'Weekly'),
        (CONTRIBUTION_INTERVAL_MONTHLY, 'Monthly')
    ]
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member_contributions')
    contribution_amount = models.PositiveIntegerField()
    contribution_interval = models.CharField(
        max_length=10,
        choices=CONTRIBUTION_INTERVAL_CHOICE,
        default=CONTRIBUTION_INTERVAL_DAILY)

    contribution_date = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_contributions')

    def __str__(self):
        return f"{self.member} - {self.contribution_amount} - {self.contribution_interval} - {self.contribution_date} - {self.group}"


class Contribution(models.Model):
    CONTRIBUTION_INTERVAL_DAILY = 'Daily'
    CONTRIBUTION_INTERVAL_WEEKLY = 'Weekly'
    CONTRIBUTION_INTERVAL_MONTHLY = 'Monthly'

    CONTRIBUTION_INTERVAL_CHOICE = [
        (CONTRIBUTION_INTERVAL_DAILY, 'Daily'),
        (CONTRIBUTION_INTERVAL_WEEKLY, 'Weekly'),
        (CONTRIBUTION_INTERVAL_MONTHLY, 'Monthly')
    ]
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    amount = models.PositiveIntegerField()
    interval = models.CharField(
        max_length=10,
        choices=CONTRIBUTION_INTERVAL_CHOICE,
        default=CONTRIBUTION_INTERVAL_DAILY)
    date = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_belong_to")

    def __str__(self):
        return f"{self.member} - {self.amount} - {self.interval} - {self.date} - {self.group}"

    class Meta:
        ordering = ['-date']


class GroupAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    collection_table = models.ForeignKey(CollectTable, on_delete=models.CASCADE)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.group} - {self.collection_table} - {self.contribution}"
