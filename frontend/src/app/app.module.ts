import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { StartPageComponent } from './start-page/start-page.component';
import { LoginPageComponent } from './auth/login-page/login-page.component';
import { AppRoutingModule } from './app-routing.module';
import { SignupPageComponent } from './auth/signup-page/signup-page.component';
import { RegisterPageComponent } from './auth/register-page/register-page.component';

@NgModule({
  declarations: [
    AppComponent,
    StartPageComponent,
    LoginPageComponent,
    SignupPageComponent,
    RegisterPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
