# Generated migration for GitHub SocialApp

from django.db import migrations
from django.conf import settings


def create_github_socialapp(apps, schema_editor):
    SocialApp = apps.get_model('socialaccount', 'SocialApp')
    Site = apps.get_model('sites', 'Site')
    
    # Get or create the default site
    site = Site.objects.get_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'localhost'})[0]
    
    # Create GitHub SocialApp with placeholder credentials
    # User should update these with actual GitHub OAuth credentials
    social_app = SocialApp.objects.create(
        provider='github',
        name='GitHub',
        client_id='your-github-client-id',
        secret='your-github-client-secret',
    )
    
    # Add the site to the social app
    social_app.sites.add(site)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_options_alter_profile_address_and_more'),
        ('socialaccount', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(create_github_socialapp),
    ]
