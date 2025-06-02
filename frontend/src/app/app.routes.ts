import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { CommandsComponent } from './commands/commands.component';
import { ReadingsComponent } from './readings/readings.component';
import { CamComponent } from './cam/cam.component';

export const routes: Routes = [
    {
        path: "home", component: HomeComponent
    },
    {
        path: "cam", component: CamComponent
    },
    {
        path: "commands", component: CommandsComponent
    },
    {
        path: "readings", component: ReadingsComponent
    }
];
