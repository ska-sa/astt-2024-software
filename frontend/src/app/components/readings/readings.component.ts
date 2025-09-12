import { Component } from '@angular/core';
import { Reading } from '../../interfaces/reading';
import { ReadingService } from '../../services/reading.service';

@Component({
  selector: 'app-readings',
  imports: [],
  templateUrl: './readings.component.html',
  styleUrl: './readings.component.css'
})
export class ReadingsComponent {
  readings: Reading[] = [];
  isLoading: boolean = false;

  constructor(private readingService: ReadingService) { }

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
}
