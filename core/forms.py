# forms.py
from django import forms
from .models import File, ProblemCategory, Ticket,TicketComment, Customer, Region
from django.contrib.auth.models import User
from .models import Profile, Terminal, VersionControl

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
    
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don’t match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'description', 'category', 'access_level', 'file', 'passcode', 'allow_preview', 'allow_download']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter file title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a brief description', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'access_level': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'passcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Set a passcode for restricted access'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.access_level != 'restricted':
            self.fields['passcode'].required = False  
        else:
            self.fields['passcode'].required = True



class FilePasscodeForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['passcode']
        widgets = {
            'passcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter new passcode'
            })
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone_number', 'role', 'customer', 'terminal']

    # Customize widgets for better UI
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    terminal = forms.ModelChoiceField(queryset=Terminal.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    id_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['created_by', 'assigned_to', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'brts_unit': forms.Select(attrs={'class': 'form-control'}),
            'problem_category': forms.Select(attrs={'class': 'form-control'}),
            'terminal': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'responsible': forms.Select(attrs={'class': 'form-control'})
        }

    # Override to make them required and visible
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=True)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # <- pass request.user when creating the form
        terminal_id = kwargs.pop('terminal_id', None)
        super().__init__(*args, **kwargs)

        # Default queryset (all terminals)
        self.fields['terminal'].queryset = Terminal.objects.all()
        self.fields['terminal'].label_from_instance = lambda obj: (
            f"{obj.cdm_name} (Inactive)" if not obj.is_active else obj.cdm_name
        )

        # Autofill if instance has a terminal
        if self.instance and getattr(self.instance, 'terminal', None):
            terminal = self.instance.terminal
            self.fields['customer'].initial = terminal.customer
            self.fields['region'].initial = terminal.region
        elif terminal_id:
            try:
                terminal = Terminal.objects.get(id=terminal_id)
                self.fields['customer'].initial = terminal.customer
                self.fields['region'].initial = terminal.region
            except Terminal.DoesNotExist:
                pass

        # 🔹 Role-based restrictions
        if user:
            profile = getattr(user, "profile", None)

            # If user is custodian → only his terminal, customer, and region
            if profile and getattr(profile, "terminal", None):
                assigned_terminal = profile.terminal
                assigned_customer = assigned_terminal.customer
                assigned_region = assigned_terminal.region

                self.fields['terminal'].queryset = Terminal.objects.filter(id=assigned_terminal.id)
                self.fields['customer'].queryset = Customer.objects.filter(id=assigned_customer.id)
                self.fields['region'].queryset = Region.objects.filter(id=assigned_region.id)

                # lock them
                self.fields['terminal'].disabled = True
                self.fields['customer'].disabled = True
                self.fields['region'].disabled = True

            # If user is overseer → all terminals of his customer, customer locked, region limited
            elif Customer.objects.filter(overseer=user).exists():
                assigned_customer = Customer.objects.filter(overseer=user).first()

                self.fields['customer'].queryset = Customer.objects.filter(id=assigned_customer.id)
                self.fields['terminal'].queryset = Terminal.objects.filter(customer=assigned_customer)
                self.fields['region'].queryset = Region.objects.filter(
                    id__in=self.fields['terminal'].queryset.values_list("region_id", flat=True)
                )

                # lock customer, region/terminal remain selectable
                self.fields['customer'].disabled = True


class ProblemCategoryForm(forms.ModelForm):
    class Meta:
        model = ProblemCategory
        fields = ['brts_unit', 'name']
        widgets = {
            'brts_unit': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }

class TerminalForm(forms.ModelForm):
    class Meta:
        model = Terminal
        fields = ['customer', 'branch_name', 'cdm_name', 'serial_number', 'region', 'model', 'zone']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'branch_name': forms.TextInput(attrs={'class': 'form-control', 'value': 'Main Branch'}),
            'cdm_name': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'zone': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.branch_name:
            self.fields['branch_name'].required = False  

    
class TerminalUploadForm(forms.Form):
    file = forms.FileField(
        label='Upload CSV or Excel File',
        widget=forms.FileInput(attrs={'accept': '.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'})
    )

class VersionControlForm(forms.ModelForm):
    class Meta:
        model = VersionControl
        fields = [
            'terminal', 'manufacturer', 'template', 'firmware',
            'xfs', 'ejournal',
            'brits', 'app_version', 'neo_atm'
        ]
        widgets = {
            'terminal': forms.Select(attrs={'class': 'form-control'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
            'template': forms.TextInput(attrs={'class': 'form-control'}),
            'firmware': forms.TextInput(attrs={'class': 'form-control'}),
            'xfs': forms.TextInput(attrs={'class': 'form-control'}),
            'ejournal': forms.TextInput(attrs={'class': 'form-control'}),
            #'responsible': forms.TextInput(attrs={'class': 'form-control'}),
            'brits': forms.TextInput(attrs={'class': 'form-control'}),
            'app_version': forms.TextInput(attrs={'class': 'form-control'}),
            'neo_atm': forms.TextInput(attrs={'class': 'form-control'}),
        }

        
class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a comment...', 'class': 'form-control'})
        }

class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'priority', 'comment_summary', 'problem_category', 'description','resolution']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'comment_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'problem_category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resolution': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class EscalationNoteForm(forms.Form):
    note = forms.CharField(
        label="Escalation Note",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add a note for the escalation'
        }),
        required=False
    )