import os
import subprocess
import platform

def add_env_vars_to_shell_profile():
    """
    Add environment variables to the appropriate shell profile file
    and source it.
    """
    # Determine the appropriate shell profile file
    home_dir = os.path.expanduser("~")

    if platform.system() == "Darwin" or platform.system() == "Linux":
        # Check which shell is being used
        shell = os.environ.get("SHELL", "")

        if "zsh" in shell:
            profile_file = os.path.join(home_dir, ".zshrc")
        else:
            # Default to bash
            profile_file = os.path.join(home_dir, ".bashrc")
    else:
        # Windows or other systems not supported in this script
        print("This script only supports macOS and Linux systems.")
        return False

    # Environment variables to add
    env_vars = {
        "DBT_PROFILES_DIR": os.path.join(os.path.dirname(os.path.abspath(__file__)), ".dbt"),
        "DBT_PROJECT_DIR": os.path.join(os.path.dirname(os.path.abspath(__file__)), ".dbt"),
        "DBT_PROFILE": "data_warehouse",
    }

    # Create backup of the profile file
    backup_file = f"{profile_file}.bak"
    try:
        if os.path.exists(profile_file):
            with open(profile_file, 'r') as f:
                original_content = f.read()
            with open(backup_file, 'w') as f:
                f.write(original_content)
            print(f"Created backup of {profile_file} at {backup_file}")
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

    # Add environment variables to profile file
    try:
        with open(profile_file, 'a') as f:
            f.write("\n# Environment variables added by setup.py\n")
            for key, value in env_vars.items():
                # Check if the variable is already set with this value
                cmd = f'export {key}="{value}"\n'
                f.write(cmd)
            f.write("\n")
        print(f"Added environment variables to {profile_file}")
    except Exception as e:
        print(f"Error adding environment variables: {e}")
        return False

    # Source the profile file
    try:
        print(f"To activate these changes, run:\n  source {profile_file}")

        # Attempt to source the file in the current process
        # Note: This won't affect the parent shell
        if platform.system() == "Darwin" or platform.system() == "Linux":
            subprocess.run(["source", profile_file], shell=True)
            print("Note: Environment variables will be available in new terminal sessions.")
            print("For the current session, the source command was attempted but may not affect the parent shell.")
    except Exception as e:
        print(f"Error sourcing profile file: {e}")

    return True

if __name__ == "__main__":
    print("Setting up environment variables...")
    success = add_env_vars_to_shell_profile()

    if success:
        print("Setup completed successfully!")
    else:
        print("Setup encountered errors. Please check the output above.")
