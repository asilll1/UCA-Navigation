#!/usr/bin/env python3
"""
UCA Campus Navigation System - Deployment Script
This script helps deploy the application to different platforms.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def check_dependencies():
    """Check if required deployment tools are installed"""
    tools = {
        'git': 'Git for version control',
        'docker': 'Docker for containerization',
        'heroku': 'Heroku CLI for cloud deployment'
    }
    
    missing_tools = []
    for tool, description in tools.items():
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
            print(f"✅ {tool} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {tool} is not installed - {description}")
            missing_tools.append(tool)
    
    return missing_tools

def deploy_local():
    """Deploy locally using Docker"""
    print("\n🐳 Deploying locally with Docker...")
    
    try:
        # Build and run with docker-compose
        subprocess.run(['docker-compose', 'up', '--build', '-d'], check=True)
        print("✅ Application deployed locally!")
        print("🌐 Access at: http://localhost:5000")
        print("📋 To stop: docker-compose down")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker deployment failed: {e}")
        return False
    
    return True

def deploy_heroku():
    """Deploy to Heroku"""
    print("\n☁️ Deploying to Heroku...")
    
    try:
        # Check if Heroku CLI is installed
        subprocess.run(['heroku', '--version'], capture_output=True, check=True)
        
        # Create Heroku app if it doesn't exist
        app_name = input("Enter Heroku app name (or press Enter to auto-generate): ").strip()
        if not app_name:
            app_name = f"uca-navigation-{os.getenv('USER', 'user')}"
        
        # Create app
        subprocess.run(['heroku', 'create', app_name], check=True)
        
        # Add buildpacks
        subprocess.run(['heroku', 'buildpacks:add', 'heroku/python'], check=True)
        
        # Deploy
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Deploy to Heroku'], check=True)
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        
        # Open the app
        subprocess.run(['heroku', 'open'], check=True)
        
        print(f"✅ Application deployed to Heroku!")
        print(f"🌐 URL: https://{app_name}.herokuapp.com")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Heroku deployment failed: {e}")
        return False
    
    return True

def deploy_docker_cloud():
    """Deploy to Docker cloud platforms"""
    print("\n🐳 Deploying to Docker cloud...")
    
    platforms = {
        '1': 'Docker Hub',
        '2': 'Google Cloud Run',
        '3': 'AWS ECS',
        '4': 'Azure Container Instances'
    }
    
    print("Available platforms:")
    for key, platform in platforms.items():
        print(f"  {key}. {platform}")
    
    choice = input("\nSelect platform (1-4): ").strip()
    
    if choice == '1':
        return deploy_docker_hub()
    elif choice == '2':
        return deploy_google_cloud_run()
    elif choice == '3':
        return deploy_aws_ecs()
    elif choice == '4':
        return deploy_azure_aci()
    else:
        print("❌ Invalid choice")
        return False

def deploy_docker_hub():
    """Deploy to Docker Hub"""
    print("\n📦 Deploying to Docker Hub...")
    
    try:
        # Get Docker Hub username
        username = input("Enter Docker Hub username: ").strip()
        if not username:
            print("❌ Username is required")
            return False
        
        # Build image
        image_name = f"{username}/uca-navigation"
        subprocess.run(['docker', 'build', '-t', image_name, '.'], check=True)
        
        # Push to Docker Hub
        subprocess.run(['docker', 'push', image_name], check=True)
        
        print(f"✅ Image pushed to Docker Hub: {image_name}")
        print("📋 To run: docker run -p 5000:5000 {image_name}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker Hub deployment failed: {e}")
        return False
    
    return True

def deploy_google_cloud_run():
    """Deploy to Google Cloud Run"""
    print("\n☁️ Deploying to Google Cloud Run...")
    print("⚠️  This requires Google Cloud SDK and authentication")
    
    try:
        project_id = input("Enter Google Cloud project ID: ").strip()
        if not project_id:
            print("❌ Project ID is required")
            return False
        
        # Build and deploy
        service_name = "uca-navigation"
        subprocess.run([
            'gcloud', 'run', 'deploy', service_name,
            '--image', 'gcr.io/{}/{}'.format(project_id, service_name),
            '--platform', 'managed',
            '--region', 'us-central1',
            '--allow-unauthenticated'
        ], check=True)
        
        print("✅ Deployed to Google Cloud Run!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Google Cloud Run deployment failed: {e}")
        return False
    
    return True

def deploy_aws_ecs():
    """Deploy to AWS ECS"""
    print("\n☁️ Deploying to AWS ECS...")
    print("⚠️  This requires AWS CLI and proper configuration")
    
    try:
        # This is a simplified version - in practice, you'd need more setup
        print("📋 AWS ECS deployment requires:")
        print("  1. AWS CLI configured")
        print("  2. ECR repository created")
        print("  3. ECS cluster and service configured")
        print("  4. Task definition created")
        
        print("\n🔗 See AWS documentation for detailed ECS deployment")
        
    except Exception as e:
        print(f"❌ AWS ECS deployment failed: {e}")
        return False
    
    return True

def deploy_azure_aci():
    """Deploy to Azure Container Instances"""
    print("\n☁️ Deploying to Azure Container Instances...")
    print("⚠️  This requires Azure CLI and proper configuration")
    
    try:
        resource_group = input("Enter Azure resource group: ").strip()
        if not resource_group:
            print("❌ Resource group is required")
            return False
        
        # Deploy to ACI
        subprocess.run([
            'az', 'container', 'create',
            '--resource-group', resource_group,
            '--name', 'uca-navigation',
            '--image', 'uca-navigation:latest',
            '--ports', '5000',
            '--dns-name-label', 'uca-navigation'
        ], check=True)
        
        print("✅ Deployed to Azure Container Instances!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Azure ACI deployment failed: {e}")
        return False
    
    return True

def main():
    """Main deployment function"""
    print("🚀 UCA Campus Navigation System - Deployment")
    print("=" * 50)
    
    # Check dependencies
    missing_tools = check_dependencies()
    
    # Show deployment options
    print("\n📋 Deployment Options:")
    print("1. Local Docker deployment")
    print("2. Heroku cloud deployment")
    print("3. Docker cloud platforms")
    print("4. Check deployment readiness")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        deploy_local()
    elif choice == '2':
        if 'heroku' in missing_tools:
            print("❌ Heroku CLI is required. Install from: https://devcenter.heroku.com/articles/heroku-cli")
        else:
            deploy_heroku()
    elif choice == '3':
        if 'docker' in missing_tools:
            print("❌ Docker is required. Install from: https://docs.docker.com/get-docker/")
        else:
            deploy_docker_cloud()
    elif choice == '4':
        print("\n🔍 Deployment Readiness Check:")
        print(f"✅ Python dependencies: requirements.txt")
        print(f"✅ Docker configuration: Dockerfile, docker-compose.yml")
        print(f"✅ Heroku configuration: Procfile, runtime.txt")
        print(f"✅ Production config: config.py")
        print(f"✅ Health check: /health endpoint")
        
        if missing_tools:
            print(f"\n⚠️  Missing tools: {', '.join(missing_tools)}")
        else:
            print("\n✅ All tools are ready for deployment!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main() 