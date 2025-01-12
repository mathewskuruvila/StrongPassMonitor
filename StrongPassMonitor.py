import re
import hashlib
import requests
import time
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)


def check_password_strength(password):
    """
    Check the strength of a password based on predefined criteria.
    """
    # Define the criteria for password strength
    criteria = {
        "length": r".{8,}",  # At least 8 characters
        "lowercase": r"[a-z]",  # At least one lowercase letter
        "uppercase": r"[A-Z]",  # At least one uppercase letter
        "digit": r"\d",  # At least one digit
        "special": r"[!@#$%^&*(),.?\":{}|<>]"  # At least one special character
    }

    # Messages for each criteria
    messages = {
        "length": "Password must be at least 8 characters long.",
        "lowercase": "Password must contain at least one lowercase letter.",
        "uppercase": "Password must contain at least one uppercase letter.",
        "digit": "Password must contain at least one digit.",
        "special": "Password must contain at least one special character."
    }

    # Check all conditions
    feedback = []
    for key, regex in criteria.items():
        if not re.search(regex, password):
            feedback.append(messages[key])

    if feedback:
        return f"{Fore.RED}Weak: {' '.join(feedback)}{Style.RESET_ALL}"
    return f"{Fore.GREEN}Strong: Your password meets all the criteria!{Style.RESET_ALL}"


def check_password_leak(password):
    """
    Check if a password has been leaked using the Have I Been Pwned API.
    """
    try:
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_password[:5]
        suffix = sha1_password[5:]
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")

        if response.status_code != 200:
            return f"{Fore.YELLOW}Error: Could not check password leak status (API error).{Style.RESET_ALL}"

        # Process the response to find matches
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return f"{Fore.RED}Leaked: This password has been found {count} times in data breaches.{Style.RESET_ALL}"

        return f"{Fore.GREEN}Safe: This password has not been found in data breaches.{Style.RESET_ALL}"

    except requests.exceptions.RequestException:
        return f"{Fore.YELLOW}Error: Network error occurred while checking password leak status.{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.YELLOW}Error: An unexpected error occurred: {str(e)}{Style.RESET_ALL}"


def main():
    """
    Main function to interact with the user and check password strength and leaks.
    """
    print(f"{Fore.CYAN}Welcome to StrongPassMonitor!{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Type 'exit' to quit at any time.\n{Style.RESET_ALL}")

    while True:
        try:
            # Get the password (visible input)
            password = input(f"{Fore.YELLOW}Enter your password: {Style.RESET_ALL}")
            if password.lower() == "exit":
                print(f"{Fore.CYAN}Exiting StrongPassMonitor. Goodbye!{Style.RESET_ALL}")
                break

            # Check password strength
            strength_result = check_password_strength(password)
            print(f"{Fore.BLUE}Strength Check: {Style.RESET_ALL}{strength_result}")

            # Check password leak only if it's strong
            if "Strong" in strength_result:
                print(f"{Fore.MAGENTA}Checking if your password has been leaked...{Style.RESET_ALL}")
                leak_result = check_password_leak(password)
                print(f"{Fore.BLUE}Leak Check: {Style.RESET_ALL}{leak_result}")
                time.sleep(1)  # Respect API rate limits

            print()

        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Exiting StrongPassMonitor. Goodbye!{Style.RESET_ALL}")
            break


if __name__ == "__main__":
    main()
