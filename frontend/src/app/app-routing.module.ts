import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginPageComponent } from './auth/login-page/login-page.component';
import { RegisterPageComponent } from './auth/register-page/register-page.component';
import { SignupPageComponent } from './auth/signup-page/signup-page.component';
import { ChatPageComponent } from './chat-page/chat-page.component';
import { MainPageComponent } from './main-page/main-page.component';
import { MatchPageComponent } from './match-page/match-page.component';
import { ProfilePageComponent } from './profile-page/profile-page.component';
import { StartPageComponent } from './start-page/start-page.component';



const routes: Routes = [
  { path: '', component: StartPageComponent },
  { path: 'main', component: StartPageComponent },
  { path: 'login', component: LoginPageComponent },
  { path: 'sign-up', component: SignupPageComponent },
  { path: 'register', component: RegisterPageComponent },
  { path: 'swipe', component: MainPageComponent },
  { path: 'chat', component: ChatPageComponent },
  { path: 'match', component: MatchPageComponent },
  { path: 'profile', component: ProfilePageComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
