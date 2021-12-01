import { Directive, HostListener, Output, EventEmitter } from '@angular/core';

@Directive({
  selector: '[appHammertime]'
})
export class HammertimeDirective {

  @Output() doubleClick = new EventEmitter();
  @Output() tripleClick = new EventEmitter();

  constructor() { }

  
  @HostListener('tap',  ['$event']) 
  onTap(e: any) {
    if (e.tapCount === 2) {
      this.doubleClick.emit(e)
    }

    if (e.tapCount === 3) {
      this.tripleClick.emit(e)
    }
  }

}
