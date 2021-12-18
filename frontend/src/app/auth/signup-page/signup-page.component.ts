import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NavigationExtras, Router } from '@angular/router';
import { AuthService } from '../shared/auth.service';
import { FirstRegisterPayload } from '../shared/first-register.payload';

@Component({
  selector: 'app-signup-page',
  templateUrl: './signup-page.component.html',
  styleUrls: ['./signup-page.component.css']
})
export class SignupPageComponent implements OnInit {

  firstRegisterPayload: FirstRegisterPayload;
  signupForm!: FormGroup;
  constructor(private authService: AuthService, private router: Router) {
    this.firstRegisterPayload = {
      email: '',
      password: '',
      conf_password: ''
    };
  }

  ngOnInit(){
    this.signupForm = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', Validators.required),
      conf_password: new FormControl('', Validators.required)
    });
  }

  signup() {
    this.firstRegisterPayload.email = this.signupForm.get('email')?.value;
    this.firstRegisterPayload.password = this.signupForm.get('password')?.value;
    this.firstRegisterPayload.conf_password = this.signupForm.get('conf_password')?.value;
    console.log(this.firstRegisterPayload);

    this.authService.signup(this.firstRegisterPayload).subscribe(() => {
      console.log('Signup Successful');
    }, () => {
      console.log('Signup Failed');
    });
  
    this.router.navigate(['/register'],  { state: { email: this.firstRegisterPayload.email } });

  }

}
