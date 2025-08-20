#!/usr/bin/env python3
"""
Mail.tm Console Client - Enhanced Commercial Grade Version
A comprehensive console application for managing temporary email accounts
"""

import os
import sys
import time
import random
import string
import signal
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from rich.console import Group
from rich.columns import Columns
from rich.status import Status
from rich.syntax import Syntax
from rich.traceback import install

from mailtm_client import MailTMClient, MailAccount, MailMessage
from config import config
from logger import logger
from cache import cache
from exceptions import *

# Install rich traceback handler
install(show_locals=False)

console = Console()


class MailTMConsoleApp:
    """Enhanced console application for mail.tm"""
    
    def __init__(self):
        self.client = MailTMClient()
        self.running = True
        self.auto_refresh_task = None
        self.setup_signal_handlers()
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        console.print("\n[yellow]Shutdown signal received. Cleaning up...[/yellow]")
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Cleanup resources before exit"""
        try:
            if self.client.is_logged_in():
                self.client.logout()
            logger.info("Application shutdown complete")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def generate_random_string(self, length: int = 8) -> str:
        """Generate a random string for usernames"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)
    
    def show_welcome(self):
        """Display enhanced welcome screen"""
        welcome_text = Text("Mail.tm Console Client", style="bold blue")
        subtitle = Text("Professional Temporary Email Management Tool", style="italic")
        version = Text("v2.0.0", style="dim")
        
        console.print(Panel(
            Align.center(welcome_text + "\n" + subtitle + "\n" + version),
            border_style="blue",
            box=box.ROUNDED
        ))
        
        # Show configuration status
        self.show_config_status()
        console.print()
    
    def show_config_status(self):
        """Display configuration status"""
        config_items = [
            f"Cache: {'✓' if config.get('cache_enabled') else '✗'}",
            f"Auto-refresh: {'✓' if config.get('auto_refresh') else '✗'}",
            f"Log Level: {config.get('log_level', 'INFO')}",
            f"API Timeout: {config.get('api_timeout', 30)}s"
        ]
        
        console.print(Columns(config_items, equal=True, expand=True))
    
    def show_main_menu(self):
        """Display enhanced main menu"""
        if self.client.is_logged_in():
            account = self.client.current_account
            stats = self.client.get_account_stats()
            
            # Account status panel
            status_panel = Panel(
                f"[bold]{account.address}[/bold]\n"
                f"Quota: {stats['quota_used']:,}/{stats['quota_total']:,} bytes "
                f"({stats['quota_percentage']}%)\n"
                f"Created: {stats['created_at'][:10]} | "
                f"Requests: {stats['request_count']}",
                title="Account Status",
                border_style="green"
            )
            console.print(status_panel)
            
            options = [
                "📧 Check Mailbox",
                "🔄 Refresh Mailbox", 
                "📝 View Message",
                "👁️  Mark Message as Read",
                "🗑️  Delete Message",
                "📊 Account Statistics",
                "⚙️  Settings",
                "❌ Delete Account",
                "🚪 Logout",
                "❌ Exit"
            ]
        else:
            options = [
                "➕ Create New Account",
                "🔑 Login to Account",
                "⚙️  Settings",
                "❌ Exit"
            ]
        
        table = Table(title="Main Menu", box=box.ROUNDED, border_style="blue")
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        
        for i, option in enumerate(options, 1):
            if "📧" in option:
                table.add_row(str(i), "Check for new emails")
            elif "🔄" in option:
                table.add_row(str(i), "Refresh mailbox for latest messages")
            elif "📝" in option:
                table.add_row(str(i), "View full message content")
            elif "👁️" in option:
                table.add_row(str(i), "Mark a message as read")
            elif "🗑️" in option:
                table.add_row(str(i), "Delete a message")
            elif "📊" in option:
                table.add_row(str(i), "View account statistics and cache info")
            elif "⚙️" in option:
                table.add_row(str(i), "Configure application settings")
            elif "❌" in option and "Account" in option:
                table.add_row(str(i), "Delete current account")
            elif "🚪" in option:
                table.add_row(str(i), "Logout from current account")
            elif "➕" in option:
                table.add_row(str(i), "Create a new temporary email account")
            elif "🔑" in option:
                table.add_row(str(i), "Login to existing account")
            elif "❌" in option and "Exit" in option:
                table.add_row(str(i), "Exit the application")
        
        console.print(table)
        console.print()
    
    def show_settings_menu(self):
        """Display and manage application settings"""
        console.print("[bold blue]Settings[/bold blue]")
        console.print()
        
        while True:
            settings_table = Table(title="Current Settings", box=box.ROUNDED)
            settings_table.add_column("Setting", style="cyan")
            settings_table.add_column("Value", style="white")
            settings_table.add_column("Description", style="dim")
            
            settings = [
                ("Cache Enabled", str(config.get('cache_enabled')), "Enable/disable caching"),
                ("Auto Refresh", str(config.get('auto_refresh')), "Auto-refresh mailbox"),
                ("Refresh Interval", f"{config.get('refresh_interval')}s", "Mailbox refresh interval"),
                ("Max Messages", str(config.get('max_messages_display')), "Max messages to display"),
                ("API Timeout", f"{config.get('api_timeout')}s", "API request timeout"),
                ("Log Level", config.get('log_level'), "Logging verbosity"),
                ("Max Retries", str(config.get('max_retries')), "API retry attempts")
            ]
            
            for setting, value, description in settings:
                settings_table.add_row(setting, value, description)
            
            console.print(settings_table)
            console.print()
            
            console.print("Options:")
            console.print("1. Toggle cache")
            console.print("2. Toggle auto-refresh")
            console.print("3. Change refresh interval")
            console.print("4. Change log level")
            console.print("5. Clear cache")
            console.print("6. Back to main menu")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                current = config.get('cache_enabled')
                config.set('cache_enabled', not current)
                console.print(f"[green]Cache {'enabled' if not current else 'disabled'}[/green]")
            elif choice == "2":
                current = config.get('auto_refresh')
                config.set('auto_refresh', not current)
                console.print(f"[green]Auto-refresh {'enabled' if not current else 'disabled'}[/green]")
            elif choice == "3":
                interval = IntPrompt.ask("Enter refresh interval (seconds)", default=config.get('refresh_interval'))
                config.set('refresh_interval', interval)
                console.print(f"[green]Refresh interval set to {interval} seconds[/green]")
            elif choice == "4":
                levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
                level = Prompt.ask("Select log level", choices=levels, default=config.get('log_level'))
                config.set('log_level', level)
                console.print(f"[green]Log level set to {level}[/green]")
            elif choice == "5":
                if Confirm.ask("Clear all cached data?"):
                    self.client.clear_cache()
                    console.print("[green]Cache cleared[/green]")
            elif choice == "6":
                break
            
            console.print()
    
    def create_account(self):
        """Create a new mail.tm account with enhanced validation"""
        console.print("[bold blue]Creating New Account[/bold blue]")
        console.print()
        
        try:
            # Get available domains
            with console.status("[bold green]Fetching available domains...", spinner="dots"):
                domains = self.client.get_domains()
            
            if not domains:
                console.print("[red]No domains available[/red]")
                return
            
            # Show available domains
            domain_table = Table(title="Available Domains", box=box.ROUNDED)
            domain_table.add_column("Domain", style="cyan")
            domain_table.add_column("Active", style="green")
            domain_table.add_column("Status", style="yellow")
            
            for domain in domains:
                status = "✓" if domain.get('isActive', False) else "✗"
                domain_table.add_row(domain['domain'], status, "Available" if domain.get('isActive', False) else "Inactive")
            
            console.print(domain_table)
            console.print()
            
            # Get user input with validation
            username = Prompt.ask("Enter username (or press Enter for random)")
            if not username:
                username = self.generate_random_string(8)
                console.print(f"[yellow]Generated username: {username}[/yellow]")
            
            # Validate username
            if not username.replace('_', '').replace('-', '').isalnum():
                console.print("[red]Username must contain only letters, numbers, underscores, and hyphens[/red]")
                return
            
            # Select domain
            active_domains = [d['domain'] for d in domains if d.get('isActive', False)]
            if not active_domains:
                console.print("[red]No active domains available[/red]")
                return
            
            domain = Prompt.ask("Enter domain", choices=active_domains)
            
            # Generate password
            password = Prompt.ask("Enter password (or press Enter for random)")
            if not password:
                password = self.generate_random_string(12)
                console.print(f"[yellow]Generated password: {password}[/yellow]")
            
            # Validate password
            if len(password) < 6:
                console.print("[red]Password must be at least 6 characters long[/red]")
                return
            
            full_address = f"{username}@{domain}"
            
            if Confirm.ask(f"Create account: [bold]{full_address}[/bold]?"):
                with console.status("[bold green]Creating account...", spinner="dots"):
                    account = self.client.create_account(full_address, password)
                
                console.print(f"[green]✓[/green] Account created successfully!")
                console.print(f"Address: [bold]{account.address}[/bold]")
                console.print(f"Password: [bold]{password}[/bold]")
                console.print()
                console.print("[yellow]⚠️  Save these credentials! You'll need them to login.[/yellow]")
                
                if Confirm.ask("Login to this account now?"):
                    self.client.login(full_address, password)
                    console.print("[green]✓[/green] Logged in successfully!")
        
        except ValidationError as e:
            console.print(f"[red]Validation error: {str(e)}[/red]")
        except AccountCreationError as e:
            console.print(f"[red]Account creation failed: {str(e)}[/red]")
        except Exception as e:
            console.print(f"[red]Error creating account: {str(e)}[/red]")
            logger.error(f"Account creation error: {e}")
    
    def login_account(self):
        """Login to existing account with enhanced error handling"""
        console.print("[bold blue]Login to Account[/bold blue]")
        console.print()
        
        try:
            address = Prompt.ask("Enter email address")
            password = Prompt.ask("Enter password", password=True)
            
            with console.status("[bold green]Logging in...", spinner="dots"):
                account, token = self.client.login(address, password)
            
            console.print(f"[green]✓[/green] Login successful!")
            console.print(f"Welcome back, [bold]{account.address}[/bold]")
            
            stats = self.client.get_account_stats()
            console.print(f"Quota: {stats['quota_used']:,}/{stats['quota_total']:,} bytes")
        
        except InvalidCredentialsError:
            console.print("[red]Invalid email or password[/red]")
        except AuthenticationError as e:
            console.print(f"[red]Authentication failed: {str(e)}[/red]")
        except Exception as e:
            console.print(f"[red]Login failed: {str(e)}[/red]")
            logger.error(f"Login error: {e}")
    
    def check_mailbox(self):
        """Check and display mailbox contents with enhanced UI"""
        if not self.client.is_logged_in():
            console.print("[red]Please login first[/red]")
            return
        
        try:
            with console.status("[bold green]Fetching messages...", spinner="dots"):
                messages = self.client.get_messages()
            
            if not messages:
                console.print("[yellow]No messages in mailbox[/yellow]")
                return
            
            # Display messages in a table
            message_table = Table(title="Mailbox", box=box.ROUNDED)
            message_table.add_column("From", style="cyan", no_wrap=True)
            message_table.add_column("Subject", style="white")
            message_table.add_column("Preview", style="dim")
            message_table.add_column("Date", style="green")
            message_table.add_column("Size", style="yellow")
            message_table.add_column("Status", style="yellow")
            
            for message in messages:
                status = "📧" if not message.seen else "👁️"
                date = message.created_at[:10]  # Just the date part
                preview = message.intro[:50] + "..." if len(message.intro) > 50 else message.intro
                size_kb = f"{message.size / 1024:.1f}KB" if message.size > 1024 else f"{message.size}B"
                
                message_table.add_row(
                    message.from_address,
                    message.subject or "(No Subject)",
                    preview,
                    date,
                    size_kb,
                    status
                )
            
            console.print(message_table)
            console.print(f"[dim]Total messages: {len(messages)}[/dim]")
            
            # Show unread count
            unread = [m for m in messages if not m.seen]
            if unread:
                console.print(f"[yellow]⚠️  {len(unread)} unread message(s)[/yellow]")
        
        except Exception as e:
            console.print(f"[red]Error fetching messages: {str(e)}[/red]")
            logger.error(f"Mailbox check error: {e}")
    
    def refresh_mailbox(self):
        """Refresh mailbox for new messages"""
        if not self.client.is_logged_in():
            console.print("[red]Please login first[/red]")
            return
        
        try:
            with console.status("[bold green]Refreshing mailbox...", spinner="dots"):
                messages = self.client.refresh_mailbox()
            
            console.print(f"[green]✓[/green] Mailbox refreshed!")
            console.print(f"Total messages: [bold]{len(messages)}[/bold]")
            
            # Check for new unread messages
            unread = [m for m in messages if not m.seen]
            if unread:
                console.print(f"[yellow]⚠️  {len(unread)} unread message(s)[/yellow]")
        
        except Exception as e:
            console.print(f"[red]Error refreshing mailbox: {str(e)}[/red]")
            logger.error(f"Mailbox refresh error: {e}")
    
    def view_message(self):
        """View full message content with enhanced display"""
        if not self.client.is_logged_in():
            console.print("[red]Please login first[/red]")
            return
        
        try:
            # First show message list
            messages = self.client.get_messages()
            if not messages:
                console.print("[yellow]No messages to view[/yellow]")
                return
            
            # Create message selection table
            msg_table = Table(title="Select Message to View", box=box.ROUNDED)
            msg_table.add_column("#", style="cyan")
            msg_table.add_column("From", style="white")
            msg_table.add_column("Subject", style="green")
            msg_table.add_column("Date", style="dim")
            msg_table.add_column("Status", style="yellow")
            
            for i, message in enumerate(messages, 1):
                date = message.created_at[:10]
                status = "📧" if not message.seen else "👁️"
                msg_table.add_row(
                    str(i),
                    message.from_address,
                    message.subject or "(No Subject)",
                    date,
                    status
                )
            
            console.print(msg_table)
            
            # Get user selection
            choice = IntPrompt.ask("Enter message number to view", default=1, show_default=True)
            if 1 <= choice <= len(messages):
                message = messages[choice - 1]
                
                with console.status("[bold green]Fetching message...", spinner="dots"):
                    full_message = self.client.get_message(message.id)
                
                # Display full message
                console.print()
                console.print(Panel(
                    f"[bold]From:[/bold] {message.from_address}\n"
                    f"[bold]To:[/bold] {message.to_address}\n"
                    f"[bold]Subject:[/bold] {message.subject or '(No Subject)'}\n"
                    f"[bold]Date:[/bold] {message.created_at}\n"
                    f"[bold]Size:[/bold] {message.size:,} bytes\n"
                    f"[bold]Attachments:[/bold] {'Yes' if message.has_attachments else 'No'}",
                    title="Message Details",
                    border_style="blue"
                ))
                
                # Display message content
                if 'text' in full_message and full_message['text']:
                    console.print(Panel(
                        full_message['text'],
                        title="Message Content",
                        border_style="green"
                    ))
                elif 'html' in full_message and full_message['html']:
                    console.print(Panel(
                        "[dim]HTML content available[/dim]",
                        title="Message Content (HTML)",
                        border_style="green"
                    ))
                else:
                    console.print(Panel(
                        "[dim]No text content available[/dim]",
                        title="Message Content",
                        border_style="green"
                    ))
                
                # Mark as seen if not already
                if not message.seen:
                    if Confirm.ask("Mark message as read?"):
                        self.client.mark_message_seen(message.id)
                        console.print("[green]✓[/green] Message marked as read")
        
        except Exception as e:
            console.print(f"[red]Error viewing message: {str(e)}[/red]")
            logger.error(f"Message view error: {e}")
    
    def mark_message_read(self):
        """Mark a message as read"""
        if not self.client.is_logged_in():
            console.print("[red]Please login first[/red]")
            return
        
        try:
            messages = self.client.get_messages()
            unread_messages = [m for m in messages if not m.seen]
            
            if not unread_messages:
                console.print("[yellow]No unread messages[/yellow]")
                return
            
            # Show unread messages
            unread_table = Table(title="Unread Messages", box=box.ROUNDED)
            unread_table.add_column("#", style="cyan")
            unread_table.add_column("From", style="white")
            unread_table.add_column("Subject", style="green")
            unread_table.add_column("Date", style="dim")
            
            for i, message in enumerate(unread_messages, 1):
                date = message.created_at[:10]
                unread_table.add_row(
                    str(i),
                    message.from_address,
                    message.subject or "(No Subject)",
                    date
                )
            
            console.print(unread_table)
            
            choice = IntPrompt.ask("Enter message number to mark as read", default=1, show_default=True)
            if 1 <= choice <= len(unread_messages):
                message = unread_messages[choice - 1]
                
                with console.status("[bold green]Marking as read...", spinner="dots"):
                    self.client.mark_message_seen(message.id)
                
                console.print(f"[green]✓[/green] Message marked as read")
        
        except Exception as e:
            console.print(f"[red]Error marking message as read: {str(e)}[/red]")
            logger.error(f"Mark as read error: {e}")
    
    def delete_message(self):
        """Delete a message"""
        if not self.client.is_logged_in():
            console.print("[red]Please login first[/red]")
            return
        
        try:
            messages = self.client.get_messages()
            if not messages:
                console.print("[yellow]No messages to delete[/yellow]")
                return
            
            # Show messages
            msg_table = Table(title="Select Message to Delete", box=box.ROUNDED)
            msg_table.add_column("#", style="cyan")
            msg_table.add_column("From", style="white")
            msg_table.add_column("Subject", style="green")
            msg_table.add_column("Date", style="dim")
            
            for i, message in enumerate(messages, 1):
                date = message.created_at[:10]
                msg_table.add_row(
                    str(i),
                    message.from_address,
                    message.subject or "(No Subject)",
                    date
                )
            
            console.print(msg_table)
            
            choice = IntPrompt.ask("Enter message number to delete", default=1, show_default=True)
            if 1 <= choice <= len(messages):
                message = messages[choice - 1]
                
                if Confirm.ask(f"Delete message from {message.from_address}?"):
                    with console.status("[bold green]Deleting message...", spinner="dots"):
                        self.client.delete_message(message.id)
                    
                    console.print(f"[green]✓[/green] Message deleted")
        
        except Exception as e:
            console.print(f"[red]Error deleting message: {str(e)}[/red]")
            logger.error(f"Message deletion error: {e}")
    
    def show_account_stats(self):
        """Display account statistics and cache information"""
        if not self.client.is_logged_in():
            console.print("[red]Please login first[/red]")
            return
        
        try:
            account_stats = self.client.get_account_stats()
            cache_stats = self.client.get_cache_stats()
            
            # Account statistics
            account_panel = Panel(
                f"[bold]Address:[/bold] {account_stats['address']}\n"
                f"[bold]Quota Used:[/bold] {account_stats['quota_used']:,} / {account_stats['quota_total']:,} bytes\n"
                f"[bold]Quota Percentage:[/bold] {account_stats['quota_percentage']}%\n"
                f"[bold]Created:[/bold] {account_stats['created_at']}\n"
                f"[bold]Last Updated:[/bold] {account_stats['last_updated']}\n"
                f"[bold]API Requests:[/bold] {account_stats['request_count']}",
                title="Account Statistics",
                border_style="blue"
            )
            
            # Cache statistics
            cache_panel = Panel(
                f"[bold]Total Entries:[/bold] {cache_stats['total_entries']}\n"
                f"[bold]Active Entries:[/bold] {cache_stats['active_entries']}\n"
                f"[bold]Expired Entries:[/bold] {cache_stats['expired_entries']}\n"
                f"[bold]Cache Size:[/bold] {cache_stats['cache_size_mb']:.2f} MB",
                title="Cache Statistics",
                border_style="green"
            )
            
            console.print(Columns([account_panel, cache_panel]))
            
        except Exception as e:
            console.print(f"[red]Error getting statistics: {str(e)}[/red]")
            logger.error(f"Statistics error: {e}")
    
    def delete_account(self):
        """Delete current account with enhanced confirmation"""
        if not self.client.is_logged_in():
            console.print("[red]Please login first[/red]")
            return
        
        account = self.client.current_account
        
        console.print("[bold red]⚠️  DANGER ZONE ⚠️[/bold red]")
        console.print(f"You are about to delete account: [bold]{account.address}[/bold]")
        console.print("[red]This action cannot be undone![/red]")
        console.print()
        
        if Confirm.ask("[red]Are you absolutely sure?[/red]"):
            if Confirm.ask("Final confirmation - delete account?"):
                try:
                    with console.status("[bold red]Deleting account...", spinner="dots"):
                        self.client.delete_account()
                    
                    console.print(f"[green]✓[/green] Account {account.address} deleted")
                    self.client.logout()
                
                except Exception as e:
                    console.print(f"[red]Error deleting account: {str(e)}[/red]")
                    logger.error(f"Account deletion error: {e}")
    
    def logout(self):
        """Logout from current account"""
        if not self.client.is_logged_in():
            console.print("[red]Not logged in[/red]")
            return
        
        account = self.client.current_account.address
        self.client.logout()
        console.print(f"[green]✓[/green] Logged out from {account}")
    
    def run(self):
        """Main application loop with enhanced error handling"""
        self.show_welcome()
        
        while self.running:
            try:
                self.show_main_menu()
                
                if self.client.is_logged_in():
                    choice = Prompt.ask("Select option", choices=[str(i) for i in range(1, 11)])
                    
                    if choice == "1":
                        self.check_mailbox()
                    elif choice == "2":
                        self.refresh_mailbox()
                    elif choice == "3":
                        self.view_message()
                    elif choice == "4":
                        self.mark_message_read()
                    elif choice == "5":
                        self.delete_message()
                    elif choice == "6":
                        self.show_account_stats()
                    elif choice == "7":
                        self.show_settings_menu()
                    elif choice == "8":
                        self.delete_account()
                    elif choice == "9":
                        self.logout()
                    elif choice == "10":
                        self.running = False
                else:
                    choice = Prompt.ask("Select option", choices=[str(i) for i in range(1, 5)])
                    
                    if choice == "1":
                        self.create_account()
                    elif choice == "2":
                        self.login_account()
                    elif choice == "3":
                        self.show_settings_menu()
                    elif choice == "4":
                        self.running = False
                
                if self.running:
                    console.print()
                    Prompt.ask("Press Enter to continue...")
                    console.clear()
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted by user[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Unexpected error: {str(e)}[/red]")
                logger.error(f"Unexpected error: {e}")
                Prompt.ask("Press Enter to continue...")
        
        # Cleanup
        self.cleanup()
        console.print("[green]Goodbye![/green]")


def main():
    """Main entry point with enhanced error handling"""
    try:
        app = MailTMConsoleApp()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]Fatal error: {str(e)}[/red]")
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
