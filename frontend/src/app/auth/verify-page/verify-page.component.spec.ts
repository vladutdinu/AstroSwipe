import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VerifyPageComponent } from './verify-page.component';

describe('VerifyPageComponent', () => {
  let component: VerifyPageComponent;
  let fixture: ComponentFixture<VerifyPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VerifyPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VerifyPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
