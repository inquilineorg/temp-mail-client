#!/usr/bin/env python3
"""
Example usage of the MailTMClient class
Demonstrates how to use the client programmatically
"""

from mailtm_client import MailTMClient
import time


def example_usage():
    """Example of using the PryvonTempMailClient programmatically"""
    
    # Initialize the client
    client = MailTMClient()
    
    try:
        print("=== Pryvon Temp Mail Client Example ===\n")
        
        # 1. Get available domains
        print("1. Fetching available domains...")
        domains = client.get_domains()
        print(f"   Found {len(domains)} domains")
        for domain in domains[:3]:  # Show first 3
            print(f"   - {domain['domain']} (Active: {domain.get('isActive', False)})")
        print()
        
        # 2. Create a new account
        print("2. Creating a new account...")
        username = "testuser123"
        domain = domains[0]['domain'] if domains else "example.com"
        password = "testpass123"
        
        try:
            account = client.create_account(f"{username}@{domain}", password)
            print(f"   ✓ Account created: {account.address}")
            print(f"   Account ID: {account.id}")
            print(f"   Quota: {account.used}/{account.quota} bytes")
            print()
            
            # 3. Login to the account
            print("3. Logging in to the account...")
            logged_account, token = client.login(f"{username}@{domain}", password)
            print(f"   ✓ Logged in successfully")
            print(f"   Token: {token[:20]}...")
            print()
            
            # 4. Check mailbox
            print("4. Checking mailbox...")
            messages = client.get_messages()
            print(f"   Found {len(messages)} messages")
            
            if messages:
                print("   Latest message:")
                latest = messages[0]
                print(f"   - From: {latest.from_address}")
                print(f"   - Subject: {latest.subject or '(No Subject)'}")
                print(f"   - Date: {latest.created_at}")
                print(f"   - Seen: {latest.seen}")
                print()
                
                # 5. View full message content
                print("5. Getting full message content...")
                full_message = client.get_message(latest.id)
                print(f"   Message size: {full_message.get('size', 'Unknown')} bytes")
                if 'text' in full_message:
                    print(f"   Text content: {full_message['text'][:100]}...")
                print()
                
                # 6. Mark message as seen
                if not latest.seen:
                    print("6. Marking message as seen...")
                    client.mark_message_seen(latest.id)
                    print("   ✓ Message marked as seen")
                    print()
            
            # 7. Refresh mailbox
            print("7. Refreshing mailbox...")
            refreshed_messages = client.refresh_mailbox()
            print(f"   Mailbox refreshed, {len(refreshed_messages)} total messages")
            print()
            
            # 8. Logout
            print("8. Logging out...")
            client.logout()
            print("   ✓ Logged out successfully")
            print()
            
            # 9. Delete the account
            print("9. Deleting the account...")
            # Note: We need to login again to delete the account
            client.login(f"{username}@{domain}", password)
            client.delete_account()
            print("   ✓ Account deleted successfully")
            
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
            print("   (This might happen if the account already exists)")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Cleanup
        if client.is_logged_in():
            client.logout()
        print("\n=== Example completed ===")


def interactive_example():
    """Interactive example with user input"""
    
    client = MailTMClient()
    
    try:
        print("=== Interactive Pryvon Temp Mail Client Example ===\n")
        
        # Get domains
        print("Fetching available domains...")
        domains = client.get_domains()
        
        if not domains:
            print("No domains available")
            return
        
        print("Available domains:")
        for i, domain in enumerate(domains[:5], 1):  # Show first 5
            status = "✓" if domain.get('isActive', False) else "✗"
            print(f"{i}. {domain['domain']} {status}")
        
        # User selects domain
        domain_choice = input(f"\nSelect domain (1-{min(5, len(domains))}): ")
        try:
            selected_domain = domains[int(domain_choice) - 1]['domain']
        except (ValueError, IndexError):
            selected_domain = domains[0]['domain']
            print(f"Invalid choice, using: {selected_domain}")
        
        # User provides username and password
        username = input(f"Enter username for @{selected_domain}: ").strip()
        if not username:
            username = "testuser"
            print(f"Using default username: {username}")
        
        password = input("Enter password: ").strip()
        if not password:
            password = "testpass123"
            print(f"Using default password: {password}")
        
        full_address = f"{username}@{selected_domain}"
        
        # Create account
        print(f"\nCreating account: {full_address}")
        try:
            account = client.create_account(full_address, password)
            print(f"✓ Account created successfully!")
            print(f"Address: {account.address}")
            print(f"Password: {password}")
            
            # Ask if user wants to login
            if input("\nLogin to this account? (y/n): ").lower() == 'y':
                logged_account, token = client.login(full_address, password)
                print("✓ Logged in successfully!")
                
                # Check mailbox
                print("\nChecking mailbox...")
                messages = client.get_messages()
                print(f"Found {len(messages)} messages")
                
                if messages:
                    print("\nLatest messages:")
                    for i, msg in enumerate(messages[:3], 1):
                        print(f"{i}. From: {msg.from_address}")
                        print(f"   Subject: {msg.subject or '(No Subject)'}")
                        print(f"   Date: {msg.created_at[:10]}")
                        print(f"   Seen: {'Yes' if msg.seen else 'No'}")
                        print()
                
                # Logout
                client.logout()
                print("✓ Logged out")
            
            # Ask if user wants to delete account
            if input("\nDelete this account? (y/n): ").lower() == 'y':
                if not client.is_logged_in():
                    client.login(full_address, password)
                client.delete_account()
                print("✓ Account deleted")
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        if client.is_logged_in():
            client.logout()


if __name__ == "__main__":
    print("Choose an example:")
    print("1. Automated example")
    print("2. Interactive example")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        interactive_example()
    else:
        example_usage()
