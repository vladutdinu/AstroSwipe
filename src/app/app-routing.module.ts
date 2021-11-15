import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginPageComponent } from './auth/login-page/login-page.component';
import { SignupPageComponent } from './auth/signup-page/signup-page.component';
import { StartPageComponent } from './start-page/start-page.component';



const routes: Routes = [
  { path: '', component: StartPageComponent },
  { path: 'main', component: StartPageComponent },
  { path: 'login', component: LoginPageComponent },
  { path: 'sign-up', component: SignupPageComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
