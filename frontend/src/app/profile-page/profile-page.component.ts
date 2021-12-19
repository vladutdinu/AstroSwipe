import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ProfilePayload } from '../models/profile.payload';
import { ProfileService } from '../services/profile.service';

@Component({
  selector: 'app-profile-page',
  templateUrl: './profile-page.component.html',
  styleUrls: ['./profile-page.component.css']
})
export class ProfilePageComponent implements OnInit {
  zodiacSign: any[] = ['Pisces' , 'Gemini', 'Aries', 'Aquarius', 'Taurus', 'Leo', 'Cancer', 'Libra', 'Virgo', 'Capricornus', 'Sagittarius']; 
  Sex: any = ['M', 'F'];
  selectedZodiac!: string;
  profileInfo!: any;
  profilePayload!: ProfilePayload;
  constructor(private router: Router, private profileService: ProfileService) { 
    if(localStorage.getItem("token")===null)
      this.router.navigate(['/']);
    this.profilePayload = {
      first_name: '',
      last_name: '',
      country: '',
      city: '',
      personal_bio: '',
      preffered_zodiac_sign: '',
      age: 1,
      sex: ''
  }
  }

  async ngOnInit(): Promise<void> {
    await this.getInfo().then((r) => this.profileInfo = r.info);
    this.getInfoHandler(this.profileInfo)
    console.log(this.profileInfo)
    console.log(this.profilePayload)

  }
  getInfoHandler(value: any){
    this.profilePayload.age = value.age ;
    this.profilePayload.city = value.city ;
    this.profilePayload.country = value.country ;
    this.profilePayload.first_name = value.first_name ;
    this.profilePayload.last_name = value.last_name ;
    this.profilePayload.personal_bio = value.personal_bio ;
    this.profilePayload.preffered_zodiac_sign = value.preffered_zodiac_sign ;
    this.profilePayload.sex = value.sex ;
  }
  choseZodiacSign(zodiac: string){
    this.selectedZodiac = zodiac;
  }
  async getInfo(){
    const token = localStorage.getItem("token");
    return this.profileService.getInfo(token!);
  }
  updateBio(){
   this.profileService.updateBio(this.profilePayload, localStorage.getItem("token")!).subscribe(() =>{
    console.log('Bio Updated succesffuly!')
    window.location.reload();
  }, () => {
    console.log('Bio Updated  Failed');
  });

  }
  deleteProfile(){
    this.profileService.deleteProfile(localStorage.getItem("token")!).subscribe(() =>{
      console.log('Delete succesffuly!')
      localStorage.removeItem("token")
    }, () => {
      console.log('Delete Failed');
    });
    this.router.navigate(['/']);
  }
}
