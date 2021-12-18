import { Component, OnInit } from '@angular/core';

import { trigger, keyframes, animate, transition } from '@angular/animations';
import * as kf from './keyframes';
import { Router } from '@angular/router';
import { SwipeService } from '../services/swipe.service';
import { compileClassMetadata } from '@angular/compiler';
import { LikePayload } from '../models/like.payload';
@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.css'],
  animations: [
    trigger('cardAnimator', [
      transition('* => wobble', animate(1000, keyframes(kf.wobble))),
      transition('* => swing', animate(1000, keyframes(kf.swing))),
      transition('* => jello', animate(1000, keyframes(kf.jello))),
      transition('* => zoomOutRight', animate(1000, keyframes(kf.zoomOutRight))),
      transition('* => slideOutLeft', animate(1000, keyframes(kf.slideOutLeft))),
      transition('* => slideOutRight', animate(1000, keyframes(kf.slideOutRight))),
      transition('* => rotateOutUpRight', animate(1000, keyframes(kf.rotateOutUpRight))),
      transition('* => flipOutY', animate(1000, keyframes(kf.flipOutY))),
      transition('* => fadeOutTopLeft', animate(1000, keyframes(kf.fadeOutTopLeft))),
      transition('* => fadeOutTopRight', animate(1000, keyframes(kf.fadeOutTopRight))),
      transition('* => fadeOutUp', animate(1000, keyframes(kf.fadeOutUp))),
    ])
  ]
})
export class MainPageComponent implements OnInit {
  
  animationState!: string;
  props!: any;
  people: any = [];
  peopleShown!: any;
  index: number = 1;
  likePayload!: LikePayload;
  constructor(private router: Router, private swipeService: SwipeService){
    this.props={
      email: localStorage.getItem('email'),
      token: localStorage.getItem('token')
    }
    if(this.props.email === null)
      this.router.navigate(['/login'])
    this.likePayload = {
      email1: '',
      email2: ''
    }
  }
  startAnimation(state: string) {
    console.log(state)
    if (!this.animationState) {
      this.animationState = state;
    }
  }
  
  resetAnimationState() {
    this.animationState = '';
  }
 
  async ngOnInit() {
    await this.getPersonsByZodiac().then((r) => this.people = r);
    this.peopleShown = this.people[this.index];
    console.log(this.people)
  }


  async getPersonsByZodiac(){
    return this.swipeService.getPersonsByZodiac(this.props.token);
  }

  like(){
    try {
      if(this.people.length - this.index == 0){
        this.likePayload.email1 = this.props.email;
        this.likePayload.email2 = this.people.at(-1).email;
        this.swipeService.likePerson(this.likePayload, this.props.token).subscribe();
        this.people = []
      }
      else{
       this.likePayload.email1 = this.props.email;
       this.likePayload.email2 = this.people.at(-1).email;
       this.swipeService.likePerson(this.likePayload, this.props.token).subscribe();
       this.people = this.people.slice(0, this.people.length - this.index)
       
      }
    } catch (error) {
      
    }
  }
  superLike(){
    try {
      if(this.people.length - this.index == 0){
        this.people = []
      }
      else{
       this.people = this.people.slice(0, this.people.length - this.index)
      }
    } catch (error) {
      
    }
  }

  pass(){
    try {
      if(this.people.length - this.index == 0){
        this.people = []
      }
      else{
       this.people = this.people.slice(0, this.people.length - this.index)
      }
    } catch (error) {
      
    }
  }

}
