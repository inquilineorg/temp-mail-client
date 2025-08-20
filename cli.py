#!/usr/bin/env python3
"""
Pryvon Temp Mail CLI - Command Line Interface
Quick operations without the full interactive console
"""

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from mailtm_client import MailTMClient
from config import config
from logger import logger
from exceptions import *

console = Console()


@click.group()
@click.version_option(version="2.0.0", prog_name="pryvon-temp-mail")
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug):
    """Pryvon Temp Mail Command Line Interface"""
    if debug:
        config.set('log_level', 'DEBUG')
        console.print("[yellow]Debug mode enabled[/yellow]")


@cli.command()
@click.option('--username', '-u', help='Username for the account')
@click.option('--domain', '-d', help='Domain for the account')
@click.option('--password', '-p', help='Password for the account')
@click.option('--auto-login', is_flag=True, help='Automatically login after creation')
def create(username, domain, password, auto_login):
    """Create a new temporary email account"""
    try:
        client = MailTMClient()
        
        # Get available domains if not specified
        if not domain:
            with console.status("Fetching available domains..."):
                domains = client.get_domains()
                if not domains:
                    console.print("[red]No domains available[/red]")
                    return
                
                # Use first active domain
                domain = next((d['domain'] for d in domains if d.get('isActive', False)), None)
                if not domain:
                    console.print("[red]No active domains available[/red]")
                    return
        
        # Generate username if not specified
        if not username:
            import random
            import string
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            console.print(f"[yellow]Generated username: {username}[/yellow]")
        
        # Generate password if not specified
        if not password:
            import random
            import string
            password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12)
            console.print(f"[yellow]Generated password: {password}[/yellow]")
        
        full_address = f"{username}@{domain}"
        
        with console.status(f"Creating account {full_address}..."):
            account = client.create_account(full_address, password)
        
        console.print(f"[green]✓[/green] Account created successfully!")
        console.print(f"Address: [bold]{account.address}[/bold]")
        console.print(f"Password: [bold]{password}[/bold]")
        
        if auto_login:
            with console.status("Logging in..."):
                client.login(full_address, password)
            console.print("[green]✓[/green] Logged in successfully!")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('address')
@click.option('--password', '-p', prompt=True, hide_input=True, help='Account password')
def login(address, password):
    """Login to an existing account"""
    try:
        client = MailTMClient()
        
        with console.status("Logging in..."):
            account, token = client.login(address, password)
        
        console.print(f"[green]✓[/green] Login successful!")
        console.print(f"Welcome back, [bold]{account.address}[/bold]")
        
        stats = client.get_account_stats()
        console.print(f"Quota: {stats['quota_used']:,}/{stats['quota_total']:,} bytes ({stats['quota_percentage']}%)")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--limit', '-l', default=10, help='Number of messages to show')
@click.option('--unread-only', is_flag=True, help='Show only unread messages')
def list(limit, unread_only):
    """List messages in the current account"""
    try:
        client = MailTMClient()
        
        if not client.is_logged_in():
            console.print("[red]Please login first using: pryvon-temp-mail login <address>[/red]")
            return
        
        with console.status("Fetching messages..."):
            messages = client.get_messages(limit=limit)
        
        if not messages:
            console.print("[yellow]No messages found[/yellow]")
            return
        
        # Filter unread messages if requested
        if unread_only:
            messages = [m for m in messages if not m.seen]
            if not messages:
                console.print("[yellow]No unread messages[/yellow]")
                return
        
        # Display messages
        table = Table(title="Messages", box=box.ROUNDED)
        table.add_column("From", style="cyan")
        table.add_column("Subject", style="white")
        table.add_column("Date", style="green")
        table.add_column("Size", style="yellow")
        table.add_column("Status", style="yellow")
        
        for message in messages:
            status = "📧" if not message.seen else "👁️"
            date = message.created_at[:10]
            size_kb = f"{message.size / 1024:.1f}KB" if message.size > 1024 else f"{message.size}B"
            
            table.add_row(
                message.from_address,
                message.subject or "(No Subject)",
                date,
                size_kb,
                status
            )
        
        console.print(table)
        console.print(f"[dim]Showing {len(messages)} messages[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('message_id')
def view(message_id):
    """View a specific message by ID"""
    try:
        client = MailTMClient()
        
        if not client.is_logged_in():
            console.print("[red]Please login first using: pryvon-temp-mail login <address>[/red]")
            return
        
        with console.status("Fetching message..."):
            message_data = client.get_message(message_id)
        
        # Display message details
        console.print(Panel(
            f"[bold]From:[/bold] {message_data.get('from', {}).get('address', 'Unknown')}\n"
            f"[bold]Subject:[/bold] {message_data.get('subject', '(No Subject)')}\n"
            f"[bold]Date:[/bold] {message_data.get('createdAt', 'Unknown')}\n"
            f"[bold]Size:[/bold] {message_data.get('size', 0):,} bytes",
            title="Message Details",
            border_style="blue"
        ))
        
        # Display content
        if 'text' in message_data and message_data['text']:
            console.print(Panel(
                message_data['text'],
                title="Message Content",
                border_style="green"
            ))
        else:
            console.print("[dim]No text content available[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('message_id')
def mark_read(message_id):
    """Mark a message as read"""
    try:
        client = MailTMClient()
        
        if not client.is_logged_in():
            console.print("[red]Please login first using: pryvon-temp-mail login <address>[/red]")
            return
        
        with console.status("Marking message as read..."):
            client.mark_message_seen(message_id)
        
        console.print("[green]✓[/green] Message marked as read")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('message_id')
def delete(message_id):
    """Delete a message"""
    try:
        client = MailTMClient()
        
        if not client.is_logged_in():
            console.print("[red]Please login first using: pryvon-temp-mail login <address>[/red]")
            return
        
        with console.status("Deleting message..."):
            client.delete_message(message_id)
        
        console.print("[green]✓[/green] Message deleted")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def refresh():
    """Refresh mailbox for new messages"""
    try:
        client = MailTMClient()
        
        if not client.is_logged_in():
            console.print("[red]Please login first using: pryvon-temp-mail login <address>[/red]")
            return
        
        with console.status("Refreshing mailbox..."):
            messages = client.refresh_mailbox()
        
        console.print(f"[green]✓[/green] Mailbox refreshed!")
        console.print(f"Total messages: [bold]{len(messages)}[/bold]")
        
        unread = [m for m in messages if not m.seen]
        if unread:
            console.print(f"[yellow]⚠️  {len(unread)} unread message(s)[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def stats():
    """Show account and cache statistics"""
    try:
        client = MailTMClient()
        
        if not client.is_logged_in():
            console.print("[red]Please login first using: pryvon-temp-mail login <address>[/red]")
            return
        
        account_stats = client.get_account_stats()
        cache_stats = client.get_cache_stats()
        
        # Account statistics
        account_panel = Panel(
            f"[bold]Address:[/bold] {account_stats['address']}\n"
            f"[bold]Quota Used:[/bold] {account_stats['quota_used']:,} / {account_stats['quota_total']:,} bytes\n"
            f"[bold]Quota Percentage:[/bold] {account_stats['quota_percentage']}%\n"
            f"[bold]Created:[/bold] {account_stats['created_at']}\n"
            f"[bold]API Requests:[/bold] {account_stats['request_count']}",
            title="Account Statistics",
            border_style="blue"
        )
        
        # Cache statistics
        cache_panel = Panel(
            f"[bold]Total Entries:[/bold] {cache_stats['total_entries']}\n"
            f"[bold]Active Entries:[/bold] {cache_stats['active_entries']}\n"
            f"[bold]Cache Size:[/bold] {cache_stats['cache_size_mb']:.2f} MB",
            title="Cache Statistics",
            border_style="green"
        )
        
        from rich.columns import Columns
        console.print(Columns([account_panel, cache_panel]))
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def logout():
    """Logout from current account"""
    try:
        client = MailTMClient()
        
        if not client.is_logged_in():
            console.print("[yellow]Not logged in[/yellow]")
            return
        
        client.logout()
        console.print("[green]✓[/green] Logged out successfully")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def domains():
    """List available domains"""
    try:
        client = MailTMClient()
        
        with console.status("Fetching domains..."):
            domains = client.get_domains()
        
        if not domains:
            console.print("[yellow]No domains available[/yellow]")
            return
        
        table = Table(title="Available Domains", box=box.ROUNDED)
        table.add_column("Domain", style="cyan")
        table.add_column("Active", style="green")
        table.add_column("Status", style="yellow")
        
        for domain in domains:
            status = "✓" if domain.get('isActive', False) else "✗"
            table.add_row(
                domain['domain'],
                status,
                "Available" if domain.get('isActive', False) else "Inactive"
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def clear_cache():
    """Clear all cached data"""
    try:
        client = MailTMClient()
        client.clear_cache()
        console.print("[green]✓[/green] Cache cleared")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    cli()
