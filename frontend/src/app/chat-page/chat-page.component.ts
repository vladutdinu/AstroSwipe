import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import * as $ from 'jquery';
import { MatchService } from '../services/match.service';

@Component({
  selector: 'app-chat-page',
  templateUrl: './chat-page.component.html',
  styleUrls: ['./chat-page.component.css']
})
export class ChatPageComponent implements OnInit {

  props!: any;
  people: any = [];
  peopleShown!: any;
  index: number = 1;
  constructor(private router: Router, private matchService: MatchService){
    this.props={
      email: localStorage.getItem('email'),
      token: localStorage.getItem('token')
    }
    if(this.props.email === null)
      this.router.navigate(['/login'])
  }
 
  async ngOnInit() {
    $( '.friend-drawer--onhover' ).on( 'click',  function() {
  
      $( '.chat-bubble' ).hide('slow').show('slow');
      
    });
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

}
