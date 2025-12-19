# events/management/commands/setup_devtools.py

from django.core.management.base import BaseCommand
from django.conf import settings
import os
import subprocess
import sys

class Command(BaseCommand):
    help = 'Setup and install developer tools for Momenta Event Management System'

    def add_arguments(self, parser):
        parser.add_argument(
            '--install-deps',
            action='store_true',
            help='Install developer tool dependencies',
        )
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser for accessing developer tools',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔧 Setting up Momenta Developer Tools...')
        )

        if options['install_deps']:
            self.install_dependencies()

        if options['create_superuser']:
            self.create_developer_superuser()

        self.setup_debug_settings()
        self.create_profiles_directory()
        self.display_usage_info()

        self.stdout.write(
            self.style.SUCCESS('✅ Developer tools setup complete!')
        )

    def install_dependencies(self):
        """Install developer tool dependencies"""
        self.stdout.write('📦 Installing developer dependencies...')
        
        dependencies = [
            'django-debug-toolbar>=4.2.0',
            'django-extensions>=3.2.0',
            'django-silk>=5.0.0',
        ]
        
        for dep in dependencies:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
                self.stdout.write(f'  ✅ Installed {dep}')
            except subprocess.CalledProcessError:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Failed to install {dep}')
                )

    def create_developer_superuser(self):
        """Create a superuser for developer access"""
        from django.contrib.auth.models import User
        
        username = 'developer'
        email = 'developer@momenta.local'
        password = 'devpass123'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f'👤 Created developer superuser: {username}')
            )
            self.stdout.write(f'   Email: {email}')
            self.stdout.write(f'   Password: {password}')
        else:
            self.stdout.write(
                self.style.WARNING(f'👤 Developer superuser already exists: {username}')
            )

    def setup_debug_settings(self):
        """Ensure debug settings are properly configured"""
        if not settings.DEBUG:
            self.stdout.write(
                self.style.WARNING('⚠️  DEBUG is False. Developer tools work best with DEBUG=True')
            )
        else:
            self.stdout.write('✅ DEBUG mode is enabled')

        # Check if developer tools are in INSTALLED_APPS
        dev_apps = ['debug_toolbar', 'django_extensions', 'silk']
        missing_apps = [app for app in dev_apps if app not in settings.INSTALLED_APPS]
        
        if missing_apps:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Missing developer apps in INSTALLED_APPS: {missing_apps}')
            )
        else:
            self.stdout.write('✅ Developer apps are configured')

    def create_profiles_directory(self):
        """Create directory for Silk profiling data"""
        profiles_dir = settings.BASE_DIR / 'profiles'
        if not profiles_dir.exists():
            profiles_dir.mkdir()
            self.stdout.write(f'📁 Created profiles directory: {profiles_dir}')
        else:
            self.stdout.write(f'📁 Profiles directory exists: {profiles_dir}')

    def display_usage_info(self):
        """Display usage information for developer tools"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('🚀 DEVELOPER TOOLS USAGE'))
        self.stdout.write('='*60)
        
        self.stdout.write('\n📊 Available Tools:')
        self.stdout.write('  • Django Debug Toolbar: Available on all pages (right sidebar)')
        self.stdout.write('  • Silk Performance Profiler: /silk/')
        self.stdout.write('  • Developer Dashboard: /dev/dashboard/')
        self.stdout.write('  • Browser Dev Tools: Ctrl+Shift+D (toggle panel)')
        
        self.stdout.write('\n🔗 URLs:')
        self.stdout.write('  • Developer Dashboard: http://localhost:8000/dev/dashboard/')
        self.stdout.write('  • Django Admin: http://localhost:8000/admin/')
        self.stdout.write('  • Silk Profiler: http://localhost:8000/silk/')
        self.stdout.write('  • Debug Toolbar: Appears automatically on pages')
        
        self.stdout.write('\n⌨️  Keyboard Shortcuts:')
        self.stdout.write('  • Ctrl+Shift+D: Toggle browser dev panel')
        self.stdout.write('  • Ctrl+Shift+C: Clear console logs')
        self.stdout.write('  • Ctrl+Shift+P: Show performance metrics')
        
        self.stdout.write('\n🔧 Management Commands:')
        self.stdout.write('  • python manage.py shell_plus: Enhanced Django shell')
        self.stdout.write('  • python manage.py runserver_plus: Enhanced dev server')
        self.stdout.write('  • python manage.py show_urls: Display all URL patterns')
        
        self.stdout.write('\n💡 Tips:')
        self.stdout.write('  • Use browser dev tools (F12) alongside Momenta tools')
        self.stdout.write('  • Check Network tab for AJAX request monitoring')
        self.stdout.write('  • Monitor SQL queries in Debug Toolbar')
        self.stdout.write('  • Use Silk for detailed performance profiling')
        
        self.stdout.write('\n' + '='*60)