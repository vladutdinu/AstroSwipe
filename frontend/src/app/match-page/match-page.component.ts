import { i18nMetaToJSDoc } from '@angular/compiler/src/render3/view/i18n/meta';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LikePayload } from '../models/like.payload';
import { MatchService } from '../services/match.service';

@Component({
  selector: 'app-match-page',
  templateUrl: './match-page.component.html',
  styleUrls: ['./match-page.component.css']
})
export class MatchPageComponent implements OnInit {
  props!: any;
  people: any = [];
  peopleShown!: any;
  index: number = 1;
  hasMatches!: boolean;
  likePayload!: LikePayload;
  constructor(private router: Router, private matchService: MatchService){
    this.props={
      email: localStorage.getItem('email'),
      token: localStorage.getItem('token')
    }
    this.hasMatches = false;
    if(this.props.email === null)
      this.router.navigate(['/login'])
    this.likePayload = {
      email1: '',
      email2: ''
    }
  }
 
  async ngOnInit() {
    await this.getMatches().then((r) => {
      this.people = r;
    });
    this.peopleShown = this.people[this.index];
    if(this.people[0].first_name === undefined)
      this.people = [];

  }


  async getMatches(){
    return this.matchService.getMatches(this.props.token);
  }

  unmatch(email: string){
    this.likePayload.email1 = this.props.email;
    this.likePayload.email2 = email;
    this.matchService.unmatch(this.likePayload, this.props.token).subscribe((params) => {

      window.location.reload();
    });
    
  }

}
