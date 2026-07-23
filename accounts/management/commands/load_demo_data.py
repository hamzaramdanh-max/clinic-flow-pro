"""
Demo Data Loader for ClinicFlow Pro
Usage: python manage.py load_demo_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

from clinic.models import (
    Patient, Doctor, Appointment, Medicine, Invoice, Department, ClinicSettings
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Load demo data for ClinicFlow Pro'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading demo data',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🚀 Starting Demo Data Loading...\n'))

        # ==================== Clear Data (Optional) ====================
        if options['clear']:
            self.stdout.write(self.style.WARNING('🗑️  Clearing existing data...'))
            Invoice.objects.all().delete()
            Appointment.objects.all().delete()
            Medicine.objects.all().delete()
            Doctor.objects.all().delete()
            Patient.objects.all().delete()
            Department.objects.all().delete()
            # Delete non-superuser users
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('✅ Data cleared!\n'))

        # ==================== 1. Create Departments ====================
        self.stdout.write('📁 Creating Departments...')
        departments_data = [
            {'name': 'Cardiology', 'description': 'Heart and cardiovascular system'},
            {'name': 'Pediatrics', 'description': 'Children medical care'},
            {'name': 'Dermatology', 'description': 'Skin diseases and treatments'},
            {'name': 'Dental', 'description': 'Dental care and oral health'},
            {'name': 'General Medicine', 'description': 'General health services'},
            {'name': 'Orthopedics', 'description': 'Bones and joints'},
            {'name': 'Ophthalmology', 'description': 'Eye care and vision'},
        ]
        
        departments = []
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'  ✅ Created: {dept.name}')
        
        self.stdout.write(self.style.SUCCESS(f'✅ Total Departments: {len(departments)}\n'))

        # ==================== 2. Create Users & Doctors ====================
        self.stdout.write('👨‍⚕️ Creating Doctors...')
        doctors_data = [
            {'username': 'dr_ahmed_sami', 'first_name': 'Ahmed', 'last_name': 'Sami', 
             'specialization': 'Cardiologist', 'dept': 'Cardiology', 'fees': 500},
            {'username': 'dr_mohamed_fathy', 'first_name': 'Mohamed', 'last_name': 'Fathy',
             'specialization': 'Dermatologist', 'dept': 'Dermatology', 'fees': 400},
            {'username': 'dr_nour_eldin', 'first_name': 'Nour', 'last_name': 'Eldin',
             'specialization': 'Pediatrician', 'dept': 'Pediatrics', 'fees': 350},
            {'username': 'dr_layla_mahmoud', 'first_name': 'Layla', 'last_name': 'Mahmoud',
             'specialization': 'Dentist', 'dept': 'Dental', 'fees': 300},
            {'username': 'dr_khaled_hassan', 'first_name': 'Khaled', 'last_name': 'Hassan',
             'specialization': 'General Practitioner', 'dept': 'General Medicine', 'fees': 250},
            {'username': 'dr_sara_ibrahim', 'first_name': 'Sara', 'last_name': 'Ibrahim',
             'specialization': 'Orthopedic Surgeon', 'dept': 'Orthopedics', 'fees': 600},
            {'username': 'dr_omar_ali', 'first_name': 'Omar', 'last_name': 'Ali',
             'specialization': 'Ophthalmologist', 'dept': 'Ophthalmology', 'fees': 450},
            {'username': 'dr_mona_saeed', 'first_name': 'Mona', 'last_name': 'Saeed',
             'specialization': 'Pediatric Cardiologist', 'dept': 'Cardiology', 'fees': 700},
        ]
        
        doctors = []
        for doc_data in doctors_data:
            # Create User
            user, user_created = User.objects.get_or_create(
                username=doc_data['username'],
                defaults={
                    'first_name': doc_data['first_name'],
                    'last_name': doc_data['last_name'],
                    'email': f"{doc_data['username']}@clinic.com",
                }
            )
            if user_created:
                user.set_password('demo1234')
                user.save()
            
            # Get Department
            dept = Department.objects.filter(name=doc_data['dept']).first()
            
            # Create Doctor
            doctor, doc_created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'department': dept,
                    'specialization': doc_data['specialization'],
                    'consultation_fees': Decimal(doc_data['fees']),
                }
            )
            doctors.append(doctor)
            if doc_created:
                self.stdout.write(f'  ✅ Dr. {doc_data["first_name"]} {doc_data["last_name"]} - {doc_data["specialization"]}')
        
        self.stdout.write(self.style.SUCCESS(f'✅ Total Doctors: {len(doctors)}\n'))

        # ==================== 3. Create Patients ====================
        self.stdout.write('👥 Creating Patients...')
        patients_data = [
            {'name': 'Ahmed Mohamed Ali', 'phone': '01012345678', 'email': 'ahmed.mohamed@email.com'},
            {'name': 'Fatma Hassan Ibrahim', 'phone': '01098765432', 'email': 'fatma.hassan@email.com'},
            {'name': 'Mahmoud Abdelrahman', 'phone': '01123456789', 'email': 'mahmoud.abd@email.com'},
            {'name': 'Sara Khaled Ahmed', 'phone': '01234567890', 'email': 'sara.khaled@email.com'},
            {'name': 'Youssef Ibrahim', 'phone': '01345678901', 'email': 'youssef.ibrahim@email.com'},
            {'name': 'Nour Ali Hassan', 'phone': '01456789012', 'email': 'nour.ali@email.com'},
            {'name': 'Mostafa Kamal', 'phone': '01567890123', 'email': 'mostafa.kamal@email.com'},
            {'name': 'Aisha Mahmoud', 'phone': '01678901234', 'email': 'aisha.mahmoud@email.com'},
            {'name': 'Omar Farouk', 'phone': '01789012345', 'email': 'omar.farouk@email.com'},
            {'name': 'Heba Mostafa', 'phone': '01890123456', 'email': 'heba.mostafa@email.com'},
            {'name': 'Karim Nasser', 'phone': '01901234567', 'email': 'karim.nasser@email.com'},
            {'name': 'Yasmin Adel', 'phone': '01011223344', 'email': 'yasmin.adel@email.com'},
            {'name': 'Hassan Salah', 'phone': '01022334455', 'email': 'hassan.salah@email.com'},
            {'name': 'Rania Waleed', 'phone': '01033445566', 'email': 'rania.waleed@email.com'},
            {'name': 'Tarek Mahmoud', 'phone': '01044556677', 'email': 'tarek.mahmoud@email.com'},
            {'name': 'Marwa Sherif', 'phone': '01055667788', 'email': 'marwa.sherif@email.com'},
            {'name': 'Amr Hesham', 'phone': '01066778899', 'email': 'amr.hesham@email.com'},
            {'name': 'Dina Ashraf', 'phone': '01077889900', 'email': 'dina.ashraf@email.com'},
            {'name': 'Mahmoud Sobhy', 'phone': '01088990011', 'email': 'mahmoud.sobhy@email.com'},
            {'name': 'Salma Ibrahim', 'phone': '01099001122', 'email': 'salma.ibrahim@email.com'},
        ]
        
        # Get admin user for created_by
        admin_user = User.objects.filter(is_superuser=True).first()
        
        patients = []
        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                phone=patient_data['phone'],
                defaults={
                    'name': patient_data['name'],
                    'email': patient_data['email'],
                    'created_by': admin_user,
                }
            )
            patients.append(patient)
            if created:
                self.stdout.write(f'  ✅ {patient.name}')
        
        self.stdout.write(self.style.SUCCESS(f'✅ Total Patients: {len(patients)}\n'))

        # ==================== 4. Create Medicines ====================
        self.stdout.write('💊 Creating Medicines...')
        medicines_data = [
            {'name': 'Panadol Extra', 'price': 25.00, 'stock': 150, 'days_to_expiry': 365},
            {'name': 'Augmentin 1g', 'price': 85.00, 'stock': 45, 'days_to_expiry': 180},
            {'name': 'Insulin Lantus', 'price': 320.00, 'stock': 8, 'days_to_expiry': 90},
            {'name': 'Vitamin D3 50000', 'price': 60.00, 'stock': 200, 'days_to_expiry': 730},
            {'name': 'Concor 5mg', 'price': 45.00, 'stock': 75, 'days_to_expiry': 500},
            {'name': 'Ventolin Inhaler', 'price': 55.00, 'stock': 30, 'days_to_expiry': 365},
            {'name': 'Nexium 40mg', 'price': 120.00, 'stock': 60, 'days_to_expiry': 400},
            {'name': 'Cataflam 50mg', 'price': 35.00, 'stock': 100, 'days_to_expiry': 300},
            {'name': 'Amoxicillin 500mg', 'price': 40.00, 'stock': 5, 'days_to_expiry': 120},
            {'name': 'Aspirin 75mg', 'price': 15.00, 'stock': 250, 'days_to_expiry': 600},
            {'name': 'Metformin 500mg', 'price': 30.00, 'stock': 90, 'days_to_expiry': 450},
            {'name': 'Omega-3 Fish Oil', 'price': 95.00, 'stock': 40, 'days_to_expiry': 500},
            {'name': 'Claritine 10mg', 'price': 42.00, 'stock': 3, 'days_to_expiry': 200},
            {'name': 'Voltaren Gel', 'price': 65.00, 'stock': 55, 'days_to_expiry': 400},
            {'name': 'Zithromax 500mg', 'price': 110.00, 'stock': 25, 'days_to_expiry': 250},
        ]
        
        medicines = []
        for med_data in medicines_data:
            expiry = timezone.now().date() + timedelta(days=med_data['days_to_expiry'])
            medicine, created = Medicine.objects.get_or_create(
                name=med_data['name'],
                defaults={
                    'price': Decimal(str(med_data['price'])),
                    'stock': med_data['stock'],
                    'expiry_date': expiry,
                    'is_active': True,
                }
            )
            medicines.append(medicine)
            if created:
                stock_status = '⚠️ LOW STOCK' if med_data['stock'] < 10 else '✅'
                self.stdout.write(f'  {stock_status} {medicine.name} - {med_data["price"]} EGP - Stock: {med_data["stock"]}')
        
        self.stdout.write(self.style.SUCCESS(f'✅ Total Medicines: {len(medicines)}\n'))

        # ==================== 5. Create Appointments ====================
        self.stdout.write('📅 Creating Appointments...')
        statuses = ['Pending', 'Confirmed', 'Completed', 'Cancelled']
        status_weights = [3, 4, 5, 1]  # More Completed, Less Cancelled
        
        appointments = []
        now = timezone.now()
        
        for i in range(30):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            
            # Random date: -30 days to +30 days
            days_offset = random.randint(-30, 30)
            hours_offset = random.choice([9, 10, 11, 12, 14, 15, 16, 17, 18])
            appt_date = now + timedelta(days=days_offset)
            appt_date = appt_date.replace(hour=hours_offset, minute=random.choice([0, 30]), second=0, microsecond=0)
            
            # Status based on date
            if days_offset < -5:
                status = 'Completed'
            elif days_offset < 0:
                status = random.choices(['Completed', 'Cancelled'], weights=[8, 2])[0]
            elif days_offset == 0:
                status = random.choices(['Confirmed', 'Completed'], weights=[6, 4])[0]
            else:
                status = random.choices(['Pending', 'Confirmed'], weights=[4, 6])[0]
            
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date_time=appt_date,
                status=status,
            )
            appointments.append(appointment)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Total Appointments: {len(appointments)}\n'))

        # ==================== 6. Create Invoices ====================
        self.stdout.write('💰 Creating Invoices...')
        invoices = []
        
        for i in range(25):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            
            # Random amount
            amount = Decimal(random.choice([200, 250, 300, 350, 400, 450, 500, 600, 700, 850, 1000, 1200, 1500]))
            
            # Random paid status (70% paid)
            is_paid = random.choices([True, False], weights=[7, 3])[0]
            
            # Random due date
            days_offset = random.randint(-30, 15)
            due_date = (now + timedelta(days=days_offset)).date()
            
            invoice_number = f"INV-{1001 + i}"
            invoice = Invoice.objects.create(
                invoice_number=invoice_number,
                patient=patient,
                doctor=doctor,
                amount=amount,
                is_paid=is_paid,
                due_date=due_date,
            )
            invoices.append(invoice)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Total Invoices: {len(invoices)}\n'))

        # ==================== Summary ====================
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🎉 DEMO DATA LOADED SUCCESSFULLY!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'📁 Departments:  {Department.objects.count()}')
        self.stdout.write(f'👨‍⚕️ Doctors:      {Doctor.objects.count()}')
        self.stdout.write(f'👥 Patients:     {Patient.objects.count()}')
        self.stdout.write(f'💊 Medicines:    {Medicine.objects.count()}')
        self.stdout.write(f'📅 Appointments: {Appointment.objects.count()}')
        self.stdout.write(f'💰 Invoices:     {Invoice.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('\n💡 Login Credentials:'))
        self.stdout.write(self.style.SUCCESS('   Doctors Password: demo1234'))
        self.stdout.write(self.style.SUCCESS('   Example: dr_ahmed_sami / demo1234\n'))