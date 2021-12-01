import { Inject, Injectable, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { StartPageComponent } from './start-page/start-page.component';
import { LoginPageComponent } from './auth/login-page/login-page.component';
import { AppRoutingModule } from './app-routing.module';
import { SignupPageComponent } from './auth/signup-page/signup-page.component';
import { RegisterPageComponent } from './auth/register-page/register-page.component';
import { MenuBarComponent } from './menu-bar/menu-bar.component';
import { MainPageComponent } from './main-page/main-page.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import { HammertimeDirective } from './hammertime.directive'
import * as Hammer from 'hammerjs';
import { HammerGestureConfig, HAMMER_GESTURE_CONFIG } from '@angular/platform-browser';
import { ChatPageComponent } from './chat-page/chat-page.component';
import { MatchPageComponent } from './match-page/match-page.component';
import { ProfilePageComponent } from './profile-page/profile-page.component';

@Injectable()
export class MyHammerConfig extends HammerGestureConfig  {
  overrides = <any>{
      'swipe': { direction: Hammer.DIRECTION_ALL  }
  }
}

@NgModule({
  declarations: [
    AppComponent,
    StartPageComponent,
    LoginPageComponent,
    SignupPageComponent,
    RegisterPageComponent,
    MenuBarComponent,
    MainPageComponent,
    HammertimeDirective,
    ChatPageComponent,
    MatchPageComponent,
    ProfilePageComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatCardModule,
    MatButtonModule
  ],
  providers: [ { 
    provide: HAMMER_GESTURE_CONFIG, 
    useClass: MyHammerConfig 
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
