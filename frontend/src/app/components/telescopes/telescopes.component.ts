import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { Telescope } from '../../interfaces/telescope';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-telescopes',
  imports: [
    RouterOutlet,
    CommonModule,
    FormsModule,
  ],
  templateUrl: './telescopes.component.html',
  styleUrl: './telescopes.component.css'
})
export class TelescopesComponent implements OnInit{
  isLoading: boolean = true;
  telescopes: Telescope[] = [];

  newTelescopeName: string = "";

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.isLoading = true;
    this.loadTelescopes();
    this.isLoading = false;
  }

  loadTelescopes(): void {
    this.telescopes = [
      {
        id: 1,
        name: "ASTT 2024",
        health_status: 1,
        created_at: new Date()
      }
    ];
  }

  addTelescope(): void {
    const newTelescope: Telescope = {
      id: this.telescopes.length,
      name: this.newTelescopeName,
      health_status: 1,
      created_at: new Date()
    };
    this.telescopes.push(newTelescope);
    this.newTelescopeName = "";
    return;
  }

  controlTelescope(telescopeId: number): void {
    this.router.navigate(["/telescopes", telescopeId, "cam"]);
    return;
  }

  editTelescope(telescopeId: number): void {
    return;
  }

  deleteTelescope(telescopeId: number): void {
    const telescopeToDelete = this.telescopes.find(telescope => telescope.id === telescopeId);
    if (telescopeToDelete) {
      const newTelescopes: Telescope[] = this.telescopes.filter(telescope => telescope.id !== telescopeId);
      this.telescopes = newTelescopes;
    }
  }
}

