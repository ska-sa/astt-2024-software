import { Component, OnInit } from '@angular/core';
import { CommandService } from '../../services/command.service';
import { Command } from '../../interfaces/command';
import { CommonModule } from '@angular/common';
import { UserService } from '../../services/user.service';
import { User } from '../../interfaces/user';

@Component({
  selector: 'app-commands',
  imports: [CommonModule],
  templateUrl: './commands.component.html',
  styleUrl: './commands.component.css'
})
export class CommandsComponent implements OnInit {
  isLoading: boolean = false;
  areCommandsLoading: boolean = false;
  areUsersLoading: boolean = false;

  commands: Command[] = [];
  users: User[] = [];
  userEmails: { [key: number]: string } = {};

  constructor(private commandService: CommandService, private userService: UserService) {}

  ngOnInit(): void {
    this.loadUsers();
    this.loadCommands();
    this.isLoading = !this.areCommandsLoading && !this.areUsersLoading;
    this.commands.forEach((command) => {
      this.userEmails[command.user_id] = this.users.find(u => u.id == command.user_id)?.email_address ?? 'Unknown User';
    });
  }

  loadCommands(): void {
    this.areCommandsLoading = true;
    this.commandService.getCommands().subscribe({
      next: (commands: Command[]) => {
        this.commands = commands;
        console.log('Commands loaded successfully:', commands);
        this.areCommandsLoading = false;
      },
      error: (error) => {
        console.error('Error loading commands:', error);
        this.areCommandsLoading = false;
      }
    });
  }

  loadUsers(): void {
    this.areUsersLoading = true;
    this.userService.getUsers().subscribe({
      next: (users: User[]) => {
        console.log('Users loaded successfully:', users);
        this.areUsersLoading = false;
      },
      error: (error) => {
        console.error('Error loading users:', error);
        this.areUsersLoading = false;
      }
    });
  }

  getUserById(userId: number): User | undefined {
    return this.users.find(user => user.id === userId);
  }
}
