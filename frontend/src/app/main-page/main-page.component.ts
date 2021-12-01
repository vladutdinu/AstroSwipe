import { Component, OnInit } from '@angular/core';

import { trigger, keyframes, animate, transition } from '@angular/animations';
import * as kf from './keyframes';

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

  startAnimation(state: string) {
    console.log(state)
    if (!this.animationState) {
      this.animationState = state;
    }
  }

  resetAnimationState() {
    this.animationState = '';
  }

  ngOnInit(): void {
  }

}
