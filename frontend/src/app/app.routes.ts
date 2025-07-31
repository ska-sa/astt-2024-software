import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CommandsComponent } from './components/commands/commands.component';
import { ReadingsComponent } from './components/readings/readings.component';
import { CamComponent } from './components/cam/cam.component';
import { SignInComponent } from './components/sign-in/sign-in.component';
import { TelescopesComponent } from './components/telescopes/telescopes.component';
import { TelescopeDetailsComponent } from './components/telescope-details/telescope-details.component';
import { UsersComponent } from './components/users/users.component';
import { SourcesComponent } from './components/sources/sources.component';
import { SourceDetailsComponent } from './components/source-details/source-details.component';
import { UserDetailsComponent } from './components/user-details/user-details.component';
import { AppLayoutComponent } from './components/app-layout/app-layout.component';

export const routes: Routes = [
    { 
        path: '', redirectTo: 'sign-in', pathMatch: 'full' 
    },
    { 
        path: 'sign-in', component: SignInComponent 
    },
    {
        path: '', component: AppLayoutComponent, children: [
            { 
                path: 'telescopes', component: TelescopesComponent, children: [
                    {
                        path: ':id/details', component: TelescopeDetailsComponent
                    },
                    {
                        path: ':id/cam', component: CamComponent
                    },
                    {
                        path: ':id/commands', component: CommandsComponent
                    },
                    {
                        path: ':id/readings', component: ReadingsComponent
                    },
                ]
            },
            {
                path: 'commands', component: CommandsComponent
            },
            {
                path: 'readings', component: ReadingsComponent
            },
            { 
                path: 'users', component: UsersComponent, children: [
                    {
                        path: ':id/details', component: UserDetailsComponent
                    }
                ]
            },
            {
                path: 'sources', component: SourcesComponent, children: [
                    {
                        path: ':id/details', component: SourceDetailsComponent
                    }
                ]
            }
        ]
    },/*
    { 
        path: '**', redirectTo: 'sign-in', pathMatch: 'full' 
    }*/
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
