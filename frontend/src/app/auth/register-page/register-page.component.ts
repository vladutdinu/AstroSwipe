import { Component, OnInit , Input} from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, NavigationExtras, Router } from '@angular/router';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { AuthService } from '../shared/auth.service';
import { SecondRegisterPayload } from '../shared/second-register.payload';

@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./register-page.component.css']
})
export class RegisterPageComponent implements OnInit {

  selectedZodiac!: string;
  secondRegisterPayload!: SecondRegisterPayload;
  signupForm!: FormGroup;
  zodiacSign: any[] = ['Pisces' , 'Gemini', 'Aries', 'Aquarius', 'Taurus', 'Leo', 'Cancer', 'Libra', 'Virgo', 'Capricornus', 'Sagittarius']; 
  Sex: any = ['M', 'F'];
  passedEmail!: string;
  adresaEmail!: string;

  constructor(private authService: AuthService, private router: Router, public activatedRoute: ActivatedRoute) { 
    this.secondRegisterPayload = {
      email: "",
      first_name: "",
      last_name: "",
      country: "",
      city: "",
      sex: "",
      zodiac_sign: "",
      personal_bio: "",
      preffered_zodiac_sign: "",
      age: 0,
      user_type: "",
    }

    try {
      this.passedEmail = this.router.getCurrentNavigation()!.extras.state!.email;
    } catch (error) {
      this.router.navigate(['/sign-up']);
    }

  }

  ngOnInit() {
    console.log(this.passedEmail);
    this.signupForm = new FormGroup({
      first_name: new FormControl('', Validators.required),
      last_name: new FormControl('', Validators.required),
      sex: new FormControl('', Validators.required),
      country: new FormControl('', Validators.required),
      city: new FormControl('', Validators.required),
      age: new FormControl('', Validators.required),
      personal_bio: new FormControl('', Validators.required),
      preffered_zodiac_sign: new FormControl('', Validators.required),
    });
    this.adresaEmail = this.passedEmail;
  }


  choseZodiacSign(zodiac: string){
    this.selectedZodiac = zodiac;
  }
  register(){
    this.secondRegisterPayload.age = this.signupForm.get('age')!.value;
    this.secondRegisterPayload.zodiac_sign = this.selectedZodiac;
    this.secondRegisterPayload.city = this.signupForm.get('city')!.value;
    this.secondRegisterPayload.country = this.signupForm.get('country')!.value;
    this.secondRegisterPayload.first_name = this.signupForm.get('first_name')!.value;
    this.secondRegisterPayload.last_name = this.signupForm.get('last_name')!.value;
    this.secondRegisterPayload.personal_bio = this.signupForm.get('personal_bio')!.value;
    this.secondRegisterPayload.preffered_zodiac_sign = this.signupForm.get('preffered_zodiac_sign')!.value;
    this.secondRegisterPayload.sex = this.signupForm.get('sex')!.value;
    this.secondRegisterPayload.user_type = 'B';
    this.secondRegisterPayload.email = this.adresaEmail;
    this.authService.register(this.secondRegisterPayload).subscribe(() =>{

      console.log('Register succesffuly!')
    }, () => {
      console.log('Register Failed');
    });


    this.router.navigate(['/verify']);
  }

}
