import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../shared/auth.service';
import { LoginPayload } from '../shared/login.payload';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {

  loginPayload!: LoginPayload;
  loginForm!: FormGroup;
  loginToken!: string;
  loginService!: any;
  constructor(private authService: AuthService, private router: Router) { 
    this.loginPayload = {
      email: "",
      password: ""
    }
  }
  
  ngOnInit(){
    this.loginForm = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', Validators.required),
    });
  }

  login(){

    this.loginPayload.email = this.loginForm.get('email')?.value;
    this.loginPayload.password = this.loginForm.get('password')?.value;
    
    this.loginService = this.authService.login(this.loginPayload).subscribe((params) => {
      
      this.loginToken = params.token;
      this.router.navigate(['/swipe'], {state: {token: this.loginToken}});
      console.log('Login Successful');
    }, () => {
      this.router.navigate(['/login']);
      console.log('Login Failed');
    });

  }
  

}
