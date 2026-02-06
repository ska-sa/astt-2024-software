import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CanvasJSAngularChartsModule, CanvasJS } from '@canvasjs/angular-charts';
import { FormsModule } from '@angular/forms';
import { CreateCommand } from '../../interfaces/create-command';
import { Command } from '../../interfaces/command';
import { CommandService } from '../../services/command.service';
import { getUser } from '../../signal';
import { ActivatedRoute } from '@angular/router';
import { Reading } from '../../interfaces/reading';
import { ReadingService } from '../../services/reading.service';
import { interval, Subscription, switchMap } from 'rxjs';

@Component({
  selector: 'app-cam',
  imports: [
    CommonModule,
    CanvasJSAngularChartsModule,
    FormsModule,
  ],
  templateUrl: './cam.component.html',
  styleUrl: './cam.component.css'
})
export class CamComponent {
  reading: Reading | null = null;
  width = 360; // Width of the SVG
  height = 90; // Height of the SVG
  knobPosition: { x: number, y: number } = { x: 0, y: 0 };
  isDragging = false;
  isPointing = true;
  isPointingPageActive = false;
  isLoading = false;
  azimuth = 180; // Initial azimuth value
  elevation = 45; // Initial elevation value
  latitude = 40.730610; // Sample latitude value
  longitude = -73.935242; // Sample longitude value
  altitude = 10; // Sample altitude value
  gridLines = this.generateGridLines();
  sources = [
    { id: 1, name: 'Sun' },
    { id: 2, name: 'Moon' },
    { id: 3, name: 'Mars' }
  ];
  selectedSource: number = this.sources[0].id;
  telescopeId: number | null = null;

  chartData: { x: Date, y: number }[] = [];

  chartOptions = {
    animationEnabled: true,
    theme: "light2",
    title: {
      text: "Azimuth & Elevation Angle"
    },
    axisX: {
      valueFormatString: "MMM",
      intervalType: "month",
      interval: 1
    },
    axisY: {
      title: "Angle",
      suffix: "°"
    },
    toolTip: {
      shared: true
    },
    legend: {
      cursor: "pointer",
      itemclick: function(e: any){
        if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
          e.dataSeries.visible = false;
        } else{
          e.dataSeries.visible = true;
        }
        e.chart.render();
      }
    },
    data: [
      {
        type: "line",
        name: "Azimuth",
        showInLegend: true,
        yValueFormatString: "#,###°",
        dataPoints: [] as { x: Date, y: number }[]
      },
      {
        type: "line",
        name: "Elevation",
        showInLegend: true,
        yValueFormatString: "#,###°",
        dataPoints: [] as { x: Date, y: number }[]
      }
    ]
  };


  constructor(private commandService: CommandService, private route: ActivatedRoute, private readingService: ReadingService) {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      this.telescopeId = id ? +id : null;
    });
  }
  ngOnInit(): void {
    this.loadReading();
    this.startPollingReadings();
  }
  pollSubscription: Subscription | null = null;
  isDeviceOnline = true;
  resolutionOptions = [
    { label: '1m', durationMs: 60 * 1000 },
    { label: '5m', durationMs: 5 * 60 * 1000 },
    { label: '10m', durationMs: 10 * 60 * 1000 },
    { label: '30m', durationMs: 30 * 60 * 1000 },
    { label: '1h', durationMs: 60 * 60 * 1000 },
    { label: '1d', durationMs: 24 * 60 * 60 * 1000 },
    { label: '7d', durationMs: 7 * 24 * 60 * 60 * 1000 },
    { label: '1m (month)', durationMs: 30 * 24 * 60 * 60 * 1000 },
    { label: '1y', durationMs: 365 * 24 * 60 * 60 * 1000 }
  ];
  selectedResolution = this.resolutionOptions[0]; // default 1m

  // Store historical readings for graphing
  readingHistory: { timestamp: Date; az: number; el: number }[] = [];


  ngOnDestroy(): void {
    this.pollSubscription?.unsubscribe();
  }

  startPollingReadings(): void {
    if (!this.telescopeId) return;

    this.pollSubscription = interval(1000)
      .pipe(
        switchMap(() => this.readingService.getLatestReading(this.telescopeId!))
      )
      .subscribe({
        next: (reading: Reading) => {
          this.reading = reading;

          // Check device online status (latest reading timestamp within 2 minutes)
          const now = new Date();
          const readingTime = new Date(reading.created_at ?? now.toISOString());
          this.isDeviceOnline = (now.getTime() - readingTime.getTime()) < 2 * 60 * 1000;

          if (this.isDeviceOnline) {
            // Add to history and filter by selected resolution
            this.readingHistory.push({ timestamp: readingTime, az: reading.az_angle, el: reading.el_angle });
            this.filterReadingHistory();
            this.updateChartData();
          }
        },
        error: (err) => {
          console.error('Error polling readings:', err);
          this.isDeviceOnline = false;
        }
      });
  }

  filterReadingHistory(): void {
    const now = new Date().getTime();
    const cutoff = now - this.selectedResolution.durationMs;
    this.readingHistory = this.readingHistory.filter(r => r.timestamp.getTime() >= cutoff);
  }

  updateChartData(): void {
    // Prepare dataPoints for Azimuth and Elevation
    const azDataPoints = this.readingHistory.map(r => ({ x: r.timestamp, y: r.az }));
    const elDataPoints = this.readingHistory.map(r => ({ x: r.timestamp, y: r.el }));

    // Update chart options data
    this.chartOptions.data = [
      {
        type: "line",
        name: "Azimuth",
        showInLegend: true,
        yValueFormatString: "#,###°",
        dataPoints: azDataPoints
      },
      {
        type: "line",
        name: "Elevation",
        showInLegend: true,
        yValueFormatString: "#,###°",
        dataPoints: elDataPoints
      }
    ];

    // Update x-axis format based on resolution (simplified)
    if (this.selectedResolution.durationMs < 24 * 60 * 60 * 1000) {
      this.chartOptions.axisX.valueFormatString = "HH:mm:ss";
      this.chartOptions.axisX.intervalType = "minute";
      this.chartOptions.axisX.interval = 1;
    } else if (this.selectedResolution.durationMs < 30 * 24 * 60 * 60 * 1000) {
      this.chartOptions.axisX.valueFormatString = "MMM dd";
      this.chartOptions.axisX.intervalType = "day";
      this.chartOptions.axisX.interval = 1;
    } else {
      this.chartOptions.axisX.valueFormatString = "MMM yyyy";
      this.chartOptions.axisX.intervalType = "month";
      this.chartOptions.axisX.interval = 1;
    }
  }

  // Call this method on resolution change from the template
  onResolutionChange(): void {
    this.filterReadingHistory();
    this.updateChartData();
  }

  loadReading(): void {
    if (!this.telescopeId) {
      console.error('Telescope ID is not set.');
      return;
    }
    this.isLoading = true;
    this.readingService.getLatestReading(this.telescopeId).subscribe({
      next: (reading: Reading) => {
        this.reading = reading;
        console.log('Latest reading loaded successfully:', reading);
        this.isLoading = false;
      },
      error: (error: Error) => {
        console.error('Error loading latest reading:', error);
        this.isLoading = false;
      }
    });
    return;
  }

  startDrag(event: MouseEvent): void {
    this.isDragging = true;
    this.updateKnobPosition(event);
  }

  stopDrag(): void {
    this.isDragging = false;
    this.updateAzimuthElevation();
  }

  onMouseMove(event: MouseEvent): void {
    if (this.isDragging) {
      this.updateKnobPosition(event);
    }
  }

  point(): void {
    this.isPointing = true;
    this.updateAzimuthElevation();
  }

  track(): void {
    this.isPointing = false;
  }

  startTracking(): void {
    // Implement tracking logic here
    console.log(`Started tracking source ${this.selectedSource}`);
  }

  startPointing(): void {
    this.isLoading = true;
    const createCommand: CreateCommand = {
      user_id: getUser()?.id ?? 0,
      telescope_id: this.telescopeId ?? 0,
      target_az_angle: this.azimuth,
      target_el_angle: this.elevation
    }

    this.commandService.postCommand(createCommand).subscribe({
      next: (command: Command) => {
        console.log('Command sent successfully:', command);
        this.isLoading = false;
        this.isPointingPageActive = true;
      },
      error: (error) => {
        console.error('Error sending command:', error);
        this.isLoading = false;
      }
    });
    return;
  }

  private updateKnobPosition(event: MouseEvent): void {
    const container = event.target as HTMLElement;
    const rect = container.getBoundingClientRect();
    const offsetX = event.clientX - rect.left; // Center the knob
    const offsetY = event.clientY - rect.top; // Center the knob

    const maxXOffset = rect.width / 2; // Max movement limit
    const maxYOffset = rect.height / 2; // Max movement limit
    const x = Math.max(-maxXOffset, Math.min(maxXOffset, offsetX));
    const y = Math.max(-maxYOffset, Math.min(maxYOffset, offsetY));

    this.knobPosition = { x, y };
    this.updateAzimuthElevation();
  }

  private updateAzimuthElevation(): void {
    this.azimuth = Math.round((this.knobPosition.x / this.width) * 360);
    this.elevation = Math.round((this.knobPosition.y / this.height) * 90);
  }

  private generateGridLines(): { x1: number, y1: number, x2: number, y2: number }[] {
    const gridLines = [];
    for (let i = 0; i <= 360; i += 30) {
      gridLines.push({ x1: i, y1: 0, x2: i, y2: 90 });
    }
    for (let i = 0; i <= 90; i += 15) {
      gridLines.push({ x1: 0, y1: i, x2: 360, y2: i });
    }
    return gridLines;
  }

  public getHealthStatusClass() : string{
    if (this.reading?.health_status?.includes('nominal')) {
      return 'text-success';
    } else if (this.reading?.health_status?.includes('warning')) {
      return 'text-warning';
    } else if (this.reading?.health_status?.includes('error')) {
      return 'text-danger';
    } else {
      return '';
    }
  }
}