#!/usr/bin/env python
"""
Script pour créer un utilisateur admin
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@bibliotheque.com',
            password='admin123'
        )
        print("Utilisateur admin créé :")
        print("   - Username: admin")
        print("   - Password: admin123")
        print("   - Email: admin@bibliotheque.com")
    else:
        print("L'utilisateur admin existe déjà")

if __name__ == '__main__':
    create_admin()
