import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ControlAndMonitoringComponent } from './control-and-monitoring.component';

describe('ControlAndMonitoringComponent', () => {
  let component: ControlAndMonitoringComponent;
  let fixture: ComponentFixture<ControlAndMonitoringComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ControlAndMonitoringComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ControlAndMonitoringComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
