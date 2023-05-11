import os
import sys
import subprocess
import shutil

# get working directory


def get_cwd():
    cwd = os.getcwd()
    print(cwd)

# this is where our project will be
# it can be name of project


def create_new_project():
    # Get current working directory
    current_dir = os.getcwd()
    print("Current directory:", current_dir)

    # Prompt user to enter directory name
    dir_name = input("Enter directory/project name: ")

    # Create new directory
    os.mkdir(dir_name)

    # Change current working directory to new directory
    new_dir = os.path.join(current_dir, dir_name)
    os.chdir(new_dir)

    # Create and activate new virtual environment
    print("******creating virtual environment....********")
    os.system("python -m venv env")
    print("******created virtual environment successfully ********")
    print("******activating env.....********")
    os.system(". env/bin/activate")
    print("****** virtual environment activated 🥳🥳😊********")

   # update pip to get rid of the upgrade message
    os.system(" python.exe -m pip install --upgrade pip")
    print("****** pip updated successfully 🥳🥳😊********")

    # Install Django
    print("****** installing basic dependencies.....********")
    os.system("pip install Django")
    print("****** basic dependencies installed successfully 🥳🥳😊********")

    # Install requirements from requirements.txt file
    print("****** updating requirements.txt.....********")
    os.system("pip freeze > requirements.txt")
    print("****** requirements.txt file updated successfully 🥳🥳😊********")

    # prompt the user to enter the name of the project, must end with .
    project_name = input("Enter the name of the project: ")

    # use django-admin to start the project entered by the user
    check_project_name = os.system(
        "django-admin startproject " + project_name + " .")
    print("New project created with name: ", check_project_name)
    print("****** project created successfully 🥳🥳😊********")

    # prompt the user to enter the app name they wish to use for their project
    app_name = input("Enter the name of the app: ")
    # use django-admin or py manage.py to startapp name entered by the user

    check_app_name = os.system("py manage.py startapp " + app_name)
    print("****** app created successfully'🥳🥳😊********")
    print(check_app_name)

    # Open settings.py file and add the new app to INSTALLED_APPS
    settings_file = os.path.join(project_name, "settings.py")
    with open(settings_file, "r") as f:
        lines = f.readlines()

    installed_apps_index = None
    for i, line in enumerate(lines):
        if line.startswith("INSTALLED_APPS"):
            installed_apps_index = i
            break

    if installed_apps_index is not None:
        lines[installed_apps_index] = lines[installed_apps_index].rstrip() + \
            f" \n    '{app_name}',\n"
        with open(settings_file, "w") as f:
            f.write(''.join(lines))
        print("****** added the core app to INSTALLED_APPS list 🥳🥳😊********")

    # add core.urls to main urls
    # first lets create the url file
    # Set the name of the file to create
    filename = os.path.join(app_name, "urls.py")

    # Create the urls.py file
    with open(filename, mode='w') as f:
        f.write(
            'from django.urls import path\n\nurlpatterns = [\n    # Add your URL patterns here\n]\n')

    # Verify that the file was created
    if os.path.isfile(filename):
        print(
            f'******  File {filename} created successfully!🥳🥳😊********')
    else:
        print(f'Error creating file {filename}')

    # Now let's add it to the main urls
    # Get the path of the main urls.py file in your project
    urls_file = os.path.join(project_name, "urls.py")
    print("urls_file path:", urls_file)

    # Read the contents of the urls.py file
    with open(urls_file, "r") as f:
        lines = f.readlines()
    # Find the line where the urlpatterns are defined
    for i, line in enumerate(lines):
        if line.startswith("from django.urls import path"):
            # Add the 'include' module to the existing import line
            lines[i] = lines[i].rstrip() + ", include\n"
            print("Line modified:", lines[i])
            continue

        if line.startswith("urlpatterns"):
            # Find the index where the admin line is located
            admin_index = i
            for j, admin_line in enumerate(lines[i:], start=i):
                if "admin.site.urls" in admin_line:
                    admin_index = j
                    break

            # Insert the new line after the admin line
            lines.insert(admin_index + 1,
                         f"    path('', include('{app_name}.urls')),\n")
            print("Line modified:", lines[admin_index + 1])
            break  # Break out of the loop when the line is found

    # Write the modified contents back to the urls.py file
    with open(urls_file, "w") as f:
        f.writelines(lines)
    print("urls.py file modified successfully!")

    print("****** added the urls.py to main urls.py  🥳🥳😊********")

    # run migrations to create superuser
    os.system("py manage.py makemigrations && py manage.py migrate")
    print("****** Migrations runs successfully 🥳🥳😊********")

    # create superuser
    os.system("py manage.py createsuperuser")
    print("****** Superuser created successfully 🥳🥳😊********")

    # PATHS
    # Get the absolute path of the current script file
    script_folder = os.path.dirname(os.path.abspath(__file__))
    print(script_folder)

    # Define the paths
    automate_folder = os.path.abspath(
        os.path.join(script_folder, '../automate'))
    created_folder = f'{dir_name}'
    code_folder = os.path.abspath(os.path.join(script_folder, '../../code'))

    # Verify if the created folder exists in the automate folder
    folder_path = os.path.join(automate_folder, created_folder)
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        # Handle the error condition or exit the script if necessary

    # Move the created folder from automate to code
    try:
        new_folder_path = os.path.join(code_folder, created_folder)
        shutil.move(folder_path, new_folder_path)
        print(
            f"Moved folder '{created_folder}' from '{automate_folder}' to '{new_folder_path}'")
    except Exception as e:
        print(f"Error occurred while moving the folder: {e}")
        # Handle the error condition or exit the script if necessary

    # Change the working directory to the new location
    try:
        os.chdir(new_folder_path)
        print(f"Changed working directory to: {new_folder_path}")
    except Exception as e:
        print(f"Error occurred while changing the working directory: {e}")
        # Handle the error condition or exit the script if necessary

    # Change the working directory to the new location
    try:
        os.chdir(new_folder_path)
        print(f"Changed working directory to: {new_folder_path}")
    except Exception as e:
        print(f"Error occurred while changing the working directory: {e}")
        # Handle the error condition or exit the script if necessary

    # run the application to check if the whole process was successfully
    print("****** preparing to run the application 🥳🥳🥳🥳********")
    os.system("py manage.py runserver")


def main():
    get_cwd()
    create_new_project()


if __name__ == "__main__":
    main()
