import { Component, OnInit } from '@angular/core';
import { Reading } from '../../interfaces/reading';
import { ReadingService } from '../../services/reading.service';
import { CommonModule } from '@angular/common';
import { TelescopeService } from '../../services/telescope.service';
import { Telescope } from '../../interfaces/telescope';

@Component({
  selector: 'app-readings',
  imports: [
    CommonModule
  ],
  templateUrl: './readings.component.html',
  styleUrl: './readings.component.css'
})
export class ReadingsComponent implements OnInit {
  readings: Reading[] = [];
  isLoading: boolean = false;

  constructor(private readingService: ReadingService, private telescopeService: TelescopeService) { }

  ngOnInit(): void {
    this.loadReadings();
  }

  loadReadings(): void {
    this.isLoading = true;
    this.readingService.getReadings().subscribe({
      next: (readings: Reading[]) => {
        this.readings = readings;
        console.log('Readings loaded successfully:', readings);
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading readings:', error);
        this.isLoading = false;
      }
    });
    return;
  }

  getTelescopeNameById(telescope_id: number): string {
    let telescopeName = "Unknown Telescope";

      this.telescopeService.getTelescope(telescope_id).subscribe({
        next: (t: Telescope) => {
          telescopeName = t.name;
          console.log('Telescope loaded:', t);
          this.isLoading = false;
        },
        error: (e: Error) => {
          console.error('Error occured:', e);
          this.isLoading = false;
        }
      });
    return telescopeName;
  }
}
