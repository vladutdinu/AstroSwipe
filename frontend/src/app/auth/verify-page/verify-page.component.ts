import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../shared/auth.service';
import { VerifyPayload } from '../shared/verify.payload';

@Component({
  selector: 'app-verify-page',
  templateUrl: './verify-page.component.html',
  styleUrls: ['./verify-page.component.css']
})
export class VerifyPageComponent implements OnInit {
  verifyPayload!: VerifyPayload;
  verifyForm!: FormGroup;

  constructor(private router: Router, private authService: AuthService) { 
    this.verifyPayload= {
      token: ''
    }
  }

  ngOnInit(): void {
    this.verifyForm = new FormGroup({
      token: new FormControl('', Validators.required)
    });
  }

  async confirm(){
    await this.sendCodeToVerif().then((r) => localStorage.setItem("token", r));
    console.log(localStorage);
    this.router.navigate(['/login']);
  }
  async sendCodeToVerif(){
    this.verifyPayload.token = this.verifyForm.get('token')!.value;
    return this.authService.codeVerif(this.verifyPayload.token);
  }
}
