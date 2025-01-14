#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def create_admin():
    import django
    django.setup()  # Set up Django before using ORM
    from django.contrib.auth.models import User
    # Create admin user if it doesn't exist
    if not User.objects.filter(username="admin").exists():
        user = User.objects.create(username="admin")
        user.set_password("bakery123")
        #the permissions for the admin user 
        user.is_superuser = False
        user.is_staff = True
        user.save()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DSP_bakery.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        create_admin()
        
    execute_from_command_line(sys.argv)

    

if __name__ == '__main__':
    main()
