import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CanvasJSAngularChartsModule } from '@canvasjs/angular-charts';
import { FormsModule } from '@angular/forms';
import { CreateCommand } from '../../interfaces/create-command';
import { Command } from '../../interfaces/command';
import { CommandService } from '../../services/command.service';
import { getUser } from '../../signal';
import { ActivatedRoute } from '@angular/router';

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
    data: [{
      type:"line",
      name: "Azimuth",
      showInLegend: true,
      yValueFormatString: "#,###°F",
      dataPoints: [		
        { x: new Date(2021, 0, 1), y: 27 },
        { x: new Date(2021, 1, 1), y: 28 },
        { x: new Date(2021, 2, 1), y: 35 },
        { x: new Date(2021, 3, 1), y: 45 },
        { x: new Date(2021, 4, 1), y: 54 },
        { x: new Date(2021, 5, 1), y: 64 },
        { x: new Date(2021, 6, 1), y: 69 },
        { x: new Date(2021, 7, 1), y: 68 },
        { x: new Date(2021, 8, 1), y: 61 },
        { x: new Date(2021, 9, 1), y: 50 },
        { x: new Date(2021, 10, 1), y: 41 },
        { x: new Date(2021, 11, 1), y: 33 }
      ]
    },
    {
      type: "line",
      name: "Maximum",
      showInLegend: true,
      yValueFormatString: "#,###°F",
      dataPoints: [
        { x: new Date(2021, 0, 1), y: 40 },
        { x: new Date(2021, 1, 1), y: 42 },
        { x: new Date(2021, 2, 1), y: 50 },
        { x: new Date(2021, 3, 1), y: 62 },
        { x: new Date(2021, 4, 1), y: 72 },
        { x: new Date(2021, 5, 1), y: 80 },
        { x: new Date(2021, 6, 1), y: 85 },
        { x: new Date(2021, 7, 1), y: 84 },
        { x: new Date(2021, 8, 1), y: 76 },
        { x: new Date(2021, 9, 1), y: 64 },
        { x: new Date(2021, 10, 1), y: 54 },
        { x: new Date(2021, 11, 1), y: 44 }
      ]
    }]
  }

  constructor(private commandService: CommandService, private route: ActivatedRoute) {
    this.route.paramMap.subscribe(params => {
      const id = params.get('telescopeId');
      this.telescopeId = id ? +id : null;
    });
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
}