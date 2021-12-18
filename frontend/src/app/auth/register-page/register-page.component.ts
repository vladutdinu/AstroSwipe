import { Component, OnInit , Input} from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
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

  adresaEmail!: string;
  secondRegisterPayload!: SecondRegisterPayload;
  signupForm!: FormGroup;
  zodiacSign: any = ['Pisces' , 'Gemini', 'Aries', 'Aquarius', 'Taurus', 'Leo', 'Cancer', 'Libra', 'Virgo', 'Capricornus', 'Sagittarius']; 
  Sex: any = ['M', 'F'];


  constructor(private authService: AuthService, private router: Router, public activatedRoute: ActivatedRoute) { }

  ngOnInit() {
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

    this.activatedRoute.paramMap
      .pipe(this.adresaEmail = window.history.state);
    
    console.log(this.adresaEmail);
  }


  choseZodiacSign(zodiac: string){
    this.secondRegisterPayload.zodiac_sign = zodiac;
  }

  register(){
    this.secondRegisterPayload.age = this.signupForm.get('age')!.value;
    this.secondRegisterPayload.city = this.signupForm.get('city')!.value;
    this.secondRegisterPayload.country = this.signupForm.get('country')!.value;
    this.secondRegisterPayload.first_name = this.signupForm.get('first_name')!.value;
    this.secondRegisterPayload.last_name = this.signupForm.get('last_name')!.value;
    this.secondRegisterPayload.personal_bio = this.signupForm.get('personal_bio')!.value;
    this.secondRegisterPayload.preffered_zodiac_sign = this.signupForm.get('preffered_zodiac_sign')!.value;
    this.secondRegisterPayload.sex = this.signupForm.get('sex')!.value;
    this.secondRegisterPayload.user_type = 'B';

    this.authService.register(this.secondRegisterPayload).subscribe(() =>{
      console.log('Register succesffuly!')
    }, () => {
      console.log('Register Failed');
    });

    this.router.navigate(['/swipe']);
  }

}
