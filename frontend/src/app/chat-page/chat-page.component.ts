import { Component, OnInit } from '@angular/core';
import * as $ from 'jquery';

@Component({
  selector: 'app-chat-page',
  templateUrl: './chat-page.component.html',
  styleUrls: ['./chat-page.component.css']
})
export class ChatPageComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    $( '.friend-drawer--onhover' ).on( 'click',  function() {
  
      $( '.chat-bubble' ).hide('slow').show('slow');
      
    });
  }

}
